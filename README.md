# Sukoon — Student Wellness Companion

Capstone project for **Hirdesh Matai**, Guru Gobind Singh Indraprastha University  
AICTE ID: `STU6a3a4acf23f101782205135`

Sukoon is a **student wellness companion chatbot**. It is **not therapy, not diagnosis, and not a crisis service**. It classifies a check-in with a trained ML model, replies with a short practical next step, and hands off to Indian helplines when the message looks like a crisis.

## What it does

1. Student types how they feel.
2. **TF-IDF + Linear SVM** (calibrated) predicts mood: `calm`, `stressed`, `anxious`, `lonely`, `overwhelmed`, `crisis`.
3. Safety layer runs first. Crisis language → helplines only.
4. Otherwise: built-in replies, or optional OpenRouter / Gemini if you paste a key in the sidebar (session only).

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python train.py             # writes data/student_moods.csv + models/
streamlit run app.py
```

## Deploy (Streamlit Community Cloud)

1. Open this GitHub repo in [share.streamlit.io](https://share.streamlit.io).
2. Main file: `app.py`.
3. Keys are optional. Demo works with none.

## ML (hold-out 25%)

| Item | Detail |
|---|---|
| Data | 300 synthetic student check-ins |
| Split | 75 / 25, stratified |
| Features | TF-IDF, 1–2 grams, sublinear tf |
| Model | Linear SVM + probability calibration |
| Accuracy | **68%** |
| Macro F1 | **0.66** |
| Crisis recall | **1.00** on the test fold |

Full report: `models/metrics.json` after `python train.py`.

Honest numbers. Crisis class is the one that must not miss.

## Safety

- Persistent disclaimer.
- Crisis gate + `crisis` class → KIRAN, Tele MANAS, iCall, Vandrevala, 112.
- No medication talk. No diagnosis. Chats stay in the browser session.

If you are in danger, call **112** or **KIRAN 1800-599-0019**.

## Files

```
app.py            Streamlit UI
train.py          Train / evaluate
dataset.py        Labeled examples
mood_engine.py    Load model, predict
safety.py         Crisis gate + helplines
llm.py            Optional OpenRouter / Gemini
replies.py        Offline reply templates
data/             CSV after training
models/           Pipeline + metrics
```

## License

Academic / demo use.
