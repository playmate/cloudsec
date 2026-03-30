import streamlit as st
import json
import os

st.set_page_config(page_title="IT Career Planner – MAX ELITE", layout="wide")

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

        col1, col2 = st.columns([0.75, 0.25])

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

# ---------------- CURRICULUM ----------------

AZ900 = [
    ("1", "Cloud Concepts (IaaS/PaaS/SaaS)", "https://learn.microsoft.com/en-us/training/modules/principles-cloud-computing/"),
    ("2", "Cloud benefits (scalability, elasticity)", "https://learn.microsoft.com/en-us/training/modules/describe-benefits-use-cloud-services/"),
    ("3", "Azure architecture basics", "https://learn.microsoft.com/en-us/training/modules/azure-architecture-fundamentals/"),
    ("4", "Pricing + SLA", "https://learn.microsoft.com/en-us/training/modules/azure-pricing-sla-lifecycle/"),
    ("5", "Identity (Entra ID basics)", "https://learn.microsoft.com/en-us/training/modules/describe-azure-active-directory/"),
]

PYTHON = [
    ("1", "Automate the Boring Stuff (core chapters)", "https://automatetheboringstuff.com/"),
    ("2", "Python loops + functions practice", "https://www.w3schools.com/python/"),
    ("3", "File automation script", ""),
    ("4", "API request script", ""),
    ("5", "Push project to GitHub", "https://github.com"),
]

DEVOPS = [
    ("1", "Docker fundamentals", "https://docs.docker.com/get-started/"),
    ("2", "Git workflow (branching)", "https://www.atlassian.com/git/tutorials"),
    ("3", "Build Docker image", ""),
    ("4", "Run container locally", ""),
    ("5", "Push DevOps project", "https://github.com"),
]

AZ104 = [
    ("1", "Identity & RBAC", "https://learn.microsoft.com/en-us/training/paths/az-104-manage-identities-governance/"),
    ("2", "Virtual machines deep dive", "https://learn.microsoft.com/en-us/training/modules/azure-virtual-machines/"),
    ("3", "Storage accounts", "https://learn.microsoft.com/en-us/training/modules/azure-storage-fundamentals/"),
    ("4", "Virtual networking", "https://learn.microsoft.com/en-us/training/modules/introduction-to-azure-virtual-networking/"),
    ("5", "Monitoring & logging", "https://learn.microsoft.com/en-us/training/modules/monitor-azure-resources/"),
]

# ---------------- UI ----------------
st.title("🚀 IT Career Planner – MAX ELITE 60 DAYS")

view = st.sidebar.selectbox("View", ["Next Task", "Daily", "Progress"])

# ---------------- NEXT TASK ----------------
if view == "Next Task":
    task = next_task()
    st.success(task if task else "ALL DONE 🚀")

# ---------------- DAILY ENGINE ----------------
elif view == "Daily":
    day = st.selectbox("Day", list(range(1, 61)))

    # AZ-900 (1–14)
    if day <= 14:
        tasks = AZ900 + [
            ("lab", "Azure Portal hands-on lab", "https://portal.azure.com")
        ]
        checklist(f"Day {day} – AZ-900", tasks)

    # Python (15–28)
    elif day <= 28:
        tasks = PYTHON.copy()
        if day % 2 == 0:
            tasks.append(("extra", "Mini automation project", ""))
        checklist(f"Day {day} – Python Automation", tasks)

    # DevOps (29–42)
    elif day <= 42:
        tasks = DEVOPS.copy()
        if day % 3 == 0:
            tasks.append(("lab", "Docker hands-on lab", ""))
        checklist(f"Day {day} – DevOps", tasks)

    # AZ-104 (43–60)
    else:
        tasks = AZ104.copy()
        if day % 2 == 0:
            tasks.append(("project", "Build full Azure environment project", ""))
        checklist(f"Day {day} – AZ-104", tasks)

# ---------------- PROGRESS ----------------
elif view == "Progress":
    p = progress()
    st.progress(p)
    st.write(f"{round(p*100)}% complete")

st.sidebar.info("MAX ELITE MODE ACTIVE 🔥")
