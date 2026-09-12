from __future__ import annotations

import os
import urllib.request
import json

SYSTEM = (
    "You are Sukoon, a student wellness companion for Indian college students. "
    "You are not a therapist, doctor, or crisis counsellor. Never diagnose. "
    "Never suggest medication. Never give instructions that could cause harm. "
    "If the student is in crisis, tell them to contact KIRAN 1800-599-0019, "
    "Tele MANAS 14416, iCall 9152987821, or 112, and stop trying to treat them. "
    "Replies: 70-130 words, warm, direct, practical. One tiny action. "
    "Hindi words are fine if the student used Hindi. "
    "Mood label from a classifier: {mood}."
)


def _post_json(url: str, headers: dict, payload: dict) -> dict:
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers=headers,
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=40) as resp:
        return json.loads(resp.read().decode("utf-8"))


def generate_llm_reply(
    mood: str,
    user_text: str,
    history: list[dict[str, str]],
    openrouter_key: str | None,
    google_key: str | None,
) -> str | None:
    sys = SYSTEM.format(mood=mood)
    if openrouter_key:
        try:
            messages = [{"role": "system", "content": sys}]
            for turn in history[-6:]:
                messages.append(turn)
            messages.append({"role": "user", "content": user_text})
            data = _post_json(
                "https://openrouter.ai/api/v1/chat/completions",
                {
                    "Authorization": f"Bearer {openrouter_key}",
                    "Content-Type": "application/json",
                    "HTTP-Referer": "https://sukoon-campus.local",
                    "X-Title": "Sukoon",
                },
                {
                    "model": "openai/gpt-4o-mini",
                    "messages": messages,
                    "max_tokens": 220,
                    "temperature": 0.6,
                },
            )
            return data["choices"][0]["message"]["content"].strip()
        except Exception:
            pass

    if google_key:
        try:
            prompt = sys + "\n\nStudent: " + user_text
            url = (
                "https://generativelanguage.googleapis.com/v1beta/models/"
                f"gemini-2.0-flash:generateContent?key={google_key}"
            )
            data = _post_json(
                url,
                {"Content-Type": "application/json"},
                {
                    "contents": [{"parts": [{"text": prompt}]}],
                    "generationConfig": {"maxOutputTokens": 220, "temperature": 0.6},
                },
            )
            return data["candidates"][0]["content"]["parts"][0]["text"].strip()
        except Exception:
            pass
    return None
