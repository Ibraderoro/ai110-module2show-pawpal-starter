import pytest
from datetime import datetime
from pawpal_system import Pet, Task, Owner

def test_task_completion():
    """Verify that calling mark_complete() actually changes the task's status."""
    task = Task(
        task_id="T-TEST",
        pet_id="P-01",
        title="Diagnostic Check",
        task_type="medical",
        start_time=datetime(2026, 7, 5, 12, 0),
        duration_minutes=20
    )
    assert task.is_completed is False
    task.mark_complete()
    assert task.is_completed is True

def test_task_addition_increments_count():
    """Verify that adding a task to a Pet increases that pet's task count."""
    pet = Pet(pet_id="P-TEST", name="Buddy", species="Dog", age=4)
    assert len(pet.tasks) == 0
    
    task = Task(
        task_id="T-TEST2",
        pet_id="P-TEST",
        title="Quick Brushing",
        task_type="grooming",
        start_time=datetime(2026, 7, 5, 15, 0),
        duration_minutes=15
    )
    pet.add_task(task)
    assert len(pet.tasks) == 1
    assert pet.tasks[0].title == "Quick Brushing"