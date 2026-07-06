import json
import os
from dataclasses import dataclass, field
from datetime import datetime, date, timedelta
from typing import List, Dict, Optional

@dataclass
class Task:
    """Represents a single activity constraint with description, time, and completion status."""
    task_id: str
    pet_id: str
    title: str
    task_type: str  # e.g., 'feeding', 'walk', 'medication', 'appointment', 'grooming'
    start_time: datetime
    duration_minutes: int
    priority: str = "Normal"  # Low, Normal, High
    is_completed: bool = False
    frequency: str = "Once"  # 'Once', 'Daily', 'Weekly'

    def mark_complete(self, scheduler: Optional['Scheduler'] = None) -> Optional['Task']:
        """Changes the task status to completed and handles recurring generation if a scheduler is provided."""
        self.is_completed = True
        if scheduler and self.frequency != "Once":
            return scheduler.handle_recurring_generation(self)
        return None

    @property
    def end_time(self) -> datetime:
        """Calculates the dynamic expiration time block based on duration minutes."""
        return self.start_time + timedelta(minutes=self.duration_minutes)

    def to_dict(self) -> dict:
        """Converts Task properties to a standard primitive dictionary for JSON conversion."""
        return {
            "task_id": self.task_id,
            "pet_id": self.pet_id,
            "title": self.title,
            "task_type": self.task_type,
            "start_time": self.start_time.isoformat(),
            "duration_minutes": self.duration_minutes,
            "priority": self.priority,
            "is_completed": self.is_completed,
            "frequency": self.frequency
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Task':
        """Instantiates a valid Task element from primitive dictionary inputs."""
        return cls(
            task_id=data["task_id"],
            pet_id=data["pet_id"],
            title=data["title"],
            task_type=data["task_type"],
            start_time=datetime.fromisoformat(data["start_time"]),
            duration_minutes=data["duration_minutes"],
            priority=data.get("priority", "Normal"),
            is_completed=data.get("is_completed", False),
            frequency=data.get("frequency", "Once")
        )


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

    def to_dict(self) -> dict:
        """Serializes Pet metadata and child tasks array to primitive elements."""
        return {
            "pet_id": self.pet_id,
            "name": self.name,
            "species": self.species,
            "age": self.age,
            "medical_notes": self.medical_notes,
            "tasks": [t.to_dict() for t in self.tasks]
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Pet':
        """Constructs a Pet record alongside its complete tree of child Task dataclasses."""
        pet = cls(
            pet_id=data["pet_id"],
            name=data["name"],
            species=data["species"],
            age=data["age"],
            medical_notes=data.get("medical_notes", [])
        )
        for task_data in data.get("tasks", []):
            pet.add_task(Task.from_dict(task_data))
        return pet


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

    def save_to_json(self, filename: str = "data.json") -> None:
        """Serializes the complete profile entity tree directly into a local JSON asset file."""
        payload = {
            "owner_id": self.owner_id,
            "name": self.name,
            "pets": {pet_id: pet.to_dict() for pet_id, pet in self.pets.items()}
        }
        with open(filename, "w") as f:
            json.dump(payload, f, indent=4)

    def load_from_json(self, filename: str = "data.json") -> bool:
        """Reconstructs the multi-pet tree framework from a local tracking asset. Returns success status."""
        if not os.path.exists(filename):
            return False
        try:
            with open(filename, "r") as f:
                data = json.load(f)
            self.owner_id = data["owner_id"]
            self.name = data["name"]
            self.pets = {pet_id: Pet.from_dict(pet_data) for pet_id, pet_data in data.get("pets", {}).items()}
            return True
        except Exception:
            return False


class Scheduler:
    """The central brain that retrieves, organizes, and manages tasks across pets."""
    def __init__(self):
        self.global_tasks: List[Task] = []

    def get_daily_agenda(self, owner: Owner, target_date: date) -> List[Task]:
        """Retrieves and chronologically organizes tasks for an owner's pets on a given date."""
        tasks = owner.get_all_tasks()
        self.global_tasks = tasks
        # Normalize comparison to ensure tasks match the requested calendar day
        daily_tasks = [t for t in tasks if t.start_time.date() == target_date]
        return self.sort_by_time(daily_tasks)

    def sort_by_time(self, tasks: List[Task]) -> List[Task]:
        """Sorts a collection of tasks chronologically by their start time."""
        return sorted(tasks, key=lambda x: x.start_time)

    def filter_tasks(self, tasks: List[Task], pet_id: Optional[str] = None, is_completed: Optional[bool] = None) -> List[Task]:
        """Filters a target subset of tasks by pet identification or completeness state flags."""
        filtered = tasks
        if pet_id is not None:
            filtered = [t for t in filtered if t.pet_id == pet_id]
        if is_completed is not None:
            filtered = [t for t in filtered if t.is_completed == is_completed]
        return filtered

    def detect_conflicts(self, owner: Owner, new_task: Task) -> List[Task]:
        """Identifies time-boundary block collisions with existing tasks assigned to the same pet."""
        conflicts = []
        all_tasks = owner.get_all_tasks()
        
        for existing_task in all_tasks:
            if existing_task.task_id == new_task.task_id:
                continue
                
            if existing_task.pet_id == new_task.pet_id:
                # Normalize dates to handle strict, date-agnostic daily time block matching
                base_date = date.today()
                
                start_a = datetime.combine(base_date, new_task.start_time.time())
                end_a = start_a + timedelta(minutes=new_task.duration_minutes)
                
                start_b = datetime.combine(base_date, existing_task.start_time.time())
                end_b = start_b + timedelta(minutes=existing_task.duration_minutes)
                
                # Absolute Intersection Formula
                if start_a < end_b and start_b < end_a:
                    conflicts.append(existing_task)
                    
        return conflicts

    def handle_recurring_generation(self, completed_task: Task) -> Task:
        """Generates a matching future task instance shifted ahead precisely by its frequency interval."""
        interval = timedelta(days=1) if completed_task.frequency == "Daily" else timedelta(weeks=1)
        next_start = completed_task.start_time + interval
        next_id = f"{completed_task.task_id}-rev"
        
        return Task(
            task_id=next_id,
            pet_id=completed_task.pet_id,
            title=completed_task.title,
            task_type=completed_task.task_type,
            start_time=next_start,
            duration_minutes=completed_task.duration_minutes,
            priority=completed_task.priority,
            frequency=completed_task.frequency
        )