import os
import sys
from datetime import date, timedelta

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pawpal_system import Owner, Pet, Task, Scheduler


def make_scheduler():
    owner = Owner("Jordan")
    dog = Pet("Buddy", "dog")
    cat = Pet("Mimi", "cat")
    owner.add_pet(dog)
    owner.add_pet(cat)
    return owner, dog, cat, Scheduler(owner)


def test_mark_complete_changes_status():
    task = Task("Walk", "09:00")
    assert task.completed is False
    task.mark_complete()
    assert task.completed is True


def test_adding_task_increases_pet_task_count():
    pet = Pet("Buddy")
    pet.add_task(Task("Walk", "09:00"))
    assert len(pet.tasks) == 1
    pet.add_task(Task("Feed", "10:00"))
    assert len(pet.tasks) == 2


def test_sort_by_time_is_chronological_across_pets():
    _, dog, cat, sched = make_scheduler()
    dog.add_task(Task("Evening walk", "18:00"))
    cat.add_task(Task("Breakfast", "08:00"))
    dog.add_task(Task("Lunch", "12:30"))
    times = [t.time for t in sched.sort_by_time()]
    assert times == ["08:00", "12:30", "18:00"]


def test_daily_task_creates_next_day_task_when_completed():
    _, dog, _, sched = make_scheduler()
    task = Task("Feed", "08:00", frequency="daily")
    dog.add_task(task)
    nxt = sched.mark_task_complete(task)
    assert task.completed is True
    assert nxt.due_date == task.due_date + timedelta(days=1)
    assert nxt.completed is False
    assert len(dog.tasks) == 2


def test_one_time_task_does_not_recur():
    _, dog, _, sched = make_scheduler()
    task = Task("Vet", "13:00", frequency="once")
    dog.add_task(task)
    assert sched.mark_task_complete(task) is None
    assert len(dog.tasks) == 1


def test_conflict_detection_flags_same_time():
    _, dog, cat, sched = make_scheduler()
    dog.add_task(Task("Breakfast", "08:00"))
    cat.add_task(Task("Medication", "08:00"))
    warnings = sched.detect_conflicts()
    assert len(warnings) == 1
    assert "08:00" in warnings[0]


def test_no_conflict_when_times_differ():
    _, dog, cat, sched = make_scheduler()
    dog.add_task(Task("Breakfast", "08:00"))
    cat.add_task(Task("Medication", "09:00"))
    assert sched.detect_conflicts() == []


def test_pet_with_no_tasks_gives_empty_schedule():
    _, _, _, sched = make_scheduler()
    assert sched.sort_by_time() == []
    assert sched.todays_schedule() == []


def test_filter_by_pet_and_status():
    _, dog, cat, sched = make_scheduler()
    done = Task("Walk", "07:00")
    done.mark_complete()
    dog.add_task(done)
    dog.add_task(Task("Feed", "08:00"))
    cat.add_task(Task("Play", "09:00"))
    assert len(sched.filter_tasks(pet_name="Buddy")) == 2
    assert len(sched.filter_tasks(completed=True)) == 1
    assert len(sched.filter_tasks(pet_name="Buddy", completed=False)) == 1
