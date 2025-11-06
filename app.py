# 🏆 Sports Guy - Streamlit Web App (Fixed for deployment)

import streamlit as st
from openai import OpenAI
import os

# --- Streamlit UI Setup ---
st.set_page_config(page_title="Sports Guy - Your Sports Assistant", page_icon="🏆", layout="centered")

st.title("🏆 Sports Guy - Your Sports Buddy 🏏⚽🏀🎾")
st.caption("Ask me anything about sports — rules, players, tournaments, and more!")

# Sidebar for API Key input
st.sidebar.header("🔑 API Key Setup")
api_key = st.sidebar.text_input("Enter your OpenRouter API Key:", type="password")

if not api_key:
    st.warning("⚠️ Please enter your OpenRouter API key in the sidebar to start chatting.")
    st.stop()

# ✅ Fix: Set API key & base URL as environment variables
os.environ["OPENAI_API_KEY"] = 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
os.environ["OPENAI_BASE_URL"] = "https://openrouter.ai/api/v1"

# Initialize OpenAI client (no parameters needed now)
client = OpenAI()

# --- Personality ---
SYSTEM_PROMPT = """
You are 'Sports Guy' — an energetic, friendly, and knowledgeable sports assistant 🏆.
You help users with:
- Rules and gameplay of major sports (cricket, football, basketball, tennis, hockey)
- Player stats, records, and trivia
- Tournament history and recent highlights
Style:
- Speak like a sports buddy (casual but informative)
- Use emojis 🏏⚽🏀🎾🏒
- Politely decline non-sports topics
"""

MODEL = "deepseek/deepseek-chat-v3.1:free"
TEMPERATURE = 0.8

# --- Chat Memory ---
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]

# --- Display Chat ---
for msg in st.session_state.messages:
    if msg["role"] == "user":
        with st.chat_message("user"):
            st.write(msg["content"])
    elif msg["role"] == "assistant":
        with st.chat_message("assistant"):
            st.write(msg["content"])

# --- Chat Input ---
if user_input := st.chat_input("Ask me about any sport..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Sports Guy is thinking... ⚡"):
            response = client.chat.completions.create(
                model=MODEL,
                temperature=TEMPERATURE,
                messages=st.session_state.messages
            )
            reply = response.choices[0].message.content
            st.write(reply)

    st.session_state.messages.append({"role": "assistant", "content": reply})
