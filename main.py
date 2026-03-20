# ============================================================
#  FENET  — 
#  Streamlit | Cyberpunk UI | Wikipedia + Local Knowledge
#  Features: Q&A · Alarms · Flashcards · Quiz · Notes
# ============================================================

import streamlit as st
from datetime import datetime
import time
import random
import requests

# ============================================================
#  WIKIPEDIA SEARCH
# ============================================================

WIKI_SUMMARY = "https://en.wikipedia.org/api/rest_v1/page/summary/{}"
WIKI_SEARCH  = "https://en.wikipedia.org/w/api.php"

def wiki_search(query: str) -> dict:
    """Search Wikipedia. Returns best result as {title, extract, url}."""
    query = query.strip()
    if not query:
        return {}

    # Step 1: Direct lookup
    try:
        r = requests.get(WIKI_SUMMARY.format(requests.utils.quote(query)), timeout=6)
        if r.status_code == 200:
            d = r.json()
            if d.get("extract"):
                return {
                    "title": d.get("title", ""),
                    "extract": d.get("extract", ""),
                    "url": d.get("content_urls", {}).get("desktop", {}).get("page", "")
                }
    except Exception:
        pass

    # Step 2: Search fallback
    try:
        r = requests.get(WIKI_SEARCH, params={
            "action": "query", "list": "search",
            "srsearch": query, "format": "json", "srlimit": 1
        }, timeout=6)
        if r.status_code == 200:
            results = r.json().get("query", {}).get("search", [])
            if results:
                title = results[0]["title"]
                r2 = requests.get(WIKI_SUMMARY.format(requests.utils.quote(title)), timeout=6)
                if r2.status_code == 200:
                    d = r2.json()
                    return {
                        "title": d.get("title", ""),
                        "extract": d.get("extract", ""),
                        "url": d.get("content_urls", {}).get("desktop", {}).get("page", "")
                    }
    except Exception:
        pass

    return {}


def best_sentences(question: str, extract: str, n: int = 4) -> str:
    """Pull the most relevant sentences from Wikipedia extract."""
    if not extract:
        return ""

    stop = {"what","is","are","the","a","an","of","in","on","at","to","for",
            "how","why","when","where","who","was","were","did","do","does",
            "can","could","would","tell","me","about","explain","define"}
    keywords = set(question.lower().split()) - stop

    sentences = [s.strip() for s in extract.replace("\n", " ").split(".") if s.strip()]
    if not sentences:
        return extract[:600]

    scored = sorted(
        [(sum(1 for kw in keywords if kw in s.lower()), s) for s in sentences],
        reverse=True
    )

    top = [s for score, s in scored[:n] if score > 0]
    return (". ".join(top) + ".") if top else (". ".join(sentences[:3]) + ".")

# ============================================================
#  LOCAL KNOWLEDGE BASE (instant offline fallback)
# ============================================================

