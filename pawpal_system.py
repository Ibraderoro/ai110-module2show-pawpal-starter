from dataclasses import dataclass, field
from datetime import datetime, date
from typing import List, Dict, Optional

@dataclass
class Task:
    """Represents a single activity constraint with description, time, and completion status."""
    task_id: str
    pet_id: str
    title: str
    task_type: str  # e.g., 'feeding', 'walk', 'medication', 'appointment'
    start_time: datetime
    duration_minutes: int
    priority: str = "Normal"  # Low, Normal, High
    is_completed: bool = False

    def mark_complete(self) -> None:
        """Changes the task status to completed."""
        self.is_completed = True


@dataclass
class Pet:
    """Stores pet details and an internal list of associated tasks."""
    pet_id: str
    name: str
    species: str
    age: int
    medical_notes: List[str] = field(default_factory=list)
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Appends a care task directly to this pet's internal tracker."""
        self.tasks.append(task)


class Owner:
    """Manages multiple pets and provides aggregated access to all their tasks."""
    def __init__(self, owner_id: str, name: str):
        self.owner_id: str = owner_id
        self.name: str = name
        self.pets: Dict[str, Pet] = {}

    def add_pet(self, pet: Pet) -> None:
        """Associates a new pet profile with this owner."""
        self.pets[pet.pet_id] = pet

    def get_pet(self, pet_id: str) -> Optional[Pet]:
        """Safely retrieves a pet profile by its unique identifier."""
        return self.pets.get(pet_id)

    def get_all_tasks(self) -> List[Task]:
        """Aggregates and returns every task across all registered pets."""
        all_tasks = []
        for pet in self.pets.values():
            all_tasks.extend(pet.tasks)
        return all_tasks


class Scheduler:
    """The central brain that retrieves, organizes, and manages tasks across pets."""
    def __init__(self):
        self.global_tasks: List[Task] = []

    def get_daily_agenda(self, owner: Owner, target_date: date) -> List[Task]:
        """Retrieves and chronologically organizes tasks for an owner's pets on a given date."""
        # Retrieve all tasks from the owner's pets
        tasks = owner.get_all_tasks()
        # Filter for the target calendar date and sort them chronologically
        daily_tasks = [t for t in tasks if t.start_time.date() == target_date]
        daily_tasks.sort(key=lambda x: x.start_time)
        return daily_tasks

    def detect_conflicts(self, new_task: Task) -> List[Task]:
        """Identifies time conflicts (Stub to be fully optimized in Phase 4)."""
        return []