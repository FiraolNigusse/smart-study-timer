import time
import json
from datetime import datetime

LOG_FILE = "logs/study_log.json"
WORK_DURATION = 25 * 60  # 25 minutes
BREAK_DURATION = 5 * 60  # 5 minutes

def countdown(seconds):
    while seconds:
        mins, secs = divmod(seconds, 60)
        timer = f"{mins:02d}:{secs:02d}"
        print(f"\r⏳ {timer}", end="")
        time.sleep(1)
        seconds -= 1
    print("\r⏰ 00:00 - Time's up!")

countdown(10)  # just 10 seconds to test
def log_session(start_time, duration_minutes):
    session = {
        "start": start_time.strftime("%Y-%m-%d %H:%M:%S"),
        "duration_min": duration_minutes
    }

    try:
        with open(LOG_FILE, "r") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        data = []

    data.append(session)

    with open(LOG_FILE, "w") as f:
        json.dump(data, f, indent=2)

    print("📚 Session logged successfully.")

def start_study_session():
    print("🎯 Study session starting now!")
    start_time = datetime.now()
    countdown(WORK_DURATION)
    log_session(start_time, WORK_DURATION // 60)

def main():
    while True:
        print("\n--- Smart Study Timer ---")
        print("1. Start 25-min Study Session")
        print("2. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            start_study_session()
        elif choice == "2":
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid option, try again.")

if __name__ == "__main__":
    main()