LOCAL = {
    # MATH
    "addition": "Addition combines numbers to get a total. Example: 3 + 4 = 7. The result is called the sum.",
    "subtraction": "Subtraction takes one number away from another. Example: 9 − 4 = 5.",
    "multiplication": "Multiplication is repeated addition. 3 × 4 = 12. The result is the product.",
    "division": "Division splits into equal parts. 12 ÷ 4 = 3. The result is the quotient.",
    "fraction": "A fraction is part of a whole. 3/4 means 3 out of 4 equal parts. Top = numerator. Bottom = denominator.",
    "percentage": "Percentage is out of 100. 75% = 75/100 = 0.75. To find 20% of 50: 50 × 0.20 = 10.",
    "prime number": "A prime is only divisible by 1 and itself. Primes: 2, 3, 5, 7, 11, 13, 17, 19...",
    "area": "Area = space inside a 2D shape. Rectangle: l×w. Triangle: ½×b×h. Circle: πr².",
    "perimeter": "Perimeter = total distance around a shape. Rectangle: 2(l+w).",
    "volume": "Volume = space inside a 3D shape. Cuboid: l×w×h. Cylinder: πr²h.",
    "algebra": "Algebra uses letters for unknowns. Solve x + 5 = 12 → x = 7. Keep both sides balanced.",
    "pythagoras": "In a right triangle: a² + b² = c² where c is the hypotenuse. Example: 3²+4²=5².",
    "mean": "Mean = sum of values ÷ count. Example: (4+8+6) ÷ 3 = 6.",
    "median": "Median = middle value when sorted. Example: 2,5,7,9,11 → median = 7.",
    "mode": "Mode = most frequent value. Example: 2,4,4,5,7 → mode = 4.",
    "probability": "Probability = favorable ÷ total outcomes. Coin heads = 1/2 = 50%.",
    "pi": "π ≈ 3.14159. Circumference = 2πr. Area = πr². Goes on forever without repeating.",
    "ratio": "Ratio compares quantities. 2:3 means for every 2 of one there are 3 of another.",
    "angle": "Right angle = 90°. Straight = 180°. Full turn = 360°. Triangle angles sum to 180°.",
    "density": "Density = mass ÷ volume. Objects less dense than water float; more dense sink.",
    # BIOLOGY
    "cell": "Cell is the basic unit of life. Has nucleus (control), membrane (boundary), cytoplasm. Plant cells also have cell wall and chloroplasts.",
    "photosynthesis": "Plants use sunlight + CO₂ + H₂O → glucose + O₂. Equation: 6CO₂+6H₂O+light→C₆H₁₂O₆+6O₂. Happens in chloroplasts.",
    "respiration": "Aerobic: glucose+O₂→CO₂+H₂O+energy. Anaerobic (no oxygen): glucose→lactic acid+energy.",
    "dna": "DNA carries genetic instructions in a double helix. Base pairs: A-T and C-G. Found in nucleus. Controls traits.",
    "evolution": "Species change over generations via natural selection. Better-adapted organisms survive and reproduce more.",
    "food chain": "Energy flow: Producer→Primary consumer→Secondary→Tertiary. Example: grass→rabbit→fox→eagle.",
    "osmosis": "Water moves through semi-permeable membrane from low to high solute concentration. Passive — no energy needed.",
    "diffusion": "Particles move from high to low concentration until even. Passive transport, no energy needed.",
    "enzyme": "Biological catalysts that speed up reactions without being used up. Lock-and-key specificity.",
    "mitosis": "Cell division producing 2 identical daughter cells. Used for growth and repair.",
    # PHYSICS
    "gravity": "Force of attraction between masses. g = 9.8 m/s² on Earth. Weight = mass × gravity.",
    "force": "Push or pull measured in Newtons. F = ma. Balanced forces = no movement. Unbalanced = acceleration.",
    "friction": "Force opposing motion between surfaces. Produces heat. Static friction > kinetic friction.",
    "kinetic energy": "Energy of motion. KE = ½mv². Double speed = 4× kinetic energy.",
    "potential energy": "Stored energy. GPE = mgh. Higher position = more potential energy.",
    "speed": "Speed = distance ÷ time. Scalar (no direction). Measured in m/s or km/h.",
    "velocity": "Velocity = displacement ÷ time. Like speed but with direction. Vector quantity.",
    "acceleration": "Acceleration = (v−u) ÷ t. Change in velocity over time. Measured in m/s².",
    "newton's laws": "1st: Objects stay still/moving unless force acts. 2nd: F=ma. 3rd: Every action has equal opposite reaction.",
    "wave": "Waves transfer energy without transferring matter. Transverse (light) or longitudinal (sound).",
    "light": "Electromagnetic radiation at 3×10⁸ m/s. Can reflect, refract, diffract. White light = full spectrum.",
    "sound": "Longitudinal wave needing a medium. Speed ≈ 340 m/s in air. Frequency = pitch. Amplitude = volume.",
    "electricity": "V = IR (Ohm's law). Current in Amps, Voltage in Volts, Resistance in Ohms.",
    "atom": "Protons(+) and neutrons in nucleus. Electrons(−) in shells. Atomic number = protons.",
    "pressure": "Pressure = force ÷ area. Measured in Pascals.",
    # CHEMISTRY
    "acid": "pH < 7. Produces H⁺ ions. Examples: HCl, H₂SO₄, citric acid. Turns litmus red. Tastes sour.",
    "base": "pH > 7. Produces OH⁻ ions. Examples: NaOH, ammonia, baking soda. Turns litmus blue.",
    "ph": "Scale 0−14. Below 7 = acidic. 7 = neutral. Above 7 = alkaline. Each unit = 10× concentration change.",
    "neutralisation": "Acid + Base → Salt + Water. HCl + NaOH → NaCl + H₂O. pH moves toward 7.",
    "periodic table": "Elements organized by atomic number. Groups (columns) = similar properties. Periods (rows) = electron shells.",
    "states of matter": "Solid: fixed shape/volume. Liquid: fixed volume, takes shape. Gas: fills container. Plasma: ionized gas.",
    "combustion": "Fuel + O₂ → CO₂ + H₂O + energy. Complete needs enough oxygen. Incomplete makes CO.",
    "molecule": "Two or more atoms bonded. H₂O = 2H+O. CO₂ = C+2O. NaCl = Na+Cl.",
}

