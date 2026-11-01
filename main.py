"""CLI demo for PawPal+ (backend check before the UI)."""
from pawpal_system import Owner, Pet, Task, Scheduler


def show(title, tasks):
    print(f"\n{title}")
    print("-" * len(title))
    if not tasks:
        print("  (no tasks)")
    for t in tasks:
        mark = "x" if t.completed else " "
        print(f"  [{mark}] {t.time}  {t.pet_name:<6} {t.description} ({t.frequency}, {t.due_date})")


def main():
    owner = Owner("Jordan")
    buddy = Pet("Buddy", "dog")
    mimi = Pet("Mimi", "cat")
    owner.add_pet(buddy)
    owner.add_pet(mimi)

    # Added out of order on purpose
    buddy.add_task(Task("Evening walk", "18:00", "daily"))
    buddy.add_task(Task("Breakfast", "08:00", "daily"))
    mimi.add_task(Task("Medication", "08:00", "once"))   # conflicts with Breakfast
    mimi.add_task(Task("Vet appointment", "13:30", "once"))

    scheduler = Scheduler(owner)

    show("Today's Schedule (sorted by time)", scheduler.todays_schedule())

    print("\nConflict check")
    print("--------------")
    for w in scheduler.detect_conflicts() or ["No conflicts."]:
        print(" ", w)

    show("Filter: Mimi's tasks", scheduler.filter_tasks(pet_name="Mimi"))

    print("\nCompleting 'Breakfast' (daily) ...")
    breakfast = buddy.tasks[1]
    nxt = scheduler.mark_task_complete(breakfast)
    print(f"  Next occurrence created for {nxt.due_date} at {nxt.time}")

    show("Filter: completed tasks", scheduler.filter_tasks(completed=True))
    show("Filter: Buddy's pending tasks", scheduler.filter_tasks(pet_name="Buddy", completed=False))


if __name__ == "__main__":
    main()
