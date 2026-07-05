import streamlit as st
from datetime import datetime, date
from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+ Smart Planner", page_icon="🐾", layout="wide")

st.title("🐾 PawPal+ Smart Care Assistant")
st.caption("An intelligent planning ecosystem for busy pet parents.")

# Ensure unified persistent engines are stored securely in session state
if "owner" not in st.session_state:
    st.session_state.owner = Owner(owner_id="O-88", name="Salisu Ibrahim")

if "scheduler" not in st.session_state:
    st.session_state.scheduler = Scheduler()

# Onboard a baseline standard profile if the workspace state is brand new
if not st.session_state.owner.pets:
    st.session_state.owner.add_pet(Pet(pet_id="P-MOCHI", name="Mochi", species="cat", age=2))

# --- LAYOUT DIVISION ---
col_sidebar, col_main = st.columns([1, 2.2])

with col_sidebar:
    st.header("👤 Profiles")
    st.write(f"Manager: **{st.session_state.owner.name}**")
    st.divider()
    
    st.subheader("➕ Onboard a Pet")
    with st.form("onboard_pet_form", clear_on_submit=True):
        new_pet_name = st.text_input("Pet Name")
        new_species = st.selectbox("Species Types", ["dog", "cat", "other"])
        new_age = st.number_input("Age (Years)", min_value=0, max_value=30, value=2)
        
        submit_pet = st.form_submit_button("Register Pet")
        if submit_pet and new_pet_name:
            generated_id = f"P-{new_pet_name.upper()}-{datetime.now().strftime('%M%S')}"
            new_pet_obj = Pet(pet_id=generated_id, name=new_pet_name, species=new_species, age=int(new_age))
            st.session_state.owner.add_pet(new_pet_obj)
            st.success(f"Registered {new_pet_name}!")
            st.rerun()

with col_main:
    st.header("📅 Add Care Routine Step")
    
    selected_pet_id = st.selectbox(
        "Select Target Pet Profile", 
        options=list(st.session_state.owner.pets.keys()),
        format_func=lambda x: st.session_state.owner.pets[x].name
    )
    
    with st.form("add_task_form", clear_on_submit=True):
        c1, c2 = st.columns(2)
        with c1:
            task_title = st.text_input("Task Title (e.g., Evening Park Run)", value="Grooming Session")
            task_type = st.selectbox("Category", ["walk", "feeding", "medication", "appointment", "grooming"])
            task_time = st.time_input("Target Start Time")
        with c2:
            duration = st.number_input("Duration (Minutes)", min_value=1, max_value=240, value=30)
            priority = st.selectbox("Priority Urgency", ["Low", "Normal", "High"], index=1)
            frequency = st.selectbox("Interval Frequency", ["Once", "Daily", "Weekly"])
            
        submit_task = st.form_submit_button("Log Activity Block")
        
        if submit_task and task_title:
            simulated_start = datetime.combine(date.today(), task_time)
            generated_task_id = f"T-{datetime.now().strftime('%M%S')}"
            
            # Instantiate candidate verification token
            candidate_task = Task(
                task_id=generated_task_id, pet_id=selected_pet_id, title=task_title,
                task_type=task_type, start_time=simulated_start, duration_minutes=int(duration),
                priority=priority, frequency=frequency
            )
            
            # ALGORITHMIC CHECK: Intercept block to run overlap warning logic
            pre_existing_conflicts = st.session_state.scheduler.detect_conflicts(st.session_state.owner, candidate_task)
            
            if pre_existing_conflicts:
                st.warning(f"⚠️ **Timeline Conflict Warning:** This slot overlaps with an existing task for this pet!")
                for b in pre_existing_conflicts:
                    st.write(f"👉 Blocker: **{b.title}** ({b.start_time.strftime('%H:%M')} - {b.end_time.strftime('%H:%M')})")
            
            # Save task regardless of outcome to align with user choice execution
            target_pet = st.session_state.owner.get_pet(selected_pet_id)
            target_pet.add_task(candidate_task)
            st.success(f"Successfully pinned '{task_title}' to data structures.")
            st.rerun()

    st.divider()

    # --- BRAIN ENGINE OUTPUT: GENERATE & EXPLAIN PLAN ---
    st.subheader("🧠 System Generated Schedule & Care Explanations")
    
    compiled_agenda = st.session_state.scheduler.get_daily_agenda(st.session_state.owner, date.today())
    
    if compiled_agenda:
        for t in compiled_agenda:
            t_pet = st.session_state.owner.get_pet(t.pet_id)
            p_name = t_pet.name if t_pet else "Unknown"
            
            # Layout the scannable timeline list row
            r_col1, r_col2, r_col3 = st.columns([1, 3, 1.2])
            with r_col1:
                st.markdown(f"⏱️ **{t.start_time.strftime('%H:%M')} - {t.end_time.strftime('%H:%M')}**")
            with r_col2:
                status_icon = "✅" if t.is_completed else "⏳"
                st.markdown(f"**{t.title}** for *{p_name}* ({t.duration_minutes} mins) — `[{t.priority.upper()}]` — `{t.frequency}`")
                
                # REASONING ENGINE: Explain why this task is positioned here
                if t.priority == "High":
                    st.caption("💡 *System Reasoning:* Prioritized as high-priority because missing this care step could disrupt your pet's wellness routine.")
                else:
                    st.caption("💡 *System Reasoning:* Scheduled chronologically to distribute your care tasks evenly across the day.")
                    
            with r_col3:
                if not t.is_completed:
                    if st.button("Mark Done", key=t.task_id):
                        # RECURRENCE CHECK: If daily/weekly, trigger automated generation loop
                        next_cycle = t.mark_complete(st.session_state.scheduler)
                        if next_cycle and t_pet:
                            t_pet.add_task(next_cycle)
                            st.toast(f"🔄 Recurring task rolled forward to tomorrow!")
                        st.rerun()
                else:
                    st.markdown("<span style='color:green;'>Completed</span>", unsafe_allow_html=True)
            st.divider()
    else:
        st.info("No timeline items registered for today's environment baseline schedule yet.")