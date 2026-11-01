import streamlit as st
from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾")
st.title("🐾 PawPal+")
st.caption("Smart pet care scheduling")

# Keep the Owner alive between reruns
if "owner" not in st.session_state:
    st.session_state.owner = Owner("Jordan")
owner = st.session_state.owner
scheduler = Scheduler(owner)

owner.name = st.text_input("Owner name", value=owner.name)

st.subheader("Add a pet")
with st.form("add_pet", clear_on_submit=True):
    pet_name = st.text_input("Pet name")
    species = st.selectbox("Species", ["dog", "cat", "other"])
    if st.form_submit_button("Add pet"):
        if not pet_name.strip():
            st.warning("Please enter a pet name.")
        elif owner.get_pet(pet_name):
            st.warning(f"{pet_name} already exists.")
        else:
            owner.add_pet(Pet(pet_name.strip(), species))
            st.success(f"Added {pet_name}!")

st.subheader("Schedule a task")
if not owner.pets:
    st.info("Add a pet first.")
else:
    with st.form("add_task", clear_on_submit=True):
        target = st.selectbox("Pet", [p.name for p in owner.pets])
        description = st.text_input("Task description")
        when = st.time_input("Time")
        frequency = st.selectbox("Frequency", ["once", "daily", "weekly"])
        if st.form_submit_button("Add task"):
            if not description.strip():
                st.warning("Please enter a description.")
            else:
                owner.get_pet(target).add_task(
                    Task(description.strip(), when.strftime("%H:%M"), frequency)
                )
                st.success(f"Task added for {target}.")

st.subheader("Schedule")
conflicts = scheduler.detect_conflicts()
for w in conflicts:
    st.warning(w)

col1, col2 = st.columns(2)
pet_filter = col1.selectbox("Filter by pet", ["All"] + [p.name for p in owner.pets])
status_filter = col2.selectbox("Filter by status", ["All", "Pending", "Completed"])

tasks = scheduler.filter_tasks(
    pet_name=None if pet_filter == "All" else pet_filter,
    completed={"All": None, "Pending": False, "Completed": True}[status_filter],
)
tasks = scheduler.sort_by_time(tasks)

if not tasks:
    st.info("No tasks to show.")
else:
    st.table([
        {"Time": t.time, "Date": str(t.due_date), "Pet": t.pet_name,
         "Task": t.description, "Repeats": t.frequency,
         "Done": "✅" if t.completed else "⏳"}
        for t in tasks
    ])
    st.write("Mark a task complete:")
    for i, t in enumerate(tasks):
        if not t.completed and st.button(f"✔ {t.pet_name}: {t.description} ({t.time}, {t.due_date})", key=f"done_{i}"):
            nxt = scheduler.mark_task_complete(t)
            if nxt:
                st.session_state["msg"] = f"Next {nxt.frequency} task scheduled for {nxt.due_date}."
            st.rerun()

if "msg" in st.session_state:
    st.success(st.session_state.pop("msg"))
