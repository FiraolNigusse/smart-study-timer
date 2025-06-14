import json
from datetime import datetime, timedelta
from collections import defaultdict

LOG_FILE = "logs/study_log.json"

def load_sessions():
    try:
        with open(LOG_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def summarize_sessions():
    sessions = load_sessions()
    today = datetime.now().date()
    this_week = today - timedelta(days=6)

    daily_total = defaultdict(int)
    weekly_total = defaultdict(int)

    for session in sessions:
        session_date = datetime.strptime(session["start"], "%Y-%m-%d %H:%M:%S").date()
        minutes = session["duration_min"]
        session_type = session.get("type", "study")

        if session_date == today:
            daily_total[session_type] += minutes
        if session_date >= this_week:
            weekly_total[session_type] += minutes

    return daily_total, weekly_total

def display_stats():
    daily, weekly = summarize_sessions()

    print("\n📅 DAILY SUMMARY (Today):")
    print(f"  📖 Study: {daily.get('study', 0)} min")
    print(f"  ☕ Break: {daily.get('break', 0)} min")

    print("\n📈 WEEKLY SUMMARY (Last 7 days):")
    print(f"  📖 Study: {weekly.get('study', 0)} min")
    print(f"  ☕ Break: {weekly.get('break', 0)} min")
    print("\nKeep going! 🎯")
