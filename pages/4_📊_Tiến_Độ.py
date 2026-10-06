import streamlit as st
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from curriculum import MODULES, PHASES, get_all_lessons, get_total_xp
from progress import load_progress, get_level, get_streak, get_weekly_xp, get_completion_pct, save_progress

st.set_page_config(page_title="Tiến Độ — DevPath AI", page_icon="📊", layout="wide")

st.markdown("""
<style>
.stat-card {
    background: linear-gradient(135deg, #0F172A, #1E1B4B);
    border: 1px solid #312E81;
    border-radius: 12px;
    padding: 20px;
    text-align: center;
    margin: 4px;
}
.stat-num { font-size: 2.4rem; font-weight: 900; color: #818CF8; }
.stat-lbl { font-size: 0.8rem; color: #9CA3AF; margin-top: 4px; }
.achievement-card {
    background: #111827;
    border: 1px solid #1F2937;
    border-radius: 10px;
    padding: 12px 14px;
    margin: 6px 0;
    display: flex;
    align-items: center;
    gap: 12px;
}
.achievement-locked { opacity: 0.4; filter: grayscale(100%); }
.progress-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 8px 0;
    border-bottom: 1px solid #1F2937;
}
</style>
""", unsafe_allow_html=True)

ACHIEVEMENTS = [
    {"id": "first_lesson", "icon": "🌱", "name": "Khởi đầu", "desc": "Hoàn thành bài học đầu tiên",
     "check": lambda p: len(p.get("completed_lessons", [])) >= 1},
    {"id": "streak_3", "icon": "🔥", "name": "Tam Liên", "desc": "Học 3 ngày liên tiếp",
     "check": lambda p: p.get("streak_days", 0) >= 3},
    {"id": "streak_7", "icon": "🌟", "name": "Thói quen tốt", "desc": "Học 7 ngày liên tiếp",
     "check": lambda p: p.get("streak_days", 0) >= 7},
    {"id": "xp_100", "icon": "⚡", "name": "Tích điện", "desc": "Đạt 100 XP",
     "check": lambda p: p.get("total_xp", 0) >= 100},
    {"id": "xp_500", "icon": "💥", "name": "Power User", "desc": "Đạt 500 XP",
     "check": lambda p: p.get("total_xp", 0) >= 500},
    {"id": "lessons_5", "icon": "📚", "name": "Bookworm", "desc": "Hoàn thành 5 bài học",
     "check": lambda p: len(p.get("completed_lessons", [])) >= 5},
    {"id": "quiz_perfect", "icon": "🎯", "name": "Quiz Master", "desc": "Đạt 100% một quiz",
     "check": lambda p: any(v == 100 for v in p.get("quiz_scores", {}).values())},
    {"id": "phase1_done", "icon": "🏆", "name": "Phase 1 Champion", "desc": "Hoàn thành Phase 1",
     "check": lambda p: all(
         l["id"] in p.get("completed_lessons", [])
         for m in MODULES if m["phase"] == 1
         for l in m.get("lessons", [])
     )},
]