def find_answer_local(question: str) -> str:
    q = question.lower().strip().rstrip("?")
    for prefix in ["what is","what are","explain","define","tell me about","what's","how does","describe"]:
        if q.startswith(prefix):
            q = q[len(prefix):].strip()
            break
    if q in LOCAL:
        return LOCAL[q]
    stop = {"what","is","are","the","a","an","of","in","to","for","how","why","when","who","was"}
    keywords = set(q.split()) - stop
    best_key, best_score = None, 0
    for key in LOCAL:
        score = len(keywords & set(key.split()))
        if score > best_score:
            best_score, best_key = score, key
    if best_score >= 1 and best_key:
        return LOCAL[best_key]
    return ""

# ============================================================
#  MAIN Q&A: Wikipedia first, local fallback
# ============================================================

def ask_fenet(question: str, use_internet: bool) -> dict:
    if use_internet:
        result = wiki_search(question)
        if result and result.get("extract"):
            answer = best_sentences(question, result["extract"])
            return {"answer": answer, "source": "wikipedia", "title": result["title"], "url": result["url"]}

    # Local fallback
    local_ans = find_answer_local(question)
    if local_ans:
        return {"answer": local_ans, "source": "local", "title": "", "url": ""}

    if use_internet:
        return {"answer": f"Couldn't find anything for '{question}'. Try rephrasing.", "source": "none", "title": "", "url": ""}
    else:
        return {
            "answer": f"Not in local knowledge base. Try topics like: photosynthesis, gravity, fractions, DNA, acid, pythagoras, electricity...",
            "source": "none", "title": "", "url": ""
        }

# ============================================================
#  FLASHCARDS & QUIZ
# ============================================================

