import uuid
import requests
import streamlit as st


# ============================================================
# CONFIG
# ============================================================

BACKEND_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="ShopEase",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ============================================================
# SESSION STATE
# ============================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "conversation_id" not in st.session_state:
    st.session_state.conversation_id = str(uuid.uuid4())

if "chat_open" not in st.session_state:
    st.session_state.chat_open = False


# ============================================================
# GLOBAL CSS
# ============================================================

st.html("""
<style>

    /* ========================================================
       HIDE STREAMLIT DEFAULT UI
       ======================================================== */

    [data-testid="stHeader"] {
        display: none !important;
    }

    #MainMenu {
        display: none !important;
    }

    footer {
        display: none !important;
    }

    [data-testid="stSidebar"] {
        display: none !important;
    }

    .block-container {
        padding: 0 !important;
        max-width: 100% !important;
    }


    /* ========================================================
       PAGE
       ======================================================== */

    html, body {
        margin: 0 !important;
        padding: 0 !important;
        font-family: Arial, Helvetica, sans-serif;
        background: #f7f8fa;
    }


    /* ========================================================
       NAVBAR
       ======================================================== */

    .shop-navbar {
        height: 72px;
        background: #ffffff;
        border-bottom: 1px solid #eeeeee;
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0 7%;
        box-sizing: border-box;
    }

    .shop-logo {
        font-size: 25px;
        font-weight: 800;
        color: #111827;
    }

    .shop-logo span {
        color: #2563eb;
    }

    .nav-links {
        display: flex;
        gap: 32px;
        color: #4b5563;
        font-size: 14px;
    }

    .nav-links span {
        cursor: default;
    }

    .nav-icons {
        display: flex;
        gap: 18px;
        font-size: 21px;
        color: #374151;
    }


    /* ========================================================
       HERO
       ======================================================== */

    .hero {
        min-height: 430px;
        display: flex;
        align-items: center;
        padding: 50px 8%;
        box-sizing: border-box;

        background:
            linear-gradient(
                90deg,
                rgba(17, 24, 39, 0.88),
                rgba(17, 24, 39, 0.35)
            ),
            url("https://images.unsplash.com/photo-1556742049-0cfed4f6a45d?auto=format&fit=crop&w=1800&q=80");

        background-size: cover;
        background-position: center;
    }

    .hero-content {
        max-width: 620px;
        color: white;
    }

    .hero-small {
        font-size: 14px;
        font-weight: 600;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin-bottom: 15px;
        opacity: 0.9;
    }

    .hero h1 {
        font-size: 52px;
        line-height: 1.08;
        margin: 0 0 20px 0;
        font-weight: 800;
    }

    .hero p {
        font-size: 18px;
        line-height: 1.6;
        margin: 0;
        color: #e5e7eb;
    }

    .hero-badge {
        display: inline-block;
        margin-top: 28px;
        padding: 11px 20px;
        border-radius: 8px;
        background: #2563eb;
        font-weight: 600;
        font-size: 14px;
    }


    /* ========================================================
       SECTION
       ======================================================== */

    .section {
        padding: 60px 7%;
        box-sizing: border-box;
        background: #ffffff;
    }

    .section-title {
        text-align: center;
        font-size: 30px;
        font-weight: 800;
        color: #111827;
        margin-bottom: 10px;
    }

    .section-subtitle {
        text-align: center;
        color: #6b7280;
        margin-bottom: 35px;
        font-size: 15px;
    }


    /* ========================================================
       CATEGORIES
       ======================================================== */

    .categories {
        display: grid;
        grid-template-columns: repeat(6, 1fr);
        gap: 18px;
    }

    .category-card {
        border: 1px solid #e5e7eb;
        border-radius: 14px;
        padding: 28px 15px;
        text-align: center;
        background: #ffffff;
        box-sizing: border-box;
    }

    .category-icon {
        font-size: 35px;
        margin-bottom: 12px;
    }

    .category-name {
        font-size: 14px;
        font-weight: 700;
        color: #374151;
    }


    /* ========================================================
       BENEFITS
       ======================================================== */

    .benefits-section {
        background: #f8fafc;
        padding: 45px 7%;
    }

    .benefits {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 25px;
    }

    .benefit {
        display: flex;
        gap: 14px;
        align-items: center;
    }

    .benefit-icon {
        width: 48px;
        height: 48px;
        border-radius: 12px;
        background: #eff6ff;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 22px;
        flex-shrink: 0;
    }

    .benefit-title {
        font-size: 14px;
        font-weight: 700;
        color: #111827;
        margin-bottom: 4px;
    }

    .benefit-text {
        font-size: 12px;
        color: #6b7280;
    }


    /* ========================================================
       PRODUCTS
       ======================================================== */

    .products {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 24px;
    }

    .product-card {
        background: white;
        border: 1px solid #e5e7eb;
        border-radius: 14px;
        overflow: hidden;
    }

    .product-image {
        height: 220px;
        background: #f3f4f6;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 70px;
    }

    .product-info {
        padding: 18px;
    }

    .product-name {
        font-size: 16px;
        font-weight: 700;
        color: #111827;
        margin-bottom: 8px;
    }

    .product-price {
        font-size: 18px;
        font-weight: 800;
        color: #2563eb;
    }

    .product-rating {
        font-size: 13px;
        color: #f59e0b;
        margin-top: 8px;
    }


    /* ========================================================
       FOOTER
       ======================================================== */

    .shop-footer {
        background: #111827;
        color: #d1d5db;
        text-align: center;
        padding: 35px;
        font-size: 13px;
    }


    /* ========================================================
       FLOATING SUPPORT BUTTON
       ======================================================== */

    div[class*="st-key-support_button"] {
        position: fixed !important;
        right: 28px !important;
        bottom: 28px !important;
        width: 64px !important;
        height: 64px !important;
        z-index: 999999 !important;
    }

    div[class*="st-key-support_button"] button {
        width: 64px !important;
        height: 64px !important;
        min-height: 64px !important;
        border-radius: 50% !important;
        border: none !important;
        background: #2563eb !important;
        color: white !important;
        font-size: 26px !important;
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.22) !important;
        transition: all 0.2s ease !important;
    }

    div[class*="st-key-support_button"] button:hover {
        transform: scale(1.06);
        background: #1d4ed8 !important;
    }


    /* ========================================================
       FLOATING CHAT WINDOW
       ======================================================== */

    div[class*="st-key-chat_window"] {
        position: fixed !important;
        right: 28px !important;
        bottom: 105px !important;
        width: 480px !important;
        height: 650px !important;
        max-width: calc(100vw - 35px) !important;

        background: white !important;
        border: 1px solid #e5e7eb !important;
        border-radius: 20px !important;

        box-shadow:
            0 20px 50px rgba(0, 0, 0, 0.18) !important;

        z-index: 999998 !important;

        overflow-y: auto !important;
        overflow-x: hidden !important;

        padding: 0 !important;
    }

    div[class*="st-key-chat_window"] > div {
        padding: 0 18px 18px 18px !important;
    }


    /* ========================================================
       CHAT HEADER
       ======================================================== */

    .chat-header {
        margin: 0 -18px 18px -18px;
        padding: 18px 20px;
        background: #2563eb;
        color: white;
        border-radius: 20px 20px 0 0;

        display: flex;
        align-items: center;
        justify-content: space-between;
    }

    .chat-title {
        font-size: 16px;
        font-weight: 700;
    }

    .chat-status {
        font-size: 12px;
        margin-top: 3px;
        opacity: 0.9;
    }


    /* ========================================================
       WELCOME MESSAGE
       ======================================================== */

    .welcome-box {
        background: #f8fafc;
        border: 1px solid #e5e7eb;
        border-radius: 14px;
        padding: 17px;
        margin-bottom: 16px;
    }

    .welcome-title {
        font-size: 15px;
        font-weight: 700;
        color: #111827;
        margin-bottom: 8px;
    }

    .welcome-text {
        font-size: 13px;
        line-height: 1.55;
        color: #4b5563;
    }


    /* ========================================================
       CHAT MESSAGES
       ======================================================== */

    div[class*="st-key-chat_window"] [data-testid="stChatMessage"] {
        margin-bottom: 8px !important;
    }


    /* ========================================================
       CHAT INPUT
       ======================================================== */

    div[class*="st-key-chat_window"] [data-testid="stForm"] {
        border: 1px solid #d1d5db !important;
        border-radius: 12px !important;
        padding: 8px !important;
        background: white !important;
        margin-top: 12px !important;
    }

    div[class*="st-key-chat_window"] [data-testid="stTextInput"] input {
        border: none !important;
        box-shadow: none !important;
        font-size: 14px !important;
    }

    div[class*="st-key-chat_window"] [data-testid="stTextInput"] input:focus {
        border: none !important;
        box-shadow: none !important;
    }

    div[class*="st-key-chat_window"] [data-testid="stFormSubmitButton"] button {
        background: #2563eb !important;
        color: white !important;
        border: none !important;
        border-radius: 9px !important;
        min-height: 40px !important;
        font-size: 18px !important;
    }

    div[class*="st-key-chat_window"] [data-testid="stFormSubmitButton"] button:hover {
        background: #1d4ed8 !important;
    }


    /* ========================================================
       MOBILE
       ======================================================== */

    @media (max-width: 700px) {

        .nav-links {
            display: none;
        }

        .hero {
            min-height: 400px;
            padding: 40px 25px;
        }

        .hero h1 {
            font-size: 38px;
        }

        .categories {
            grid-template-columns: repeat(2, 1fr);
        }

        .benefits {
            grid-template-columns: repeat(2, 1fr);
        }

        .products {
            grid-template-columns: repeat(2, 1fr);
        }

        div[class*="st-key-chat_window"] {
            right: 12px !important;
            bottom: 92px !important;
            width: calc(100vw - 24px) !important;
            height: 70vh !important;
        }

        div[class*="st-key-support_button"] {
            right: 18px !important;
            bottom: 18px !important;
        }
    }

</style>
""")


