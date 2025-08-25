
import streamlit as st
import base64
from multilingual_utils import detect_language, translate_to_english, translate_from_english
from retriever import generate_answer
# ---------------------------
# Knowledge Base
# ---------------------------
knowledge_base = {
    "does guvi provide certificates?": "Yes, GUVI provides verifiable certificates for completed courses.",
    "does guvi provide placement support?": "Yes, GUVI offers placement support through Zen Class and career services.",
    "where can i find the courses?": "You can explore courses directly on GUVI’s official website.",
    "tell me about guvi?": "GUVI is an online learning platform offering courses in Data Science, AI, Full Stack, and more."
}

# ---------------------------
# Fallback Response Function
# ---------------------------
def get_response(user_query, knowledge_base):
    response = knowledge_base.get(user_query.lower())
    if response:
        return response
    else:
        return """I'm sorry, I don’t have an exact answer for that. 
        But I can help you with GUVI courses, certifications, and placement support. 
        You may explore GUVI’s official site for more options."""

# ---------------------------
# Page Config
# ---------------------------
st.set_page_config(page_title="GUVI Multilingual GPT Chatbot", page_icon="🌍")

# Load and encode GUVI logo
with open("/content/guvilogo.png", "rb") as f:
    encoded = base64.b64encode(f.read()).decode()

# Center logo + Title
st.markdown(
    f"""
    <div style="text-align: center;">
        <img src="data:image/png;base64,{encoded}" width="250"><br>
        <h1>GUVI Multilingual GPT Chatbot</h1>
    </div>
    """,
    unsafe_allow_html=True
)

st.write("Talk to a multilingual chatbot powered by RAG + LLMs")

# Initialize conversation history
if "history" not in st.session_state:
    st.session_state.history = []

# ---------------------------
# Layout: Row-wise Input + Language
# ---------------------------
# Input row with Clear Chat button on right
col1, col2 = st.columns([4,1])

with col1:
    user_input = st.text_input("💬 Your Message:", "", key="user_input", placeholder="Type your message...")

with col2:
    st.write("")  # spacing
    st.write("")  # spacing
    if st.button("🗑️ Clear Chat"):
        st.session_state.history = []

# Language row (all in one line, horizontal)
st.markdown("🌐 **Language Settings**")
lang_option = st.radio(
    "Select language",
    ["Auto Detect", "English", "Tamil", "Hindi", "Telugu", "Kannada"],
    index=0,
    horizontal=True
)
# ---------------------------
# Handle message
# ---------------------------
if user_input.strip():
    # Step 1: Detect language (or override with manual selection)
    if lang_option == "Auto Detect":
        lang = detect_language(user_input)
    else:
        lang_map = {"English": "en", "Tamil": "ta", "Hindi": "hi", "Telugu": "te", "Kannada": "kn"}
        lang = lang_map.get(lang_option, "en")

    # Step 2: Translate to English if needed
    query_en = translate_to_english(user_input) if lang != 'en' else user_input

    # Show translation preview
    st.markdown("🔎 **English Translation (for processing):**")
    st.info(query_en)

    # Step 3: Generate answer using RAG retriever
    response_en = generate_answer(query_en)

    # Step 4: Fallback if retriever fails
    if response_en and response_en.strip():
        bot_response = response_en
    else:
        bot_response = get_response(query_en, knowledge_base)

    # Step 5: Translate back if input wasn’t English
    final_response = translate_from_english(bot_response, lang) if lang != 'en' else response_en

    # Step 6: Save conversation
    st.session_state.history.append(("You", user_input))
    st.session_state.history.append(("Bot", final_response))

# ---------------------------
# Chat history display
# ---------------------------
st.markdown("---")
for speaker, msg in st.session_state.history:
    if speaker == "You":
        st.markdown(f"**👤 {speaker}:** {msg}")
    else:
        st.markdown(f"**🤖 {speaker}:** {msg}")

