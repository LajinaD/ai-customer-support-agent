from fastapi import APIRouter
from langchain_core.messages import ToolMessage

from services.llm import get_llm

from tools.order_tool import (
    get_order_status,
    get_order_details,
    get_shipping_tracking,
)

from tools.refund_tool import (
    check_refund_eligibility_tool,
    process_refund_tool,
)

from tools.knowledge_tool import search_knowledge_tool

from tools.support_ticket_tool import create_support_ticket_tool

from services.conversation_state import (
    save_pending_action,
    get_pending_action,
    clear_pending_action,
    ensure_conversation
)

import time
from services.agent_logger import (
    create_agent_log,
    log_tool_call,
    log_error,
    finish_agent_log,
)


router = APIRouter(
    prefix="",
    tags=["Chat"]
)

llm = get_llm()

tools = [
    get_order_status,
    get_order_details,
    get_shipping_tracking,
    check_refund_eligibility_tool,
    search_knowledge_tool,
    create_support_ticket_tool
]

llm_with_tools = llm.bind_tools(tools)

tool_map = {
    "get_order_status": get_order_status,
    "get_order_details": get_order_details,
    "get_shipping_tracking": get_shipping_tracking,
    "check_refund_eligibility_tool": check_refund_eligibility_tool,
    "search_knowledge_tool": search_knowledge_tool,
    "create_support_ticket_tool": create_support_ticket_tool
}


def extract_order_id(text: str):
    """
    Extract an explicit order ID from customer message.

    Example:

    "I want a refund for ORD-1003"

    returns:

    "ORD-1003"
    """

    import re

    match = re.search(
        r"\bORD-\d+\b",
        text.upper()
    )

    if match:
        return match.group(0)

    return None


def classify_pending_refund_message(user_input: str):
    """
    Ask the LLM to understand what the customer is doing
    while a refund confirmation is pending.

    The LLM handles conversational reasoning.

    Python handles the actual safety decisions.
    """

    response = llm.invoke([
        (
            "system",
            """
            The customer currently has a pending refund confirmation.

            Determine what the customer is doing.

            Return ONLY one of these values:

            YES
            NO
            QUESTION
            NEW_ORDER
            AMBIGUOUS

            YES:
            The customer explicitly confirms the pending refund.

            Examples:
            - yes
            - yes please
            - proceed
            - go ahead
            - do it
            - please process it
            - confirm
            - absolutely

            NO:
            The customer explicitly rejects or cancels the refund.

            Examples:
            - no
            - cancel
            - don't process it
            - stop
            - not now
            - I don't want it

            QUESTION:
            The customer is asking for information about
            the pending refund without confirming or cancelling it.

            Examples:
            - how much will I get?
            - what is the refund amount?
            - when will I receive the refund?
            - how much money will be refunded?
            - what happens next?
            - can you explain?

            NEW_ORDER:
            The customer explicitly mentions a different order
            and wants to discuss/refund that order.

            Examples:
            - I want a refund for ORD-1003
            - Actually, refund ORD-1003
            - What about ORD-1002?

            AMBIGUOUS:
            The customer's intent cannot be determined clearly.

            Examples:
            - maybe
            - I'm not sure
            - let me think

            IMPORTANT:

            A question is NOT confirmation.

            Never classify a question as YES.

            Only classify as YES when the customer clearly
            authorizes the refund.
            """
        ),
        (
            "user",
            user_input
        )
    ])

    return response.content.strip().upper()


# Guardrail #1: Explicit confirmation
def validate_refund_confirmation(
    pending_action: dict,
    confirmation: str
):
    """
    Application-level guardrail for refund execution.

    A refund can only proceed when:

    1. A pending action exists
    2. The pending action is a refund
    3. Customer explicitly confirmed YES
    4. Order ID exists
    """

    if not pending_action:

        return (
            False,
            "No pending refund action exists."
        )

    if pending_action.get("pending_action") != "refund":

        return (
            False,
            "The pending action is not a refund."
        )

    if confirmation != "YES":

        return (
            False,
            "Customer has not explicitly confirmed the refund."
        )

    data = pending_action.get("data", {})

    if not data.get("order_id"):

        return (
            False,
            "Refund order ID is missing."
        )

    return True, None