FLASHCARDS = [
    ("What is photosynthesis?", "Plants use sunlight + CO₂ + H₂O → glucose + O₂. Happens in chloroplasts."),
    ("What is Newton's 2nd law?", "F = ma. Force = mass × acceleration."),
    ("What is osmosis?", "Water through semi-permeable membrane from low to high solute concentration."),
    ("What is pH of pure water?", "7 — neutral."),
    ("Products of aerobic respiration?", "CO₂ + water + energy (ATP)."),
    ("Formula for speed?", "Speed = distance ÷ time."),
    ("Formula for kinetic energy?", "KE = ½mv²"),
    ("Pythagoras theorem?", "a² + b² = c² in a right-angled triangle."),
    ("What is the mean?", "Sum of all values ÷ number of values."),
    ("What is mitosis?", "Cell division → 2 identical daughter cells for growth and repair."),
    ("What is atomic number?", "The number of protons in the nucleus of an atom."),
    ("Formula for density?", "Density = mass ÷ volume."),
    ("What is natural selection?", "Better-adapted organisms survive, reproduce, and pass traits on."),
    ("What is Ohm's law?", "V = IR. Voltage = Current × Resistance."),
    ("Acids vs Bases?", "Acids pH < 7 (H⁺ ions). Bases pH > 7 (OH⁻ ions)."),
    ("What is an enzyme?", "Biological catalyst — speeds up reactions, not used up. Lock-and-key model."),
    ("Formula for gravitational PE?", "GPE = mgh (mass × gravity × height)."),
    ("What are prime numbers?", "Numbers > 1 divisible only by 1 and themselves. E.g. 2,3,5,7,11..."),
    ("3 states of matter?", "Solid (fixed shape), Liquid (fixed volume), Gas (fills container)."),
    ("What is diffusion?", "Particles move from high to low concentration. Passive — no energy needed."),
]

QUIZ = [
    {"q": "7 × 8 = ?", "opts": ["54","56","63","48"], "ans": "56"},
    {"q": "Gas produced in photosynthesis?", "opts": ["CO₂","Nitrogen","Oxygen","Hydrogen"], "ans": "Oxygen"},
    {"q": "Area of a circle formula?", "opts": ["2πr","πr²","πd","2πr²"], "ans": "πr²"},
    {"q": "Unit of force?", "opts": ["Joule","Watt","Newton","Pascal"], "ans": "Newton"},
    {"q": "Human chromosomes count?", "opts": ["23","46","48","32"], "ans": "46"},
    {"q": "pH 7 means?", "opts": ["Acidic","Alkaline","Neutral","Corrosive"], "ans": "Neutral"},
    {"q": "Speed = ?", "opts": ["distance×time","distance÷time","time÷distance","force÷mass"], "ans": "distance÷time"},
    {"q": "Photosynthesis happens in?", "opts": ["Nucleus","Mitochondria","Ribosome","Chloroplast"], "ans": "Chloroplast"},
    {"q": "15% of 200?", "opts": ["25","30","35","20"], "ans": "30"},
    {"q": "Powerhouse of the cell?", "opts": ["Nucleus","Chloroplast","Mitochondria","Ribosome"], "ans": "Mitochondria"},
    {"q": "Speed of light?", "opts": ["3×10⁶ m/s","3×10⁸ m/s","3×10¹⁰ m/s","3×10⁴ m/s"], "ans": "3×10⁸ m/s"},
    {"q": "Acid + Base →?", "opts": ["Gas+Water","Salt+Water","Salt+Gas","Oxide+Water"], "ans": "Salt+Water"},
    {"q": "Median of 2,3,5,7,9?", "opts": ["3","5","7","9"], "ans": "5"},
    {"q": "Newton's 2nd law?", "opts": ["1st law","2nd law: F=ma","3rd law","Ohm's law"], "ans": "2nd law: F=ma"},
    {"q": "Kinetic energy formula?", "opts": ["mgh","½mv²","mv","Fd"], "ans": "½mv²"},
]

# ============================================================
#  SOUND
# ============================================================

def play_ring():
    try:
        with open("ring.mp3", "rb") as f:
            st.audio(f.read(), format="audio/mp3")
    except Exception:
        st.warning("🔔 ALARM! (ring.mp3 missing)")

# ============================================================
#  STYLE
# ============================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Share+Tech+Mono&display=swap');

