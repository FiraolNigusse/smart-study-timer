import tkinter as tk
from tkinter import messagebox
import time
import threading
from datetime import datetime
import json
from playsound import playsound

# Global settings
TEST_MODE = False
WORK_DURATION = 25 * 60
BREAK_DURATION = 5 * 60
LOG_FILE = "logs/study_log.json"
DING_PATH = "assets/ding.mp3"

# Timer state
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

    duration = 10 if TEST_MODE else WORK_DURATION
    if session_type == "break":
        duration = 5 if TEST_MODE else BREAK_DURATION

    threading.Thread(target=countdown, args=(duration, label, session_type), daemon=True).start()

def stop_timer(label):
    global is_running
    is_running = False
    label.config(text="00:00")

def toggle_test_mode(mode_label):
    global TEST_MODE
    TEST_MODE = not TEST_MODE
    mode_label.config(text=f"Test Mode: {'ON' if TEST_MODE else 'OFF'}")

def launch_gui():
    root = tk.Tk()
    root.title("Smart Study Timer")
    root.geometry("400x400")
    root.configure(bg="#f4f4f4")

    # Fonts and colors
    font_title = ("Segoe UI", 20, "bold")
    font_timer = ("Consolas", 48)
    font_btn = ("Segoe UI", 12)

    def style_button(btn):
        btn.configure(
            bg="#4CAF50", fg="white",
            activebackground="#45a049",
            font=font_btn,
            relief="flat",
            bd=0,
            padx=10,
            pady=5,
            cursor="hand2"
        )

    # Layout Frame
    frame = tk.Frame(root, bg="#f4f4f4")
    frame.place(relx=0.5, rely=0.5, anchor="center")

    # Title
    title = tk.Label(frame, text="Smart Study Timer", font=font_title, bg="#f4f4f4", fg="#333")
    title.pack(pady=(0, 20))

    # Time Display
    time_label = tk.Label(frame, text="00:00", font=font_timer, bg="#f4f4f4", fg="#222")
    time_label.pack(pady=10)

    # Buttons
    btn_study = tk.Button(frame, text="Start Study", command=lambda: start_session("study", time_label))
    style_button(btn_study)
    btn_study.pack(pady=5)

    btn_break = tk.Button(frame, text="Start Break", command=lambda: start_session("break", time_label))
    style_button(btn_break)
    btn_break.pack(pady=5)

    btn_stop = tk.Button(frame, text="Stop", command=lambda: stop_timer(time_label))
    style_button(btn_stop)
    btn_stop.pack(pady=5)

    # Test mode toggle
    mode_label = tk.Label(frame, text="Test Mode: OFF", font=("Segoe UI", 10), bg="#f4f4f4", fg="#444")
    mode_label.pack(pady=(15, 5))

    btn_toggle = tk.Button(frame, text="Toggle Test Mode", command=lambda: toggle_test_mode(mode_label))
    style_button(btn_toggle)
    btn_toggle.configure(bg="#2196F3", activebackground="#1e88e5")
    btn_toggle.pack()

    root.mainloop()


if __name__ == "__main__":
    launch_gui()
