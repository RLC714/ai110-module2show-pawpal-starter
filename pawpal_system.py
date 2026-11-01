"""PawPal+ logic layer: Task, Pet, Owner, Scheduler."""
from dataclasses import dataclass, field
from datetime import date, timedelta
from typing import List, Optional

FREQUENCY_DAYS = {"daily": 1, "weekly": 7}


@dataclass
class Task:
    """A single pet-care activity."""
    description: str
    time: str  # "HH:MM", 24-hour
    frequency: str = "once"  # "once", "daily", or "weekly"
    due_date: date = field(default_factory=date.today)
    completed: bool = False
    pet_name: str = ""

    def mark_complete(self) -> None:
        """Mark this task as completed."""
        self.completed = True

    def next_occurrence(self) -> Optional["Task"]:
        """Return a fresh task for the next occurrence, or None if one-time."""
        days = FREQUENCY_DAYS.get(self.frequency)
        if days is None:
            return None
        return Task(
            description=self.description,
            time=self.time,
            frequency=self.frequency,
            due_date=self.due_date + timedelta(days=days),
            pet_name=self.pet_name,
        )


@dataclass
class Pet:
    """A pet and its list of tasks."""
    name: str
    species: str = "dog"
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Attach a task to this pet."""
        task.pet_name = self.name
        self.tasks.append(task)

    def remove_task(self, task: Task) -> None:
        """Remove a task from this pet."""
        self.tasks.remove(task)

    def list_tasks(self) -> List[Task]:
        """Return a copy of this pet's tasks."""
        return list(self.tasks)


@dataclass
class Owner:
    """An owner who manages multiple pets."""
    name: str
    pets: List[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner."""
        self.pets.append(pet)

    def get_pet(self, name: str) -> Optional[Pet]:
        """Find a pet by name (case-insensitive)."""
        for pet in self.pets:
            if pet.name.lower() == name.lower():
                return pet
        return None

    def get_all_tasks(self) -> List[Task]:
        """Return every task across all pets."""
        return [t for pet in self.pets for t in pet.tasks]


class Scheduler:
    """The 'brain': retrieves, sorts, filters, and manages tasks across pets."""

    def __init__(self, owner: Owner):
        self.owner = owner

    def get_all_tasks(self) -> List[Task]:
        """Get all tasks from the owner's pets."""
        return self.owner.get_all_tasks()

    def sort_by_time(self, tasks: Optional[List[Task]] = None) -> List[Task]:
        """Sort tasks chronologically by due date, then HH:MM time."""
        tasks = self.get_all_tasks() if tasks is None else tasks
        return sorted(tasks, key=lambda t: (t.due_date, t.time))

    def filter_tasks(self, pet_name: Optional[str] = None,
                     completed: Optional[bool] = None) -> List[Task]:
        """Filter tasks by pet name and/or completion status."""
        result = self.get_all_tasks()
        if pet_name is not None:
            result = [t for t in result if t.pet_name.lower() == pet_name.lower()]
        if completed is not None:
            result = [t for t in result if t.completed == completed]
        return result

    def todays_schedule(self) -> List[Task]:
        """Return today's incomplete tasks in time order."""
        today = date.today()
        due = [t for t in self.get_all_tasks()
               if t.due_date == today and not t.completed]
        return self.sort_by_time(due)

    def detect_conflicts(self) -> List[str]:
        """Return warning messages for incomplete tasks at the same date and time."""
        slots = {}
        for t in self.get_all_tasks():
            if not t.completed:
                slots.setdefault((t.due_date, t.time), []).append(t)
        warnings = []
        for (d, tm), group in sorted(slots.items()):
            if len(group) > 1:
                names = ", ".join(f"{t.pet_name}: {t.description}" for t in group)
                warnings.append(f"WARNING: conflict on {d} at {tm} -> {names}")
        return warnings

    def mark_task_complete(self, task: Task) -> Optional[Task]:
        """Complete a task; if recurring, add the next occurrence to its pet."""
        task.mark_complete()
        nxt = task.next_occurrence()
        if nxt is not None:
            pet = self.owner.get_pet(task.pet_name)
            if pet is not None:
                pet.add_task(nxt)
        return nxt
