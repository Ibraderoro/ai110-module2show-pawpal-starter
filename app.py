import streamlit as st
from datetime import datetime, date
# Step 1: Establish the connection by importing your backend engine
from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+ Care Manager", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+ Care Manager")

# Step 2: Manage the Application "Memory" (Stateless Prevention Vault)
if "owner" not in st.session_state:
    st.session_state.owner = Owner(owner_id="O-88", name="Salisu Ibrahim")

if "scheduler" not in st.session_state:
    st.session_state.scheduler = Scheduler()

# Initialize a standard pet profile if the owner's record is completely fresh
if not st.session_state.owner.pets:
    default_pet = Pet(pet_id="P-MOCHI", name="Mochi", species="cat", age=2)
    st.session_state.owner.add_pet(default_pet)

# --- SIDEBAR: Profile Management ---
with st.sidebar:
    st.header("👤 Profile Environment")
    st.write(f"**Manager:** {st.session_state.owner.name}")
    st.divider()
    
    st.subheader("➕ Onboard a New Pet")
    with st.form("onboard_pet_form", clear_on_submit=True):
        new_pet_name = st.text_input("Pet Name")
        new_species = st.selectbox("Species Types", ["dog", "cat", "other"])
        new_age = st.number_input("Age (Years)", min_value=0, max_value=30, value=2)
        
        submit_pet = st.form_submit_button("Register Pet")
        if submit_pet and new_pet_name:
            generated_id = f"P-{new_pet_name.upper()}-{datetime.now().strftime('%M%S')}"
            new_pet_obj = Pet(pet_id=generated_id, name=new_pet_name, species=new_species, age=int(new_age))
            st.session_state.owner.add_pet(new_pet_obj)
            st.success(f"Registered {new_pet_name} successfully!")
            st.rerun()

# --- MAIN INTERFACE: Step 3 Wiring UI Actions to Logic ---
st.subheader("📅 Add a Care Task to Backend Memory")

# Dropdown selection sourced directly from live object keys
selected_pet_id = st.selectbox(
    "Target Pet Profile", 
    options=list(st.session_state.owner.pets.keys()),
    format_func=lambda x: st.session_state.owner.pets[x].name
)

col1, col2, col3 = st.columns(3)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
with col3:
    priority = st.selectbox("Priority Ranking", ["low", "medium", "high"], index=2)

if st.button("Add task"):
    if task_title:
        # Create a clean backend tracking timestamp for today
        simulated_start = datetime.combine(date.today(), datetime.now().time())
        generated_task_id = f"T-{datetime.now().strftime('%M%S')}"
        
        # Instantiate task object contract
        new_task = Task(
            task_id=generated_task_id,
            pet_id=selected_pet_id,
            title=task_title,
            task_type="walk" if "walk" in task_title.lower() else "feeding",
            start_time=simulated_start,
            duration_minutes=int(duration),
            priority=priority
        )
        
        # Wire action directly to backend class method to update data structures
        target_pet = st.session_state.owner.get_pet(selected_pet_id)
        target_pet.add_task(new_task)
        st.success(f"✅ Securely injected '{task_title}' into {target_pet.name}'s task tracking backlog!")
    else:
        st.error("Please enter a valid task title.")

st.divider()

# Display active structural data currently resting in memory
all_active_tasks = st.session_state.owner.get_all_tasks()

if all_active_tasks:
    st.markdown("### 🗄️ Core Backlog Snapshot (`st.session_state`)")
    formatted_table_data = []
    for t in all_active_tasks:
        target_pet_obj = st.session_state.owner.get_pet(t.pet_id)
        formatted_table_data.append({
            "Pet Target": target_pet_obj.name if target_pet_obj else "Unknown",
            "Activity Title": t.title,
            "Duration": f"{t.duration_minutes} mins",
            "Priority Weight": t.priority,
            "Execution State": "✅ Completed" if t.is_completed else "⏳ Pending"
        })
    st.table(formatted_table_data)
else:
    st.info("No active backend task objects logged in this session framework yet.")

st.divider()

st.subheader("🧠 Algorithmic Execution Engine")
st.caption("Triggers your centralized query scheduler logic layers.")

if st.button("Generate schedule"):
    # Invoke daily agenda compiler calculation loop
    compiled_agenda = st.session_state.scheduler.get_daily_agenda(st.session_state.owner, date.today())
    
    st.success("📊 Chronological Engine Run Complete!")
    if compiled_agenda:
        for t in compiled_agenda:
            st.markdown(f"⏱️ **{t.start_time.strftime('%H:%M')}** — {t.title} ({t.duration_minutes} min) — `[{t.priority.upper()}]`")
    else:
        st.info("No timeline objects found scheduled for today's calendar date configuration.")