# ============================================================
# STORE FRONT
# ============================================================

st.html("""
<div class="shop-navbar">

    <div class="shop-logo">
        Shop<span>Ease</span>
    </div>

    <div class="nav-links">
        <span>Home</span>
        <span>Categories</span>
        <span>Deals</span>
        <span>New Arrivals</span>
    </div>

    <div class="nav-icons">
        <span>⌕</span>
        <span>♡</span>
        <span>🛒</span>
    </div>

</div>


<div class="hero">

    <div class="hero-content">

        <div class="hero-small">
            Welcome to ShopEase
        </div>

        <h1>
            Everything you need.<br>
            All in one place.
        </h1>

        <p>
            Discover great products, exciting deals and
            everything you need for everyday life.
        </p>

        <div class="hero-badge">
            Explore Our Collection
        </div>

    </div>

</div>


<div class="section">

    <div class="section-title">
        Shop by Category
    </div>

    <div class="section-subtitle">
        Find exactly what you're looking for
    </div>

    <div class="categories">

        <div class="category-card">
            <div class="category-icon">📱</div>
            <div class="category-name">Electronics</div>
        </div>

        <div class="category-card">
            <div class="category-icon">👕</div>
            <div class="category-name">Fashion</div>
        </div>

        <div class="category-card">
            <div class="category-icon">🏠</div>
            <div class="category-name">Home</div>
        </div>

        <div class="category-card">
            <div class="category-icon">🎮</div>
            <div class="category-name">Gaming</div>
        </div>

        <div class="category-card">
            <div class="category-icon">💄</div>
            <div class="category-name">Beauty</div>
        </div>

        <div class="category-card">
            <div class="category-icon">⚽</div>
            <div class="category-name">Sports</div>
        </div>

    </div>

</div>


<div class="benefits-section">

    <div class="benefits">

        <div class="benefit">

            <div class="benefit-icon">
                🚚
            </div>

            <div>
                <div class="benefit-title">
                    Fast Delivery
                </div>

                <div class="benefit-text">
                    Quick and reliable delivery
                </div>
            </div>

        </div>


        <div class="benefit">

            <div class="benefit-icon">
                🔒
            </div>

            <div>
                <div class="benefit-title">
                    Secure Payments
                </div>

                <div class="benefit-text">
                    Your payments are protected
                </div>
            </div>

        </div>


        <div class="benefit">

            <div class="benefit-icon">
                ↩️
            </div>

            <div>
                <div class="benefit-title">
                    Easy Returns
                </div>

                <div class="benefit-text">
                    Simple return process
                </div>
            </div>

        </div>


        <div class="benefit">

            <div class="benefit-icon">
                🎧
            </div>

            <div>
                <div class="benefit-title">
                    24/7 Support
                </div>

                <div class="benefit-text">
                    We're always here to help
                </div>
            </div>

        </div>

    </div>

</div>


<div class="section">

    <div class="section-title">
        Popular Products
    </div>

    <div class="section-subtitle">
        Some of our customer favourites
    </div>

    <div class="products">

        <div class="product-card">

            <div class="product-image">
                🎧
            </div>

            <div class="product-info">

                <div class="product-name">
                    Wireless Headphones
                </div>

                <div class="product-price">
                    ₹2,499
                </div>

                <div class="product-rating">
                    ★★★★★
                </div>

            </div>

        </div>


        <div class="product-card">

            <div class="product-image">
                ⌚
            </div>

            <div class="product-info">

                <div class="product-name">
                    Smart Watch
                </div>

                <div class="product-price">
                    ₹3,999
                </div>

                <div class="product-rating">
                    ★★★★★
                </div>

            </div>

        </div>


        <div class="product-card">

            <div class="product-image">
                👟
            </div>

            <div class="product-info">

                <div class="product-name">
                    Running Shoes
                </div>

                <div class="product-price">
                    ₹2,199
                </div>

                <div class="product-rating">
                    ★★★★☆
                </div>

            </div>

        </div>


        <div class="product-card">

            <div class="product-image">
                📷
            </div>

            <div class="product-info">

                <div class="product-name">
                    Digital Camera
                </div>

                <div class="product-price">
                    ₹24,999
                </div>

                <div class="product-rating">
                    ★★★★★
                </div>

            </div>

        </div>

    </div>

</div>


<div class="shop-footer">
    © 2026 ShopEase · Your trusted online shopping destination
</div>
""")


