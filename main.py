# FENET BADASS – Homework Reminder Bot (Streamlit)
# 🔥 Offline, browser-based, dark & slick UI with sci-fi background
# ⚡ Features: multiple alarms, mark done, neon cards, auto-refresh, emojis, deadlines

import streamlit as st
from datetime import datetime
import time

st.set_page_config(page_title="FENET", page_icon="⏰", layout="centered")

# ======= STYLE =======
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&display=swap');

:root{
  --neon-pink: #ff1ac6;
  --neon-cyan: #00ffd6;
  --neon-purple: #7a00ff;
  --glass: rgba(255,255,255,0.03);
  --card-bg: rgba(8,8,12,0.6);
}

/* Base background: image + animated neon gradient overlay */
html, body, #root, .stApp, [data-testid="stAppViewContainer"], .main, .block-container {
  background-color: #050010 !important;
  background-image:
    radial-gradient(circle at 10% 20%, rgba(122,0,255,0.12), transparent 12%),
    radial-gradient(circle at 90% 80%, rgba(255,26,198,0.09), transparent 12%),
    linear-gradient(135deg, rgba(7,8,16,0.6), rgba(2,2,6,0.8));
  background-blend-mode: screen, screen, normal;
  color: var(--text-color, #e6f7ff);
  font-family: 'Orbitron', monospace;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  min-height: 100vh;
  position: relative;
  overflow-x: hidden;
}

/* animated neon wash */
.stApp::before{
  content: "";
  position: absolute;
  inset: 0;
  background: linear-gradient(120deg, rgba(255,26,198,0.12), rgba(0,255,214,0.10), rgba(122,0,255,0.08));
  background-size: 300% 300%;
  mix-blend-mode: screen;
  animation: wash 12s linear infinite;
  pointer-events: none;
  z-index: 0;
}
@keyframes wash {
  0% {background-position: 0% 50%;}
  50% {background-position: 100% 50%;}
  100% {background-position: 0% 50%;}
}

/* subtle scanlines */
.stApp::after{
  content: "";
  position: absolute;
  inset: 0;
  background-image: repeating-linear-gradient(to bottom, rgba(255,255,255,0.01) 0 1px, transparent 1px 6px);
  opacity: 0.06;
  pointer-events: none;
  z-index: 1;
}

/* Make content sit above overlays */
section[data-testid="stAppViewContainer"] > div, .block-container, main {
  position: relative;
  z-index: 2;
}

/* Make blocks transparent and add neon outlines */
[data-testid="stBlock"], .css-18e3th9, .css-1d391kg, .css-145kmo2, section[data-testid="stAppViewContainer"] > div {
  background-color: transparent !important;
  box-shadow: none !important;
}

/* Neon title */
.fenet-title{
  font-size: 56px;
  font-weight: 900;
  text-align: center;
  color: var(--neon-cyan);
  background: linear-gradient(90deg, var(--neon-cyan), var(--neon-pink));
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
  text-shadow: 0 0 12px rgba(0,255,214,0.12), 0 0 40px rgba(122,0,255,0.06);
  letter-spacing: 2px;
  margin-top: 18px;
}

/* Glitched subtitle */
.fenet-sub{
  text-align:center;
  color: rgba(230,247,255,0.9);
  opacity: 0.95;
  margin-bottom: 22px;
  font-size: 14px;
  position: relative;
}
.fenet-sub::after{
  content: "";
  position: absolute;
  left: 50%; top: 50%;
  width: 60%; height: 6px;
  transform: translate(-50%,-40%);
  background: linear-gradient(90deg, transparent, rgba(255,26,198,0.25), transparent);
  border-radius: 4px;
  filter: blur(6px);
}

