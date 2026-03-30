import streamlit as st
import json
import os

st.set_page_config(page_title="IT Study Planner ELITE", layout="wide")

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
if st.sidebar.button("🔄 Reset Progress"):
    st.session_state.progress = {}
    if os.path.exists(DATA_FILE):
        os.remove(DATA_FILE)

# ---------------- CHECKLIST ----------------
def checklist(day, tasks):
    st.subheader(day)
    for key, text, link in tasks:
        k = f"{day}_{key}"
        if k not in st.session_state.progress:
            st.session_state.progress[k] = False
        col1, col2 = st.columns([0.7, 0.3])
        with col1:
            val = st.checkbox(text, value=st.session_state.progress[k])
            st.session_state.progress[k] = val
        with col2:
            if link:
                st.markdown(f"[Open]({link})")
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

# ---------------- UI ----------------
st.title("🚀 IT Career Planner – ELITE 60 DAYS")

view = st.sidebar.selectbox("View", ["Next Task", "Daily", "Progress"])

# ---------------- NEXT ----------------
if view == "Next Task":
    task = next_task()
    st.success(task if task else "All done 🚀")

# ---------------- DAILY ----------------
elif view == "Daily":
    day = st.selectbox("Day", list(range(1, 61)))

    # -------- AZURE AZ-900 (Day 1–14) --------
    if day <= 14:
        checklist(f"Day {day} - AZ-900", [
            ("1", "Microsoft Learn AZ-900 module", "https://learn.microsoft.com/en-us/training/paths/azure-fundamentals/"),
            ("2", "Watch John Savill AZ-900", "https://www.youtube.com/results?search_query=az-900+john+savill"),
            ("3", "Use Azure Portal", "https://portal.azure.com"),
            ("4", "Take notes + summarize", ""),
            ("5", "Repeat + lab", "https://portal.azure.com"),
        ])

    # -------- PYTHON (15–28) --------
    elif day <= 28:
        checklist(f"Day {day} - Python", [
            ("1", "Automate the Boring Stuff", "https://automatetheboringstuff.com/"),
            ("2", "W3Schools Python practice", "https://www.w3schools.com/python/"),
            ("3", "Build script (logs/API)", ""),
            ("4", "Improve script", ""),
            ("5", "Push to GitHub", "https://github.com"),
        ])

    # -------- DOCKER/GIT (29–42) --------
    elif day <= 42:
        checklist(f"Day {day} - DevOps", [
            ("1", "Docker course", "https://www.udemy.com/course/docker-kubernetes-the-practical-guide/"),
            ("2", "Git crash course", "https://www.youtube.com/results?search_query=git+github+crash+course"),
            ("3", "Build container", ""),
            ("4", "Push repo", "https://github.com"),
            ("5", "Deploy locally", ""),
        ])

    # -------- AZ-104 (43–60) --------
    else:
        checklist(f"Day {day} - AZ-104", [
            ("1", "AZ-104 Learn path", "https://learn.microsoft.com/en-us/training/paths/az-104-administrator-prerequisites/"),
            ("2", "Azure lab work", "https://portal.azure.com"),
            ("3", "Build full project", ""),
            ("4", "Monitor/logging", ""),
            ("5", "Document in GitHub", "https://github.com"),
        ])

# ---------------- PROGRESS ----------------
elif view == "Progress":
    p = progress()
    st.progress(p)
    st.write(f"{round(p*100)}% complete")

st.sidebar.info("Elite mode activated 🔥")
