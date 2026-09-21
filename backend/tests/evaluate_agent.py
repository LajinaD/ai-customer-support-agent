import uuid
import requests

from langsmith import Client
import os
from dotenv import load_dotenv

load_dotenv()

print("LangSmith tracing:", os.getenv("LANGSMITH_TRACING"))
print("LangSmith project:", os.getenv("LANGSMITH_PROJECT"))
print(
    "LangSmith API key loaded:",
    bool(os.getenv("LANGSMITH_API_KEY"))
)

LANGSMITH_PROJECT = "customer-support-agent"
DATASET_NAME = "customer-support-agent-v1"

BACKEND_URL = "http://127.0.0.1:8000"


client = Client()


def run_agent(question: str):
    conversation_id = str(uuid.uuid4())

    response = requests.post(
        f"{BACKEND_URL}/chat",
        params={
            "user_input": question,
            "conversation_id": conversation_id,
        },
        timeout=60,
    )

    response.raise_for_status()

    return response.json()


def extract_tool_names(result: dict):
    tools_used = result.get("tools_used", [])

    return [
        tool["tool_name"]
        for tool in tools_used
    ]


def evaluate_tools(
    expected_tools: list[str],
    actual_tools: list[str],
):
    expected = set(expected_tools)
    actual = set(actual_tools)

    missing = expected - actual

    if missing:
        return {
            "score": 0,
            "pass": False,
            "missing_tools": list(missing),
            "actual_tools": actual_tools,
        }

    return {
        "score": 1,
        "pass": True,
        "missing_tools": [],
        "actual_tools": actual_tools,
    }


def main():

    dataset = client.read_dataset(
        dataset_name=DATASET_NAME
    )

    examples = list(
        client.list_examples(
            dataset_id=dataset.id
        )
    )

    print(
        f"\nRunning {len(examples)} evaluation examples...\n"
    )

    passed = 0

    for index, example in enumerate(examples, start=1):

        question = example.inputs["question"]

        expected_tools = (
            example.outputs["expected_tools"]
        )

        print("=" * 60)
        print(f"Example {index}")
        print(f"Question: {question}")
        print(f"Expected: {expected_tools}")

        try:

            result = run_agent(question)

            actual_tools = extract_tool_names(
                result
            )

            evaluation = evaluate_tools(
                expected_tools,
                actual_tools
            )

            print(
                f"Actual:   {actual_tools}"
            )

            print(
                f"Result:   "
                f"{'PASS ✅' if evaluation['pass'] else 'FAIL ❌'}"
            )

            if evaluation["missing_tools"]:
                print(
                    "Missing:",
                    evaluation["missing_tools"]
                )

            if evaluation["pass"]:
                passed += 1

        except Exception as e:

            print("ERROR ❌")
            print(e)

    print("\n" + "=" * 60)

    print(
        f"Final score: "
        f"{passed}/{len(examples)} passed"
    )


if __name__ == "__main__":
    main()