/* Cards: glass + neon border */
.fenet-card{
  background: linear-gradient(135deg, rgba(10,10,12,0.75), rgba(20,8,30,0.55));
  border-radius: 14px;
  padding: 18px;
  margin-bottom: 14px;
  border: 1px solid rgba(255,255,255,0.04);
  position: relative;
  overflow: hidden;
  color: #e6f7ff;
  transition: transform 0.18s ease, box-shadow 0.18s ease;
}
.fenet-card::before{
  content: "";
  position: absolute;
  inset: -2px;
  background: linear-gradient(120deg, rgba(255,26,198,0.18), rgba(0,255,214,0.12));
  opacity: 0;
  filter: blur(18px);
  transition: opacity 0.25s ease;
  pointer-events: none;
}
.fenet-card:hover::before{ opacity: 1; }
.fenet-card:hover{ transform: translateY(-6px); box-shadow: 0 10px 40px rgba(0,0,0,0.6); }

/* Alarm text */
.alarm{
  color: #ff6b6b;
  font-weight: 900;
  font-size: 20px;
  text-shadow: 0 0 10px rgba(255,107,107,0.2);
}

/* Buttons */
.stButton>button, button[kind]{
  background: linear-gradient(90deg, var(--neon-pink), var(--neon-cyan));
  color: #0b0f12 !important;
  border: none !important;
  padding: 8px 16px !important;
  border-radius: 10px !important;
  box-shadow: 0 6px 20px rgba(0,0,0,0.6), 0 0 22px rgba(255,26,198,0.08);
  transition: transform .12s ease, box-shadow .12s ease;
}
.stButton>button:hover{ transform: translateY(-3px); box-shadow: 0 10px 34px rgba(0,0,0,0.7), 0 0 28px rgba(0,255,214,0.08); }

/* Inputs (simplified) */
input, .stTextInput>div>input, .stTextInput>div>textarea{
  background: rgba(255,255,255,0.02) !important;
  border: 1px solid rgba(255,255,255,0.04) !important;
  color: #e6f7ff !important;
  border-radius: 8px !important;
  padding: 8px 10px !important;
}

/* Small helpers */
.center { text-align: center; }
.small { font-size: 13px; opacity: .85; }

/* Responsive tweaks */
@media (max-width: 600px){
  .fenet-title{ font-size: 36px; }
  .fenet-card{ padding: 14px; }
}
</style>
""", unsafe_allow_html=True)

# ======= SESSION STATE =======
if 'alarms' not in st.session_state:
    st.session_state.alarms = []

# ======= HEADER =======
st.markdown("<div class='fenet-title'>FENET</div>", unsafe_allow_html=True)
st.markdown("<div class='fenet-sub'>Your homework. Your rules. No excuses.</div>", unsafe_allow_html=True)

# ======= ADD ALARM =======
st.subheader("⚡ Arm a Homework Alarm")
subject = st.text_input("📘 Subject")
col1, col2 = st.columns(2)
with col1:
    date = st.text_input("📅 Date (YYYY-MM-DD)")
with col2:
    time_input = st.text_input("⏰ Time (HH:MM)")

if st.button("🔥 SET ALARM"):
    if subject and date and time_input:
        st.session_state.alarms.append({
            "subject": subject,
            "time": f"{date} {time_input}",
            "done": False
        })
        st.success(f"Alarm armed for {date} {time_input}.")

st.divider()

# ======= ACTIVE ALARMS =======
st.subheader("📌 Armed Homework")

now = datetime.now().strftime("%Y-%m-%d %H:%M")
remaining = []

if not st.session_state.alarms:
    st.info("No homework armed. Chill and enjoy ✨")

for idx, alarm in enumerate(st.session_state.alarms):
    if alarm['done']:
        continue
    card_html = f"<div class='fenet-card'>📘 <b>{alarm['subject']}</b><br>⏰ {alarm['time']}</div>"
    if now == alarm['time']:
        card_html = f"<div class='fenet-card alarm'>⏰ {alarm['subject']} IS DUE NOW!</div>"
        st.balloons()
    st.markdown(card_html, unsafe_allow_html=True)
    done_key = f"done_{idx}"
    if st.button("Mark Done ✅", key=done_key):
        st.session_state.alarms[idx]['done'] = True

# ======= FOOTER =======
st.divider()
st.caption("⚠️ Keep this tab open. FENET watches the clock and makes homework fun and pretty good.")

# ======= AUTO REFRESH =======
time.sleep(1)
