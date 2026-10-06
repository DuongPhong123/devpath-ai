import json
import os
from datetime import datetime, date

PROGRESS_FILE = os.path.join(os.path.dirname(__file__), "data", "progress.json")

DEFAULT_PROGRESS = {
    "user_name": "Học viên",
    "started_at": None,
    "total_xp": 0,
    "level": 1,
    "streak_days": 0,
    "last_study_date": None,
    "completed_lessons": [],
    "completed_modules": [],
    "quiz_scores": {},
    "lesson_notes": {},
    "daily_xp": {},
}

LEVEL_THRESHOLDS = [0, 100, 250, 500, 900, 1400, 2100, 3000, 4200, 5800, 8000]
LEVEL_NAMES = ["Tân binh", "Học viên", "Lập trình viên", "Developer Jr", "Developer",
               "Developer Sr", "Tech Lead", "Architect", "Expert", "Master", "Legend"]


def _ensure_dir():
    os.makedirs(os.path.dirname(PROGRESS_FILE), exist_ok=True)


def load_progress() -> dict:
    _ensure_dir()
    if not os.path.exists(PROGRESS_FILE):
        p = DEFAULT_PROGRESS.copy()
        p["started_at"] = datetime.now().isoformat()
        return p
    try:
        with open(PROGRESS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        for k, v in DEFAULT_PROGRESS.items():
            data.setdefault(k, v)
        return data
    except Exception:
        p = DEFAULT_PROGRESS.copy()
        p["started_at"] = datetime.now().isoformat()
        return p


def save_progress(progress: dict):
    _ensure_dir()
    with open(PROGRESS_FILE, "w", encoding="utf-8") as f:
        json.dump(progress, f, ensure_ascii=False, indent=2)


def get_level(xp: int) -> tuple[int, str, int, int]:
    level = 1
    for i, threshold in enumerate(LEVEL_THRESHOLDS):
        if xp >= threshold:
            level = i + 1
    level = min(level, len(LEVEL_NAMES))
    name = LEVEL_NAMES[level - 1]
    current_threshold = LEVEL_THRESHOLDS[level - 1]
    next_threshold = LEVEL_THRESHOLDS[level] if level < len(LEVEL_THRESHOLDS) else LEVEL_THRESHOLDS[-1] + 9999
    return level, name, current_threshold, next_threshold


def complete_lesson(lesson_id: str, xp_earned: int, quiz_score: int = None) -> dict:
    progress = load_progress()
    today = date.today().isoformat()

    if lesson_id not in progress["completed_lessons"]:
        progress["completed_lessons"].append(lesson_id)
        progress["total_xp"] += xp_earned
        daily = progress.setdefault("daily_xp", {})
        daily[today] = daily.get(today, 0) + xp_earned

    if quiz_score is not None:
        progress["quiz_scores"][lesson_id] = quiz_score

    last = progress.get("last_study_date")
    if last:
        last_date = date.fromisoformat(last)
        delta = (date.today() - last_date).days
        if delta == 1:
            progress["streak_days"] = progress.get("streak_days", 0) + 1
        elif delta > 1:
            progress["streak_days"] = 1
    else:
        progress["streak_days"] = 1

    progress["last_study_date"] = today
    level, _, _, _ = get_level(progress["total_xp"])
    progress["level"] = level

    save_progress(progress)
    return progress


def save_note(lesson_id: str, note: str):
    progress = load_progress()
    progress.setdefault("lesson_notes", {})[lesson_id] = note
    save_progress(progress)


def get_streak(progress: dict) -> int:
    if not progress.get("last_study_date"):
        return 0
    last = date.fromisoformat(progress["last_study_date"])
    delta = (date.today() - last).days
    if delta <= 1:
        return progress.get("streak_days", 0)
    return 0


def get_weekly_xp(progress: dict) -> list[int]:
    daily = progress.get("daily_xp", {})
    today = date.today()
    result = []
    for i in range(6, -1, -1):
        d = (today.replace(day=today.day - i) if today.day > i else today).isoformat()
        from datetime import timedelta
        d = (today - timedelta(days=i)).isoformat()
        result.append(daily.get(d, 0))
    return result


def get_completion_pct(progress: dict) -> float:
    from curriculum import get_all_lessons
    total = len(get_all_lessons())
    if total == 0:
        return 0.0
    return len(progress.get("completed_lessons", [])) / total * 100
