"""
Streamlit app: Cloud Security Study Planner (Azure + IT Security)
Features:
- Simple login (demo)
- Weekly + daily structured study plan
- Progress tracking saved to JSON
- Links to learning resources
- GitHub-ready structure

Run:
streamlit run app.py
"""

import streamlit as st
import json
import os
from datetime import datetime

DATA_FILE = "progress.json"

# ----------------------
# Demo users (replace with streamlit-authenticator or DB in production)
# ----------------------
USERS = {
    "admin": "admin123",
    "student": "cloud123"
}

# ----------------------
# Study Plan (12 weeks)
# ----------------------
STUDY_PLAN = {
    "Week 1": {
        "title": "IT Security & Cloud Fundamentals",
        "days": {
            "Day 1": "What is cybersecurity? CIA triad",
            "Day 2": "Networking basics (IP, DNS, HTTP/HTTPS)",
            "Day 3": "Cloud basics + shared responsibility model",
            "Day 4": "Introduction to Azure",
            "Day 5": "Azure core services overview",
            "Day 6": "Practice: Azure portal tour",
            "Day 7": "Review + quiz"
        },
        "links": [
            "https://learn.microsoft.com/en-us/training/modules/describe-cloud-computing/",
            "https://learn.microsoft.com/en-us/training/azure/"
        ]
    },
    "Week 2": {
        "title": "Azure Identity & Access",
        "days": {
            "Day 1": "Azure Active Directory basics",
            "Day 2": "Authentication vs Authorization",
            "Day 3": "RBAC roles",
            "Day 4": "MFA & Conditional Access",
            "Day 5": "Identity Protection",
            "Day 6": "Lab: Create users & roles",
            "Day 7": "Review"
        },
        "links": [
            "https://learn.microsoft.com/en-us/training/modules/secure-azure-resources-with-rbac/"
        ]
    },
    "Week 3": {
        "title": "Network Security in Azure",
        "days": {
            "Day 1": "VNets & Subnets",
            "Day 2": "Network Security Groups (NSG)",
            "Day 3": "Azure Firewall",
            "Day 4": "DDoS Protection",
            "Day 5": "Private endpoints",
            "Day 6": "Lab: Secure network setup",
            "Day 7": "Review"
        },
        "links": [
            "https://learn.microsoft.com/en-us/training/modules/secure-network-connectivity-azure/"
        ]
    },
    "Week 4": {
        "title": "Security Monitoring",
        "days": {
            "Day 1": "Microsoft Defender for Cloud",
            "Day 2": "Azure Monitor",
            "Day 3": "Log Analytics",
            "Day 4": "Security alerts",
            "Day 5": "SIEM basics (Sentinel intro)",
            "Day 6": "Lab: Enable monitoring",
            "Day 7": "Review"
        },
        "links": [
            "https://learn.microsoft.com/en-us/azure/defender-for-cloud/"
        ]
    }
}

# ----------------------
# Load/save progress
# ----------------------

def load_progress():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {}


def save_progress(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

# ----------------------
# Login
# ----------------------

def login():
    st.title("Cloud Security Study Planner")
    st.subheader("Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username in USERS and USERS[username] == password:
            st.session_state["user"] = username
            st.success("Logged in!")
        else:
            st.error("Invalid credentials")

# ----------------------
# Dashboard
# ----------------------

def dashboard(user):
    st.title(f"Welcome {user}")
    st.write("Your Cloud Security Learning Path (Azure-focused)")

    progress = load_progress()
    if user not in progress:
        progress[user] = {}

    for week, content in STUDY_PLAN.items():
        st.header(week + " - " + content["title"])

        for day, task in content["days"].items():
            key = f"{week}-{day}"
            checked = progress[user].get(key, False)

            new_val = st.checkbox(f"{day}: {task}", value=checked, key=key)
            progress[user][key] = new_val

        st.subheader("Resources")
        for link in content["links"]:
            st.markdown(f"- {link}")

    if st.button("Save progress"):
        save_progress(progress)
        st.success("Progress saved!")

# ----------------------
# Main
# ----------------------

def main():
    if "user" not in st.session_state:
        login()
    else:
        dashboard(st.session_state["user"])


if __name__ == "__main__":
    main()
