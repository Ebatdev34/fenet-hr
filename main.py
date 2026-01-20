# FENET BADASS – Homework Reminder Bot (FINAL)
# 🔥 Real alarms + sound + anti-miss logic
# ⚡ Streamlit | Offline UI | Cyberpunk vibes

import streamlit as st
from datetime import datetime
import time
import requests

WIKI_API = "https://en.wikipedia.org/api/rest_v1/page/summary/{}"

# ================= AI =================
def ask_fenet_ai(query: str) -> str:
    query = query.strip()
    if not query:
        return "Ask me anything—homework, history, science. I got Wikipedia on speed dial."

    try:
        resp = requests.get(
            WIKI_API.format(requests.utils.quote(query)), timeout=6
        )
        if resp.status_code == 200:
            return resp.json().get("extract", "Nothing useful found.")
        elif resp.status_code == 404:
            return f"No Wikipedia page for “{query}”."
        else:
            return f"Wikipedia error {resp.status_code}."
    except Exception as e:
        return f"Network hiccup: {e}"

# ================= SOUND =================
def play_ring():
    with open("ring.mp3", "rb") as f:
        st.audio(f.read(), format="audio/mp3")

# ================= STYLE =================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&display=swap');

html, body, .stApp {
  background-color: #050010 !important;
  color: #e6f7ff;
  font-family: 'Orbitron', monospace;
}

.fenet-title{
  font-size: 56px;
  font-weight: 900;
  text-align: center;
  background: linear-gradient(90deg, #00ffd6, #ff1ac6);
  -webkit-background-clip: text;
  color: transparent;
  margin-top: 20px;
}

.fenet-sub{
  text-align:center;
  opacity: .9;
  font-size: 14px;
  margin-bottom: 20px;
}

.fenet-card{
  background: rgba(15,15,30,.75);
  border-radius: 14px;
  padding: 18px;
  margin-bottom: 14px;
  border: 1px solid rgba(255,255,255,.05);
}

.alarm{
  color: #ff6b6b;
  font-weight: 900;
  font-size: 20px;
}

button {
  background: linear-gradient(90deg, #ff1ac6, #00ffd6) !important;
  color: #000 !important;
  border-radius: 10px !important;
}
</style>
""", unsafe_allow_html=True)

# ================= SESSION STATE =================
if "alarms" not in st.session_state:
    st.session_state.alarms = []

if "triggered" not in st.session_state:
    st.session_state.triggered = set()

if "chat" not in st.session_state:
    st.session_state.chat = []

# ================= HEADER =================
st.markdown("<div class='fenet-title'>FENET</div>", unsafe_allow_html=True)
st.markdown("<div class='fenet-sub'>Your homework. Your rules. No excuses.</div>", unsafe_allow_html=True)

# ================= ADD ALARM =================
st.subheader("⚡ Arm a Homework Alarm")

subject = st.text_input("📘 Subject")
col1, col2 = st.columns(2)

with col1:
    date = st.text_input("📅 Date (YYYY-MM-DD)")
with col2:
    time_input = st.text_input("⏰ Time (HH:MM)")

if st.button("🔥 SET ALARM"):
    try:
        datetime.strptime(f"{date} {time_input}", "%Y-%m-%d %H:%M")
        st.session_state.alarms.append({
            "subject": subject,
            "time": f"{date} {time_input}",
            "done": False
        })
        st.success("Alarm armed.")
    except:
        st.error("Invalid date or time format.")

st.divider()

# ================= ACTIVE ALARMS =================
st.subheader("📌 Armed Homework")

now = datetime.now()

if not st.session_state.alarms:
    st.info("No alarms. You’re free… for now.")

for idx, alarm in enumerate(st.session_state.alarms):
    if alarm["done"]:
        continue

    alarm_time = datetime.strptime(alarm["time"], "%Y-%m-%d %H:%M")
    alarm_id = f"{alarm['subject']}_{alarm['time']}"

    if now >= alarm_time and alarm_id not in st.session_state.triggered:
        st.session_state.triggered.add(alarm_id)
        st.markdown(
            f"<div class='fenet-card alarm'>⏰ {alarm['subject']} IS DUE NOW!</div>",
            unsafe_allow_html=True
        )
        play_ring()
        st.balloons()
    else:
        st.markdown(
            f"<div class='fenet-card'>📘 <b>{alarm['subject']}</b><br>⏰ {alarm['time']}</div>",
            unsafe_allow_html=True
        )

    if st.button("Mark Done ✅", key=f"done_{idx}"):
        st.session_state.alarms[idx]["done"] = True

st.divider()

# ================= CHAT =================
st.subheader("🧠 Ask FENET")

user_msg = st.text_input("Ask about homework, studying, or anything nerdy")

if st.button("Send 🧠") and user_msg:
    st.session_state.chat.append(("You", user_msg))
    with st.spinner("Thinking..."):
        time.sleep(1)
        reply = ask_fenet_ai(user_msg)
    st.session_state.chat.append(("FENET", reply))

for role, msg in st.session_state.chat[-6:]:
    if role == "You":
        st.markdown(f"**🧍 You:** {msg}")
    else:
        st.markdown(f"**🤖 FENET:** {msg}")

# ================= FOOTER =================
st.divider()
st.caption("⚠️ Keep this tab open. FENET doesn’t forget. You do.")

# ================= AUTO REFRESH =================
time.sleep(30)
st.experimental_rerun()
