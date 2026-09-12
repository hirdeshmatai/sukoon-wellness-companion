from __future__ import annotations

import random

TIPS = {
    "calm": [
        "Keep a 3-line journal tonight: one win, one thanks, one plan.",
        "Protect this calm. Ten minutes without your phone is enough.",
        "If energy is here, do one small task you have been postponing.",
    ],
    "stressed": [
        "Pick the one deadline that actually explodes tomorrow. Only that.",
        "Set a 25-minute timer. Close every other tab.",
        "Write the list, circle two items, hide the rest.",
    ],
    "anxious": [
        "Name five things you can see in the room. Slow your exhale.",
        "Unclench your jaw. Drop your shoulders. Breathe out longer than in.",
        "You do not have to solve the whole future tonight.",
    ],
    "lonely": [
        "Send one ordinary text to someone safe. Not a speech, just hello.",
        "Sit in a public campus spot for twenty minutes. Presence first.",
        "Join a mess table even if the talk is small. Small is still contact.",
    ],
    "overwhelmed": [
        "One next action only: drink water, then open one file.",
        "Put everything on paper. Choose a 10-minute slice.",
        "If the mountain is too big, shrink the first step until it is silly-small.",
    ],
}

OPENERS = {
    "calm": [
        "Good to hear some steady ground under you.",
        "A quiet day still counts. I am here with you.",
    ],
    "stressed": [
        "That load is real. We can shrink it, not pretend it is fine.",
        "Deadlines stack. Let us pick one thing that matters today.",
    ],
    "anxious": [
        "Anxiety is loud. We can slow the body first, then the plan.",
        "You do not have to be certain to take the next small step.",
    ],
    "lonely": [
        "Feeling left out on campus is more common than people admit.",
        "You reached out. That is already contact.",
    ],
    "overwhelmed": [
        "Too much at once shuts the brain down. We go tiny.",
        "You are not failing. You are full. Different problem.",
    ],
}


def template_reply(mood: str, user_text: str) -> str:
    mood = mood if mood in OPENERS else "stressed"
    opener = random.choice(OPENERS[mood])
    tip = random.choice(TIPS[mood])
    return (
        f"{opener}\n\n"
        f"I am Sukoon, a student wellness companion — not a therapist "
        f"and not a diagnosis.\n\n"
        f"Try this: {tip}\n\n"
        f"If this gets heavier than campus stress, talk to a counsellor "
        f"or KIRAN 1800-599-0019."
    )


def breathing_script() -> str:
    return (
        "Box breathing, one round:\n"
        "1. Inhale 4 seconds\n"
        "2. Hold 4 seconds\n"
        "3. Exhale 4 seconds\n"
        "4. Hold 4 seconds\n"
        "Repeat four times. Eyes on one spot in the room."
    )
