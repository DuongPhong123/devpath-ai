import streamlit as st
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from curriculum import MODULES, PHASES, get_lesson_by_id
from progress import load_progress, complete_lesson, save_note

st.set_page_config(page_title="Bài Học — DevPath AI", page_icon="📚", layout="wide")

st.markdown("""
<style>
.module-card {
    background: #111827;
    border: 1px solid #1F2937;
    border-radius: 10px;
    padding: 14px 16px;
    margin-bottom: 10px;
    cursor: pointer;
    transition: border-color 0.2s;
}
.module-card:hover { border-color: #4F7CFF; }
.lesson-item {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 10px 14px;
    border-radius: 8px;
    margin: 4px 0;
    background: #0D1117;
    border: 1px solid #1F2937;
    cursor: pointer;
}
.lesson-done { border-left: 3px solid #10B981; }
.lesson-todo { border-left: 3px solid #374151; }
.lesson-active { border-left: 3px solid #4F7CFF; background: #0F172A; }
.quiz-option {
    padding: 10px 14px;
    border-radius: 8px;
    margin: 6px 0;
    border: 1px solid #374151;
    cursor: pointer;
}
.quiz-correct { background: #064E3B; border-color: #10B981; }
.quiz-wrong { background: #450A0A; border-color: #EF4444; }
</style>
""", unsafe_allow_html=True)

progress = load_progress()
done_lessons = set(progress.get("completed_lessons", []))

if "open_lesson" not in st.session_state:
    st.session_state.open_lesson = None
if "quiz_answers" not in st.session_state:
    st.session_state.quiz_answers = {}
if "quiz_submitted" not in st.session_state:
    st.session_state.quiz_submitted = False


def lesson_sidebar():
    with st.sidebar:
        st.markdown("### 📚 Danh sách bài học")
        for mod in MODULES:
            phase_info = PHASES.get(mod["phase"], {})
            mod_lessons = mod.get("lessons", [])
            done_count = sum(1 for l in mod_lessons if l["id"] in done_lessons)

            with st.expander(f"{mod['icon']} {mod['title']} ({done_count}/{len(mod_lessons)})", expanded=True):
                for les in mod_lessons:
                    is_done = les["id"] in done_lessons
                    is_active = st.session_state.open_lesson == les["id"]
                    icon = "✅" if is_done else ("▶️" if is_active else "⭕")
                    btn_label = f"{icon} {les['title']} · {les['xp']}XP"
                    if st.button(btn_label, key=f"btn_{les['id']}", use_container_width=True):
                        st.session_state.open_lesson = les["id"]
                        st.session_state.quiz_answers = {}
                        st.session_state.quiz_submitted = False
                        st.rerun()


