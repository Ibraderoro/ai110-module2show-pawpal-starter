import streamlit as st
from datetime import datetime, date
from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+ Smart Care Assistant", page_icon="🐾", layout="wide")

st.title("🐾 PawPal+ Smart Care Assistant")
st.caption("An intelligent planning ecosystem for busy pet parents.")

# --- PERSISTENT STATE MEMORY & FILE ECOSYSTEM LIFECYCLE (Challenge 2) ---
if "owner" not in st.session_state:
    st.session_state.owner = Owner(owner_id="O-88", name="Salisu Ibrahim")
    # Attempt to load local database; fallback to baseline seeds if fresh
    if not st.session_state.owner.load_from_json():
        st.session_state.owner.add_pet(Pet(pet_id="P-MOCHI", name="Mochi", species="cat", age=2))
        st.session_state.owner.add_pet(Pet(pet_id="P-JEST", name="Jest", species="dog", age=3))
        st.session_state.owner.save_to_json()

if "scheduler" not in st.session_state:
    st.session_state.scheduler = Scheduler()

# --- SIDEBAR & MAIN LAYOUT (Symmetric Workspace Split) ---
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
            st.session_state.owner.save_to_json()  # Database Commit
            st.success(f"Registered {new_pet_name} successfully!")
            st.rerun()

with col_main:
    st.header("📅 Add Care Routine Step")
    
    # Dynamic key-mapped dropdown selector
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
            
            # Use dynamic selected_pet_id argument binding
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
                st.session_state.owner.save_to_json()  # Database Commit
                st.success(f"Successfully pinned '{task_title}' to {target_pet.name}'s schedule tracker!")
                st.rerun()

    st.divider()

    # --- BRAIN ENGINE VIEW, SORTING & LIVE WARNINGS (Challenge 4 UI Polish) ---
    st.subheader("🧠 System Generated Schedule & Care Explanations")
    
    # Formatting Maps for Challenge 4
    CATEGORY_EMOJIS = {
        "walk": "🐕",
        "feeding": "🍖",
        "medication": "💊",
        "appointment": "🏥",
        "grooming": "✂️"
    }
    
    PRIORITY_COLORS = {
        "High": "#FF4B4B",     # Crimson Alert
        "Normal": "#00C49F",   # Emerald Green
        "Low": "#707070"       # Muted Gray
    }
    
    # Executes internal chronological sort_by_time auto-ordering
    compiled_agenda = st.session_state.scheduler.get_daily_agenda(st.session_state.owner, date.today())
    
    if compiled_agenda:
        for t in compiled_agenda:
            t_pet = st.session_state.owner.get_pet(t.pet_id)
            p_name = t_pet.name if t_pet else "Unknown"
            
            # Map type emojis and priority colors dynamically
            emoji = CATEGORY_EMOJIS.get(t.task_type, "📋")
            badge_color = PRIORITY_COLORS.get(t.priority, "#707070")
            
            # Live Intercept: Query conflict matrix directly in row execution loop
            conflicts = st.session_state.scheduler.detect_conflicts(st.session_state.owner, t)
            
            r_col1, r_col2, r_col3 = st.columns([1, 3, 1.2])
            with r_col1:
                st.markdown(f"⏱️ **{t.start_time.strftime('%H:%M')} - {t.end_time.strftime('%H:%M')}**")
            with r_col2:
                # Compile dynamic inline HTML color-coded badge tags
                priority_badge = f"<span style='background-color: {badge_color}; color: white; padding: 2px 6px; border-radius: 4px; font-size: 11px; font-weight: bold;'>{t.priority.upper()}</span>"
                st.markdown(f"{emoji} **{t.title}** for *{p_name}* ({t.duration_minutes} mins) — {priority_badge} — `{t.frequency}`", unsafe_allow_html=True)
                
                # Render inline error if overlapping collision arrays are flagged
                if conflicts:
                    st.error(f"⚠️ **Schedule Collision:** Overlaps with **'{conflicts[0].title}'** ({conflicts[0].start_time.strftime('%H:%M')} - {conflicts[0].end_time.strftime('%H:%M')})!")
                
                # Contextual Explanation Engine
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
                            st.toast("🔄 Recurring interval rollforward generated.")
                        st.session_state.owner.save_to_json()  # Database Commit
                        st.rerun()
                else:
                    st.markdown("<span style='color:#00C49F; font-weight:bold;'>✅ Completed</span>", unsafe_allow_html=True)
            st.divider()
            
        # Expanded registry snapshot grid for deep auditing checks
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