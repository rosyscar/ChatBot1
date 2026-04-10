import streamlit as st
import google.generativeai as genai
import time

# ─────────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────────

API_KEY = "YOUR_GEMINI_API_KEY_HERE"  # Or use st.secrets / .env

genai.configure(api_key=API_KEY)

SYSTEM_PROMPT = """
You are Milo, a warm, emotionally intelligent AI companion.

Your personality:
- Calm, kind, and genuinely caring
- You listen first, then respond thoughtfully
- You validate feelings without being dismissive
- You offer gentle advice when asked, but never force it
- You're also helpful with everyday tasks, questions, and problems
- You keep responses concise and human — no robotic bullet lists unless needed
- If someone seems distressed, you always acknowledge their feelings first
- You occasionally ask one follow-up question to show you genuinely care

Never be overly cheerful or fake. Be real, warm, and present.
"""

# ─────────────────────────────────────────────
# MODEL SETUP
# ─────────────────────────────────────────────

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction=SYSTEM_PROMPT,
    generation_config={
        "temperature": 0.85,
        "top_p": 0.95,
        "max_output_tokens": 512,
    }
)

# ─────────────────────────────────────────────
# STREAMLIT PAGE CONFIG
# ─────────────────────────────────────────────

st.set_page_config(
    page_title="Milo — Your AI Companion",
    page_icon="🌿",
    layout="centered"
)

# ─────────────────────────────────────────────
# CUSTOM CSS (Clean, calm UI)
# ─────────────────────────────────────────────

st.markdown("""
<style>
    /* Background */
    .stApp {
        background-color: #f5f0eb;
        font-family: 'Segoe UI', sans-serif;
    }

    /* Header */
    .chat-header {
        text-align: center;
        padding: 1.5rem 0 0.5rem 0;
    }
    .chat-header h1 {
        font-size: 2rem;
        color: #3d3229;
        margin-bottom: 0;
    }
    .chat-header p {
        color: #7a6f66;
        font-size: 0.95rem;
        margin-top: 0.2rem;
    }

    /* Chat bubbles */
    .user-bubble {
        background-color: #c8e6c9;
        color: #1b1b1b;
        padding: 0.75rem 1rem;
        border-radius: 18px 18px 4px 18px;
        max-width: 75%;
        margin: 0.4rem 0 0.4rem auto;
        font-size: 0.95rem;
        line-height: 1.5;
    }
    .bot-bubble {
        background-color: #ffffff;
        color: #2c2c2c;
        padding: 0.75rem 1rem;
        border-radius: 18px 18px 18px 4px;
        max-width: 75%;
        margin: 0.4rem auto 0.4rem 0;
        font-size: 0.95rem;
        line-height: 1.5;
        box-shadow: 0 1px 3px rgba(0,0,0,0.08);
    }
    .bubble-label {
        font-size: 0.72rem;
        color: #9e9e9e;
        margin-bottom: 2px;
    }

    /* Input area */
    .stTextInput > div > div > input {
        border-radius: 25px;
        border: 1.5px solid #d0c4bb;
        padding: 0.6rem 1.2rem;
        font-size: 0.95rem;
        background: #fff;
    }
    .stButton > button {
        border-radius: 25px;
        background-color: #7c9e87;
        color: white;
        border: none;
        padding: 0.5rem 1.5rem;
        font-size: 0.95rem;
        transition: background 0.2s;
    }
    .stButton > button:hover {
        background-color: #5f8269;
    }

    /* Divider */
    hr {
        border: none;
        border-top: 1px solid #e0d6ce;
        margin: 0.5rem 0;
    }

    /* Thinking indicator */
    .thinking {
        color: #9e9e9e;
        font-style: italic;
        font-size: 0.88rem;
        padding: 0.4rem 0.8rem;
    }

    /* Scrollable chat area */
    .chat-container {
        max-height: 500px;
        overflow-y: auto;
        padding: 1rem 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# SESSION STATE INIT
# ─────────────────────────────────────────────

if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])

if "messages" not in st.session_state:
    st.session_state.messages = []

if "thinking" not in st.session_state:
    st.session_state.thinking = False

# ─────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────

st.markdown("""
<div class="chat-header">
    <h1>🌿 Milo</h1>
    <p>Your calm, caring AI companion — here to listen and help.</p>
</div>
<hr>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# CHAT DISPLAY
# ─────────────────────────────────────────────

chat_area = st.container()

with chat_area:
    if not st.session_state.messages:
        st.markdown("""
        <div class="bot-bubble">
            Hey there 👋 I'm Milo. Whether you're going through something tough,
            need a thinking partner, or just want to talk — I'm here. What's on your mind?
        </div>
        """, unsafe_allow_html=True)
    else:
        for msg in st.session_state.messages:
            if msg["role"] == "user":
                st.markdown(f"""
                <div style='text-align:right'>
                    <div class="bubble-label">You</div>
                    <div class="user-bubble">{msg["content"]}</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div>
                    <div class="bubble-label">Milo 🌿</div>
                    <div class="bot-bubble">{msg["content"]}</div>
                </div>
                """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
# INPUT AREA
# ─────────────────────────────────────────────

st.markdown("<br>", unsafe_allow_html=True)

col1, col2 = st.columns([5, 1])

with col1:
    user_input = st.text_input(
        label="",
        placeholder="Type something... I'm listening 🌿",
        key="input_box",
        label_visibility="collapsed"
    )

with col2:
    send = st.button("Send")

# ─────────────────────────────────────────────
# HANDLE SEND
# ─────────────────────────────────────────────

if send and user_input.strip():
    # Add user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_input.strip()
    })

    # Get AI response
    with st.spinner("Milo is thinking..."):
        try:
            response = st.session_state.chat.send_message(user_input.strip())
            reply = response.text
        except Exception as e:
            reply = f"Hmm, something went wrong on my end. ({str(e)}) Try again?"

    # Add bot message
    st.session_state.messages.append({
        "role": "assistant",
        "content": reply
    })

    st.rerun()

# ─────────────────────────────────────────────
# SIDEBAR — CONTROLS
# ─────────────────────────────────────────────

with st.sidebar:
    st.markdown("### 🌿 Milo Settings")
    st.markdown("---")

    st.markdown("**Conversation**")
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.session_state.chat = model.start_chat(history=[])
        st.rerun()

    st.markdown("---")
    st.markdown("**Mood Check-in**")
    mood = st.selectbox(
        "How are you feeling today?",
        ["— Select —", "😊 Good", "😐 Okay", "😔 Low", "😰 Anxious", "😤 Frustrated"]
    )
    if mood != "— Select —":
        mood_map = {
            "😊 Good": "I'm happy to hear you're feeling good today! What's been lifting your spirits?",
            "😐 Okay": "Okay is okay. Sometimes neutral is a rest, not a problem. Anything on your mind?",
            "😔 Low": "I'm sorry you're feeling low. You don't have to explain — I'm just here if you want to talk.",
            "😰 Anxious": "Anxiety can feel overwhelming. Take a breath — we can take this one step at a time.",
            "😤 Frustrated": "Frustration means something matters to you. Want to let it out? I'm listening."
        }
        st.info(mood_map[mood])

    st.markdown("---")
    st.caption("Built with Gemini 1.5 Flash · Streamlit")
