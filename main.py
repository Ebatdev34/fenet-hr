# ================================================================
#  FENET  —  Unified Study & Productivity Platform
#  Streamlit | Dark Academic · Neon Ink aesthetic
#  Integrated: Flashcards ↔ Tasks ↔ Alarms ↔ Quiz ↔ Q&A
# ================================================================

import streamlit as st
from datetime import datetime, timedelta
import time
import random
import json
import requests

st.set_page_config(
    page_title="FENET",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ================================================================
#  STYLE  —  Dark Academic × Neon Ink
# ================================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;700;800&family=DM+Mono:wght@300;400;500&display=swap');

*, *::before, *::after { box-sizing: border-box; }

html, body, .stApp {
    background: #0a0a0f !important;
    color: #c8d8e8;
    font-family: 'DM Mono', monospace;
}

/* Animated background grid */
.stApp::before {
    content: '';
    position: fixed;
    inset: 0;
    background-image:
        linear-gradient(rgba(0,255,180,0.03) 1px, transparent 1px),
        linear-gradient(90deg, rgba(0,255,180,0.03) 1px, transparent 1px);
    background-size: 40px 40px;
    pointer-events: none;
    z-index: 0;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: #07070d !important;
    border-right: 1px solid rgba(0,255,180,0.1) !important;
}
section[data-testid="stSidebar"] * { font-family: 'DM Mono', monospace !important; }

/* Main content */
.block-container { padding: 2rem 2rem 4rem !important; position: relative; z-index: 1; }

/* Typography */
h1, h2, h3 { font-family: 'Syne', sans-serif !important; letter-spacing: -0.02em; }

/* FENET Logo */
.fenet-logo {
    font-family: 'Syne', sans-serif;
    font-size: 13px;
    font-weight: 800;
    letter-spacing: 6px;
    color: #00ffb4;
    text-transform: uppercase;
    padding: 20px 0 4px;
    text-align: center;
    text-shadow: 0 0 20px rgba(0,255,180,0.5);
}
.fenet-tagline {
    font-size: 10px;
    letter-spacing: 3px;
    color: rgba(200,216,232,0.3);
    text-align: center;
    margin-bottom: 24px;
    text-transform: uppercase;
}

/* Page header */
.page-header {
    border-bottom: 1px solid rgba(0,255,180,0.15);
    padding-bottom: 12px;
    margin-bottom: 24px;
}
.page-title {
    font-family: 'Syne', sans-serif;
    font-size: 28px;
    font-weight: 800;
    color: #e8f0f8;
    margin: 0;
}
.page-subtitle {
    font-size: 11px;
    color: rgba(200,216,232,0.4);
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-top: 4px;
}

/* Cards */
.card {
    background: rgba(255,255,255,0.02);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 12px;
    padding: 18px 20px;
    margin-bottom: 10px;
    transition: border-color 0.2s;
}
.card:hover { border-color: rgba(0,255,180,0.2); }

.card-accent-green { border-left: 3px solid #00ffb4; }
.card-accent-blue  { border-left: 3px solid #4d9fff; }
.card-accent-pink  { border-left: 3px solid #ff4d9f; }
.card-accent-gold  { border-left: 3px solid #ffb84d; }

.card-label {
    font-size: 10px;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: rgba(200,216,232,0.35);
    margin-bottom: 6px;
}
.card-title {
    font-family: 'Syne', sans-serif;
    font-size: 16px;
    font-weight: 700;
    color: #e8f0f8;
}
.card-meta {
    font-size: 11px;
    color: rgba(200,216,232,0.4);
    margin-top: 4px;
}

/* Badges */
.badge {
    display: inline-block;
    padding: 2px 10px;
    border-radius: 20px;
    font-size: 10px;
    letter-spacing: 1px;
    text-transform: uppercase;
    font-weight: 500;
}
.badge-green { background: rgba(0,255,180,0.12); color: #00ffb4; border: 1px solid rgba(0,255,180,0.25); }
.badge-blue  { background: rgba(77,159,255,0.12); color: #4d9fff; border: 1px solid rgba(77,159,255,0.25); }
.badge-pink  { background: rgba(255,77,159,0.12); color: #ff4d9f; border: 1px solid rgba(255,77,159,0.25); }
.badge-gold  { background: rgba(255,184,77,0.12); color: #ffb84d; border: 1px solid rgba(255,184,77,0.25); }
.badge-red   { background: rgba(255,80,80,0.15);  color: #ff5050; border: 1px solid rgba(255,80,80,0.3); }

/* Alarm card */
.alarm-fire {
    background: rgba(255,80,80,0.08);
    border: 1px solid rgba(255,80,80,0.4);
    border-radius: 12px;
    padding: 20px;
    margin-bottom: 12px;
    animation: pulse 1s ease-in-out infinite alternate;
}
@keyframes pulse {
    from { box-shadow: 0 0 10px rgba(255,80,80,0.2); }
    to   { box-shadow: 0 0 30px rgba(255,80,80,0.5); }
}

/* Flashcard */
.flashcard {
    background: linear-gradient(135deg, rgba(0,255,180,0.04), rgba(77,159,255,0.04));
    border: 1px solid rgba(0,255,180,0.2);
    border-radius: 20px;
    padding: 48px 40px;
    text-align: center;
    min-height: 220px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    position: relative;
    overflow: hidden;
    margin-bottom: 20px;
}
.flashcard::before {
    content: '';
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: radial-gradient(circle at 30% 30%, rgba(0,255,180,0.04) 0%, transparent 60%);
    pointer-events: none;
}
.flashcard-q {
    font-family: 'Syne', sans-serif;
    font-size: 20px;
    font-weight: 700;
    color: #e8f0f8;
    line-height: 1.4;
}
.flashcard-a {
    font-size: 15px;
    color: #00ffb4;
    line-height: 1.7;
    margin-top: 8px;
}
.flashcard-tag {
    position: absolute;
    top: 16px;
    right: 16px;
    font-size: 10px;
    letter-spacing: 2px;
    color: rgba(0,255,180,0.4);
    text-transform: uppercase;
}

/* Progress bar custom */
.prog-wrap {
    background: rgba(255,255,255,0.05);
    border-radius: 4px;
    height: 4px;
    margin: 12px 0;
    overflow: hidden;
}
.prog-fill {
    height: 100%;
    background: linear-gradient(90deg, #00ffb4, #4d9fff);
    border-radius: 4px;
    transition: width 0.4s ease;
}

/* Stats row */
.stat-box {
    background: rgba(255,255,255,0.02);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 10px;
    padding: 16px;
    text-align: center;
}
.stat-num {
    font-family: 'Syne', sans-serif;
    font-size: 28px;
    font-weight: 800;
    color: #00ffb4;
    line-height: 1;
}
.stat-label {
    font-size: 10px;
    letter-spacing: 2px;
    color: rgba(200,216,232,0.35);
    text-transform: uppercase;
    margin-top: 6px;
}

/* Answer box */
.answer-wrap {
    background: rgba(0,255,180,0.03);
    border-left: 2px solid #00ffb4;
    border-radius: 0 10px 10px 0;
    padding: 16px 20px;
    margin: 8px 0;
    font-size: 14px;
    line-height: 1.8;
    color: #c8d8e8;
}
.you-wrap {
    background: rgba(77,159,255,0.04);
    border-left: 2px solid #4d9fff;
    border-radius: 0 10px 10px 0;
    padding: 12px 20px;
    margin: 6px 0;
    font-size: 13px;
    color: rgba(200,216,232,0.7);
}
.wiki-src { font-size: 10px; color: rgba(200,216,232,0.3); margin-top: 8px; }

/* Quiz */
.quiz-q {
    font-family: 'Syne', sans-serif;
    font-size: 22px;
    font-weight: 700;
    color: #e8f0f8;
    line-height: 1.4;
    padding: 24px 0 16px;
}

/* Streamlit overrides */
.stButton > button {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    color: #c8d8e8 !important;
    border-radius: 8px !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 13px !important;
    transition: all 0.2s !important;
    padding: 8px 18px !important;
}
.stButton > button:hover {
    border-color: rgba(0,255,180,0.4) !important;
    color: #00ffb4 !important;
    background: rgba(0,255,180,0.06) !important;
}
.stButton > button:active {
    background: rgba(0,255,180,0.1) !important;
}

/* Primary button */
.stButton.primary > button {
    background: rgba(0,255,180,0.1) !important;
    border-color: rgba(0,255,180,0.4) !important;
    color: #00ffb4 !important;
}

div[data-testid="stTextInput"] input,
div[data-testid="stTextArea"] textarea,
div[data-testid="stSelectbox"] select {
    background: rgba(255,255,255,0.03) !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 8px !important;
    color: #c8d8e8 !important;
    font-family: 'DM Mono', monospace !important;
}
div[data-testid="stTextInput"] input:focus,
div[data-testid="stTextArea"] textarea:focus {
    border-color: rgba(0,255,180,0.3) !important;
    box-shadow: 0 0 0 1px rgba(0,255,180,0.1) !important;
}

div[data-testid="stForm"] {
    background: rgba(255,255,255,0.02) !important;
    border: 1px solid rgba(255,255,255,0.06) !important;
    border-radius: 12px !important;
    padding: 20px !important;
}

.stProgress > div > div {
    background: linear-gradient(90deg, #00ffb4, #4d9fff) !important;
}

div[data-testid="stMetric"] {
    background: rgba(255,255,255,0.02);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 10px;
    padding: 12px;
}

label { color: rgba(200,216,232,0.5) !important; font-size: 11px !important; letter-spacing: 1px !important; }

hr { border-color: rgba(255,255,255,0.06) !important; }
.stCaption { color: rgba(200,216,232,0.35) !important; font-size: 11px !important; }

/* Selectbox nav */
div[data-testid="stSelectbox"] > div > div {
    background: rgba(255,255,255,0.03) !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    color: #c8d8e8 !important;
}

/* Toggle */
div[data-testid="stToggle"] { color: #c8d8e8 !important; }

/* Expander */
div[data-testid="stExpander"] {
    background: rgba(255,255,255,0.02) !important;
    border: 1px solid rgba(255,255,255,0.06) !important;
    border-radius: 10px !important;
}

/* Divider label */
.section-label {
    font-size: 10px;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: rgba(200,216,232,0.25);
    margin: 20px 0 12px;
}

/* Spaced repetition due indicator */
.due-now { color: #ff5050; }
.due-soon { color: #ffb84d; }
.due-later { color: #00ffb4; }

/* Task checkbox override */
div[data-testid="stCheckbox"] label {
    font-size: 14px !important;
    color: #c8d8e8 !important;
    letter-spacing: 0 !important;
}

/* Integration notification */
.integration-note {
    background: rgba(255,184,77,0.06);
    border: 1px solid rgba(255,184,77,0.2);
    border-radius: 8px;
    padding: 10px 14px;
    font-size: 12px;
    color: #ffb84d;
    margin: 8px 0;
}

.notif {
    background: rgba(0,255,180,0.06);
    border: 1px solid rgba(0,255,180,0.2);
    border-radius: 8px;
    padding: 10px 14px;
    font-size: 12px;
    color: #00ffb4;
    margin: 6px 0;
}
</style>
""", unsafe_allow_html=True)

# ================================================================
#  DATA — Flashcards & Quiz
# ================================================================

ALL_FLASHCARDS = [
    {"id": 1,  "subject": "Biology",   "q": "What is photosynthesis?",           "a": "Plants use sunlight + CO₂ + H₂O → glucose + O₂. Equation: 6CO₂+6H₂O+light → C₆H₁₂O₆+6O₂. Happens in chloroplasts."},
    {"id": 2,  "subject": "Physics",   "q": "What is Newton's 2nd law?",         "a": "F = ma. Force equals mass times acceleration. Measured in Newtons."},
    {"id": 3,  "subject": "Biology",   "q": "What is osmosis?",                  "a": "Water moving through a semi-permeable membrane from low to high solute concentration. Passive — no energy needed."},
    {"id": 4,  "subject": "Chemistry", "q": "What is pH of pure water?",         "a": "pH 7 — neutral. Below 7 = acidic. Above 7 = alkaline."},
    {"id": 5,  "subject": "Biology",   "q": "Products of aerobic respiration?",  "a": "Glucose + O₂ → CO₂ + water + ATP energy."},
    {"id": 6,  "subject": "Physics",   "q": "Formula for speed?",                "a": "Speed = distance ÷ time. Measured in m/s. Scalar quantity (no direction)."},
    {"id": 7,  "subject": "Physics",   "q": "Formula for kinetic energy?",       "a": "KE = ½mv². Double the speed = 4× the kinetic energy."},
    {"id": 8,  "subject": "Math",      "q": "Pythagoras theorem?",               "a": "a² + b² = c² in a right-angled triangle. c is always the hypotenuse (longest side)."},
    {"id": 9,  "subject": "Math",      "q": "What is the mean?",                 "a": "Mean = sum of all values ÷ number of values. Example: (4+8+6) ÷ 3 = 6."},
    {"id": 10, "subject": "Biology",   "q": "What is mitosis?",                  "a": "Cell division producing 2 identical daughter cells. Used for growth and tissue repair."},
    {"id": 11, "subject": "Physics",   "q": "What is atomic number?",            "a": "Number of protons in the nucleus. Determines the element's identity on the periodic table."},
    {"id": 12, "subject": "Physics",   "q": "Formula for density?",              "a": "Density = mass ÷ volume. Objects less dense than water float; more dense sink."},
    {"id": 13, "subject": "Biology",   "q": "What is natural selection?",        "a": "Better-adapted organisms survive, reproduce more, and pass their traits to offspring. Drives evolution."},
    {"id": 14, "subject": "Physics",   "q": "What is Ohm's law?",                "a": "V = IR. Voltage (V) = Current (A) × Resistance (Ω)."},
    {"id": 15, "subject": "Chemistry", "q": "Acids vs Bases?",                   "a": "Acids: pH < 7, H⁺ ions, turns litmus red. Bases: pH > 7, OH⁻ ions, turns litmus blue."},
    {"id": 16, "subject": "Biology",   "q": "What is an enzyme?",                "a": "Biological catalyst — speeds up reactions without being consumed. Lock-and-key specificity."},
    {"id": 17, "subject": "Physics",   "q": "Formula for gravitational PE?",     "a": "GPE = mgh (mass × gravity × height). More height = more stored energy."},
    {"id": 18, "subject": "Math",      "q": "What are prime numbers?",           "a": "Numbers > 1 divisible only by 1 and themselves. Examples: 2, 3, 5, 7, 11, 13, 17..."},
    {"id": 19, "subject": "Physics",   "q": "3 states of matter?",              "a": "Solid (fixed shape & volume), Liquid (fixed volume), Gas (fills container)."},
    {"id": 20, "subject": "Biology",   "q": "What is diffusion?",               "a": "Particles move from high to low concentration until evenly spread. Passive — no energy required."},
    {"id": 21, "subject": "Math",      "q": "Area of a circle?",                "a": "A = πr². Circumference = 2πr. π ≈ 3.14159."},
    {"id": 22, "subject": "Chemistry", "q": "What is neutralisation?",           "a": "Acid + Base → Salt + Water. Example: HCl + NaOH → NaCl + H₂O."},
    {"id": 23, "subject": "Biology",   "q": "Function of the mitochondria?",     "a": "Powerhouse of the cell — site of aerobic respiration. Produces ATP energy from glucose."},
    {"id": 24, "subject": "Math",      "q": "What is the median?",               "a": "The middle value when numbers are arranged in order. If even count, average the two middle values."},
    {"id": 25, "subject": "Physics",   "q": "Newton's 3rd law?",                "a": "Every action has an equal and opposite reaction. Example: rocket propulsion, walking."},
]

QUIZ_QUESTIONS = [
    {"q": "7 × 8 = ?",                              "opts": ["54","56","63","48"],                    "ans": "56",             "subject": "Math"},
    {"q": "Gas produced in photosynthesis?",         "opts": ["CO₂","Nitrogen","Oxygen","Hydrogen"],  "ans": "Oxygen",         "subject": "Biology"},
    {"q": "Area of a circle formula?",               "opts": ["2πr","πr²","πd","2πr²"],               "ans": "πr²",            "subject": "Math"},
    {"q": "Unit of force?",                          "opts": ["Joule","Watt","Newton","Pascal"],       "ans": "Newton",         "subject": "Physics"},
    {"q": "Human chromosomes count?",                "opts": ["23","46","48","32"],                    "ans": "46",             "subject": "Biology"},
    {"q": "pH 7 means?",                             "opts": ["Acidic","Alkaline","Neutral","Base"],   "ans": "Neutral",        "subject": "Chemistry"},
    {"q": "Speed = ?",                               "opts": ["d×t","d÷t","t÷d","F÷m"],              "ans": "d÷t",            "subject": "Physics"},
    {"q": "Photosynthesis happens in?",              "opts": ["Nucleus","Mitochondria","Ribosome","Chloroplast"], "ans": "Chloroplast", "subject": "Biology"},
    {"q": "15% of 200?",                             "opts": ["25","30","35","20"],                    "ans": "30",             "subject": "Math"},
    {"q": "Powerhouse of the cell?",                 "opts": ["Nucleus","Chloroplast","Mitochondria","Ribosome"], "ans": "Mitochondria", "subject": "Biology"},
    {"q": "Speed of light (m/s)?",                   "opts": ["3×10⁶","3×10⁸","3×10¹⁰","3×10⁴"],    "ans": "3×10⁸",          "subject": "Physics"},
    {"q": "Acid + Base → ?",                         "opts": ["Gas+Water","Salt+Water","Salt+Gas","Oxide+Water"], "ans": "Salt+Water", "subject": "Chemistry"},
    {"q": "Median of 2,3,5,7,9?",                   "opts": ["3","5","7","9"],                        "ans": "5",              "subject": "Math"},
    {"q": "F = ma is Newton's ... law?",             "opts": ["1st","2nd","3rd","4th"],                "ans": "2nd",            "subject": "Physics"},
    {"q": "Kinetic energy formula?",                 "opts": ["mgh","½mv²","mv","Fd"],                "ans": "½mv²",           "subject": "Physics"},
    {"q": "DNA base pairs: A pairs with?",           "opts": ["C","G","T","U"],                        "ans": "T",              "subject": "Biology"},
    {"q": "Density = ?",                             "opts": ["m×v","m÷v","v÷m","m+v"],              "ans": "m÷v",            "subject": "Physics"},
    {"q": "Square root of 144?",                     "opts": ["11","12","13","14"],                    "ans": "12",             "subject": "Math"},
    {"q": "Neutralisation produces?",                "opts": ["Acid+Base","Salt+Water","CO₂+H₂O","O₂+H₂O"], "ans": "Salt+Water", "subject": "Chemistry"},
    {"q": "Largest planet in solar system?",         "opts": ["Saturn","Neptune","Jupiter","Uranus"],  "ans": "Jupiter",        "subject": "Science"},
]

SUBJECT_COLORS = {
    "Math":      "badge-blue",
    "Biology":   "badge-green",
    "Physics":   "badge-pink",
    "Chemistry": "badge-gold",
    "Science":   "badge-blue",
    "General":   "badge-blue",
}

# ================================================================
#  WIKIPEDIA Q&A
# ================================================================

WIKI_SUMMARY = "https://en.wikipedia.org/api/rest_v1/page/summary/{}"
WIKI_SEARCH  = "https://en.wikipedia.org/w/api.php"

def wiki_fetch(query: str) -> dict:
    q = query.strip()
    if not q:
        return {}
    try:
        r = requests.get(WIKI_SUMMARY.format(requests.utils.quote(q)), timeout=5)
        if r.status_code == 200:
            d = r.json()
            if d.get("extract"):
                return {"title": d.get("title",""), "extract": d.get("extract",""),
                        "url": d.get("content_urls",{}).get("desktop",{}).get("page","")}
    except Exception:
        pass
    try:
        r = requests.get(WIKI_SEARCH, params={"action":"query","list":"search",
            "srsearch":q,"format":"json","srlimit":1}, timeout=5)
        if r.status_code == 200:
            results = r.json().get("query",{}).get("search",[])
            if results:
                r2 = requests.get(WIKI_SUMMARY.format(requests.utils.quote(results[0]["title"])), timeout=5)
                if r2.status_code == 200:
                    d = r2.json()
                    return {"title": d.get("title",""), "extract": d.get("extract",""),
                            "url": d.get("content_urls",{}).get("desktop",{}).get("page","")}
    except Exception:
        pass
    return {}

def best_answer(question: str, extract: str) -> str:
    if not extract:
        return ""
    stop = {"what","is","are","the","a","an","of","in","on","to","for","how",
            "why","when","where","who","was","were","do","does","did","can"}
    kw = set(question.lower().split()) - stop
    sents = [s.strip() for s in extract.replace("\n"," ").split(".") if s.strip()]
    if not sents:
        return extract[:500]
    scored = sorted([(sum(1 for w in kw if w in s.lower()), s) for s in sents], reverse=True)
    top = [s for sc, s in scored[:4] if sc > 0]
    return (". ".join(top) + ".") if top else (". ".join(sents[:3]) + ".")

# ================================================================
#  SPACED REPETITION (simplified SM-2 style)
# ================================================================

def get_next_review(ease: int, interval: int, quality: int) -> tuple:
    """Returns (new_interval_days, new_ease). quality: 0=fail,1=hard,2=ok,3=easy"""
    if quality == 0:
        return 1, max(1, ease - 1)
    elif quality == 1:
        return max(1, interval), ease
    elif quality == 2:
        return max(2, int(interval * 1.5)), ease
    else:
        return max(3, int(interval * 2.5)), min(5, ease + 1)

def days_until_review(card_id: int) -> int:
    sr = st.session_state.sr_data.get(str(card_id), {})
    if not sr.get("next_review"):
        return 0
    next_dt = datetime.fromisoformat(sr["next_review"])
    delta = (next_dt - datetime.now()).days
    return max(0, delta)

def is_due(card_id: int) -> bool:
    return days_until_review(card_id) == 0

# ================================================================
#  SESSION STATE
# ================================================================

def init_state():
    defaults = {
        "alarms": [],
        "triggered": set(),
        "tasks": [],
        "chat": [],
        "flash_idx": 0,
        "flash_show": False,
        "flash_deck": None,
        "flash_filter": "All",
        "quiz_idx": 0,
        "quiz_score": 0,
        "quiz_answered": False,
        "quiz_selected": None,
        "quiz_deck": None,
        "notes": "",
        "notifications": [],
        "sr_data": {},      # card_id -> {interval, ease, next_review, reviews}
        "quiz_history": [], # list of {subject, correct, total}
        "tasks_added_by_system": set(),
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

    if st.session_state.flash_deck is None:
        deck = ALL_FLASHCARDS.copy()
        random.shuffle(deck)
        st.session_state.flash_deck = deck

    if st.session_state.quiz_deck is None:
        deck = QUIZ_QUESTIONS.copy()
        random.shuffle(deck)
        st.session_state.quiz_deck = deck

init_state()

# ================================================================
#  INTEGRATION HELPERS
# ================================================================

def add_notification(msg: str):
    st.session_state.notifications.insert(0, {
        "msg": msg,
        "time": datetime.now().strftime("%H:%M")
    })
    if len(st.session_state.notifications) > 10:
        st.session_state.notifications.pop()

def add_task(title: str, tag: str = "Study", source: str = "manual", alarm_time: str = None):
    task_key = f"{title}_{tag}"
    if task_key not in st.session_state.tasks_added_by_system:
        st.session_state.tasks.append({
            "id": len(st.session_state.tasks),
            "title": title,
            "tag": tag,
            "done": False,
            "created": datetime.now().isoformat(),
            "alarm_time": alarm_time,
            "source": source,
        })
        if source == "system":
            st.session_state.tasks_added_by_system.add(task_key)

def due_cards_count() -> int:
    return sum(1 for c in ALL_FLASHCARDS if is_due(c["id"]))

def sound_alarm():
    try:
        with open("ring.mp3", "rb") as f:
            st.audio(f.read(), format="audio/mp3")
    except Exception:
        pass

# ================================================================
#  SIDEBAR
# ================================================================

with st.sidebar:
    st.markdown("<div class='fenet-logo'>FENET</div>", unsafe_allow_html=True)
    st.markdown("<div class='fenet-tagline'>Study · Focus · Execute</div>", unsafe_allow_html=True)

    page = st.selectbox("", [
        "⬛ Dashboard",
        "🧠 Ask & Learn",
        "🃏 Flashcards",
        "❓ Quiz",
        "✅ Tasks",
        "⏰ Alarms",
        "📝 Notes",
    ], label_visibility="collapsed")

    st.markdown("---")

    # Live stats
    due = due_cards_count()
    active_tasks = sum(1 for t in st.session_state.tasks if not t["done"])
    active_alarms = sum(1 for a in st.session_state.alarms if not a["done"])

    st.markdown(f"""
    <div style='display:grid;grid-template-columns:1fr 1fr;gap:8px;'>
        <div class='stat-box'><div class='stat-num'>{due}</div><div class='stat-label'>Due Cards</div></div>
        <div class='stat-box'><div class='stat-num'>{active_tasks}</div><div class='stat-label'>Tasks</div></div>
        <div class='stat-box'><div class='stat-num'>{active_alarms}</div><div class='stat-label'>Alarms</div></div>
        <div class='stat-box'><div class='stat-num'>{len(ALL_FLASHCARDS)}</div><div class='stat-label'>Cards</div></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # Notifications
    if st.session_state.notifications:
        st.markdown("<div class='section-label'>Recent Activity</div>", unsafe_allow_html=True)
        for n in st.session_state.notifications[:4]:
            st.markdown(f"<div style='font-size:11px;color:rgba(200,216,232,0.4);padding:3px 0;'>{n['time']} — {n['msg']}</div>", unsafe_allow_html=True)

# ================================================================
#  CHECK ALARMS (runs every page load)
# ================================================================

now = datetime.now()
for alarm in st.session_state.alarms:
    if alarm["done"]:
        continue
    try:
        alarm_time = datetime.strptime(alarm["time"], "%Y-%m-%d %H:%M")
        alarm_id = f"alarm_{alarm['subject']}_{alarm['time']}"
        if now >= alarm_time and alarm_id not in st.session_state.triggered:
            st.session_state.triggered.add(alarm_id)
            add_notification(f"⏰ Alarm: {alarm['subject']}")
    except Exception:
        pass

# ================================================================
#  PAGE: DASHBOARD
# ================================================================

if page == "⬛ Dashboard":
    st.markdown("""
    <div class='page-header'>
        <div class='page-title'>Dashboard</div>
        <div class='page-subtitle'>Your study command center</div>
    </div>
    """, unsafe_allow_html=True)

    # Firing alarms
    for alarm in st.session_state.alarms:
        if alarm["done"]:
            continue
        try:
            alarm_time = datetime.strptime(alarm["time"], "%Y-%m-%d %H:%M")
            alarm_id = f"alarm_{alarm['subject']}_{alarm['time']}"
            if now >= alarm_time and alarm_id in st.session_state.triggered:
                st.markdown(f"""
                <div class='alarm-fire'>
                    🚨 <strong style='color:#ff5050;font-size:18px;'>{alarm['subject'].upper()}</strong>
                    <span style='color:rgba(255,80,80,0.6);font-size:12px;'> — DUE NOW</span>
                </div>
                """, unsafe_allow_html=True)
                sound_alarm()
                st.balloons()
        except Exception:
            pass

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"<div class='stat-box'><div class='stat-num'>{due_cards_count()}</div><div class='stat-label'>Cards Due</div></div>", unsafe_allow_html=True)
    with col2:
        done_tasks = sum(1 for t in st.session_state.tasks if t["done"])
        total_tasks = len(st.session_state.tasks)
        st.markdown(f"<div class='stat-box'><div class='stat-num'>{done_tasks}/{total_tasks}</div><div class='stat-label'>Tasks Done</div></div>", unsafe_allow_html=True)
    with col3:
        total_reviews = sum(st.session_state.sr_data.get(str(c["id"]),{}).get("reviews",0) for c in ALL_FLASHCARDS)
        st.markdown(f"<div class='stat-box'><div class='stat-num'>{total_reviews}</div><div class='stat-label'>Reviews</div></div>", unsafe_allow_html=True)
    with col4:
        if st.session_state.quiz_history:
            total_q = sum(x["total"] for x in st.session_state.quiz_history)
            total_c = sum(x["correct"] for x in st.session_state.quiz_history)
            pct = int(total_c / total_q * 100) if total_q else 0
        else:
            pct = 0
        st.markdown(f"<div class='stat-box'><div class='stat-num'>{pct}%</div><div class='stat-label'>Quiz Avg</div></div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col_left, col_right = st.columns([3, 2])

    with col_left:
        st.markdown("<div class='section-label'>Due Flashcards</div>", unsafe_allow_html=True)
        due_cards = [c for c in ALL_FLASHCARDS if is_due(c["id"])][:5]
        if due_cards:
            for c in due_cards:
                color = SUBJECT_COLORS.get(c["subject"], "badge-blue")
                st.markdown(f"""
                <div class='card card-accent-green'>
                    <span class='badge {color}'>{c["subject"]}</span>
                    <div class='card-title' style='margin-top:6px;font-size:14px;'>{c["q"]}</div>
                </div>
                """, unsafe_allow_html=True)
            if st.button("→ Review Now", key="dash_review"):
                st.session_state.flash_filter = "Due Only"
                st.rerun()
        else:
            st.markdown("<div class='notif'>✓ All cards reviewed. Come back tomorrow.</div>", unsafe_allow_html=True)

        st.markdown("<div class='section-label'>Active Tasks</div>", unsafe_allow_html=True)
        pending = [t for t in st.session_state.tasks if not t["done"]][:4]
        if pending:
            for t in pending:
                tag_color = {"Study": "badge-blue", "Review": "badge-green", "Deadline": "badge-red", "Personal": "badge-gold"}.get(t["tag"], "badge-blue")
                st.markdown(f"""
                <div class='card card-accent-blue'>
                    <span class='badge {tag_color}'>{t["tag"]}</span>
                    <div class='card-title' style='margin-top:5px;font-size:14px;'>{t["title"]}</div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown("<div style='color:rgba(200,216,232,0.3);font-size:13px;'>No pending tasks.</div>", unsafe_allow_html=True)

    with col_right:
        st.markdown("<div class='section-label'>Upcoming Alarms</div>", unsafe_allow_html=True)
        upcoming = sorted(
            [a for a in st.session_state.alarms if not a["done"]],
            key=lambda x: x["time"]
        )[:4]
        if upcoming:
            for a in upcoming:
                try:
                    alarm_time = datetime.strptime(a["time"], "%Y-%m-%d %H:%M")
                    diff = alarm_time - now
                    mins = int(diff.total_seconds() / 60)
                    if mins < 0:
                        time_label = "<span class='due-now'>OVERDUE</span>"
                    elif mins < 60:
                        time_label = f"<span class='due-soon'>in {mins}m</span>"
                    else:
                        time_label = f"<span class='due-later'>in {mins//60}h {mins%60}m</span>"
                except Exception:
                    time_label = a["time"]
                st.markdown(f"""
                <div class='card card-accent-gold'>
                    <div class='card-title' style='font-size:14px;'>{a["subject"]}</div>
                    <div class='card-meta'>{a["time"]} · {time_label}</div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown("<div style='color:rgba(200,216,232,0.3);font-size:13px;'>No upcoming alarms.</div>", unsafe_allow_html=True)

        st.markdown("<div class='section-label'>Quick Add Task</div>", unsafe_allow_html=True)
        with st.form("quick_task"):
            qt = st.text_input("Task", placeholder="What needs doing?", label_visibility="collapsed")
            qt_tag = st.selectbox("Tag", ["Study","Review","Deadline","Personal"], label_visibility="collapsed")
            if st.form_submit_button("+ Add Task"):
                if qt.strip():
                    add_task(qt.strip(), qt_tag)
                    add_notification(f"Task added: {qt.strip()}")
                    st.rerun()

# ================================================================
#  PAGE: ASK & LEARN
# ================================================================

elif page == "🧠 Ask & Learn":
    st.markdown("""
    <div class='page-header'>
        <div class='page-title'>Ask & Learn</div>
        <div class='page-subtitle'>Wikipedia-powered answers · instant knowledge</div>
    </div>
    """, unsafe_allow_html=True)

    use_internet = st.toggle("🌐 Wikipedia Search", value=True)

    user_msg = st.text_input("", placeholder="What is photosynthesis? How does gravity work? What is algebra?", label_visibility="collapsed")

    c1, c2 = st.columns([1,5])
    with c1:
        ask_btn = st.button("Ask →", use_container_width=True)
    with c2:
        if st.button("Clear chat"):
            st.session_state.chat = []
            st.rerun()

    if ask_btn and user_msg.strip():
        st.session_state.chat.append(("You", user_msg))
        with st.spinner("Searching..."):
            if use_internet:
                result = wiki_fetch(user_msg)
                if result and result.get("extract"):
                    ans = best_answer(user_msg, result["extract"])
                    st.session_state.chat.append(("FENET", {"answer": ans, "title": result["title"], "url": result["url"]}))
                else:
                    st.session_state.chat.append(("FENET", {"answer": "Nothing found. Try rephrasing.", "title": "", "url": ""}))
            else:
                st.session_state.chat.append(("FENET", {"answer": "Internet is off. Turn on Wikipedia Search.", "title": "", "url": ""}))

    for role, msg in reversed(st.session_state.chat[-12:]):
        if role == "You":
            st.markdown(f"<div class='you-wrap'>You  ·  {msg}</div>", unsafe_allow_html=True)
        else:
            answer = msg["answer"] if isinstance(msg, dict) else msg
            url = msg.get("url","") if isinstance(msg, dict) else ""
            title = msg.get("title","") if isinstance(msg, dict) else ""
            src = f"<div class='wiki-src'>📖 <a href='{url}' target='_blank' style='color:rgba(200,216,232,0.3);'>{title} — Wikipedia</a></div>" if url else ""
            st.markdown(f"<div class='answer-wrap'>FENET  ·  {answer}{src}</div>", unsafe_allow_html=True)

# ================================================================
#  PAGE: FLASHCARDS
# ================================================================

elif page == "🃏 Flashcards":
    st.markdown("""
    <div class='page-header'>
        <div class='page-title'>Flashcards</div>
        <div class='page-subtitle'>Spaced repetition · rate each card to schedule reviews</div>
    </div>
    """, unsafe_allow_html=True)

    filter_opt = st.radio("Show", ["All", "Due Only", "Math", "Biology", "Physics", "Chemistry"],
                          horizontal=True, index=["All","Due Only","Math","Biology","Physics","Chemistry"].index(
                              st.session_state.flash_filter if st.session_state.flash_filter in
                              ["All","Due Only","Math","Biology","Physics","Chemistry"] else "All"))
    st.session_state.flash_filter = filter_opt

    if filter_opt == "Due Only":
        deck = [c for c in ALL_FLASHCARDS if is_due(c["id"])]
    elif filter_opt == "All":
        deck = ALL_FLASHCARDS.copy()
    else:
        deck = [c for c in ALL_FLASHCARDS if c["subject"] == filter_opt]

    if not deck:
        st.markdown("<div class='notif'>✓ No cards due in this filter. Great job!</div>", unsafe_allow_html=True)
    else:
        idx = st.session_state.flash_idx % len(deck)
        card = deck[idx]
        sr = st.session_state.sr_data.get(str(card["id"]), {"interval": 1, "ease": 2, "reviews": 0, "next_review": None})

        pct = (idx + 1) / len(deck)
        st.markdown(f"""
        <div class='prog-wrap'><div class='prog-fill' style='width:{pct*100:.0f}%'></div></div>
        """, unsafe_allow_html=True)

        col_info, col_count = st.columns([3,1])
        with col_info:
            st.caption(f"Card {idx+1} of {len(deck)} · {card['subject']}")
        with col_count:
            st.caption(f"Reviews: {sr.get('reviews',0)}")

        color = SUBJECT_COLORS.get(card["subject"], "badge-blue")
        content = card["q"] if not st.session_state.flash_show else card["a"]
        tag_text = "QUESTION" if not st.session_state.flash_show else "ANSWER"
        tag_color = "#4d9fff" if not st.session_state.flash_show else "#00ffb4"

        st.markdown(f"""
        <div class='flashcard'>
            <div class='flashcard-tag' style='color:{tag_color};'>{tag_text}</div>
            <span class='badge {color}' style='margin-bottom:16px;'>{card["subject"]}</span>
            <div class='{"flashcard-q" if not st.session_state.flash_show else "flashcard-a"}'>{content}</div>
        </div>
        """, unsafe_allow_html=True)

        if not st.session_state.flash_show:
            c1, c2, c3 = st.columns([2,1,1])
            with c1:
                if st.button("👁  Reveal Answer", use_container_width=True):
                    st.session_state.flash_show = True
                    st.rerun()
            with c2:
                if st.button("⏭  Skip", use_container_width=True):
                    st.session_state.flash_idx += 1
                    st.session_state.flash_show = False
                    st.rerun()
            with c3:
                if st.button("🔀  Shuffle", use_container_width=True):
                    random.shuffle(st.session_state.flash_deck)
                    st.session_state.flash_idx = 0
                    st.session_state.flash_show = False
                    st.rerun()
        else:
            st.markdown("<div style='text-align:center;margin:8px 0 4px;font-size:11px;letter-spacing:2px;color:rgba(200,216,232,0.3);text-transform:uppercase;'>How well did you know this?</div>", unsafe_allow_html=True)
            c1, c2, c3, c4 = st.columns(4)
            ratings = [("❌ Forgot", 0, "#ff5050"), ("😬 Hard", 1, "#ffb84d"), ("✓ Good", 2, "#4d9fff"), ("⚡ Easy", 3, "#00ffb4")]
            for col, (label, quality, color) in zip([c1,c2,c3,c4], ratings):
                with col:
                    if st.button(label, use_container_width=True, key=f"rate_{quality}"):
                        interval = sr.get("interval", 1)
                        ease = sr.get("ease", 2)
                        new_interval, new_ease = get_next_review(ease, interval, quality)
                        next_review = (datetime.now() + timedelta(days=new_interval)).isoformat()
                        st.session_state.sr_data[str(card["id"])] = {
                            "interval": new_interval,
                            "ease": new_ease,
                            "reviews": sr.get("reviews", 0) + 1,
                            "next_review": next_review,
                        }
                        # Integration: if forgot, add review task
                        if quality == 0:
                            add_task(f"Re-review: {card['q'][:50]}...", "Review", source="system")
                            add_notification(f"Task added: re-review {card['subject']} card")
                            st.markdown("<div class='integration-note'>⚡ Task added to re-review this card today.</div>", unsafe_allow_html=True)

                        add_notification(f"Reviewed: {card['subject']} card ({label})")
                        st.session_state.flash_idx += 1
                        st.session_state.flash_show = False
                        st.rerun()

# ================================================================
#  PAGE: QUIZ
# ================================================================

elif page == "❓ Quiz":
    st.markdown("""
    <div class='page-header'>
        <div class='page-title'>Quiz Mode</div>
        <div class='page-subtitle'>Test yourself · track your weak subjects</div>
    </div>
    """, unsafe_allow_html=True)

    deck = st.session_state.quiz_deck
    total = len(deck)
    qidx = st.session_state.quiz_idx % total
    current = deck[qidx]

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f"<div class='stat-box'><div class='stat-num'>{st.session_state.quiz_score}</div><div class='stat-label'>Correct</div></div>", unsafe_allow_html=True)
    with c2:
        st.markdown(f"<div class='stat-box'><div class='stat-num'>{qidx}/{total}</div><div class='stat-label'>Progress</div></div>", unsafe_allow_html=True)
    with c3:
        pct = int(st.session_state.quiz_score / max(qidx,1) * 100)
        st.markdown(f"<div class='stat-box'><div class='stat-num'>{pct}%</div><div class='stat-label'>Accuracy</div></div>", unsafe_allow_html=True)

    st.progress(qidx / total)

    color = SUBJECT_COLORS.get(current["subject"], "badge-blue")
    st.markdown(f"""
    <span class='badge {color}'>{current['subject']}</span>
    <div class='quiz-q'>{current['q']}</div>
    """, unsafe_allow_html=True)

    if not st.session_state.quiz_answered:
        cols = st.columns(2)
        for i, opt in enumerate(current["opts"]):
            with cols[i % 2]:
                if st.button(opt, key=f"q_{opt}_{qidx}", use_container_width=True):
                    st.session_state.quiz_selected = opt
                    st.session_state.quiz_answered = True
                    correct = opt == current["ans"]
                    if correct:
                        st.session_state.quiz_score += 1
                    st.session_state.quiz_history.append({
                        "subject": current["subject"],
                        "correct": 1 if correct else 0,
                        "total": 1
                    })
                    # Integration: if wrong, add flashcard review task
                    if not correct:
                        related = [c for c in ALL_FLASHCARDS if c["subject"] == current["subject"]]
                        if related:
                            add_task(f"Review {current['subject']} flashcards — quiz mistake", "Review", source="system")
                            add_notification(f"Task: review {current['subject']} cards after quiz mistake")
                    st.rerun()
    else:
        cols = st.columns(2)
        for i, opt in enumerate(current["opts"]):
            with cols[i % 2]:
                if opt == current["ans"]:
                    st.success(f"✅ {opt}")
                elif opt == st.session_state.quiz_selected:
                    st.error(f"❌ {opt}")
                else:
                    st.markdown(f"<div style='padding:8px 0;color:rgba(200,216,232,0.3);'>{opt}</div>", unsafe_allow_html=True)

        if st.session_state.quiz_selected == current["ans"]:
            st.markdown("<div class='notif'>🎯 Correct!</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div style='background:rgba(255,80,80,0.06);border:1px solid rgba(255,80,80,0.2);border-radius:8px;padding:10px 14px;font-size:12px;color:#ff8080;margin:8px 0;'>✗ Correct answer: <strong>{current['ans']}</strong></div>", unsafe_allow_html=True)
            if st.session_state.quiz_selected != current["ans"]:
                st.markdown("<div class='integration-note'>⚡ Review task added for this subject.</div>", unsafe_allow_html=True)

        if st.button("Next Question →", use_container_width=True):
            st.session_state.quiz_idx += 1
            st.session_state.quiz_answered = False
            st.session_state.quiz_selected = None
            st.rerun()

    st.markdown("---")
    if st.button("🔄 Reset Quiz"):
        deck = QUIZ_QUESTIONS.copy()
        random.shuffle(deck)
        st.session_state.quiz_deck = deck
        st.session_state.quiz_idx = 0
        st.session_state.quiz_score = 0
        st.session_state.quiz_answered = False
        st.session_state.quiz_selected = None
        st.rerun()

# ================================================================
#  PAGE: TASKS
# ================================================================

elif page == "✅ Tasks":
    st.markdown("""
    <div class='page-header'>
        <div class='page-title'>Tasks</div>
        <div class='page-subtitle'>Study goals · deadlines · auto-generated reviews</div>
    </div>
    """, unsafe_allow_html=True)

    with st.form("add_task_form"):
        c1, c2, c3 = st.columns([3,1,1])
        with c1:
            new_task = st.text_input("New task", placeholder="What needs doing?", label_visibility="collapsed")
        with c2:
            tag = st.selectbox("Tag", ["Study","Review","Deadline","Personal"], label_visibility="collapsed")
        with c3:
            submitted = st.form_submit_button("+ Add", use_container_width=True)
        if submitted and new_task.strip():
            add_task(new_task.strip(), tag)
            add_notification(f"Task added: {new_task.strip()}")
            st.rerun()

    filter_tag = st.radio("Filter", ["All","Study","Review","Deadline","Personal","Done"], horizontal=True)

    pending = [t for t in st.session_state.tasks if not t["done"]]
    done_list = [t for t in st.session_state.tasks if t["done"]]

    def show_tasks(task_list, show_done=False):
        for i, task in enumerate(task_list):
            if filter_tag != "All" and filter_tag != "Done" and task["tag"] != filter_tag:
                continue
            if filter_tag == "Done" and not task["done"]:
                continue

            tag_color = {"Study":"badge-blue","Review":"badge-green","Deadline":"badge-red","Personal":"badge-gold"}.get(task["tag"],"badge-blue")
            src_note = " · auto" if task.get("source") == "system" else ""
            accent = "card-accent-green" if task["done"] else {"Study":"card-accent-blue","Review":"card-accent-green","Deadline":"card-accent-pink","Personal":"card-accent-gold"}.get(task["tag"],"card-accent-blue")

            c1, c2 = st.columns([5,1])
            with c1:
                done = st.checkbox(
                    f"{'~~' if task['done'] else ''}{task['title']}{'~~' if task['done'] else ''}",
                    value=task["done"],
                    key=f"task_cb_{task['id']}"
                )
                if done != task["done"]:
                    st.session_state.tasks[st.session_state.tasks.index(task)]["done"] = done
                    if done:
                        add_notification(f"Task completed: {task['title'][:30]}")
                    st.rerun()
            with c2:
                if st.button("🗑", key=f"del_{task['id']}"):
                    st.session_state.tasks = [t for t in st.session_state.tasks if t["id"] != task["id"]]
                    st.rerun()

    if filter_tag == "Done":
        show_tasks(done_list, show_done=True)
        if not done_list:
            st.markdown("<div style='color:rgba(200,216,232,0.3);font-size:13px;'>No completed tasks yet.</div>", unsafe_allow_html=True)
    else:
        show_tasks(pending)
        if not pending:
            st.markdown("<div class='notif'>✓ All tasks done. Add something new.</div>", unsafe_allow_html=True)

    if st.session_state.tasks:
        total = len(st.session_state.tasks)
        done_count = sum(1 for t in st.session_state.tasks if t["done"])
        pct = done_count / total
        st.markdown(f"""
        <div style='margin-top:20px;'>
            <div class='prog-wrap'><div class='prog-fill' style='width:{pct*100:.0f}%'></div></div>
            <div style='font-size:11px;color:rgba(200,216,232,0.35);'>{done_count}/{total} tasks complete</div>
        </div>
        """, unsafe_allow_html=True)

# ================================================================
#  PAGE: ALARMS
# ================================================================

elif page == "⏰ Alarms":
    st.markdown("""
    <div class='page-header'>
        <div class='page-title'>Alarms</div>
        <div class='page-subtitle'>Study sessions · deadlines · reminders</div>
    </div>
    """, unsafe_allow_html=True)

    # Firing alarms
    for alarm in st.session_state.alarms:
        if alarm["done"]:
            continue
        try:
            alarm_time = datetime.strptime(alarm["time"], "%Y-%m-%d %H:%M")
            alarm_id = f"alarm_{alarm['subject']}_{alarm['time']}"
            if now >= alarm_time and alarm_id in st.session_state.triggered:
                st.markdown(f"<div class='alarm-fire'>🚨 <strong style='color:#ff5050;'>{alarm['subject'].upper()}</strong> — DUE NOW</div>", unsafe_allow_html=True)
                sound_alarm()
        except Exception:
            pass

    with st.form("alarm_form"):
        c1, c2, c3 = st.columns([2,1,1])
        with c1:
            subject = st.text_input("Alarm label", placeholder="e.g. Study Biology · Wake up · Math deadline")
        with c2:
            date = st.text_input("Date (YYYY-MM-DD)", placeholder="2025-06-01")
        with c3:
            time_inp = st.text_input("Time (HH:MM)", placeholder="07:30")

        also_add_task = st.checkbox("Also add to Tasks", value=True)
        submitted = st.form_submit_button("⏰ Set Alarm")

    if submitted:
        try:
            datetime.strptime(f"{date} {time_inp}", "%Y-%m-%d %H:%M")
            if subject.strip():
                st.session_state.alarms.append({
                    "subject": subject.strip(),
                    "time": f"{date} {time_inp}",
                    "done": False
                })
                # Integration: add task too
                if also_add_task:
                    add_task(f"{subject.strip()} — {date} {time_inp}", "Deadline", source="system", alarm_time=f"{date} {time_inp}")
                    st.markdown("<div class='integration-note'>⚡ Task also added to your task list.</div>", unsafe_allow_html=True)
                add_notification(f"Alarm set: {subject.strip()} at {time_inp}")
                st.success(f"✅ Alarm set — {subject.strip()} at {date} {time_inp}")
            else:
                st.error("Enter a label for the alarm.")
        except Exception:
            st.error("Invalid format. Date: YYYY-MM-DD · Time: HH:MM (24hr)")

    st.markdown("---")
    active_alarms = [a for a in st.session_state.alarms if not a["done"]]
    done_alarms = [a for a in st.session_state.alarms if a["done"]]

    st.markdown(f"<div class='section-label'>Active ({len(active_alarms)})</div>", unsafe_allow_html=True)
    if not active_alarms:
        st.markdown("<div style='color:rgba(200,216,232,0.3);font-size:13px;'>No active alarms.</div>", unsafe_allow_html=True)

    for idx, alarm in enumerate(st.session_state.alarms):
        if alarm["done"]:
            continue
        try:
            alarm_time = datetime.strptime(alarm["time"], "%Y-%m-%d %H:%M")
            diff = alarm_time - now
            total_mins = int(diff.total_seconds() / 60)
            if total_mins < 0:
                time_label = "OVERDUE"
                badge_class = "badge-red"
            elif total_mins < 60:
                time_label = f"in {total_mins}m"
                badge_class = "badge-gold"
            else:
                time_label = f"in {total_mins//60}h {total_mins%60}m"
                badge_class = "badge-green"
        except Exception:
            time_label = "—"
            badge_class = "badge-blue"

        c1, c2 = st.columns([5,1])
        with c1:
            st.markdown(f"""
            <div class='card card-accent-gold'>
                <span class='badge {badge_class}'>{time_label}</span>
                <div class='card-title' style='margin-top:6px;'>{alarm["subject"]}</div>
                <div class='card-meta'>⏰ {alarm["time"]}</div>
            </div>
            """, unsafe_allow_html=True)
        with c2:
            if st.button("✓ Done", key=f"adone_{idx}"):
                st.session_state.alarms[idx]["done"] = True
                add_notification(f"Alarm dismissed: {alarm['subject']}")
                st.rerun()

# ================================================================
#  PAGE: NOTES
# ================================================================

elif page == "📝 Notes":
    st.markdown("""
    <div class='page-header'>
        <div class='page-title'>Notes</div>
        <div class='page-subtitle'>Write anything · download anytime</div>
    </div>
    """, unsafe_allow_html=True)

    notes = st.text_area("", value=st.session_state.notes, height=480,
        placeholder="Formulas, summaries, things to remember, random thoughts...",
        label_visibility="collapsed")
    st.session_state.notes = notes

    c1, c2, c3 = st.columns([1,1,3])
    with c1:
        st.download_button("💾 Download",
            data=notes,
            file_name=f"fenet_notes_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
            mime="text/plain", use_container_width=True)
    with c2:
        if st.button("🗑 Clear", use_container_width=True):
            st.session_state.notes = ""
            st.rerun()

    word_count = len(notes.split()) if notes.strip() else 0
    st.caption(f"{word_count} words · {len(notes)} characters")

# ================================================================
#  AUTO REFRESH
# ================================================================

time.sleep(30)
st.rerun()