# ============================================================
# SUPPORT BUTTON
# ============================================================

support_icon = "✕" if st.session_state.chat_open else "🤖"

if st.button(
    support_icon,
    key="support_button",
    help="Customer Support",
):

    st.session_state.chat_open = not st.session_state.chat_open

    st.rerun()


# ============================================================
# VARIABLES
# ============================================================

send_message = False
user_input = ""


# ============================================================
# CHAT WINDOW
# ============================================================

if st.session_state.chat_open:

    with st.container(key="chat_window"):

        # ----------------------------------------------------
        # CHAT HEADER
        # ----------------------------------------------------

        st.html("""
        <div class="chat-header">

            <div>

                <div class="chat-title">
                    Customer Support
                </div>

                <div class="chat-status">
                    ● Online
                </div>

            </div>

        </div>
        """)


        # ----------------------------------------------------
        # WELCOME MESSAGE
        # ----------------------------------------------------

        if len(st.session_state.messages) == 0:

            st.html("""
            <div class="welcome-box">

                <div class="welcome-title">
                    👋 Hi! Welcome to ShopEase.
                </div>

                <div class="welcome-text">

                    I'm your Customer Support Agent.

                    <br><br>

                    I can help you with:

                    <br>
                    📦 Order status
                    <br>
                    🚚 Delivery information
                    <br>
                    🔄 Returns and refunds
                    <br>
                    🛍️ Product questions

                    <br><br>

                    How can I help you today?

                </div>

            </div>
            """)


        # ----------------------------------------------------
        # CHAT HISTORY
        # ----------------------------------------------------

        for message in st.session_state.messages:

            role = message.get("role", "assistant")
            content = message.get("content", "")

            with st.chat_message(role):

                st.markdown(content)

                # ====================================================
                # DEBUG / AGENT DETAILS
                # Comment out this entire section whenever you don't
                # want to show tool details and agent logs.
                # ====================================================

                if role == "assistant":

                    tools_used = message.get("tools_used", [])
                    agent_log = message.get("agent_log", {})

                    # -------------------------------
                    # TOOLS USED
                    # -------------------------------

                    if tools_used:

                        with st.expander("🔧 Tools Used"):

                            if isinstance(tools_used, list):

                                for tool in tools_used:
                                    st.code(
                                        str(tool),
                                        language="text",
                                    )

                            else:
                                st.code(
                                    str(tools_used),
                                    language="text",
                                )


                    # -------------------------------
                    # AGENT LOG
                    # -------------------------------

                    if agent_log:

                        with st.expander("🧠 Agent Log"):

                            if isinstance(agent_log, dict):

                                for key, value in agent_log.items():

                                    st.markdown(
                                        f"**{key}:**"
                                    )

                                    st.code(
                                        str(value),
                                        language="text",
                                    )

                            else:

                                st.code(
                                    str(agent_log),
                                    language="text",
                                )

        # ----------------------------------------------------
        # INPUT FORM
        # ----------------------------------------------------

        with st.form(
            "chat_form",
            clear_on_submit=True,
        ):

            col1, col2 = st.columns(
                [5, 1],
                vertical_alignment="center",
            )

            with col1:

                user_input = st.text_input(
                    "Message",
                    placeholder="Type your message...",
                    label_visibility="collapsed",
                    key="chat_message_input",
                )

            with col2:

                send_message = st.form_submit_button(
                    "➤",
                    use_container_width=True,
                )


