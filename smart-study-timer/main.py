import time
import json
from datetime import datetime
from utils import clear_screen, play_sound, show_banner

LOG_FILE = "logs/study_log.json"
WORK_DURATION = 25 * 60   # 25 min
BREAK_DURATION = 5 * 60   # 5 min
TEST_MODE = False         # Default to OFF


def countdown(seconds, label="⏳"):
    while seconds:
        mins, secs = divmod(seconds, 60)
        timer = f"{mins:02d}:{secs:02d}"
        print(f"\r{label} {timer}", end="")
        time.sleep(1)
        seconds -= 1
    print(f"\r⏰ 00:00 - {label.strip()} Complete!")


def log_session(start_time, duration_minutes, session_type="study"):
    session = {
        "start": start_time.strftime("%Y-%m-%d %H:%M:%S"),
        "duration_min": duration_minutes,
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

    print("📚 Session logged.")


def start_study_session(duration):
    clear_screen()
    show_banner()
    print("🎯 Starting Study Session...")
    start_time = datetime.now()
    countdown(duration, "📖 Studying")
    play_sound()
    log_session(start_time, duration // 60, "study")
    print("✅ Study complete!")


def start_break(duration):
    print("\n🧘 Break Time!")
    countdown(duration, "☕ Break")
    play_sound()
    log_session(datetime.now(), duration // 60, "break")
    print("🔁 Break over. Ready for another session?")


def main():
    global TEST_MODE
    while True:
        clear_screen()
        show_banner()
        print("1. Start Study Session")
        print("2. Toggle Test Mode (currently: {})".format("ON" if TEST_MODE else "OFF"))
        print("3. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            duration = 10 if TEST_MODE else WORK_DURATION
            break_duration = 5 if TEST_MODE else BREAK_DURATION
            start_study_session(duration)
            start_break(break_duration)
            input("\n🔁 Press Enter to return to menu...")
        elif choice == "2":
            TEST_MODE = not TEST_MODE
        elif choice == "3":
            print("👋 Goodbye! Stay productive!")
            break
        else:
            print("❌ Invalid choice.")
            time.sleep(1)

if __name__ == "__main__":
    main()

