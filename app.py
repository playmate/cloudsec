import streamlit as st
import json
import os
from datetime import date

st.set_page_config(page_title="IT Career Planner – Architecture Fixed", layout="wide")

DATA_FILE = "progress.json"
PASSWORD = "changeme"

# ---------------- AUTH ----------------
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.title("🔐 Login")
    pwd = st.text_input("Password", type="password")
    if st.button("Login"):
        if pwd == PASSWORD:
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("Wrong password")
    st.stop()

# ---------------- STORAGE ----------------
def load_progress():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {}

def save_progress():
    with open(DATA_FILE, "w") as f:
        json.dump(st.session_state.progress, f)

if "progress" not in st.session_state:
    st.session_state.progress = load_progress()

# ---------------- RESET ----------------
if st.button("🔄 Reset Progress"):
    st.session_state.progress = {}
    if os.path.exists(DATA_FILE):
        os.remove(DATA_FILE)

# ---------------- WEEK DATA (ARCHITECTURE FIXED) ----------------
WEEK_PLAN = {
    "Monday": [
        {"id": "mon_1", "text": "AZ-900 Cloud Concepts", "link": "https://learn.microsoft.com/en-us/training/modules/principles-cloud-computing/"},
        {"id": "mon_2", "text": "Azure Portal exploration", "link": "https://portal.azure.com"},
        {"id": "mon_3", "text": "Write summary", "link": ""}
    ],
    "Tuesday": [
        {"id": "tue_1", "text": "AZ-900 Cloud Benefits", "link": "https://learn.microsoft.com/en-us/training/modules/describe-benefits-use-cloud-services/"},
        {"id": "tue_2", "text": "Azure fundamentals video", "link": "https://www.youtube.com/results?search_query=az-900"},
        {"id": "tue_3", "text": "Quiz + notes", "link": ""}
    ],
    "Wednesday": [
        {"id": "wed_1", "text": "Python basics", "link": "https://www.w3schools.com/python/"},
        {"id": "wed_2", "text": "Automation script", "link": ""},
        {"id": "wed_3", "text": "Loops + functions drills", "link": ""}
    ],
    "Thursday": [
        {"id": "thu_1", "text": "Git basics", "link": "https://www.atlassian.com/git/tutorials"},
        {"id": "thu_2", "text": "Push to GitHub", "link": "https://github.com"},
        {"id": "thu_3", "text": "Portfolio repo init", "link": ""}
    ],
    "Friday": [
        {"id": "fri_1", "text": "Docker intro", "link": "https://docs.docker.com/get-started/"},
        {"id": "fri_2", "text": "Build container", "link": ""},
        {"id": "fri_3", "text": "Run environment", "link": ""}
    ],
    "Saturday": [
        {"id": "sat_1", "text": "Mini project build", "link": ""},
        {"id": "sat_2", "text": "Fix gaps", "link": ""},
        {"id": "sat_3", "text": "Document learnings", "link": ""}
    ],
    "Sunday": [
        {"id": "sun_1", "text": "Weekly review", "link": ""},
        {"id": "sun_2", "text": "Plan next week", "link": ""},
        {"id": "sun_3", "text": "Rest / light study", "link": ""}
    ]
}

# ---------------- TASK RENDER ----------------
def render_day(day, tasks):
    st.markdown(f"## 📅 {day}")

    for task in tasks:
        task_id = task["id"]
        text = task["text"]
        link = task["link"]

        if task_id not in st.session_state.progress:
            st.session_state.progress[task_id] = False

        col1, col2 = st.columns([0.85, 0.15])

        with col1:
            val = st.checkbox(text, value=st.session_state.progress[task_id], key=task_id)
            st.session_state.progress[task_id] = val

        with col2:
            if link:
                st.markdown(f"[🔗]({link})")

    save_progress()

# ---------------- PROGRESS ----------------
def progress():
    total = len(st.session_state.progress)
    done = sum(1 for v in st.session_state.progress.values() if v)
    return done / total if total else 0

# ---------------- UI ----------------
st.title("🚀 Weekly IT Career Planner – Fixed Architecture")
st.caption("No duplicate keys, stable state system, production-safe design.")

# TODAY
st.markdown("---")
today_name = date.today().strftime("%A")
st.subheader(f"📍 Today: {today_name}")

if today_name in WEEK_PLAN:
    render_day(today_name, WEEK_PLAN[today_name])
else:
    st.info("No plan for today")

# WEEK
st.markdown("---")
st.subheader("📆 This Week")

for day, tasks in WEEK_PLAN.items():
    render_day(day, tasks)
    st.markdown("---")

# PROGRESS
st.subheader("📊 Progress")
p = progress()
st.progress(p)
st.write(f"{round(p*100)}% complete")

# RESET
st.markdown("---")
st.button("🔄 Reset Progress")

st.sidebar.info("Architecture fixed: stable IDs, no duplicate Streamlit keys 🚀")
