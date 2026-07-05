from datetime import datetime, date
from pawpal_system import Owner, Pet, Task, Scheduler

def run_algorithmic_demo():
    print("=" * 70)
    print("🧠 PAWPAL+ INTELLIGENT ALGORITHMIC TESTING GROUND 🧠")
    print("=" * 70)

    scheduler = Scheduler()
    owner = Owner(owner_id="O-88", name="Salisu Ibrahim")
    
    rex = Pet(pet_id="P-01", name="Rex", species="Dog", age=3)
    owner.add_pet(rex)

    # 1. TEST: Chronological Sorting (Adding tasks intentionally out of order)
    print("\n[Testing Sorting Engine] Adding mixed afternoon/morning entries out of chronological order...")
    afternoon_walk = Task(
        task_id="T-01", pet_id="P-01", title="Afternoon Park Run",
        task_type="walk", start_time=datetime(2026, 7, 5, 16, 0), duration_minutes=40
    )
    morning_meds = Task(
        task_id="T-02", pet_id="P-01", title="Critical Morning Meds",
        task_type="medication", start_time=datetime(2026, 7, 5, 7, 30), duration_minutes=10, priority="High"
    )
    
    rex.add_task(afternoon_walk)
    rex.add_task(morning_meds)
    
    agenda = scheduler.get_daily_agenda(owner, date(2026, 7, 5))
    print("Resulting sorted agenda order:")
    for t in agenda:
        print(f"  ⏱️ {t.start_time.strftime('%H:%M')} -> {t.title}")

    # 2. TEST: Overlap Conflict Detection
    print("\n[Testing Overlap Analytics] Injecting a colliding task window...")
    colliding_walk = Task(
        task_id="T-CONFL", pet_id="P-01", title="Colliding Grooming Session",
        task_type="grooming", start_time=datetime(2026, 7, 5, 16, 15), duration_minutes=30
    )
    
    conflicts = scheduler.detect_conflicts(owner, colliding_walk)
    if conflicts:
        print(f"⚠️ WARNING: Conflict detected! Your proposed time blocks collide with:")
        for c in conflicts:
            print(f"  ❌ Blocker: '{c.title}' ({c.start_time.strftime('%H:%M')} - {c.end_time.strftime('%H:%M')})")

    # 3. TEST: Recurring Task Replication Loop
    print("\n[Testing Recurrence Systems] Tracking a Daily Care loop completion...")
    daily_feeding = Task(
        task_id="T-REC", pet_id="P-01", title="Daily Standard Feeding",
        task_type="feeding", start_time=datetime(2026, 7, 5, 12, 0), duration_minutes=15, frequency="Daily"
    )
    rex.add_task(daily_feeding)
    
    print(f"  Current instance date: {daily_feeding.start_time.strftime('%Y-%m-%d %H:%M')}")
    next_cycle = daily_feeding.mark_complete(scheduler)
    
    if next_cycle:
        rex.add_task(next_cycle)
        print(f"  🔄 Success! Rolled forward next cycle to: {next_cycle.start_time.strftime('%Y-%m-%d %H:%M')}")

    print("\n" + "=" * 70)

if __name__ == "__main__":
    run_algorithmic_demo()