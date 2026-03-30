import streamlit as st
import json
import os
from datetime import date

st.set_page_config(page_title="IT Career Planner – Weekly Focus", layout="wide")

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

# ---------------- DATA ----------------
WEEK_PLAN = {
    "Monday": [
        ("learn", "AZ-900 Cloud Concepts", "https://learn.microsoft.com/en-us/training/modules/principles-cloud-computing/"),
        ("practice", "Azure Portal exploration", "https://portal.azure.com"),
        ("notes", "Write summary", "")
    ],
    "Tuesday": [
        ("learn", "AZ-900 Cloud Benefits", "https://learn.microsoft.com/en-us/training/modules/describe-benefits-use-cloud-services/"),
        ("video", "Azure fundamentals video", "https://www.youtube.com/results?search_query=az-900+john+savill"),
        ("practice", "Quiz + notes", "")
    ],
    "Wednesday": [
        ("learn", "Python basics", "https://www.w3schools.com/python/"),
        ("code", "Write automation script", ""),
        ("practice", "Loops + functions", "")
    ],
    "Thursday": [
        ("learn", "Git basics", "https://www.atlassian.com/git/tutorials"),
        ("practice", "Push to GitHub", "https://github.com"),
        ("project", "Portfolio repo init", "")
    ],
    "Friday": [
        ("learn", "Docker intro", "https://docs.docker.com/get-started/"),
        ("practice", "Build container", ""),
        ("lab", "Run environment", "")
    ],
    "Saturday": [
        ("project", "Mini project build", ""),
        ("review", "Fix gaps", ""),
        ("notes", "Document learnings", "")
    ],
    "Sunday": [
        ("review", "Weekly review", ""),
        ("plan", "Plan next week", ""),
        ("rest", "Light study / rest", "")
    ]
}

# ---------------- CHECKLIST ----------------
def render_day(day, tasks):
    st.markdown(f"## 📅 {day}")

    for key, text, link in tasks:
        k = f"{day}_{key}"

        if k not in st.session_state.progress:
            st.session_state.progress[k] = False

        col1, col2 = st.columns([0.85, 0.15])

        with col1:
            val = st.checkbox(text, value=st.session_state.progress[k], key=k)
            st.session_state.progress[k] = val

        with col2:
            if link:
                st.markdown(f"[🔗]({link})")

    save_progress()

# ---------------- NEXT TASK ----------------
def next_task():
    for k, v in st.session_state.progress.items():
        if not v:
            return k
    return None

# ---------------- PROGRESS ----------------
def progress():
    total = len(st.session_state.progress)
    done = sum(1 for v in st.session_state.progress.values() if v)
    return done / total if total else 0

# ---------------- UI (NO DROPDOWNS, NO NAVIGATION) ----------------
st.title("🚀 Weekly IT Career Planner")
st.caption("Focus mode: one system, one plan, no distractions.")

# TODAY (always visible)
today_name = date.today().strftime("%A")
st.markdown("---")
st.subheader(f"📍 Today: {today_name}")

if today_name in WEEK_PLAN:
    render_day(today_name, WEEK_PLAN[today_name])
else:
    st.info("No plan for today")

st.markdown("---")

# FULL WEEK (always visible, no collapse)
st.subheader("📆 This Week")

for day, tasks in WEEK_PLAN.items():
    render_day(day, tasks)
    st.markdown("---")

# PROGRESS (always visible)
st.subheader("📊 Progress")
p = progress()
st.progress(p)
st.write(f"{round(p*100)}% complete")

# RESET (bottom only)
st.markdown("---")
st.button("🔄 Reset Progress")

st.sidebar.info("No dropdowns. Full focus weekly system 🧠")
