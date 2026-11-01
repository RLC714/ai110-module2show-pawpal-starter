# 🐾 PawPal+

PawPal+ is a pet care scheduling app. Owners add pets, schedule care tasks (feedings, walks, medications, appointments), and get a sorted schedule with conflict warnings and automatic recurring tasks.

## System Overview

| Class | Responsibility |
|-------|----------------|
| `Task` | One activity: description, time (`HH:MM`), frequency, due date, completion status. Can `mark_complete()` and create its `next_occurrence()`. |
| `Pet` | Pet details plus its list of tasks (`add_task`, `remove_task`, `list_tasks`). |
| `Owner` | Owner details and a list of pets; can gather all tasks across pets. |
| `Scheduler` | The "brain": retrieves, sorts, filters, and manages tasks across all of an owner's pets. |

UML diagrams: `diagrams/uml_draft.mmd` (initial) and `diagrams/uml_final.mmd` (matches final code).

## Features

- **Sorting by time:** `Scheduler.sort_by_time()` orders tasks by due date, then `HH:MM`.
- **Filtering:** `Scheduler.filter_tasks(pet_name, completed)` filters by pet and/or completion status.
- **Conflict detection:** `Scheduler.detect_conflicts()` returns warning messages when incomplete tasks share the same date and time (same or different pets). It warns instead of crashing.
- **Recurring tasks:** `Scheduler.mark_task_complete()` completes a task and, for `daily` or `weekly` tasks, adds the next occurrence using `timedelta` (today + 1 or + 7 days).
- **Today's schedule:** `Scheduler.todays_schedule()` returns today's pending tasks in time order.

## Smarter Scheduling

| Feature | Method | Behavior |
|---------|--------|----------|
| Sorting | `Scheduler.sort_by_time()` | Chronological by `(due_date, time)` across all pets |
| Filtering | `Scheduler.filter_tasks()` | By pet name, completion status, or both |
| Conflict detection | `Scheduler.detect_conflicts()` | Exact date + time matches among incomplete tasks; returns warning strings |
| Recurring tasks | `Scheduler.mark_task_complete()` / `Task.next_occurrence()` | Daily creates tomorrow's task, weekly creates next week's |

## Demo Walkthrough

**UI features (Streamlit):** set the owner name, add pets, schedule tasks (pet, description, time, frequency), filter by pet or status, mark tasks complete.

**Example workflow:** add a pet (Buddy) → schedule "Breakfast" at 08:00 daily → schedule "Medication" for another pet at 08:00 → the schedule appears sorted by time with a conflict warning → mark Breakfast complete → tomorrow's Breakfast is created automatically.

**Key Scheduler behaviors shown:** sorting by time, conflict warnings (`st.warning`), filtering, and recurring task creation.

### Sample Output

Run `python main.py`:

```

Today's Schedule (sorted by time)
---------------------------------
  [ ] 08:00  Buddy  Breakfast (daily, 2026-11-01)
  [ ] 08:00  Mimi   Medication (once, 2026-11-01)
  [ ] 13:30  Mimi   Vet appointment (once, 2026-11-01)
  [ ] 18:00  Buddy  Evening walk (daily, 2026-11-01)

Conflict check
--------------
  WARNING: conflict on 2026-11-01 at 08:00 -> Buddy: Breakfast, Mimi: Medication

Filter: Mimi's tasks
--------------------
  [ ] 08:00  Mimi   Medication (once, 2026-11-01)
  [ ] 13:30  Mimi   Vet appointment (once, 2026-11-01)

Completing 'Breakfast' (daily) ...
  Next occurrence created for 2026-11-02 at 08:00

Filter: completed tasks
-----------------------
  [x] 08:00  Buddy  Breakfast (daily, 2026-11-01)

Filter: Buddy's pending tasks
-----------------------------
  [ ] 18:00  Buddy  Evening walk (daily, 2026-11-01)
  [ ] 08:00  Buddy  Breakfast (daily, 2026-11-02)
```

## Getting Started

```bash
pip install -r requirements.txt
python main.py            # CLI demo
streamlit run app.py      # web app
python -m pytest          # run tests
```

## Testing PawPal+

Command: `python -m pytest`

Tests (in `tests/test_pawpal.py`) cover:
- Task completion changes status
- Adding tasks increases a pet's task count
- Sorting returns chronological order across multiple pets
- Daily recurrence creates a next-day task; one-time tasks do not recur
- Conflict detection flags duplicate times and stays quiet otherwise
- Edge cases: a pet with no tasks, filtering by pet and status

Test output:

```
PASTE YOUR python -m pytest OUTPUT HERE
```

**Confidence Level:** ⭐⭐⭐⭐ (4/5). Core behaviors and key edge cases pass; overlapping durations and time-zone handling are not covered.
