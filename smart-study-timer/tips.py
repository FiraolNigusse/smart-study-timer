import random

TIPS = [
    "Break work into Pomodoros to stay focused.",
    "Avoid multitasking during study sessions.",
    "Use active recall, not passive reading.",
    "Reward yourself after deep work.",
    "Keep your phone out of reach.",
    "Review your goals daily.",
    "Use study playlists without lyrics.",
]

def get_random_tip():
    return random.choice(TIPS)
