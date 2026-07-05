from dataclasses import dataclass, field
from datetime import datetime, date, timedelta
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
        tasks = owner.get_all_tasks()
        self.global_tasks = tasks
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
                # Mathematical Overlap Equation: StartA < EndB and StartB < EndA
                if new_task.start_time < existing_task.end_time and existing_task.start_time < new_task.end_time:
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