def main():
    progress = load_progress()
    xp = progress["total_xp"]
    level, level_name, cur_thresh, next_thresh = get_level(xp)
    streak = get_streak(progress)
    done_lessons = set(progress.get("completed_lessons", []))
    all_lessons = get_all_lessons()
    completion = get_completion_pct(progress)
    total_possible_xp = get_total_xp()
    weekly = get_weekly_xp(progress)

    st.markdown("# 📊 Tiến Độ Học Tập")
    st.markdown("---")

    c1, c2, c3, c4, c5 = st.columns(5)
    stats = [
        (f"{xp:,}", "⚡ Tổng XP"),
        (f"Lv.{level}", f"🏅 {level_name}"),
        (f"{streak}", "🔥 Streak (ngày)"),
        (f"{len(done_lessons)}", f"📚 Bài xong/{len(all_lessons)}"),
        (f"{completion:.0f}%", "🎯 Hoàn thành"),
    ]
    for col, (num, lbl) in zip([c1, c2, c3, c4, c5], stats):
        with col:
            st.markdown(f"""<div class="stat-card">
<div class="stat-num">{num}</div>
<div class="stat-lbl">{lbl}</div></div>""", unsafe_allow_html=True)

    st.markdown("")

    xp_in_level = xp - cur_thresh
    xp_to_next = next_thresh - cur_thresh
    pct_level = min(xp_in_level / max(xp_to_next, 1) * 100, 100)
    st.markdown(f"**Tiến đến Lv.{level+1}:** {xp_in_level:,} / {xp_to_next:,} XP")
    st.progress(pct_level / 100)
    st.markdown("---")

    col_chart, col_phase = st.columns([2, 1])

    with col_chart:
        if any(x > 0 for x in weekly):
            st.markdown("### 📈 XP 7 ngày qua")
            import pandas as pd
            from datetime import date, timedelta
            today = date.today()
            days = [(today - timedelta(days=6 - i)).strftime("%d/%m") for i in range(7)]
            df = pd.DataFrame({"Ngày": days, "XP": weekly})
            st.bar_chart(df.set_index("Ngày"), color="#4F7CFF", height=280)
        else:
            st.markdown("### 📈 XP 7 ngày qua")
            st.info("Chưa có dữ liệu học tập. Bắt đầu học bài đầu tiên nhé anh!")

        st.markdown("### 📋 Chi tiết bài học")
        for mod in MODULES:
            phase_info = PHASES.get(mod["phase"], {})
            mod_lessons = mod.get("lessons", [])
            done_in_mod = sum(1 for l in mod_lessons if l["id"] in done_lessons)
            pct_mod = done_in_mod / len(mod_lessons) * 100 if mod_lessons else 0

            with st.expander(f"{mod['icon']} {mod['title']} — {done_in_mod}/{len(mod_lessons)} bài"):
                for les in mod_lessons:
                    is_done = les["id"] in done_lessons
                    score = progress.get("quiz_scores", {}).get(les["id"])
                    icon = "✅" if is_done else "⭕"
                    score_str = f" · Quiz: {score}%" if score is not None else ""
                    st.markdown(f"""<div class="progress-row">
<span>{icon} {les['title']}</span>
<span style="color:#9CA3AF;font-size:0.8rem">⚡{les['xp']}XP{score_str}</span>
</div>""", unsafe_allow_html=True)

    with col_phase:
        st.markdown("### 🗺️ Lộ trình Phase")
        for phase_id, phase_info in PHASES.items():
            phase_modules = [m for m in MODULES if m["phase"] == phase_id]
            phase_lessons = [l for m in phase_modules for l in m.get("lessons", [])]
            done_in_phase = sum(1 for l in phase_lessons if l["id"] in done_lessons)
            pct_phase = done_in_phase / len(phase_lessons) * 100 if phase_lessons else 0

            st.markdown(f"**{phase_info['icon']} Phase {phase_id}: {phase_info['name']}**")
            st.progress(pct_phase / 100, text=f"{done_in_phase}/{len(phase_lessons)} bài")
            st.markdown("")

    st.markdown("---")
    st.markdown("### 🏆 Thành tích")

    unlocked = []
    locked = []
    for ach in ACHIEVEMENTS:
        if ach["check"](progress):
            unlocked.append(ach)
        else:
            locked.append(ach)

    st.markdown(f"**{len(unlocked)}/{len(ACHIEVEMENTS)} thành tích đã mở khóa**")

    cols = st.columns(4)
    all_ach = unlocked + locked
    for i, ach in enumerate(all_ach):
        is_unlocked = ach in unlocked
        with cols[i % 4]:
            opacity = "1.0" if is_unlocked else "0.35"
            bg = "#064E3B" if is_unlocked else "#111827"
            border = "#10B981" if is_unlocked else "#1F2937"
            st.markdown(f"""
<div style="background:{bg};border:1px solid {border};border-radius:10px;
padding:12px;text-align:center;margin:4px 0;opacity:{opacity}">
  <div style="font-size:2rem">{ach['icon']}</div>
  <div style="font-weight:700;font-size:0.85rem;margin:4px 0">{ach['name']}</div>
  <div style="font-size:0.75rem;color:#9CA3AF">{ach['desc']}</div>
</div>""", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### ⚙️ Hồ sơ học viên")
    col_profile, col_reset = st.columns([3, 1])
    with col_profile:
        name = st.text_input("Tên hiển thị", value=progress.get("user_name", "Học viên"))
        if st.button("💾 Lưu tên", use_container_width=True):
            progress["user_name"] = name
            save_progress(progress)
            st.success("✅ Đã lưu!")

        started = progress.get("started_at", "")
        if started:
            from datetime import datetime
            try:
                dt = datetime.fromisoformat(started)
                days_since = (datetime.now() - dt).days
                st.markdown(f"📅 Bắt đầu học: **{dt.strftime('%d/%m/%Y')}** ({days_since} ngày trước)")
            except Exception:
                pass

    with col_reset:
        st.markdown("")
        st.markdown("")
        if st.button("⚠️ Reset tiến độ", use_container_width=True):
            if st.session_state.get("confirm_reset"):
                from progress import DEFAULT_PROGRESS, PROGRESS_FILE, _ensure_dir
                import json
                _ensure_dir()
                p = DEFAULT_PROGRESS.copy()
                from datetime import datetime
                p["started_at"] = datetime.now().isoformat()
                p["user_name"] = name
                with open(PROGRESS_FILE, "w", encoding="utf-8") as f:
                    json.dump(p, f, ensure_ascii=False, indent=2)
                st.session_state.pop("confirm_reset", None)
                st.success("✅ Đã reset!")
                st.rerun()
            else:
                st.session_state["confirm_reset"] = True
                st.warning("Nhấn lại để xác nhận reset toàn bộ tiến độ!")


if __name__ == "__main__":
    main()
