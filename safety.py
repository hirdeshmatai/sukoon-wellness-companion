from __future__ import annotations

import re

# Operational crisis gate only. Never used as user-facing copy.
_CRISIS = re.compile(
    r"("
    r"\b(kill myself|killing myself|want to die|wanna die|end my life|"
    r"ending my life|suicide|suicidal|self harm|self-harm|hurt myself|"
    r"hurting myself|don't want to live|dont want to live|"
    r"do not want to live|no reason to live|better off dead|"
    r"end it all|ending it all)\b|"
    r"\b(i can't go on|i cannot go on|i cant go on|"
    r"i don't want to be here|i dont want to be here|"
    r"i want to disappear forever|i need emergency help|"
    r"i am in a crisis|i'm in a crisis|im in a crisis|"
    r"please send help now)\b"
    r")",
    re.IGNORECASE,
)

HELPLINES = [
    {
        "name": "KIRAN (Govt. of India)",
        "phone": "1800-599-0019",
        "note": "24x7 mental health helpline",
    },
    {
        "name": "Tele MANAS",
        "phone": "14416",
        "note": "National tele mental health",
    },
    {
        "name": "iCall (TISS)",
        "phone": "9152987821",
        "note": "Mon–Sat, counselling",
    },
    {
        "name": "Vandrevala Foundation",
        "phone": "9999666555",
        "note": "24x7",
    },
    {
        "name": "Emergency",
        "phone": "112",
        "note": "If you are in immediate danger",
    },
]


def is_crisis_text(text: str) -> bool:
    return bool(_CRISIS.search(text or ""))


def crisis_message() -> str:
    lines = [
        "I am glad you reached out. I am a campus wellness bot, not a counsellor.",
        "If you feel unsafe or in crisis, please talk to a real person now.",
        "",
        "KIRAN: 1800-599-0019",
        "Tele MANAS: 14416",
        "iCall: 9152987821",
        "Vandrevala: 9999666555",
        "Emergency: 112",
        "",
        "If you can, tell a trusted friend, family member, or your campus counsellor.",
        "You do not have to handle this alone.",
    ]
    return "\n".join(lines)
