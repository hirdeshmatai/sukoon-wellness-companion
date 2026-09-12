from __future__ import annotations

from pathlib import Path

import joblib

ROOT = Path(__file__).resolve().parent
MODEL_PATH = ROOT / "models" / "mood_pipeline.joblib"
VECTORIZER_PATH = ROOT / "models" / "tfidf.joblib"
META_PATH = ROOT / "models" / "metrics.json"

LABELS = ["calm", "stressed", "anxious", "lonely", "overwhelmed", "crisis"]

_pipe = None


def load_pipeline():
    global _pipe
    if _pipe is None:
        if not MODEL_PATH.exists():
            from train import train

            train()
        _pipe = joblib.load(MODEL_PATH)
    return _pipe


def predict_mood(text: str) -> tuple[str, float, dict[str, float]]:
    pipe = load_pipeline()
    proba = pipe.predict_proba([text])[0]
    classes = list(pipe.classes_)
    scores = {cls: float(p) for cls, p in zip(classes, proba)}
    label = max(scores, key=scores.get)
    return label, scores[label], scores
