import os

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def play_sound():
    try:
        from playsound import playsound
        playsound("assets/ding.mp3")
    except:
        print("🔔 (Sound would play here if available.)")


def show_banner():
    try:
        with open("assets/ascii_banner.txt", "r") as f:
            print(f.read())
    except:
        print("=== Smart Study Timer ===")
