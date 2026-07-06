import streamlit as st
from datetime import datetime, date
from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+ Smart Care Assistant", page_icon="🐾", layout="wide")

st.title("🐾 PawPal+ Smart Care Assistant")
st.caption("An intelligent planning ecosystem for busy pet parents.")

# --- PERSISTENT STATE MEMORY & FILE ECOSYSTEM LIFECYCLE ---
if "owner" not in st.session_state:
    st.session_state.owner = Owner(owner_id="O-88", name="Salisu Ibrahim")
    # Local JSON footprint backup load
    if not st.session_state.owner.load_from_json():
        # Fallback profile seed strings to match workspace baselines
        st.session_state.owner.add_pet(Pet(pet_id="P-MOCHI", name="Mochi", species="cat", age=2))
        st.session_state.owner.add_pet(Pet(pet_id="P-JEST", name="Jest", species="dog", age=3))
        st.session_state.owner.save_to_json()

if "scheduler" not in st.session_state:
    st.session_state.scheduler = Scheduler()

# --- SIDEBAR & MAIN LAYOUT (Symmetric Layout Split) ---
col_sidebar, col_main = st.columns([1, 2.2])

with col_sidebar:
    st.header("👤 Profiles")
    st.write(f"Manager: **{st.session_state.owner.name}**")
    st.divider()
    
    st.subheader("➕ Onboard a Pet")
    with st.form("onboard_pet_form", clear_on_submit=True):
        new_pet_name = st.text_input("Pet Name", placeholder="e.g., Papii")
        new_species = st.selectbox("Species Types", ["dog", "cat", "other"])
        new_age = st.number_input("Age (Years)", min_value=0, max_value=30, value=1)
        
        submit_pet = st.form_submit_button("Register Pet")
        if submit_pet and new_pet_name:
            generated_id = f"P-{new_pet_name.upper()}-{datetime.now().strftime('%M%S')}"
            new_pet_obj = Pet(pet_id=generated_id, name=new_pet_name, species=new_species, age=int(new_age))
            st.session_state.owner.add_pet(new_pet_obj)
            st.session_state.owner.save_to_json()  # Persistent Commit
            st.success(f"Registered {new_pet_name} successfully!")
            st.rerun()

with col_main:
    st.header("📅 Add Care Routine Step")
    
    # Active Dropdown Selection Index Mapping
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
            
            candidate_task = Task(
                task_id=generated_task_id, 
                pet_id=selected_pet_id,
                title=task_title,
                task_type=task_type, 
                start_time=simulated_start, 
                duration_minutes=int(duration),
                priority=priority, 
                frequency=frequency
            )
            
            target_pet = st.session_state.owner.get_pet(selected_pet_id)
            if target_pet:
                target_pet.add_task(candidate_task)
                st.session_state.owner.save_to_json()  # Persistent Commit
                st.success(f"Successfully pinned '{task_title}' to {target_pet.name}'s track array!")
                st.rerun()

    st.divider()

    # --- LIVE TIMELINE VIEW WITH ERROR BLOCK INLINE MATCHING ---
    st.subheader("🧠 System Generated Schedule & Care Explanations")
    
    # Process Scheduler output (automatically aggregates and triggers sort_by_time)
    compiled_agenda = st.session_state.scheduler.get_daily_agenda(st.session_state.owner, date.today())
    
    if compiled_agenda:
        for t in compiled_agenda:
            t_pet = st.session_state.owner.get_pet(t.pet_id)
            p_name = t_pet.name if t_pet else "Unknown"
            
            # Context Real-Time Scanning Intercept
            conflicts = st.session_state.scheduler.detect_conflicts(st.session_state.owner, t)
            
            r_col1, r_col2, r_col3 = st.columns([1, 3, 1.2])
            with r_col1:
                st.markdown(f"⏱️ **{t.start_time.strftime('%H:%M')} - {t.end_time.strftime('%H:%M')}**")
            with r_col2:
                st.markdown(f"**{t.title}** for *{p_name}* ({t.duration_minutes} mins) — `[{t.priority.upper()}]` — `{t.frequency}`")
                
                # Active Overlap Layout Rendering Box
                if conflicts:
                    st.error(f"⚠️ **Schedule Collision:** Overlaps with **'{conflicts[0].title}'** ({conflicts[0].start_time.strftime('%H:%M')} - {conflicts[0].end_time.strftime('%H:%M')})!")
                
                # Reasoning Output Formatting Block
                if t.priority == "High":
                    st.caption("💡 *System Reasoning:* Prioritized as an essential care step because missing this time block can disrupt your pet's mandatory health routine.")
                else:
                    st.caption("💡 *System Reasoning:* Scheduled chronologically to distribute your care tasks evenly across the day.")
                    
            with r_col3:
                if not t.is_completed:
                    if st.button("Mark Done", key=t.task_id):
                        next_cycle = t.mark_complete(st.session_state.scheduler)
                        if next_cycle and t_pet:
                            t_pet.add_task(next_cycle)
                            st.toast("🔄 Recurring interval rollover generated.")
                        st.session_state.owner.save_to_json()  # Persistent Commit
                        st.rerun()
                else:
                    st.markdown("<span style='color:green; font-weight:bold;'>Completed</span>", unsafe_allow_html=True)
            st.divider()
            
        # Expanded Logging Table Details
        with st.expander("🗄️ Technical Session State Registry Overview", expanded=False):
            raw_tasks = st.session_state.owner.get_all_tasks()
            st.table([{
                "Task ID": tk.task_id,
                "Pet Target": (st.session_state.owner.get_pet(tk.pet_id).name if st.session_state.owner.get_pet(tk.pet_id) else "Unknown"),
                "Title": tk.title,
                "Start Window": tk.start_time.strftime('%H:%M'),
                "Status": "✅ Complete" if tk.is_completed else "⏳ Pending"
            } for tk in raw_tasks])
    else:
        st.info("No timeline items registered for today's configuration environment yet.")