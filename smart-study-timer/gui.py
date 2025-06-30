import tkinter as tk
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from datetime import timedelta
import time
import threading
from datetime import datetime
import json
from playsound import playsound
from stats import show_daily_chart
from export import export_to_csv
from tips import get_random_tip
from stats import get_emoji_summary

# Theme configurations
LIGHT_THEME = {
    "bg": "#f4f4f4",
    "fg": "#222222",
    "btn_bg": "#4CAF50",
    "btn_fg": "white",
    "title": "#333",
}
DARK_THEME = {
    "bg": "#1e1e1e",
    "fg": "#ffffff",
    "btn_bg": "#3c3c3c",
    "btn_fg": "#ffffff",
    "title": "#ffffff",
}
current_theme = LIGHT_THEME  # default

# Global settings
TEST_MODE = False
WORK_DURATION = 25 * 60
BREAK_DURATION = 5 * 60
LOG_FILE = "logs/study_log.json"
DING_PATH = "assets/ding.mp3"

current_timer = None
is_running = False

def log_session(duration_min, session_type="study"):
    session = {
        "start": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "duration_min": duration_min,
        "type": session_type
    }
    try:
        with open(LOG_FILE, "r") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        data = []
    data.append(session)
    with open(LOG_FILE, "w") as f:
        json.dump(data, f, indent=2)

def play_sound():
    try:
        playsound(DING_PATH)
    except:
        print("🔇 Could not play sound.")

def countdown(duration, label, session_type):
    global is_running
    start = time.time()
    while is_running and duration > 0:
        mins, secs = divmod(duration, 60)
        label.config(text=f"{mins:02d}:{secs:02d}")
        time.sleep(1)
        duration -= 1
    if is_running:
        label.config(text="Done!")
        play_sound()
        log_session((time.time() - start) // 60, session_type)
        messagebox.showinfo("Session Complete", f"{session_type.capitalize()} session finished!")

def start_session(session_type, label):
    global is_running
    if is_running:
        return
    is_running = True
    duration = 10 if TEST_MODE else (BREAK_DURATION if session_type == "break" else WORK_DURATION)
    threading.Thread(target=countdown, args=(duration, label, session_type), daemon=True).start()

def stop_timer(label):
    global is_running
    is_running = False
    label.config(text="00:00")

def toggle_test_mode(mode_label):
    global TEST_MODE
    TEST_MODE = not TEST_MODE
    mode_label.config(text=f"Test Mode: {'ON' if TEST_MODE else 'OFF'}")

def toggle_theme(widgets):
    global current_theme
    current_theme = DARK_THEME if current_theme == LIGHT_THEME else LIGHT_THEME
    apply_theme(widgets)

def apply_theme(widgets):
    for w in widgets:
        if isinstance(w, tk.Button):
            w.configure(bg=current_theme["btn_bg"], fg=current_theme["btn_fg"], activebackground=current_theme["btn_bg"])
        elif isinstance(w, tk.Label):
            w.configure(bg=current_theme["bg"], fg=current_theme["fg"])
        elif isinstance(w, tk.Frame):
            w.configure(bg=current_theme["bg"])

def show_weekly_chart_window():
    chart_win = tk.Toplevel()
    chart_win.title("Weekly Study Time Chart")
    chart_win.geometry("500x350")
    chart_win.configure(bg=current_theme["bg"])

    try:
        with open(LOG_FILE, "r") as f:
            sessions = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        sessions = []

    today = datetime.now().date()
    past_week = [today - timedelta(days=i) for i in range(6, -1, -1)]
    totals = {day: 0 for day in past_week}

    for session in sessions:
        try:
            session_date = datetime.strptime(session["start"], "%Y-%m-%d %H:%M:%S").date()
            if session_date in totals:
                totals[session_date] += float(session.get("duration_min", 0))
        except:
            continue

    days = [day.strftime("%a") for day in past_week]
    minutes = [totals[day] for day in past_week]

    fig, ax = plt.subplots(figsize=(6, 3))
    ax.bar(days, minutes, color="#2196F3")
    ax.set_title("Study Time Over Last 7 Days")
    ax.set_ylabel("Minutes")

    canvas = FigureCanvasTkAgg(fig, master=chart_win)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

def launch_gui():
    global current_theme
    root = tk.Tk()
    root.title("Smart Study Timer")
    root.geometry("400x520")
    root.configure(bg=current_theme["bg"])

    font_title = ("Segoe UI", 20, "bold")
    font_timer = ("Consolas", 48)
    font_btn = ("Segoe UI", 12)

    widgets = []  # Track all UI elements for theme switching

    frame = tk.Frame(root, bg=current_theme["bg"])
    frame.place(relx=0.5, rely=0.5, anchor="center")
    widgets.append(frame)

    title = tk.Label(frame, text="Smart Study Timer", font=font_title, bg=current_theme["bg"], fg=current_theme["title"])
    title.pack(pady=(0, 20))
    widgets.append(title)

    time_label = tk.Label(frame, text="00:00", font=font_timer, bg=current_theme["bg"], fg=current_theme["fg"])
    time_label.pack(pady=10)
    widgets.append(time_label)

    def styled_button(text, command):
        btn = tk.Button(frame, text=text, command=command)
        btn.configure(font=font_btn, relief="flat", bd=0, padx=10, pady=5, cursor="hand2")
        widgets.append(btn)
        return btn

    btn_study = styled_button("Start Study", lambda: start_session("study", time_label))
    btn_study.pack(pady=5)

    btn_break = styled_button("Start Break", lambda: start_session("break", time_label))
    btn_break.pack(pady=5)

    btn_stop = styled_button("Stop", lambda: stop_timer(time_label))
    btn_stop.pack(pady=5)

    mode_label = tk.Label(frame, text="Test Mode: OFF", font=("Segoe UI", 10), bg=current_theme["bg"], fg=current_theme["fg"])
    mode_label.pack(pady=(15, 5))
    widgets.append(mode_label)

    btn_toggle = styled_button("Toggle Test Mode", lambda: toggle_test_mode(mode_label))
    btn_toggle.pack()

    btn_chart = styled_button("Show Weekly Chart", show_weekly_chart_window)
    btn_chart.pack(pady=(20, 0))

    btn_stats = styled_button("📊 View Today’s Stats", show_daily_chart)
    btn_stats.pack(pady=(10, 0))

    btn_export = styled_button("📤 Export to CSV", export_to_csv)
    btn_export.configure(bg="#FF9800", activebackground="#FB8C00")
    btn_export.pack(pady=(10, 0))

    btn_theme = styled_button("🌙 Toggle Light/Dark Mode", lambda: toggle_theme(widgets))
    btn_theme.pack(pady=(10, 10))

    apply_theme(widgets)  # Apply initial theme
    tip_label = tk.Label(frame, text=f"💡 Tip: {get_random_tip()}", font=("Segoe UI", 10),
                         wraplength=350, bg=current_theme["bg"], fg=current_theme["fg"])
    tip_label.pack(pady=(10, 0))
    widgets.append(tip_label)
    summary_label = tk.Label(
        frame,
        text=get_emoji_summary(),
        font=("Segoe UI", 10),
        bg=current_theme["bg"],
        fg=current_theme["fg"]
    )
    summary_label.pack(pady=(5, 0))

    root.mainloop()

if __name__ == "__main__":
    launch_gui()