# ============================================================
# SEND MESSAGE TO BACKEND
# ============================================================

if (
    st.session_state.chat_open
    and send_message
    and user_input.strip()
):

    # --------------------------------------------------------
    # USER MESSAGE
    # --------------------------------------------------------

    clean_input = user_input.strip()

    st.session_state.messages.append({
        "role": "user",
        "content": clean_input,
    })


    # --------------------------------------------------------
    # BACKEND REQUEST
    # --------------------------------------------------------

    try:

        response = requests.post(
            f"{BACKEND_URL}/chat",
            params={
                "user_input": clean_input,
                "conversation_id": st.session_state.conversation_id,
            },
            timeout=60,
        )

        response.raise_for_status()

        data = response.json()

        answer = data["response"]

        tools_used = data.get(
            "tools_used",
            [],
        )

        agent_log = data.get(
            "agent_log",
            {},
        )


        # ----------------------------------------------------
        # ASSISTANT MESSAGE
        # ----------------------------------------------------

        st.session_state.messages.append({
            "role": "assistant",
            "content": answer,
            "tools_used": tools_used,
            "agent_log": agent_log,
        })


    # --------------------------------------------------------
    # CONNECTION ERROR
    # --------------------------------------------------------

    except requests.exceptions.ConnectionError:

        st.session_state.messages.append({
            "role": "assistant",
            "content": (
                "⚠️ I couldn't connect to the support server. "
                "Please make sure your FastAPI backend is running "
                "at http://127.0.0.1:8000."
            ),
        })


    # --------------------------------------------------------
    # TIMEOUT
    # --------------------------------------------------------

    except requests.exceptions.Timeout:

        st.session_state.messages.append({
            "role": "assistant",
            "content": (
                "⏳ The support server took too long to respond. "
                "Please try again."
            ),
        })


    # --------------------------------------------------------
    # HTTP ERROR
    # --------------------------------------------------------

    except requests.exceptions.HTTPError as e:

        st.session_state.messages.append({
            "role": "assistant",
            "content": (
                f"⚠️ The support server returned an error: {e}"
            ),
        })


    # --------------------------------------------------------
    # OTHER ERROR
    # --------------------------------------------------------

    except Exception as e:

        st.session_state.messages.append({
            "role": "assistant",
            "content": (
                f"⚠️ Something went wrong: {e}"
            ),
        })


    # --------------------------------------------------------
    # REFRESH CHAT
    # --------------------------------------------------------

    st.rerun()