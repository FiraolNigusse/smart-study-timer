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

import matplotlib.pyplot as plt

def show_daily_chart():
    sessions = load_sessions()
    today = datetime.now().date()
    total_study = 0
    total_break = 0

    for session in sessions:
        session_date = datetime.strptime(session["start"], "%Y-%m-%d %H:%M:%S").date()
        if session_date == today:
            if session.get("type") == "study":
                total_study += session.get("duration_min", 0)
            elif session.get("type") == "break":
                total_break += session.get("duration_min", 0)

    # Plotting the bar chart
    labels = ['Study', 'Break']
    values = [total_study, total_break]
    colors = ['#4CAF50', '#2196F3']

    plt.figure(figsize=(5, 4))
    plt.bar(labels, values, color=colors)
    plt.title("Today's Time Summary")
    plt.ylabel("Minutes")
    plt.ylim(0, max(60, max(values) + 10))  # Adjust chart height dynamically
    plt.tight_layout()
    plt.show()

def show_weekly_chart():
    if not os.path.exists(LOG_FILE):
        print("No log file found.")
        return

    with open(LOG_FILE, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            data = []

    today = datetime.now().date()
    past_week = [today - timedelta(days=i) for i in range(6, -1, -1)]
    totals = {day: 0 for day in past_week}

    for session in data:
        try:
            session_date = datetime.strptime(session["start"], "%Y-%m-%d %H:%M:%S").date()
            if session_date in totals:
                totals[session_date] += float(session.get("duration_min", 0))
        except:
            continue

    days = [day.strftime("%a") for day in past_week]
    minutes = [totals[day] for day in past_week]

    plt.figure(figsize=(8, 5))
    plt.bar(days, minutes, color="#4CAF50")
    plt.title("Study Time Over Last 7 Days")
    plt.xlabel("Day")
    plt.ylabel("Total Minutes")
    plt.tight_layout()
    plt.show()
