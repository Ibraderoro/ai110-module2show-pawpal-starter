from dataclasses import dataclass, field
from datetime import datetime, date
from typing import List, Dict, Optional

@dataclass
class Pet:
    """Represents a clean data record for an individual pet profile."""
    pet_id: str
    name: str
    species: str
    age: int
    medical_notes: List[str] = field(default_factory=list)


@dataclass
class Task:
    """Represents a routine care event, medication tracking, or appointment constraint."""
    task_id: str
    pet_id: str
    title: str
    task_type: str  # e.g., 'feeding', 'walk', 'medication', 'appointment'
    start_time: datetime
    duration_minutes: int
    is_recurring: bool = False
    priority: str = "Normal"  # Low, Normal, High


class Owner:
    """Manages high-level owner profiles and explicit pet dictionary mappings."""
    def __init__(self, owner_id: str, name: str):
        self.owner_id: str = owner_id
        self.name: str = name
        self.pets: Dict[str, Pet] = {}

    def add_pet(self, pet: Pet) -> None:
        """Associates a new pet instance under this owner profile."""
        self.pets[pet.pet_id] = pet

    def get_pet(self, pet_id: str) -> Optional[Pet]:
        """Safely extracts a tracked pet profile by its unique key identifier."""
        return self.pets.get(pet_id)


class Scheduler:
    """The analytical engine processing chronological order and timeline conflicts."""
    def __init__(self):
        self.global_tasks: List[Task] = []

    def schedule_task(self, task: Task) -> bool:
        """Appends a valid task token to the central data ledger."""
        self.global_tasks.append(task)
        return True

    def get_daily_agenda(self, pet_id: str, target_date: date) -> List[Task]:
        """Returns a chronologically organized task array filtered by date and pet identity."""
        # Method stub: Implementation rules to follow in Phase 4
        return []

    def detect_conflicts(self, new_task: Task) -> List[Task]:
        """Identifies pre-existing event constraints that physically block the new task."""
        # Method stub: Implementation rules to follow in Phase 4
        return []