import streamlit as st
import json
import os
from datetime import datetime

# File path for saving data
DATA_FILE = "streamlit_combined_data.json"

# Load data from file
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as file:
            try:
                data = json.load(file)
                # Ensure correct structure
                if not isinstance(data, dict):
                    return {"tasks": [], "completed": []}
                return {
                    "tasks": data.get("tasks", []),
                    "completed": data.get("completed", []),
                }
            except json.JSONDecodeError:
                return {"tasks": [], "completed": []}
    return {"tasks": [], "completed": []}

# Save data to file
def save_data(data):
    with open(DATA_FILE, "w") as file:
        json.dump(data, file)

# Initialize data
data = load_data()

# Custom CSS for a mobile-friendly design
st.markdown(
    """
    <style>
        .stApp {
            max-width: 600px;
            margin: auto;
        }
        h1, h2, h3 {
            text-align: center;
        }
        .task-box {
            padding: 10px;
            margin: 10px 0;
            border: 1px solid #ddd;
            border-radius: 5px;
            background-color: #f9f9f9;
        }
        .task-name {
            font-size: 1.2rem;
            font-weight: bold;
        }
        .task-meta {
            font-size: 0.9rem;
            color: #888;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Title
st.title("📋 Task & Learning Tracker")

# Sidebar for task addition
with st.sidebar:
    st.header("Add New Task")
    task_name = st.text_input("Task Name")
    category = st.selectbox("Category", ["", "Personal", "Business"])
    size = st.selectbox("Size", ["", "Small", "Medium", "Large"])
    links = st.text_area("Optional Links (comma-separated):")
    if st.button("Add Task"):
        if not task_name or not category or not size:
            st.error("Please fill in all required fields.")
        else:
            new_task = {
                "task_name": task_name,
                "category": category,
                "size": size,
                "date": datetime.now().strftime("%Y-%m-%d"),
                "links": [link.strip() for link in links.split(",") if link.strip()],
                "notes": "",
            }
            data["tasks"].append(new_task)
            save_data(data)
            st.success("Task added successfully!")

# Task List Display
st.header("Pending Tasks")
if data["tasks"]:
    for i, task in enumerate(data["tasks"]):
        with st.expander(f"Task {i + 1}: {task['task_name']} ({task['category']})"):
            st.write(f"**Size:** {task['size']}")
            st.write(f"**Date Added:** {task['date']}")
            st.write("**Links:**")
            if task["links"]:
                for j, link in enumerate(task["links"], 1):
                    st.markdown(f"[Link {j}]({link})", unsafe_allow_html=True)
            else:
                st.write("No links added.")
            st.write("**Notes:**")
            st.write(task["notes"] if task["notes"] else "No notes added.")

            # Edit links and notes
            with st.form(f"Edit Task {i}"):
                new_links = st.text_area("Add Links (comma-separated):")
                new_notes = st.text_area("Add Notes:")
                submitted = st.form_submit_button("Update Task")
                if submitted:
                    if new_links:
                        task["links"].extend([link.strip() for link in new_links.split(",") if link.strip()])
                    if new_notes:
                        task["notes"] = new_notes
                    save_data(data)
                    st.success("Task updated successfully!")

            # Mark as completed
            if st.button(f"Mark as Completed", key=f"complete_{i}"):
                data["completed"].append(task)
                del data["tasks"][i]
                save_data(data)
                st.success("Task marked as completed!")
                st.experimental_rerun()
else:
    st.info("No pending tasks. Add a new task from the sidebar!")

# Completed Tasks Section
st.header("Completed Tasks")
if data["completed"]:
    for i, task in enumerate(data["completed"]):
        with st.expander(f"Task {i + 1}: {task['task_name']} ({task['category']})"):
            st.write(f"**Size:** {task['size']}")
            st.write(f"**Date Added:** {task['date']}")
            st.write("**Links:**")
            if task["links"]:
                for j, link in enumerate(task["links"], 1):
                    st.markdown(f"[Link {j}]({link})", unsafe_allow_html=True)
            else:
                st.write("No links added.")
            st.write("**Notes:**")
            st.write(task["notes"] if task["notes"] else "No notes added.")
else:
    st.info("No completed tasks yet.")

# Footer
st.markdown(
    "<div style='text-align: center; margin-top: 20px;'>Made with ❤️ using Streamlit</div>",
    unsafe_allow_html=True,
)
