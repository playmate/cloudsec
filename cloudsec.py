import streamlit as st
import json
import os

st.set_page_config(page_title="IT Study Planner", layout="wide")

st.title("🚀 IT Career Study Planner (Detailed)")

DATA_FILE = "progress.json"

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
    for key, label in items:
        full_key = f"{section}_{key}"
        if full_key not in st.session_state.progress:
            st.session_state.progress[full_key] = False
        new_val = st.checkbox(label, value=st.session_state.progress[full_key])
        st.session_state.progress[full_key] = new_val
    save_progress()

# --------- PROGRESS ---------
def calc_progress():
    total = len(st.session_state.progress)
    done = sum(1 for v in st.session_state.progress.values() if v)
    return (done / total) if total > 0 else 0

view = st.sidebar.selectbox(
    "Choose view",
    ["Daily (Day-by-Day)", "Weekly", "Monthly", "Progress"]
)

# ---------------- DAILY ----------------
if view == "Daily (Day-by-Day)":
    st.header("📅 Detailed Daily Plan")

    day = st.selectbox("Select Day", [f"Day {i}" for i in range(1, 29)])

    if day == "Day 1":
        checklist("Day 1 - Azure Intro", [
            ("d1_1", "Create Azure account"),
            ("d1_2", "Watch AZ-900 intro video (1–2h)"),
            ("d1_3", "Read Microsoft Learn: Cloud Concepts"),
            ("d1_4", "Explore Azure Portal"),
            ("d1_5", "Write notes")
        ])

    elif day == "Day 2":
        checklist("Day 2 - Compute", [
            ("d2_1", "Learn Virtual Machines"),
            ("d2_2", "Create VM"),
            ("d2_3", "Connect to VM"),
            ("d2_4", "Understand pricing"),
            ("d2_5", "Document work")
        ])

    elif day == "Day 3":
        checklist("Day 3 - Storage", [
            ("d3_1", "Learn Blob Storage"),
            ("d3_2", "Upload files"),
            ("d3_3", "Test access"),
            ("d3_4", "Understand redundancy"),
            ("d3_5", "Take notes")
        ])

    elif day == "Day 4":
        checklist("Day 4 - Databases", [
            ("d4_1", "Learn Azure SQL"),
            ("d4_2", "Create DB"),
            ("d4_3", "Connect"),
            ("d4_4", "Run query"),
            ("d4_5", "Document")
        ])

    elif day == "Day 5":
        checklist("Day 5 - Security", [
            ("d5_1", "Learn IAM"),
            ("d5_2", "Create roles"),
            ("d5_3", "Test permissions"),
            ("d5_4", "Learn MFA"),
            ("d5_5", "Notes")
        ])

    else:
        st.info("More detailed days coming — follow weekly view for now.")

# ---------------- WEEKLY ----------------
elif view == "Weekly":
    st.header("🗓 Weekly Checklist")

    week = st.selectbox("Select Week", [
        "Week 1 - Azure Basics",
        "Week 2 - Azure Cert",
        "Week 3 - Python",
        "Week 4 - Docker & Git"
    ])

    if week == "Week 1 - Azure Basics":
        checklist("Week 1", [
            ("w1_1", "Cloud basics"),
            ("w1_2", "Create VM"),
            ("w1_3", "Storage"),
            ("w1_4", "Database"),
            ("w1_5", "Security")
        ])

    elif week == "Week 2 - Azure Cert":
        checklist("Week 2", [
            ("w2_1", "Finish AZ-900"),
            ("w2_2", "Practice exams"),
            ("w2_3", "Review"),
            ("w2_4", "Take exam"),
            ("w2_5", "Document")
        ])

# ---------------- MONTHLY ----------------
elif view == "Monthly":
    st.header("📆 Monthly Checklist")

    checklist("Month 1", [
        ("m1_1", "AZ-900"),
        ("m1_2", "Labs"),
        ("m1_3", "Pricing")
    ])

# ---------------- PROGRESS ----------------
elif view == "Progress":
    st.header("📊 Progress")

    progress = calc_progress()
    st.progress(progress)
    st.write(f"{round(progress*100)}% complete")

st.sidebar.info("Autosave enabled ✅")
