"""Train TF-IDF + Linear SVM mood classifier for Sukoon."""

from __future__ import annotations

import json
from pathlib import Path

import joblib
from sklearn.calibration import CalibratedClassifierCV
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.svm import LinearSVC

from dataset import build_dataframe
from mood_engine import LABELS, META_PATH, MODEL_PATH

ROOT = Path(__file__).resolve().parent


def train() -> dict:
    df = build_dataframe()
    ROOT.joinpath("data").mkdir(exist_ok=True)
    df.to_csv(ROOT / "data" / "student_moods.csv", index=False)

    x_train, x_test, y_train, y_test = train_test_split(
        df["text"],
        df["label"],
        test_size=0.25,
        random_state=7,
        stratify=df["label"],
    )

    pipe = Pipeline(
        [
            (
                "tfidf",
                TfidfVectorizer(
                    lowercase=True,
                    ngram_range=(1, 2),
                    min_df=1,
                    max_features=5000,
                    sublinear_tf=True,
                ),
            ),
            (
                "clf",
                CalibratedClassifierCV(
                    LinearSVC(C=1.2, class_weight="balanced", max_iter=4000),
                    cv=3,
                ),
            ),
        ]
    )
    pipe.fit(x_train, y_train)
    y_pred = pipe.predict(x_test)
    report = classification_report(y_test, y_pred, labels=LABELS, output_dict=True)
    matrix = confusion_matrix(y_test, y_pred, labels=LABELS).tolist()

    ROOT.joinpath("models").mkdir(exist_ok=True)
    joblib.dump(pipe, MODEL_PATH)

    meta = {
        "labels": LABELS,
        "n_samples": int(len(df)),
        "accuracy": report["accuracy"],
        "macro_f1": report["macro avg"]["f1-score"],
        "classification_report": report,
        "confusion_matrix": matrix,
        "confusion_matrix_labels": LABELS,
        "algorithm": "TF-IDF (1-2 grams) + Linear SVM with probability calibration",
    }
    META_PATH.write_text(json.dumps(meta, indent=2), encoding="utf-8")
    print("Samples:", len(df))
    print(classification_report(y_test, y_pred, labels=LABELS, digits=3))
    print(matrix)
    return meta


if __name__ == "__main__":
    train()
