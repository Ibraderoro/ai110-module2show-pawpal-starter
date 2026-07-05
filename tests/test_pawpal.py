import pytest
from datetime import datetime, date
from pawpal_system import Owner, Pet, Task, Scheduler

def test_chronological_task_sorting():
    """Verify that tasks are returned in strict chronological order regardless of addition sequence."""
    scheduler = Scheduler()
    owner = Owner(owner_id="O-TEST", name="Salisu")
    pet = Pet(pet_id="P-TEST", name="Mochi", species="cat", age=2)
    owner.add_pet(pet)
    
    # 1. Add tasks out of order (Late afternoon first, early morning second)
    late_task = Task(
        task_id="T1", pet_id="P-TEST", title="Evening Grooming",
        task_type="grooming", start_time=datetime(2026, 7, 5, 19, 0), duration_minutes=30
    )
    early_task = Task(
        task_id="T2", pet_id="P-TEST", title="Morning Feed",
        task_type="feeding", start_time=datetime(2026, 7, 5, 8, 0), duration_minutes=15
    )
    
    pet.add_task(late_task)
    pet.add_task(early_task)
    
    # 2. Compile daily agenda
    agenda = scheduler.get_daily_agenda(owner, date(2026, 7, 5))
    
    # 3. Assertions
    assert len(agenda) == 2
    assert agenda[0].task_id == "T2"  # 08:00 AM comes first
    assert agenda[1].task_id == "T1"  # 07:00 PM comes second


def test_empty_pet_agenda():
    """Verify that querying an agenda for a pet with zero tasks safely returns an empty list."""
    scheduler = Scheduler()
    owner = Owner(owner_id="O-TEST", name="Salisu")
    pet = Pet(pet_id="P-EMPTY", name="Rex", species="dog", age=3)
    owner.add_pet(pet)
    
    agenda = scheduler.get_daily_agenda(owner, date(2026, 7, 5))
    assert len(agenda) == 0


def test_conflict_detection_window_overlap():
    """Verify that the scheduler flags duplicate/overlapping time allocations for the same pet."""
    scheduler = Scheduler()
    owner = Owner(owner_id="O-TEST", name="Salisu")
    pet = Pet(pet_id="P-TEST", name="Mochi", species="cat", age=2)
    owner.add_pet(pet)
    
    # Task A: 16:00 to 16:40 (40 mins)
    task_a = Task(
        task_id="T-A", pet_id="P-TEST", title="Park Walk",
        task_type="walk", start_time=datetime(2026, 7, 5, 16, 0), duration_minutes=40
    )
    pet.add_task(task_a)
    
    # Task B: 16:15 to 16:45 (Overlaps with Task A)
    task_b = Task(
        task_id="T-B", pet_id="P-TEST", title="Grooming Session",
        task_type="grooming", start_time=datetime(2026, 7, 5, 16, 15), duration_minutes=30
    )
    
    conflicts = scheduler.detect_conflicts(owner, task_b)
    assert len(conflicts) == 1
    assert conflicts[0].task_id == "T-A"


def test_recurrence_logic_daily_rollforward():
    """Verify that marking a daily task complete creates a new task exactly 1 day later."""
    scheduler = Scheduler()
    task = Task(
        task_id="T-DAILY", pet_id="P-TEST", title="Daily Vitamin",
        task_type="medication", start_time=datetime(2026, 7, 5, 12, 0), duration_minutes=10, frequency="Daily"
    )
    
    next_occurrence = task.mark_complete(scheduler)
    
    assert task.is_completed is True
    assert next_occurrence is not None
    assert next_occurrence.start_time == datetime(2026, 7, 6, 12, 0)  # Roll forward +1 day
    assert next_occurrence.frequency == "Daily"
    assert "rev" in next_occurrence.task_id