def validate_refund_result(result: dict):
    """
    Validate the actual result returned by the refund tool.

    The LLM is NEVER trusted to determine whether
    the refund succeeded.
    """

    # Result must be a dictionary
    if not isinstance(result, dict):

        return (
            False,
            "Invalid refund tool response."
        )

    if "success" not in result:

        return (
            False,
            "Refund tool did not provide a success status."
        )

    if result["success"] is not True:

        return (
            False,
            result.get(
                "reason",
                "Refund could not be processed."
            )
        )

    if result.get("refund_status") != "Refunded":

        return (
            False,
            "Refund tool did not confirm the refund status."
        )

    if not result.get("order_id"):

        return (
            False,
            "Refund result is missing the order ID."
        )

    return True, None



@router.post("/chat")
def chat(
    user_input: str,
    conversation_id: str
):
    ensure_conversation(conversation_id)

    agent_log = create_agent_log()

    pending_action = get_pending_action(conversation_id)

    if pending_action:

        action = pending_action["pending_action"]

        data = pending_action["data"]


        if action == "refund":

            pending_order_id = data["order_id"]

            mentioned_order_id = extract_order_id(user_input)

            if (mentioned_order_id and mentioned_order_id != pending_order_id):

                clear_pending_action(conversation_id)

                return {
                    "response": (
                        f"I see you're asking about "
                        f"{mentioned_order_id}. "
                        f"The previous refund confirmation "
                        f"for {pending_order_id} is no longer active. "
                        f"Please submit the refund request for "
                        f"{mentioned_order_id} and I'll check "
                        f"its eligibility."
                    ),
                    "tools_used": [],
                }

            decision = classify_pending_refund_message(user_input)

            if decision == "QUESTION":

                question_response = llm.invoke([
                    (
                        "system",
                        """
                        You are a customer support agent.

                        The customer currently has a pending refund.

                        Answer the customer's question using ONLY
                        the information provided below.

                        IMPORTANT:

                        - The refund has NOT been processed yet.
                        - Never claim that the refund was processed.
                        - Never invent information.
                        - Do not change the pending refund.
                        - After answering, remind the customer that
                          they can say "yes" or "go ahead" to proceed.
                        """
                    ),
                    (
                        "system",
                        f"""
                        Pending refund information:

                        Order ID:
                        {data["order_id"]}

                        Refund amount:
                        {data["refund_amount"]}
                        """
                    ),
                    (
                        "user",
                        user_input
                    )
                ])

                # IMPORTANT: Do NOT clear pending_action. The customer can still say "yes" in the next message.

                return {
                    "response": question_response.content,
                    "tools_used": [],
                }

            if decision == "NO":

                clear_pending_action(
                    conversation_id
                )

                return {
                    "response": (
                        "No problem. I won't process the refund."
                    ),
                    "tools_used": [],
                    "intent": "refund",
                    "order_id": pending_order_id,
                    "confirmation": False,
                }

            if decision == "AMBIGUOUS":

                # IMPORTANT: Do NOT clear pending action. Customer can confirm later.

                return {
                    "response": (
                        "I still have a refund pending for "
                        f"{pending_order_id}. "
                        "Please say 'yes' to proceed or "
                        "'no' to cancel it."
                    ),
                    "tools_used": [],
                    "intent": "refund",
                    "order_id": pending_order_id,
                    "confirmation": None,
                }

            if decision == "NEW_ORDER":

                clear_pending_action(
                    conversation_id
                )

                return {
                    "response": (
                        "Your previous refund confirmation is "
                        "no longer active. Please submit the "
                        "refund request for the new order."
                    ),
                    "tools_used": [],
                    "intent": "refund",
                    "confirmation": None,
                }

            if decision == "YES":

                confirmation = "YES"

                is_allowed, guardrail_reason = (
                    validate_refund_confirmation(
                        pending_action,
                        confirmation
                    )
                )

                if not is_allowed:

                    return {
                        "response": (
                            "I can't process the refund because "
                            "the required confirmation or refund "
                            "information is missing."
                        ),
                        "tools_used": [],
                        "intent": "refund",
                        "order_id": pending_order_id,
                        "confirmation": False,
                        "error": guardrail_reason,
                    }

                order_id = data["order_id"]

                start_time = time.perf_counter()

                try:
                    refund_result = process_refund_tool.invoke({
                        "order_id": order_id
                    })

                    duration_ms = (
                        time.perf_counter() - start_time
                    ) * 1000

                    log_tool_call(
                        agent_log,
                        "process_refund_tool",
                        {
                            "order_id": order_id
                        },
                        duration_ms,
                        True
                    )

                except Exception as e:

                    # IMPORTANT: Do NOT tell the customer the refund succeeded. Also keep the pending action because the customer may retry after the service becomes available.
                    duration_ms = (
                        time.perf_counter() - start_time
                    ) * 1000

                    log_tool_call(
                        agent_log,
                        "process_refund_tool",
                        {
                            "order_id": order_id
                        },
                        duration_ms,
                        False
                    )

                    log_error(
                        agent_log,
                        repr(e)
                    )

                    return {
                        "response": (
                            "I wasn't able to process the refund "
                            "because the refund service is currently "
                            "unavailable. Please try again later."
                        ),
                        "tools_used": [
                            {
                                "tool_name": "process_refund_tool",
                                "tool_args": {
                                    "order_id": order_id
                                },
                                "tool_result": (
                                    f"Exception: {str(e)}"
                                ),
                            }
                        ],
                        "error": "Refund processing failed.",
                        "agent_log": agent_log
                    }

                is_valid, failure_reason = (
                    validate_refund_result(
                        refund_result
                    )
                )

                if not is_valid:

                    clear_pending_action(
                        conversation_id
                    )

                    return {
                        "response": (
                            "I wasn't able to process the refund. "
                            f"{failure_reason}"
                        ),
                        "tools_used": [
                            {
                                "tool_name": "process_refund_tool",
                                "tool_args": {
                                    "order_id": order_id
                                },
                                "tool_result": str(
                                    refund_result
                                ),
                            }
                        ],
                        "intent": "refund",
                        "order_id": order_id,
                        "confirmation": True,
                        "error": failure_reason,
                        "agent_log": agent_log
                    }

                clear_pending_action(
                    conversation_id
                )

                # Generate final customer response

                final_response = llm.invoke([
                    (
                        "system",
                        """
                        You are a customer support agent.

                        Explain the refund result to the customer.

                        IMPORTANT:

                        The application has already validated that
                        the refund succeeded.

                        Use ONLY the provided refund result.

                        Never invent additional information.

                        Do not say that the refund is pending.

                        Do not change the refund amount.
                        """
                    ),
                    (
                        "system",
                        f"""
                        Refund tool result:

                        {refund_result}
                        """
                    ),
                    (
                        "user",
                        user_input
                    )
                ])

                return {
                    "response": final_response.content,
                    "tools_used": [
                        {
                            "tool_name": "process_refund_tool",
                            "tool_args": {
                                "order_id": order_id
                            },
                            "tool_result": str(
                                refund_result
                            ),
                        }
                    ],
                    "intent": "refund",
                    "order_id": order_id,
                    "confirmation": True,
                    "agent_log": agent_log
                }


    messages = [

        (
            "system",
            """
            You are a helpful customer support agent.

            You have access to tools that provide real order
            information.

            Available tools:

            - get_order_status:
              Get the current order status and expected delivery date.

            - get_order_details:
              Get the product, quantity, and price.

            - get_shipping_tracking:
              Get the carrier, tracking number, and current package
              location.

            - check_refund_eligibility_tool:
              Check whether an order is eligible for a refund
              according to the company's refund policy.

            - search_knowledge_tool:
              Use the knowledge search tool when the customer asks about
              general policies, rules, procedures, or support information
              that is not specific to a particular order.
            
              Do not invent policy information.
              If relevant information may exist in the knowledge base,
              use the knowledge search tool before answering.

            - create_support_ticket_tool:
              Create a support ticket when the customer's issue cannot
              be safely resolved using the available tools and knowledge base.

              Use this tool when:
              - The customer explicitly asks to speak with human support.
              - The customer has a problem that requires human investigation.
              - The available tools cannot provide enough information to resolve
                  the customer's issue.
              - The knowledge base does not contain enough information to answer
                  an important policy or support question.
              - A previous action appears to have failed or requires manual review.

              Do NOT create a support ticket when:
              - The available tools can directly resolve the customer's request.
              - The customer is simply asking a normal order or refund question
                  that the existing tools can answer.
              - The customer is asking a general policy question that can be
                  answered from the knowledge base.

            RAG GROUNDING RULES:

            When you use search_knowledge_tool:

            1. Treat the retrieved results as the source of truth
            for company policies and support information.

            2. Only state facts that are supported by the retrieved
            knowledge results.

            3. Do not add assumptions, industry-standard practices,
            or information from your general knowledge.

            4. If the retrieved knowledge does not contain enough
            information to answer the question, say that the
            available knowledge base does not provide enough
            information.

            5. Do not invent details such as taxes, fees, shipping
            charges, refund timelines, processing times, or
            exceptions unless they are explicitly present in
            the retrieved knowledge.

            6. When retrieved information conflicts with your
            general knowledge, follow the retrieved knowledge.

            Rules:

            1. Never invent order information.

            2. Always use tools when real order information
               is required.

            3. Never decide refund eligibility yourself.

            4. If a customer asks for a refund, use
               check_refund_eligibility_tool.

            5. NEVER process a refund directly.

            6. If the refund eligibility tool says the order
               is eligible, tell the customer the refund amount
               and ask whether they want to proceed.

            7. Never claim that a refund has been processed
               unless the refund tool actually returned success.

            8. After receiving a tool result, decide what
               should happen next.

            9. If a tool returns an error or says that an order
               does not exist, do not invent an answer.

            10. Use the available tools whenever real order
                information is required.

            11. Escalate to human support when the issue cannot be safely
                resolved using the available tools and knowledge base.

            12. When creating a support ticket:
                - Provide a concise description of the customer's issue.
                - Include the order ID when one is relevant.
                - Choose an appropriate priority.
                - Never invent information that the customer did not provide.

            13. After create_support_ticket_tool successfully creates a ticket,
                tell the customer that the issue has been escalated and provide
                the ticket ID.

            14. Never claim that a support ticket was created unless the
                create_support_ticket_tool actually returns success.
            """
        ),

        (
            "user",
            user_input
        ),
    ]

    tools_used = []


    while True:

        response = llm_with_tools.invoke(
            messages
        )


        if not response.tool_calls:

            agent_log = finish_agent_log(agent_log)

            return {
                "response": response.content,
                "tools_used": tools_used,
                "agent_log": agent_log
            }

        messages.append(
            response
        )

        for tool_call in response.tool_calls:

            tool_name = tool_call["name"]

            tool_args = tool_call["args"]

            tool_call_id = tool_call["id"]

            if tool_name == "create_support_ticket_tool":
                tool_args["conversation_id"] = conversation_id

            tool = tool_map.get(
                tool_name
            )

            if tool is None:

                tool_result = {
                    "error": f"Unknown tool: {tool_name}"
                }
                log_tool_call(
                    agent_log,
                    tool_name,
                    tool_args,
                    0,
                    False
                )

            else:

                start_time = time.perf_counter()

                try:

                    tool_result = tool.invoke(
                        tool_args
                    )
                    duration_ms = (
                        time.perf_counter() - start_time
                    ) * 1000

                    log_tool_call(
                        agent_log,
                        tool_name,
                        tool_args,
                        duration_ms,
                        True
                    )

                except Exception as e:

                    # Safe failure for normal tools

                    duration_ms = (
                        time.perf_counter() - start_time
                    ) * 1000

                    log_tool_call(
                        agent_log,
                        tool_name,
                        tool_args,
                        duration_ms,
                        False
                    )

                    log_error(
                        agent_log,
                        repr(e)
                    )

                    return {
                        "response": (
                            "Sorry, something went wrong "
                            "while processing your request."
                        ),
                        "tools_used": tools_used,
                        "error": repr(e),
                        "agent_log": finish_agent_log(agent_log),
                    }

            messages.append(
                ToolMessage(
                    content=str(tool_result),
                    tool_call_id=tool_call_id,
                )
            )

            if tool_name == "check_refund_eligibility_tool":

                if (
                    isinstance(tool_result, dict)
                    and tool_result.get("eligible") is True
                ):

                    save_pending_action(
                        conversation_id,
                        "refund",
                        {
                            "order_id": tool_args["order_id"],
                            "refund_amount": tool_result.get(
                                "refund_amount"
                            ),
                        }
                    )

            tools_used.append({
                "tool_name": tool_name,
                "tool_args": tool_args,
                "tool_result": str(tool_result),
            })
