# PawPal+ Reflection

## 1. System Design

**Three core user actions:** (1) add a pet, (2) schedule a care task for a pet, (3) view today's schedule in time order with any conflicts flagged.

### 1a. Initial design
I chose four classes. `Task` holds one activity (description, time, frequency, completion). `Pet` holds its details and a list of tasks. `Owner` holds multiple pets and can gather all their tasks. `Scheduler` takes an owner and does the thinking: retrieving, sorting, and managing tasks across all pets. I used dataclasses for `Task`, `Pet`, and `Owner`, and kept `Scheduler` a regular class because it holds behavior rather than data.

### 1b. Design changes
After reviewing my skeleton I made three changes: I added `pet_name` to `Task` so the scheduler can tell which pet a task belongs to (needed for conflict messages and for adding recurring tasks to the right pet); I added `due_date` alongside `time` so recurring tasks could move to a new day; and I added `Owner.get_pet()` so the scheduler can find the right pet when a recurring task is completed.

## 2. Scheduling Logic

### 2a. Features
Sorting by date then `HH:MM`, filtering by pet and status, conflict warnings, and daily/weekly recurrence.

### 2b. Tradeoffs
The conflict detector only flags tasks with the exact same date and time. It does not check overlapping durations (for example, a 30-minute walk at 08:00 and a feeding at 08:15). This keeps the code simple and readable, and it is reasonable because tasks here have no duration field. The cost is that near-overlaps go unnoticed.

## 3. AI Collaboration

**Most effective AI features:** Chat for brainstorming classes and drafting the Mermaid diagram, and agent/edit mode for edits that touched several files at once, such as recurrence changing both `Task` and `Scheduler`.

**Suggestion I rejected or modified:** The AI suggested a single-line, heavily nested comprehension for conflict detection. It was shorter but harder to read, so I kept a clearer loop that groups tasks by `(date, time)` in a dictionary.

**Separate chat sessions:** Using a new chat for each phase (design, implementation, algorithms, testing) kept the context focused, so suggestions stayed relevant to the current task and did not drift into earlier design decisions.

**Being the lead architect:** AI is fast at producing plausible code, but it does not know what my system should be. My job was to set the scope, compare every suggestion against my UML and the requirements, and say no to extra complexity. I verified behavior with the CLI demo and pytest instead of trusting that the output looked right.

## 4. Testing and Verification
I verified the backend first with `main.py`, then with pytest tests for sorting, recurrence, conflicts, filtering, and empty-pet edge cases. Confidence: 4/5.
