import streamlit as st
import json
import os

st.set_page_config(page_title="IT Study Planner", layout="wide")

DATA_FILE = "progress.json"
PASSWORD = "changeme"  # change this

# --------- AUTH ---------
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.title("🔐 Login")
    pwd = st.text_input("Enter password", type="password")
    if st.button("Login"):
        if pwd == PASSWORD:
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("Wrong password")
    st.stop()

# --------- LOAD / SAVE ---------
def load_progress():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {}

def save_progress():
    with open(DATA_FILE, "w") as f:
        json.dump(st.session_state.progress, f)

# --------- STATE INIT ---------
if "progress" not in st.session_state:
    st.session_state.progress = load_progress()

# --------- RESET ---------
def reset_progress():
    st.session_state.progress = {}
    if os.path.exists(DATA_FILE):
        os.remove(DATA_FILE)

st.sidebar.markdown("---")
if st.sidebar.button("🔄 Reset all progress"):
    reset_progress()
    st.sidebar.success("Progress reset!")

# --------- CHECKLIST ---------
def checklist(section, items):
    st.subheader(section)
    for key, label, link in items:
        full_key = f"{section}_{key}"
        if full_key not in st.session_state.progress:
            st.session_state.progress[full_key] = False
        col1, col2 = st.columns([0.7, 0.3])
        with col1:
            new_val = st.checkbox(label, value=st.session_state.progress[full_key])
            st.session_state.progress[full_key] = new_val
        with col2:
            if link:
                st.markdown(f"[Open]({link})")
    save_progress()

# --------- NEXT TASK ---------
def next_task():
    for key, done in st.session_state.progress.items():
        if not done:
            return key
    return None

# --------- PROGRESS ---------
def calc_progress():
    total = len(st.session_state.progress)
    done = sum(1 for v in st.session_state.progress.values() if v)
    return (done / total) if total > 0 else 0

st.title("🚀 IT Career Study Planner")

view = st.sidebar.selectbox(
    "Choose view",
    ["Next Task", "Daily", "Weekly", "Progress"]
)

# ---------------- NEXT TASK ----------------
if view == "Next Task":
    st.header("🎯 Next Task")
    task = next_task()
    if task:
        st.success(f"Your next task: {task}")
    else:
        st.success("All tasks completed! 🚀")

# ---------------- DAILY ----------------
elif view == "Daily":
    st.header("📅 Daily Plan")
    day = st.selectbox("Select Day", ["Day 1", "Day 2", "Day 3"])

    if day == "Day 1":
        checklist("Day 1 - Azure Intro", [
            ("d1_1", "Create Azure account", "https://portal.azure.com"),
            ("d1_2", "Watch AZ-900 intro", "https://www.youtube.com/results?search_query=az-900+john+savill"),
            ("d1_3", "Read Cloud Concepts", "https://learn.microsoft.com/en-us/training/paths/azure-fundamentals/"),
        ])

    elif day == "Day 2":
        checklist("Day 2 - Compute", [
            ("d2_1", "Learn VMs", "https://learn.microsoft.com"),
            ("d2_2", "Create VM", "https://portal.azure.com"),
            ("d2_3", "Connect to VM", ""),
        ])

    elif day == "Day 3":
        checklist("Day 3 - Storage", [
            ("d3_1", "Learn Storage", "https://learn.microsoft.com"),
            ("d3_2", "Upload file", "https://portal.azure.com"),
        ])

# ---------------- WEEKLY ----------------
elif view == "Weekly":
    st.header("🗓 Weekly Plan")

    checklist("Week 1", [
        ("w1_1", "Cloud basics", "https://learn.microsoft.com"),
        ("w1_2", "Create VM", "https://portal.azure.com"),
    ])

# ---------------- PROGRESS ----------------
elif view == "Progress":
    st.header("📊 Progress")
    progress = calc_progress()
    st.progress(progress)
    st.write(f"{round(progress*100)}% complete")

st.sidebar.info("Autosave + Login enabled 🔐")
