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

# ---------------- CHECKLIST (CARD STYLE) ----------------
def render_card(day_label, tasks):
    with st.container():
        st.markdown(f"### 📅 {day_label}")
        st.markdown("---")

        for key, text, link in tasks:
            k = f"{day_label}_{key}"

            if k not in st.session_state.progress:
                st.session_state.progress[k] = False

            col1, col2 = st.columns([0.8, 0.2])

            with col1:
                val = st.checkbox(text, value=st.session_state.progress[k], key=k)
                st.session_state.progress[k] = val

            with col2:
                if link:
                    st.markdown(f"[🔗]({link})")

        st.markdown("\n")
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

# ---------------- DATA ----------------
AZ900 = [
    ("1", "Cloud Concepts (IaaS/PaaS/SaaS)", "https://learn.microsoft.com/en-us/training/modules/principles-cloud-computing/"),
    ("2", "Cloud benefits", "https://learn.microsoft.com/en-us/training/modules/describe-benefits-use-cloud-services/"),
    ("3", "Azure architecture basics", "https://learn.microsoft.com/en-us/training/modules/azure-architecture-fundamentals/"),
    ("4", "Pricing + SLA", "https://learn.microsoft.com/en-us/training/modules/azure-pricing-sla-lifecycle/"),
    ("5", "Identity basics", "https://learn.microsoft.com/en-us/training/modules/describe-azure-active-directory/"),
]

PYTHON = [
    ("1", "Automate the Boring Stuff", "https://automatetheboringstuff.com/"),
    ("2", "Python practice", "https://www.w3schools.com/python/"),
    ("3", "Build script", ""),
    ("4", "API script", ""),
    ("5", "Push to GitHub", "https://github.com"),
]

DEVOPS = [
    ("1", "Docker basics", "https://docs.docker.com/get-started/"),
    ("2", "Git workflow", "https://www.atlassian.com/git/tutorials"),
    ("3", "Build container", ""),
    ("4", "Run container", ""),
    ("5", "Deploy project", "https://github.com"),
]

AZ104 = [
    ("1", "Identity & RBAC", "https://learn.microsoft.com/en-us/training/paths/az-104-manage-identities-governance/"),
    ("2", "VMs", "https://learn.microsoft.com/en-us/training/modules/azure-virtual-machines/"),
    ("3", "Storage", "https://learn.microsoft.com/en-us/training/modules/azure-storage-fundamentals/"),
    ("4", "Networking", "https://learn.microsoft.com/en-us/training/modules/introduction-to-azure-virtual-networking/"),
    ("5", "Monitoring", "https://learn.microsoft.com/en-us/training/modules/monitor-azure-resources/"),
]

# ---------------- UI ----------------
st.title("🚀 IT Career Planner – CARD VIEW")

view = st.sidebar.selectbox("View", ["Next Task", "Daily Cards", "Progress"])

# ---------------- NEXT TASK ----------------
if view == "Next Task":
    task = next_task()
    st.success(task if task else "ALL DONE 🚀")

# ---------------- DAILY CARDS ----------------
elif view == "Daily Cards":
    day = st.selectbox("Select Day", list(range(1, 61)))

    if day <= 14:
        render_card(f"Day {day} – AZ-900", AZ900)

    elif day <= 28:
        tasks = PYTHON.copy()
        if day % 2 == 0:
            tasks.append(("extra", "Mini automation project", ""))
        render_card(f"Day {day} – Python", tasks)

    elif day <= 42:
        tasks = DEVOPS.copy()
        if day % 3 == 0:
            tasks.append(("lab", "Docker lab", ""))
        render_card(f"Day {day} – DevOps", tasks)

    else:
        tasks = AZ104.copy()
        if day % 2 == 0:
            tasks.append(("project", "Azure full setup project", ""))
        render_card(f"Day {day} – AZ-104", tasks)

# ---------------- PROGRESS ----------------
elif view == "Progress":
    p = progress()
    st.progress(p)
    st.write(f"{round(p*100)}% complete")

st.sidebar.info("Card UI enabled – cleaner daily view 🧠")
