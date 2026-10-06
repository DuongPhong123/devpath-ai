import streamlit as st
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from ai_mentor import stream_chat
from curriculum import get_lesson_by_id, MODULES

st.set_page_config(page_title="AI Mentor — DevPath AI", page_icon="🤖", layout="wide")

st.markdown("""
<style>
.chat-user {
    background: #1F2937;
    border-radius: 12px 12px 4px 12px;
    padding: 12px 16px;
    margin: 8px 0 8px auto;
    max-width: 75%;
    border: 1px solid #374151;
}
.chat-ai {
    background: #0F172A;
    border-radius: 12px 12px 12px 4px;
    padding: 12px 16px;
    margin: 8px auto 8px 0;
    max-width: 85%;
    border: 1px solid #1E3A5F;
}
.mentor-header {
    background: linear-gradient(135deg, #0F172A, #1E1B4B);
    border: 1px solid #312E81;
    border-radius: 12px;
    padding: 16px 20px;
    margin-bottom: 16px;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="mentor-header">
  <h2 style="margin:0">🤖 AI Mentor</h2>
  <p style="margin:4px 0 0;color:#9CA3AF;font-size:0.9rem">Hỏi bất cứ điều gì về lập trình — AI sẽ giải thích theo cách dễ hiểu nhất cho anh!</p>
</div>
""", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

if "lesson_context" not in st.session_state:
    st.session_state.lesson_context = None

with st.sidebar:
    st.markdown("### 📌 Ngữ cảnh bài học")
    lesson_options = {"Không chọn": None}
    for mod in MODULES:
        for les in mod.get("lessons", []):
            label = f"{mod['icon']} {les['title']}"
            lesson_options[label] = les["id"]

    selected_label = st.selectbox("Đang học bài:", list(lesson_options.keys()))
    selected_id = lesson_options[selected_label]
    if selected_id:
        les = get_lesson_by_id(selected_id)
        if les:
            ctx = f"Tiêu đề: {les['title']}\nNội dung tóm tắt:\n{les['content'][:500]}..."
            st.session_state.lesson_context = ctx
            st.info(f"AI đang hỗ trợ bài: **{les['title']}**")
    else:
        st.session_state.lesson_context = None

    st.markdown("---")
    st.markdown("### 💡 Câu hỏi gợi ý")
    suggestions = [
        "Biến trong Python là gì?",
        "for loop và while loop khác nhau thế nào?",
        "Tại sao cần dùng hàm?",
        "List comprehension dùng khi nào?",
        "Làm sao debug lỗi trong Python?",
    ]
    for s in suggestions:
        if st.button(s, key=f"sug_{s}", use_container_width=True):
            st.session_state["pending_question"] = s

    st.markdown("---")
    if st.button("🗑️ Xóa lịch sử chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

if st.session_state.get("quick_question"):
    st.session_state["pending_question"] = st.session_state.pop("quick_question")

for msg in st.session_state.messages:
    role = msg["role"]
    content = msg["content"]
    if role == "user":
        st.markdown(f'<div class="chat-user">👤 {content}</div>', unsafe_allow_html=True)
    else:
        with st.chat_message("assistant", avatar="🤖"):
            st.markdown(content)

pending = st.session_state.pop("pending_question", None)
user_input = st.chat_input("Hỏi AI Mentor...") or pending

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.markdown(f'<div class="chat-user">👤 {user_input}</div>', unsafe_allow_html=True)

    api_messages = [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]

    with st.chat_message("assistant", avatar="🤖"):
        response_placeholder = st.empty()
        full_response = ""
        for chunk in stream_chat(api_messages, st.session_state.lesson_context):
            full_response += chunk
            response_placeholder.markdown(full_response + "▌")
        response_placeholder.markdown(full_response)

    st.session_state.messages.append({"role": "assistant", "content": full_response})