html, body, .stApp {
    background-color: #03000f !important;
    color: #e0f0ff;
    font-family: 'Share Tech Mono', monospace;
}
.fenet-title {
    font-size: 62px; font-weight: 900; text-align: center;
    font-family: 'Orbitron', monospace;
    background: linear-gradient(90deg, #00ffd6, #7b2fff, #ff1ac6);
    -webkit-background-clip: text; color: transparent;
    margin-top: 10px; letter-spacing: 8px;
}
.fenet-sub {
    text-align: center; color: #00ffd6; font-size: 12px;
    margin-bottom: 28px; letter-spacing: 3px; opacity: 0.6;
}
.fenet-card {
    background: rgba(10,0,30,0.8); border-radius: 12px;
    padding: 16px 20px; margin-bottom: 12px;
    border: 1px solid rgba(0,255,214,0.15);
}
.alarm-card {
    background: rgba(255,30,30,0.1); border: 1px solid #ff4444;
    border-radius: 12px; padding: 16px 20px; margin-bottom: 12px;
    color: #ff6b6b; font-weight: 900; font-size: 18px;
    box-shadow: 0 0 20px rgba(255,68,68,0.3);
}
.answer-box {
    background: rgba(0,255,214,0.04); border-left: 3px solid #00ffd6;
    border-radius: 0 10px 10px 0; padding: 16px; margin-top: 10px;
    line-height: 1.9; font-size: 14px;
}
.wiki-source { font-size: 11px; opacity: 0.4; margin-top: 8px; }
.you-msg {
    background: rgba(123,47,255,0.08); border-left: 3px solid #7b2fff;
    border-radius: 0 10px 10px 0; padding: 12px; margin-bottom: 8px;
}
.flash-card {
    background: rgba(10,0,40,0.9); border: 1px solid rgba(123,47,255,0.4);
    border-radius: 16px; padding: 40px; text-align: center;
    min-height: 160px; font-size: 18px;
    box-shadow: 0 0 30px rgba(123,47,255,0.15);
}
.score-badge {
    background: linear-gradient(90deg,#00ffd6,#7b2fff);
    color: #000; border-radius: 20px; padding: 4px 16px;
    font-weight: 900; font-size: 13px; display: inline-block;
}
section[data-testid="stSidebar"] {
    background: rgba(5,0,20,0.95) !important;
    border-right: 1px solid rgba(0,255,214,0.1);
}
</style>
""", unsafe_allow_html=True)

# ============================================================
#  SESSION STATE
# ============================================================

defaults = {
    "alarms": [], "triggered": set(), "chat": [],
    "flash_idx": 0, "flash_show": False, "flash_deck": None,
    "quiz_idx": 0, "quiz_score": 0, "quiz_answered": False, "quiz_selected": None,
    "notes": "",
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

if st.session_state.flash_deck is None:
    deck = FLASHCARDS.copy()
    random.shuffle(deck)
    st.session_state.flash_deck = deck

# ============================================================
#  HEADER
# ============================================================

st.markdown("<div class='fenet-title'>FENET</div>", unsafe_allow_html=True)
st.markdown("<div class='fenet-sub'>STUDY SYSTEM · HOMEWORK TRACKER · KNOWLEDGE ENGINE</div>", unsafe_allow_html=True)

# ============================================================
#  SIDEBAR
# ============================================================

page = st.sidebar.selectbox("NAVIGATE", [
    "🧠 Ask FENET", "⚡ Alarms", "🃏 Flashcards", "❓ Quiz", "📝 Notes"
], label_visibility="collapsed")

st.sidebar.markdown("---")
use_internet = st.sidebar.toggle("🌐 Wikipedia Search", value=True,
    help="ON = search Wikipedia first, fallback to local. OFF = local knowledge only.")
if use_internet:
    st.sidebar.caption("🟢 Internet mode — Wikipedia + local fallback")
else:
    st.sidebar.caption("🔴 Offline mode — local knowledge only")

st.sidebar.markdown("---")
st.sidebar.markdown(f"📚 **{len(LOCAL)}** local topics")
st.sidebar.markdown(f"🃏 **{len(FLASHCARDS)}** flashcards")
st.sidebar.markdown(f"❓ **{len(QUIZ)}** quiz questions")

# ============================================================
#  PAGE: ASK FENET
# ============================================================

if page == "🧠 Ask FENET":
    st.subheader("🧠 Ask FENET")
    mode_label = "Wikipedia + local" if use_internet else "Local knowledge only"
    st.caption(f"Mode: {mode_label} · Toggle in sidebar")

    user_msg = st.text_input(
        "Question",
        placeholder="e.g. What is photosynthesis? What is gravity? What is algebra?",
        label_visibility="collapsed"
    )

    col1, col2 = st.columns([1, 4])
    with col1:
        send = st.button("ASK →", use_container_width=True)
    with col2:
        if st.button("Clear", use_container_width=False):
            st.session_state.chat = []
            st.rerun()

    if send and user_msg.strip():
        st.session_state.chat.append(("You", user_msg))
        with st.spinner("Searching..." if use_internet else "Thinking..."):
            result = ask_fenet(user_msg, use_internet)
        st.session_state.chat.append(("FENET", result))

    for role, msg in reversed(st.session_state.chat[-10:]):
        if role == "You":
            st.markdown(f"<div class='you-msg'>🧍 <b>You:</b> {msg}</div>", unsafe_allow_html=True)
        else:
            answer = msg["answer"]
            source = msg.get("source", "")
            url = msg.get("url", "")
            title = msg.get("title", "")

            source_line = ""
            if source == "wikipedia" and url:
                source_line = f"<div class='wiki-source'>📖 Wikipedia: <a href='{url}' target='_blank'>{title}</a></div>"
            elif source == "local":
                source_line = "<div class='wiki-source'>📚 Local knowledge base</div>"

            st.markdown(
                f"<div class='answer-box'>🤖 <b>FENET:</b><br><br>{answer}{source_line}</div>",
                unsafe_allow_html=True
            )

# ============================================================
#  PAGE: ALARMS
# ============================================================

elif page == "⚡ Alarms":
    st.subheader("⚡ Homework Alarms")

    with st.form("alarm_form"):
        subject = st.text_input("Subject", placeholder="e.g. Math homework, Biology essay")
        c1, c2 = st.columns(2)
        with c1:
            date = st.text_input("Date (YYYY-MM-DD)")
        with c2:
            t_inp = st.text_input("Time (HH:MM)")
        if st.form_submit_button("🔥 SET ALARM"):
            try:
                datetime.strptime(f"{date} {t_inp}", "%Y-%m-%d %H:%M")
                if subject.strip():
                    st.session_state.alarms.append({"subject": subject.strip(), "time": f"{date} {t_inp}", "done": False})
                    st.success(f"✅ Alarm set — {subject} at {date} {t_inp}")
                else:
                    st.error("Enter a subject name.")
            except Exception:
                st.error("Invalid format. Date: YYYY-MM-DD · Time: HH:MM")

    st.markdown("---")
    now = datetime.now()
    active = [a for a in st.session_state.alarms if not a["done"]]
    if not active:
        st.info("No active alarms.")

    for idx, alarm in enumerate(st.session_state.alarms):
        if alarm["done"]:
            continue
        alarm_time = datetime.strptime(alarm["time"], "%Y-%m-%d %H:%M")
        alarm_id = f"{alarm['subject']}_{alarm['time']}"
        overdue = now >= alarm_time

        if overdue and alarm_id not in st.session_state.triggered:
            st.session_state.triggered.add(alarm_id)
            st.markdown(f"<div class='alarm-card'>🚨 {alarm['subject'].upper()} IS DUE NOW!</div>", unsafe_allow_html=True)
            play_ring()
            st.balloons()
        else:
            diff = alarm_time - now
            mins = max(0, int(diff.total_seconds() // 60))
            label = "OVERDUE" if overdue else f"{mins} min left"
            c1, c2 = st.columns([4, 1])
            with c1:
                st.markdown(f"<div class='fenet-card'>📘 <b>{alarm['subject']}</b><br><small>⏰ {alarm['time']} · {label}</small></div>", unsafe_allow_html=True)
            with c2:
                if st.button("✅", key=f"done_{idx}"):
                    st.session_state.alarms[idx]["done"] = True
                    st.rerun()

# ============================================================
#  PAGE: FLASHCARDS
# ============================================================

elif page == "🃏 Flashcards":
    st.subheader("🃏 Flashcards")
    deck = st.session_state.flash_deck
    idx = st.session_state.flash_idx % len(deck)
    question, answer = deck[idx]

    st.progress((idx + 1) / len(deck))
    st.caption(f"Card {idx + 1} of {len(deck)}")

    content = ("❓ " + question) if not st.session_state.flash_show else ("✅ " + answer)
    st.markdown(f"<div class='flash-card'>{content}</div>", unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("👁 Reveal / Hide", use_container_width=True):
            st.session_state.flash_show = not st.session_state.flash_show
            st.rerun()
    with c2:
        if st.button("⏭ Next", use_container_width=True):
            st.session_state.flash_idx += 1
            st.session_state.flash_show = False
            st.rerun()
    with c3:
        if st.button("🔀 Shuffle", use_container_width=True):
            random.shuffle(st.session_state.flash_deck)
            st.session_state.flash_idx = 0
            st.session_state.flash_show = False
            st.rerun()

    if st.session_state.flash_show:
        st.markdown(f"<div class='answer-box'>{answer}</div>", unsafe_allow_html=True)

# ============================================================
#  PAGE: QUIZ
# ============================================================

elif page == "❓ Quiz":
    st.subheader("❓ Quiz Mode")
    total = len(QUIZ)
    qidx = st.session_state.quiz_idx % total
    current = QUIZ[qidx]

    st.markdown(f"<span class='score-badge'>Score: {st.session_state.quiz_score} / {total}</span>", unsafe_allow_html=True)
    st.markdown(f"**Question {qidx + 1} of {total}**")
    st.progress(qidx / total)
    st.markdown(f"### {current['q']}")

    if not st.session_state.quiz_answered:
        for opt in current["opts"]:
            if st.button(opt, key=f"opt_{opt}_{qidx}", use_container_width=True):
                st.session_state.quiz_selected = opt
                st.session_state.quiz_answered = True
                if opt == current["ans"]:
                    st.session_state.quiz_score += 1
                st.rerun()
    else:
        for opt in current["opts"]:
            if opt == current["ans"]:
                st.success(f"✅ {opt}")
            elif opt == st.session_state.quiz_selected:
                st.error(f"❌ {opt}")
            else:
                st.write(f"   {opt}")

        if st.session_state.quiz_selected == current["ans"]:
            st.markdown("### 🎯 Correct!")
            st.balloons()
        else:
            st.markdown(f"### ❌ Correct answer: **{current['ans']}**")

        if st.button("Next →", use_container_width=True):
            st.session_state.quiz_idx += 1
            st.session_state.quiz_answered = False
            st.session_state.quiz_selected = None
            st.rerun()

    st.markdown("---")
    if st.button("🔄 Reset Quiz"):
        st.session_state.quiz_idx = 0
        st.session_state.quiz_score = 0
        st.session_state.quiz_answered = False
        st.session_state.quiz_selected = None
        st.rerun()

# ============================================================
#  PAGE: NOTES
# ============================================================

elif page == "📝 Notes":
    st.subheader("📝 Study Notes")
    notes = st.text_area("Notes", value=st.session_state.notes, height=420,
        placeholder="Write formulas, reminders, things to review...",
        label_visibility="collapsed")
    st.session_state.notes = notes

    c1, c2 = st.columns(2)
    with c1:
        st.download_button("💾 Download", data=notes,
            file_name=f"fenet_notes_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
            mime="text/plain", use_container_width=True)
    with c2:
        if st.button("🗑 Clear", use_container_width=True):
            st.session_state.notes = ""
            st.rerun()

# ============================================================
#  FOOTER
# ============================================================

st.markdown("---")
st.caption("⚡ FENET — built by Eba for his sister · no excuses")

time.sleep(30)
st.rerun()
