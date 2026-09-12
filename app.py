import streamlit as st

from llm import generate_llm_reply
from mood_engine import predict_mood
from replies import breathing_script, template_reply
from safety import HELPLINES, crisis_message, is_crisis_text

st.set_page_config(
    page_title="Sukoon — Student Wellness Companion",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded",
)

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,560;9..144,650&family=Source+Sans+3:wght@400;500;600&display=swap');
html, body, [class*="css"] { font-family: 'Source Sans 3', sans-serif; }
.stApp { background: #F4EFE6; color: #1C2B24; }
section[data-testid="stSidebar"] { background: #E7E1D6; }
h1, h2, h3 { font-family: Fraunces, serif; color: #1C2B24; }
.hero { padding: 0.4rem 0 0.8rem; }
.hero p { color: #5C6B64; max-width: 40rem; }
.badge { display:inline-block; padding: 0.2rem 0.7rem; border-radius: 999px;
  background:#2F6F5E; color:#F4EFE6; font-size:0.8rem; letter-spacing:.04em; }
.warn { background:#F3E4D4; border:1px solid #C4A574; padding:0.75rem 1rem;
  border-radius: 12px; color:#1C2B24; font-size:0.92rem; }
.crisis { background:#F6E4E1; border:1px solid #8B3A3A; padding:1rem;
  border-radius: 12px; white-space: pre-wrap; }
.line { color:#5C6B64; font-size:0.85rem; }
.stChatMessage { background: #FFFAF3; border-radius: 14px; }
div[data-testid="stChatInput"] textarea { background: #FFFAF3; }
.stButton>button { background:#2F6F5E; color:#F4EFE6; border:0; border-radius:10px;
  height: 2.6rem; }
.stButton>button:hover { background:#245948; color:#F4EFE6; }
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "I am Sukoon. I am a student wellness companion, not a counsellor.\n\n"
                "Tell me how today feels. I will read the mood, reply simply, "
                "and share one small next step. If you are in crisis, I will "
                "give helplines instead of advice."
            ),
        }
    ]
if "last_mood" not in st.session_state:
    st.session_state.last_mood = None

with st.sidebar:
    st.markdown("### Sukoon")
    st.caption("Campus wellness companion")
    st.markdown(
        '<p class="line">Not therapy. Not diagnosis. For students who need a check-in.</p>',
        unsafe_allow_html=True,
    )
    st.divider()
    st.markdown("**India helplines**")
    for h in HELPLINES:
        st.markdown(f"**{h['name']}**  \n`{h['phone']}`  \n{h['note']}")
    st.divider()
    st.markdown("**Optional LLM (session only)**")
    st.caption("Leave empty to use the built-in replies. Key is not saved.")
    or_key = st.text_input("OpenRouter API key", type="password")
    g_key = st.text_input("Google AI Studio key", type="password")
    st.divider()
    if st.button("Box breathing"):
        st.session_state.messages.append(
            {"role": "assistant", "content": breathing_script()}
        )
        st.rerun()
    if st.button("Clear chat"):
        st.session_state.messages = st.session_state.messages[:1]
        st.session_state.last_mood = None
        st.rerun()
    st.caption("Capstone · Hirdesh Matai · GGSIPU")

left, right = st.columns([1.4, 0.6])
with left:
    st.markdown('<div class="hero">', unsafe_allow_html=True)
    st.markdown('<span class="badge">WELLNESS COMPANION</span>', unsafe_allow_html=True)
    st.title("How is your head today?")
    st.markdown(
        '<p>Check in. I classify mood with a trained model, then reply. '
        "If you need a person, I step aside.</p>",
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="warn">Sukoon is not a substitute for professional care. '
        "If you are in danger, call 112 or KIRAN 1800-599-0019.</div>",
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)

    chips = [
        "Three deadlines, I am stressed",
        "I feel left out in hostel",
        "Exam anxiety is back",
        "Too much at once, I froze",
        "I am okay, just checking in",
    ]
    cols = st.columns(len(chips))
    picked = None
    for i, c in enumerate(chips):
        if cols[i].button(c, key=f"chip_{i}"):
            picked = c

    for m in st.session_state.messages:
        with st.chat_message(m["role"]):
            if m.get("crisis"):
                st.markdown(f'<div class="crisis">{m["content"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(m["content"])

    user_text = st.chat_input("Write how you feel…")
    if picked:
        user_text = picked

    if user_text:
        st.session_state.messages.append({"role": "user", "content": user_text})
        crisis = is_crisis_text(user_text)
        mood, conf, scores = predict_mood(user_text)
        if mood == "crisis":
            crisis = True
        st.session_state.last_mood = None if crisis else (mood, conf, scores)

        if crisis:
            reply = crisis_message()
            st.session_state.messages.append(
                {"role": "assistant", "content": reply, "crisis": True}
            )
        else:
            hist = [
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
                if m["role"] in ("user", "assistant") and not m.get("crisis")
            ][:-1]
            llm = generate_llm_reply(
                mood,
                user_text,
                hist,
                or_key.strip() or None,
                g_key.strip() or None,
            )
            reply = llm or template_reply(mood, user_text)
            st.session_state.messages.append({"role": "assistant", "content": reply})
        st.rerun()

with right:
    st.markdown("#### Mood read")
    if st.session_state.last_mood:
        mood, conf, scores = st.session_state.last_mood
        st.metric("Predicted mood", mood, f"{conf:.0%} confidence")
        st.bar_chart(scores)
        st.caption("TF-IDF + Logistic Regression on student check-in text.")
    else:
        st.info("Send a message to see the classifier.")
    st.markdown("#### Grounding")
    st.write(breathing_script())