def show_lesson_content(lesson_id: str):
    les = get_lesson_by_id(lesson_id)
    if not les:
        st.error("Không tìm thấy bài học!")
        return

    mod_info = next((m for m in MODULES if any(l["id"] == lesson_id for l in m.get("lessons", []))), None)
    phase_info = PHASES.get(mod_info["phase"], {}) if mod_info else {}

    is_done = lesson_id in done_lessons

    col_title, col_meta = st.columns([3, 1])
    with col_title:
        if mod_info:
            st.markdown(f"*{mod_info['icon']} {mod_info['title']} · Phase {mod_info['phase']}*")
        st.markdown(f"# {les['title']}")
    with col_meta:
        st.markdown(f"**⚡ {les['xp']} XP** · **⏱ {les['minutes']} phút**")
        if is_done:
            st.success("✅ Đã hoàn thành")

    st.markdown("---")

    tab_labels = ["📖 Nội dung", "🧪 Quiz", "💾 Ghi chú"]
    if les.get("exercise"):
        tab_labels.insert(2, "💻 Bài tập")

    tabs = st.tabs(tab_labels)

    with tabs[0]:
        st.markdown(les["content"])
        st.markdown("---")
        if not is_done:
            if st.button("✅ Đánh dấu đã đọc xong", type="primary", use_container_width=True):
                complete_lesson(lesson_id, les["xp"] // 2)
                st.success(f"👍 Đã ghi nhận! +{les['xp'] // 2} XP")
                st.rerun()
        else:
            st.info("✅ Anh đã hoàn thành bài này rồi!")

    with tabs[1]:
        quiz_list = les.get("quiz", [])
        if not quiz_list:
            st.info("Bài học này chưa có câu hỏi quiz.")
        else:
            st.markdown(f"### 🧪 Quiz — {len(quiz_list)} câu")
            if not st.session_state.quiz_submitted:
                for i, q in enumerate(quiz_list):
                    st.markdown(f"**Câu {i+1}: {q['q']}**")
                    answer = st.radio(
                        f"Chọn đáp án câu {i+1}:",
                        q["options"],
                        key=f"q_{lesson_id}_{i}",
                        label_visibility="collapsed",
                    )
                    st.session_state.quiz_answers[i] = answer

                if st.button("📝 Nộp bài", type="primary", use_container_width=True):
                    st.session_state.quiz_submitted = True
                    st.rerun()
            else:
                correct_count = 0
                for i, q in enumerate(quiz_list):
                    user_ans = st.session_state.quiz_answers.get(i)
                    correct_ans = q["options"][q["correct"]]
                    is_correct = user_ans == correct_ans
                    if is_correct:
                        correct_count += 1

                    with st.container():
                        st.markdown(f"**Câu {i+1}: {q['q']}**")
                        for opt in q["options"]:
                            if opt == correct_ans:
                                st.markdown(f"✅ **{opt}** ← Đáp án đúng")
                            elif opt == user_ans and not is_correct:
                                st.markdown(f"❌ ~~{opt}~~ ← Anh chọn")
                            else:
                                st.markdown(f"◦ {opt}")
                        if q.get("explain"):
                            st.info(f"💡 {q['explain']}")
                        st.markdown("")

                score_pct = correct_count / len(quiz_list) * 100
                xp_bonus = int(les["xp"] * score_pct / 100)

                if score_pct >= 80:
                    st.success(f"🎉 Xuất sắc! {correct_count}/{len(quiz_list)} đúng — +{xp_bonus} XP!")
                    complete_lesson(lesson_id, xp_bonus, int(score_pct))
                elif score_pct >= 60:
                    st.warning(f"👍 Khá tốt! {correct_count}/{len(quiz_list)} đúng — +{xp_bonus} XP")
                    complete_lesson(lesson_id, xp_bonus, int(score_pct))
                else:
                    st.error(f"💪 Cần ôn thêm! {correct_count}/{len(quiz_list)} đúng. Thử lại nhé!")

                col1, col2 = st.columns(2)
                with col1:
                    if st.button("🔄 Làm lại", use_container_width=True):
                        st.session_state.quiz_answers = {}
                        st.session_state.quiz_submitted = False
                        st.rerun()
                with col2:
                    if st.button("➡️ Bài tiếp theo", use_container_width=True, type="primary"):
                        all_lessons = [l for m in MODULES for l in m.get("lessons", [])]
                        ids = [l["id"] for l in all_lessons]
                        if lesson_id in ids:
                            idx = ids.index(lesson_id)
                            if idx + 1 < len(ids):
                                st.session_state.open_lesson = ids[idx + 1]
                                st.session_state.quiz_answers = {}
                                st.session_state.quiz_submitted = False
                                st.rerun()

    exercise_tab_idx = 2 if les.get("exercise") else None
    if exercise_tab_idx is not None:
        with tabs[exercise_tab_idx]:
            ex = les["exercise"]
            st.markdown(f"### 💻 Bài tập thực hành")
            st.markdown(f"**Yêu cầu:** {ex['description']}")
            st.markdown("**Code mẫu khởi đầu:**")
            st.code(ex.get("starter_code", "# Viết code của anh ở đây\n"), language="python")
            st.info("💡 Chép code sang trang **Code Lab** để chạy thử và nhận AI review nhé anh!")
            if st.button("🚀 Mở Code Lab", use_container_width=True):
                st.session_state["code_lab_starter"] = ex.get("starter_code", "")
                st.session_state["code_lab_task"] = ex["description"]
                st.switch_page("pages/3_💻_Code_Lab.py")

    note_tab_idx = len(tab_labels) - 1
    with tabs[note_tab_idx]:
        st.markdown("### 📝 Ghi chú cá nhân")
        existing_note = progress.get("lesson_notes", {}).get(lesson_id, "")
        note = st.text_area("Ghi chú của anh về bài này:", value=existing_note, height=200,
                            placeholder="Điểm quan trọng, câu hỏi, ví dụ riêng...")
        if st.button("💾 Lưu ghi chú", use_container_width=True):
            save_note(lesson_id, note)
            st.success("✅ Đã lưu ghi chú!")


def main():
    lesson_sidebar()

    open_id = st.session_state.get("open_lesson")

    if open_id:
        show_lesson_content(open_id)
    else:
        st.markdown("# 📚 Bài Học")
        st.markdown("Chọn bài học từ danh sách bên trái để bắt đầu.")
        st.markdown("---")

        for mod in MODULES:
            phase_info = PHASES.get(mod["phase"], {})
            mod_lessons = mod.get("lessons", [])
            done_count = sum(1 for l in mod_lessons if l["id"] in done_lessons)

            st.markdown(f"""
<div class="module-card" style="border-left: 3px solid {phase_info.get('color','#4F7CFF')}">
  <div style="display:flex;justify-content:space-between">
    <span style="font-size:1.1rem;font-weight:600">{mod['icon']} {mod['title']}</span>
    <span style="color:#9CA3AF;font-size:0.85rem">{done_count}/{len(mod_lessons)} bài · Phase {mod['phase']}</span>
  </div>
</div>""", unsafe_allow_html=True)
            cols = st.columns(min(len(mod_lessons), 3))
            for i, les in enumerate(mod_lessons):
                with cols[i % 3]:
                    is_done = les["id"] in done_lessons
                    icon = "✅" if is_done else "📖"
                    if st.button(f"{icon} {les['title']}\n⚡{les['xp']}XP · {les['minutes']}p",
                                 key=f"grid_{les['id']}", use_container_width=True):
                        st.session_state.open_lesson = les["id"]
                        st.session_state.quiz_answers = {}
                        st.session_state.quiz_submitted = False
                        st.rerun()
            st.markdown("")


if __name__ == "__main__":
    main()
