import streamlit as st
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from curriculum import MODULES, PHASES, get_all_lessons, get_total_xp
from progress import load_progress, get_level, get_streak, get_completion_pct, get_weekly_xp

st.set_page_config(
    page_title="DevPath AI — Học Lập Trình",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
[data-testid="stSidebar"] { background: #0D1117; }
.metric-card {
    background: linear-gradient(135deg, #111827, #1F2937);
    border: 1px solid #374151;
    border-radius: 12px;
    padding: 18px 20px;
    text-align: center;
}
.metric-value { font-size: 2rem; font-weight: 800; color: #4F7CFF; }
.metric-label { font-size: 0.8rem; color: #9CA3AF; margin-top: 4px; }
.xp-bar-bg {
    background: #1F2937;
    border-radius: 999px;
    height: 12px;
    margin: 8px 0;
}
.xp-bar-fill {
    background: linear-gradient(90deg, #4F7CFF, #7C3AED);
    border-radius: 999px;
    height: 12px;
}
.phase-card {
    background: #111827;
    border: 1px solid #1F2937;
    border-radius: 10px;
    padding: 14px 16px;
    margin-bottom: 10px;
    cursor: pointer;
}
.lesson-row {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 8px 0;
    border-bottom: 1px solid #1F2937;
    font-size: 0.9rem;
}
.badge-done { color: #10B981; }
.badge-todo { color: #6B7280; }
</style>
""", unsafe_allow_html=True)


def sidebar():
    progress = load_progress()
    xp = progress["total_xp"]
    level, level_name, cur_thresh, next_thresh = get_level(xp)
    streak = get_streak(progress)
    pct = min((xp - cur_thresh) / max(next_thresh - cur_thresh, 1) * 100, 100)

    with st.sidebar:
        st.markdown("## 🚀 DevPath AI")
        st.markdown("---")

        name = progress.get("user_name", "Học viên")
        st.markdown(f"👋 **{name}**")
        st.markdown(f"🏅 {level_name} · Lv.{level}")
        st.markdown(f"""
<div class="xp-bar-bg">
  <div class="xp-bar-fill" style="width:{pct:.0f}%"></div>
</div>
<small style="color:#6B7280">{xp} / {next_thresh} XP</small>
""", unsafe_allow_html=True)
        st.markdown("")
        st.markdown(f"🔥 Streak: **{streak} ngày**")
        st.markdown("---")
        st.page_link("app.py", label="🏠 Dashboard", icon=None)
        st.page_link("pages/1_🤖_AI_Mentor.py", label="🤖 AI Mentor")
        st.page_link("pages/2_📚_Bài_Học.py", label="📚 Bài Học")
        st.page_link("pages/3_💻_Code_Lab.py", label="💻 Code Lab")
        st.page_link("pages/4_📊_Tiến_Độ.py", label="📊 Tiến Độ")
        st.markdown("---")

        if st.button("⚙️ Cài Đặt"):
            st.session_state["show_settings"] = True


def show_settings_modal(progress):
    if st.session_state.get("show_settings"):
        with st.expander("⚙️ Cài đặt", expanded=True):
            name = st.text_input("Tên của anh", value=progress.get("user_name", "Học viên"))
            if st.button("Lưu"):
                from progress import save_progress
                progress["user_name"] = name
                save_progress(progress)
                st.session_state["show_settings"] = False
                st.rerun()


def main():
    sidebar()
    progress = load_progress()
    show_settings_modal(progress)

    xp = progress["total_xp"]
    level, level_name, cur_thresh, next_thresh = get_level(xp)
    streak = get_streak(progress)
    done_lessons = progress.get("completed_lessons", [])
    all_lessons = get_all_lessons()
    completion = get_completion_pct(progress)

    st.markdown("# 🚀 DevPath AI — Học Lập Trình Cùng AI")
    st.markdown("*Từ zero đến developer trong 18 tháng — mỗi ngày một bài, kiên trì là chiến thắng!*")
    st.markdown("---")

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"""<div class="metric-card">
<div class="metric-value">{xp:,}</div>
<div class="metric-label">⚡ Tổng XP</div></div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""<div class="metric-card">
<div class="metric-value">{level}</div>
<div class="metric-label">🏅 Cấp độ · {level_name}</div></div>""", unsafe_allow_html=True)
    with c3:
        st.markdown(f"""<div class="metric-card">
<div class="metric-value">{streak}</div>
<div class="metric-label">🔥 Ngày liên tiếp</div></div>""", unsafe_allow_html=True)
    with c4:
        st.markdown(f"""<div class="metric-card">
<div class="metric-value">{len(done_lessons)}/{len(all_lessons)}</div>
<div class="metric-label">📚 Bài đã học</div></div>""", unsafe_allow_html=True)

    st.markdown("")
    st.progress(completion / 100, text=f"Hoàn thành {completion:.1f}% lộ trình")

    st.markdown("---")

    next_lesson = None
    for module in MODULES:
        for lesson in module.get("lessons", []):
            if lesson["id"] not in done_lessons:
                next_lesson = (module, lesson)
                break
        if next_lesson:
            break

    col_next, col_road = st.columns([1, 1])

    with col_next:
        st.markdown("### ▶️ Tiếp tục học")
        if next_lesson:
            mod, les = next_lesson
            phase_info = PHASES.get(mod["phase"], {})
            st.markdown(f"""
<div class="phase-card" style="border-left: 3px solid {phase_info.get('color','#4F7CFF')}">
  <div style="font-size:0.75rem;color:#9CA3AF">Phase {mod['phase']} · {mod['icon']} {mod['title']}</div>
  <div style="font-size:1.05rem;font-weight:600;margin:6px 0">{les['title']}</div>
  <div style="font-size:0.8rem;color:#6B7280">⚡ {les['xp']} XP · ⏱ {les['minutes']} phút</div>
</div>""", unsafe_allow_html=True)
            if st.button("🎯 Bắt đầu bài này", use_container_width=True, type="primary"):
                st.session_state["open_lesson"] = les["id"]
                st.switch_page("pages/2_📚_Bài_Học.py")
        else:
            st.success("🎉 Anh đã hoàn thành tất cả bài học! Tuyệt vời!")

    with col_road:
        st.markdown("### 🗺️ Lộ trình học")
        for phase_id, phase_info in PHASES.items():
            phase_modules = [m for m in MODULES if m["phase"] == phase_id]
            phase_lessons = [l for m in phase_modules for l in m.get("lessons", [])]
            done_in_phase = sum(1 for l in phase_lessons if l["id"] in done_lessons)
            pct_phase = done_in_phase / len(phase_lessons) * 100 if phase_lessons else 0
            st.markdown(f"""
<div class="phase-card">
  <div style="display:flex;justify-content:space-between;align-items:center">
    <span>{phase_info['icon']} <b>Phase {phase_id}</b>: {phase_info['name']}</span>
    <span style="font-size:0.8rem;color:#9CA3AF">{done_in_phase}/{len(phase_lessons)}</span>
  </div>
  <div class="xp-bar-bg" style="margin-top:8px">
    <div class="xp-bar-fill" style="width:{pct_phase:.0f}%;background:{phase_info['color']}"></div>
  </div>
</div>""", unsafe_allow_html=True)

    st.markdown("---")

    weekly = get_weekly_xp(progress)
    if any(x > 0 for x in weekly):
        st.markdown("### 📈 XP tuần này")
        from datetime import date, timedelta
        today = date.today()
        days = [(today - timedelta(days=6 - i)).strftime("%a") for i in range(7)]
        import pandas as pd
        df = pd.DataFrame({"Ngày": days, "XP": weekly})
        st.bar_chart(df.set_index("Ngày"), color="#4F7CFF")

    st.markdown("---")
    st.markdown("### 💬 Hỏi AI Mentor ngay")
    quick_q = st.text_input("Anh đang thắc mắc gì?", placeholder="Ví dụ: for loop dùng khi nào? list và tuple khác nhau thế nào?")
    if st.button("🤖 Hỏi AI", type="primary") and quick_q:
        st.session_state["quick_question"] = quick_q
        st.switch_page("pages/1_🤖_AI_Mentor.py")


if __name__ == "__main__":
    main()
