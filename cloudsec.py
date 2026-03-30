import streamlit as st

st.set_page_config(page_title="IT Study Planner", layout="wide")

st.title("🚀 IT Career Study Planner (Detailed)")

# --------- STATE INIT ---------
if "progress" not in st.session_state:
    st.session_state.progress = {}

# Helper to render checklist items with persistence
def checklist(section, items):
    st.subheader(section)
    for key, label in items:
        full_key = f"{section}_{key}"
        if full_key not in st.session_state.progress:
            st.session_state.progress[full_key] = False
        st.session_state.progress[full_key] = st.checkbox(label, value=st.session_state.progress[full_key])

# Progress calculation
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

    # Example detailed structure for first 14 days (Azure)
    if day == "Day 1":
        checklist("Day 1 - Azure Intro", [
            ("d1_1", "Create Azure account"),
            ("d1_2", "Watch AZ-900 intro video (1–2h)"),
            ("d1_3", "Read Microsoft Learn: Cloud Concepts"),
            ("d1_4", "Explore Azure Portal"),
            ("d1_5", "Write notes (important concepts)")
        ])

    elif day == "Day 2":
        checklist("Day 2 - Compute", [
            ("d2_1", "Learn Virtual Machines"),
            ("d2_2", "Create VM in Azure"),
            ("d2_3", "Connect via SSH/RDP"),
            ("d2_4", "Understand pricing basics"),
            ("d2_5", "Document what you did")
        ])

    elif day == "Day 3":
        checklist("Day 3 - Storage", [
            ("d3_1", "Learn Blob Storage"),
            ("d3_2", "Upload files"),
            ("d3_3", "Test access levels"),
            ("d3_4", "Understand redundancy"),
            ("d3_5", "Take notes")
        ])

    elif day == "Day 4":
        checklist("Day 4 - Databases", [
            ("d4_1", "Learn Azure SQL"),
            ("d4_2", "Create database"),
            ("d4_3", "Connect to DB"),
            ("d4_4", "Run simple query"),
            ("d4_5", "Document process")
        ])

    elif day == "Day 5":
        checklist("Day 5 - Security", [
            ("d5_1", "Learn IAM basics"),
            ("d5_2", "Create users/roles"),
            ("d5_3", "Test permissions"),
            ("d5_4", "Learn MFA"),
            ("d5_5", "Take notes")
        ])

    elif day == "Day 6":
        checklist("Day 6 - Review", [
            ("d6_1", "Review all topics"),
            ("d6_2", "Do practice test"),
            ("d6_3", "Identify weak areas"),
            ("d6_4", "Redo labs"),
            ("d6_5", "Summarize learning")
        ])

    elif day == "Day 7":
        checklist("Day 7 - Light Day", [
            ("d7_1", "Light review"),
            ("d7_2", "Organize notes"),
            ("d7_3", "Watch recap video"),
            ("d7_4", "Plan next week"),
            ("d7_5", "Rest")
        ])

    elif day == "Day 15":
        checklist("Day 15 - Python Start", [
            ("d15_1", "Install Python"),
            ("d15_2", "Run first script"),
            ("d15_3", "Variables & loops"),
            ("d15_4", "Practice exercises"),
            ("d15_5", "Take notes")
        ])

    else:
        st.info("Detailed plan coming for this day – continue following weekly/monthly structure.")

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
            ("w1_1", "Understand cloud basics"),
            ("w1_2", "Create VM"),
            ("w1_3", "Setup storage"),
            ("w1_4", "Create database"),
            ("w1_5", "Learn security basics")
        ])

    elif week == "Week 2 - Azure Cert":
        checklist("Week 2", [
            ("w2_1", "Finish AZ-900 course"),
            ("w2_2", "Do practice exams"),
            ("w2_3", "Review weak areas"),
            ("w2_4", "Take AZ-900 exam"),
            ("w2_5", "Document knowledge")
        ])

    elif week == "Week 3 - Python":
        checklist("Week 3", [
            ("w3_1", "Learn basics"),
            ("w3_2", "Work with files"),
            ("w3_3", "Use APIs"),
            ("w3_4", "Build script"),
            ("w3_5", "Improve project")
        ])

    elif week == "Week 4 - Docker & Git":
        checklist("Week 4", [
            ("w4_1", "Learn Git"),
            ("w4_2", "Create GitHub repo"),
            ("w4_3", "Learn Docker"),
            ("w4_4", "Build container"),
            ("w4_5", "Deploy app")
        ])

# ---------------- MONTHLY ----------------
elif view == "Monthly":
    st.header("📆 Monthly Roadmap Checklist")

    checklist("Month 1", [
        ("m1_1", "Complete AZ-900"),
        ("m1_2", "Hands-on Azure labs"),
        ("m1_3", "Understand pricing"),
    ])

    checklist("Month 2", [
        ("m2_1", "Learn Python"),
        ("m2_2", "Build automation scripts"),
        ("m2_3", "Use APIs"),
    ])

    checklist("Month 3", [
        ("m3_1", "Learn Docker"),
        ("m3_2", "Use Git"),
        ("m3_3", "Deploy app"),
    ])

    checklist("Month 4", [
        ("m4_1", "Start AZ-104"),
        ("m4_2", "Advanced Azure networking"),
        ("m4_3", "Monitoring & security"),
    ])

# ---------------- PROGRESS ----------------
elif view == "Progress":
    st.header("📊 Your Progress")

    progress = calc_progress()
    st.progress(progress)
    st.write(f"{round(progress*100)}% complete")

    st.write("Keep going — consistency wins 🚀")

st.sidebar.markdown("---")
st.sidebar.info("Your personal IT bootcamp 💻")
