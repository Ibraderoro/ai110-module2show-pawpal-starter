import pytest
from datetime import datetime, date, timedelta
from pawpal_system import Owner, Pet, Task, Scheduler

@pytest.fixture
def test_env():
    """Initializes a pristine structural core testing environment."""
    owner = Owner(owner_id="O-TEST", name="Salisu Ibrahim")
    pet = Pet(pet_id="P-TEST", name="TestPet", species="dog", age=2)
    owner.add_pet(pet)
    scheduler = Scheduler()
    return owner, pet, scheduler


def test_chronological_task_sorting(test_env):
    """Verifies that the scheduler engine correctly forces out-of-order logs into chronological alignment."""
    owner, pet, scheduler = test_env
    
    task_late = Task(
        task_id="T-LATE", pet_id=pet.pet_id, title="Late Walk", 
        task_type="walk", start_time=datetime.combine(date.today(), datetime.min.time().replace(hour=18)), duration_minutes=30
    )
    task_early = Task(
        task_id="T-EARLY", pet_id=pet.pet_id, title="Early Feeding", 
        task_type="feeding", start_time=datetime.combine(date.today(), datetime.min.time().replace(hour=7)), duration_minutes=15
    )
    
    # Intentionally append later items first
    pet.add_task(task_late)
    pet.add_task(task_early)
    
    agenda = scheduler.get_daily_agenda(owner, date.today())
    
    assert len(agenda) == 2
    assert agenda[0].task_id == "T-EARLY"
    assert agenda[1].task_id == "T-LATE"


def test_empty_pet_agenda(test_env):
    """Ensures query allocations on unconfigured agendas resolve safely to empty lists instead of exceptions."""
    owner, _, scheduler = test_env
    agenda = scheduler.get_daily_agenda(owner, date.today())
    assert isinstance(agenda, list)
    assert len(agenda) == 0


def test_conflict_detection_window_overlap(test_env):
    """Validates that absolute time window intersections register as a clear conflict list."""
    owner, pet, scheduler = test_env
    base_time = datetime.combine(date.today(), datetime.min.time().replace(hour=12))
    
    existing_task = Task(
        task_id="T-EXISTING", pet_id=pet.pet_id, title="Initial Block", 
        task_type="grooming", start_time=base_time, duration_minutes=60
    )
    pet.add_task(existing_task)
    
    # Create an intersecting task running from 12:30 to 13:00
    intersecting_task = Task(
        task_id="T-INTERSECT", pet_id=pet.pet_id, title="Collision Block", 
        task_type="feeding", start_time=base_time + timedelta(minutes=30), duration_minutes=30
    )
    
    conflicts = scheduler.detect_conflicts(owner, intersecting_task)
    assert len(conflicts) == 1
    assert conflicts[0].task_id == "T-EXISTING"


def test_recurrence_logic_daily_rollforward(test_env):
    """Verifies that clicking completion updates statuses and rolls a Daily task exactly 24 hours out."""
    owner, pet, scheduler = test_env
    base_time = datetime.combine(date.today(), datetime.min.time().replace(hour=8))
    
    recurring_task = Task(
        task_id="T-RECUR", pet_id=pet.pet_id, title="Daily Routine", 
        task_type="walk", start_time=base_time, duration_minutes=30, frequency="Daily"
    )
    
    next_task = recurring_task.mark_complete(scheduler)
    
    assert recurring_task.is_completed is True
    assert next_task is not None
    assert next_task.start_time == base_time + timedelta(days=1)
    assert next_task.frequency == "Daily"


def test_task_deserialization_defensive_fallback():
    """Defensive Testing Area: Verifies that unconvertible strings passed to JSON entries 

    trigger our custom error paths and default safely instead of executing an app-wide crash.
    """
    corrupted_json_input = {
        "task_id": "T-CORRUPT",
        "pet_id": "P-TEST",
        "title": "Malicious Date String Injected",
        "task_type": "medication",
        "start_time": "completely-invalid-date-format-string-xyz",  # Cannot be parsed by ISO formatters
        "duration_minutes": 15,
        "priority": "High",
        "is_completed": False,
        "frequency": "Once"
    }
    
    # Invoking deserialization fallback branch
    parsed_task = Task.from_dict(corrupted_json_input)
    
    assert parsed_task.task_id == "T-CORRUPT"
    assert isinstance(parsed_task.start_time, datetime)
    # Proves the validation branch intercepted the error and clamped the date smoothly to today
    assert parsed_task.start_time.date() == date.today()