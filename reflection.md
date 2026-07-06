# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

My initial architecture utilizes a strictly decoupled, "CLI-first" layout designed to isolate data models from the central scheduling orchestration logic. The design includes four core classes:

- **`Pet` (Python Dataclass):** Functions as a pure, decoupled data container housing attributes for an individual pet profile, including identity, species traits, age, and an array for long-term medical alerts.
- **`Task` (Python Dataclass):** Acts as a structural contract representing a single care event (such as feedings, walks, medications, or appointments) bound by discrete execution windows (start_time), time allocations (duration_minutes), and evaluation weights (priority).
- **`Owner` (Domain Entity):** Handles profile grouping constraints. It uses a clean lookup directory (Dict[str, Pet]) to associate, manage, and retrieve unique pet profiles under an owner's account.
- **`Scheduler` (Algorithmic Control Layer):** The central computational engine. It acts as the gatekeeper for task registrations and contains the stubs meant for executing chronological list sorting, timeline conflict checks, and agenda filtering.

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.
Yes. During architectural brainstorming with my AI collaborator, we analyzed the workflow of the conflict detection stub (`detect_conflicts`). The original plan was to check a new task against a flat, global history array (`global_tasks`).

However, we realized that doing a raw linear scan across a massive historical backlog would create an inefficient $O(n)$ verification footprint per task, turning batch lookups into an $O(n^2)$ bottleneck. To fix this before writing the implementation, I modified the design intent of the `Scheduler` to group and partition task vectors by target date and specific `pet_id` boundaries. This localizes the sorting and conflict loops to relevant subsets, preventing long-term scaling lag.

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

- Our conflict handler uses explicit, mathematical time-block overlap constraints rather than plain, loose keyword lookups or time match checks. However, a key tradeoff is that it flags a conflict and prompts the user to resolve it, rather than automatically sliding tasks around into alternative open slots. This design choice prevents the app from shifting strict, real-world care routines (like exact medication times) without the owner's knowledge, keeping schedule coordination clear and predictable.

---

## 3. AI Collaboration

**a. How you used AI**

- I utilized my AI coding assistant as a specialized technical peer across separate, phase-restricted chat contexts. It was highly effective for drafting initial code patterns, setting up the boilerplate for the Streamlit two-column grid, and isolating mathematical edge cases for the overlap formula.

- The most helpful prompts were highly specific, constraint-driven inquiries such as: *"Given an Owner object that aggregates nested Pet lists, what is the most clean, pythonic way to filter and sort their combined Task references chronologically by their datetime attributes using a lambda function?"*

**b. Judgment and verification**

- A key moment of human intervention occurred during Phase 6 when implementing the task conflict warnings. The AI initially suggested keeping the conflict detection alert isolated within the task entry form submission hook. However, upon testing, I noticed that Streamlit's immediate invocation of `st.rerun()` upon form submission wiped the warning banner from the screen before a user could see it.

- I rejected the local form-level warning design and refactored the layout to execute `Scheduler.detect_conflicts()` dynamically during the schedule compilation loop. This allowed me to mount inline error indicators (`st.error`) right on the conflicting timeline rows, making the UI robust and intuitive.

---

## 4. Testing and Verification

**a. What you tested**

- Using `pytest`, I built an automated test suite verifying four structural pillars:
    1. **Chronological Sorting (`test_chronological_task_sorting`):** Confirmed tasks added out of order successfully sort from earliest to latest.
    2. **Boundary Isolation (`test_empty_pet_agenda`):** Verified that pets with zero care activities return a clean, empty list instead of crashing.
    3. **Interval Intersection (`test_conflict_detection_window_overlap`):** Validated that the overlap formula correctly flags tasks intersecting an active timeframe.
    4. **Temporal Rollforward (`test_recurrence_logic_daily_rollforward`):** Ensured that daily tasks auto-generate a matching task precisely one day forward using `timedelta`.

- These tests were crucial for ensuring that optimizing our interface elements wouldn't inadvertently break our backend business logic.

**b. Confidence**

- I am completely confident (5/5 stars) in the scheduler's foundational mechanics. The test suite runs deterministically in 0.01 seconds, and data updates flow correctly between our state structures and the UI.

- If given more time, the next edge cases I would target include multi-day task durations that cross past midnight, handling shifts across daylight saving time (DST) boundaries using timezone-aware datetimes, and validating cascading dependency paths (e.g., preventing a "Post-Medication Feeding" task from being marked complete until its parent "Administer Meds" task is finalized).

---

## 5. Reflection

**a. What went well**

- I am highly satisfied with the seamless integration achieved between the object-oriented backend and the Streamlit view layer. Seeing the scheduler automatically sort out-of-order tasks and display real-time conflict warnings directly on the timeline rows—without degrading performance or dropping persistent data states—is rewarding.

**b. What you would improve**

- In a subsequent engineering sprint, I would redesign the persistence engine. While `st.session_state` is perfect for local prototyping, a production-grade application should back up data to a lightweight embedded database (like SQLite) or an external database. This would ensure that pet profiles, historical completed logs, and future recurring cycles survive browser refreshes and application restarts.

**c. Key takeaway**

- The biggest takeaway from this project is that as a human lead architect, clear communication and strict constraint setting are everything when working with AI. AI is incredibly efficient at writing data structures and generating boilerplate components, but it is the human developer’s responsibility to maintain a decoupled architecture, trace execution control flows, and ensure that the user interface maps cleanly to the true backend state.
