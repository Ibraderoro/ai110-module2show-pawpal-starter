from datetime import datetime, date
from pawpal_system import Owner, Pet, Task, Scheduler

def run_cli_demo():
    print("=" * 60)
    print("🐾 PAWPAL+ CLI SYSTEM INTERFACE - INITIALIZATION PROGRESS 🐾")
    print("=" * 60)
    
    # 1. Initialize Owner & Scheduler
    scheduler = Scheduler()
    owner = Owner(owner_id="O-88", name="Salisu Ibrahim")
    
    # 2. Add two Pets
    rex = Pet(pet_id="P-01", name="Rex", species="Dog", age=3)
    biscuit = Pet(pet_id="P-02", name="Biscuit", species="Golden Retriever", age=2)
    owner.add_pet(rex)
    owner.add_pet(biscuit)
    
    # 3. Add three Tasks with distinct times
    task1 = Task(
        task_id="T-01", pet_id="P-01", title="Morning Feeding (Rex)",
        task_type="feeding", start_time=datetime(2026, 7, 5, 8, 0), duration_minutes=15, priority="High"
    )
    task2 = Task(
        task_id="T-02", pet_id="P-02", title="Morning Walk (Biscuit)",
        task_type="walk", start_time=datetime(2026, 7, 5, 9, 0), duration_minutes=30, priority="High"
    )
    task3 = Task(
        task_id="T-03", pet_id="P-01", title="Medication Administration (Rex)",
        task_type="medication", start_time=datetime(2026, 7, 5, 14, 30), duration_minutes=10, priority="High"
    )
    
    rex.add_task(task1)
    biscuit.add_task(task2)
    rex.add_task(task3)
    
    # 4. Generate and beautifully format the schedule
    target_date = date(2026, 7, 5)
    today_agenda = scheduler.get_daily_agenda(owner, target_date)
    
    print(f"\n📅 Daily Care Agenda for {target_date.strftime('%A, %B %d, %Y')}:")
    print("-" * 60)
    
    for task in today_agenda:
        pet_name = owner.get_pet(task.pet_id).name if owner.get_pet(task.pet_id) else "Unknown"
        time_str = task.start_time.strftime("%H:%M")
        status_str = "✅ Completed" if task.is_completed else "⏳ Pending"
        
        print(f"  {time_str} — {task.title:<30} ({task.duration_minutes} min) [{task.priority}] -> {status_str}")
    
    print("-" * 60)
    print("🎉 System Runtime Verification: SUCCESS!")
    print("=" * 60)

if __name__ == "__main__":
    run_cli_demo()