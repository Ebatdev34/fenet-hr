# FENET BADASS – Homework Reminder Bot  (FINAL SINGLE FILE)
# 🔥 Neon UI  |  Custom ring-tone picker  |  Instant play
# ⚡ One file – drop-in replacement

import streamlit as st
from datetime import datetime
import time, pathlib, base64, io
import requests
from pydub import AudioSegment
from pydub.playback import play

# ---------- Wikipedia helper ----------
WIKI_API = "https://en.wikipedia.org/api/rest_v1/page/summary/{}"
def ask_fenet_ai(query: str) -> str:
    query = query.strip()
    if not query:
        return "Ask me anything—homework, history, science … I’ll check Wikipedia."
    try:
        resp = requests.get(WIKI_API.format(requests.utils.quote(query)), timeout=6)
        if resp.status_code == 200:
            return resp.json().get("extract", "Wikipedia had nothing on that.")
        elif resp.status_code == 404:
            return f"Wikipedia doesn’t have a page for “{query}”."
        else:
            return f"Wikipedia answered with HTTP {resp.status_code}."
    except Exception as e:
        return f"Network hiccup: {e}"

# ---------- AUDIO PLAYER ----------
def play_audio_bytes(data: bytes):
    seg = AudioSegment.from_file(io.BytesIO(data))
    play(seg)

# ---------- NEON CSS ----------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&display=swap');
:root{ --neon-pink:#ff1ac6; --neon-cyan:#00ffd6; --neon-purple:#7a00ff; }
html, body, .stApp{background:#050010;color:#e6f7ff;font-family:'Orbitron',monospace;}
.fenet-title{font-size:56px;font-weight:900;text-align:center;
 background:linear-gradient(90deg,var(--neon-cyan),var(--neon-pink));
 -webkit-background-clip:text;background-clip:text;color:transparent;}
.fenet-card{background:linear-gradient(135deg,rgba(10,10,12,0.75),rgba(20,8,30,0.55));
 border-radius:14px;padding:18px;margin-bottom:14px;border:1px solid rgba(255,255,255,0.04);
 color:#e6f7ff;transition:transform .18s ease;}
.fenet-card:hover{transform:translateY(-6px);}
.alarm{color:#ff6b6b;font-weight:900;font-size:20px;}
.stButton > button{background:linear-gradient(90deg,var(--neon-pink),var(--neon-cyan));
 color:#0b0f12;border:none;border-radius:10px;padding:8px 16px;}
</style>
""", unsafe_allow_html=True)

# ---------- SESSION ----------
if "alarms" not in st.session_state: st.session_state.alarms = []
if "chat" not in st.session_state:   st.session_state.chat = []

# ---------- HEADER ----------
st.markdown("<div class='fenet-title'>FENET</div>", unsafe_allow_html=True)
st.markdown("<div class='fenet-sub'>Your homework. Your rules. No excuses.</div>", unsafe_allow_html=True)

# ---------- ADD ALARM ----------
st.subheader("⚡ Arm a Homework Alarm")
subject = st.text_input("📘 Subject")
col1, col2 = st.columns(2)
with col1: date = st.text_input("📅 Date (YYYY-MM-DD)")
with col2: time_in = st.text_input("⏰ Time (HH:MM)")
audio_file = st.file_uploader("🔊 Pick ring-tone (mp3/wav/ogg/m4a/flac)", type=["mp3","wav","ogg","m4a","flac"])
ring_name = audio_file.name if audio_file else "default beep"

if st.button("🔥 SET ALARM"):
    if subject and date and time_in:
        st.session_state.alarms.append({
            "subject": subject, "time": f"{date} {time_in}", "done": False,
            "ring": audio_file.getvalue() if audio_file else None
        })
        st.success(f"Alarm armed for {date} {time_in}  –  ring: {ring_name}")
st.divider()

# ---------- ACTIVE ALARMS ----------
st.subheader("📌 Armed Homework")
now = datetime.now().strftime("%Y-%m-%d %H:%M")
for idx, alarm in enumerate(st.session_state.alarms):
    if alarm["done"]: continue
    card_html = f"<div class='fenet-card'>📘 <b>{alarm['subject']}</b><br>⏰ {alarm['time']}<br>🔊 {ring_name}</div>"
    if now == alarm["time"]:
        card_html = f"<div class='fenet-card alarm'>⏰ {alarm['subject']} IS DUE NOW!</div>"
        st.balloons()
        if alarm["ring"]: play_audio_bytes(alarm["ring"])
        else: st.warning("🔊  (default beep)")
    st.markdown(card_html, unsafe_allow_html=True)
    if st.button("Mark Done ✅", key=f"done_{idx}"):
        st.session_state.alarms[idx]["done"] = True
st.divider()

# ---------- CHAT ----------
st.subheader("🧠 Ask FENET")
user_msg = st.text_input("Ask FENET about homework, deadlines, or studying")
if st.button("Send 🧠") and user_msg:
    st.session_state.chat.append(("You", user_msg))
    with st.spinner("FENET is thinking..."):
        time.sleep(0.8)
        reply = ask_fenet_ai(user_msg)
    st.session_state.chat.append(("FENET", reply))
for role, msg in st.session_state.chat[-6:]:
    st.markdown(f"**{'🧍 You' if role=='You' else '🤖 FENET'}:** {msg}")

st.caption("⚠️ Keep this tab open—FENET watches the clock.")