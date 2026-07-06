# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

Paste a sample of your app's CLI or Streamlit output here so a reader can see what a generated plan looks like:

```
---

🐾 PAWPAL+ CLI SYSTEM INTERFACE - INITIALIZATION PROGRESS 🐾
============================================================

📅 Daily Care Agenda for Sunday, July 05, 2026:
------------------------------------------------------------
  08:00 — Morning Feeding (Rex)          (15 min) [High] -> ⏳ Pending
  09:00 — Morning Walk (Biscuit)         (30 min) [High] -> ⏳ Pending
  14:30 — Medication Administration (Rex) (10 min) [High] -> ⏳ Pending
------------------------------------------------------------
🎉 System Runtime Verification: SUCCESS!
============================================================

======================================================================
🧠 PAWPAL+ INTELLIGENT ALGORITHMIC TESTING GROUND 🧠
======================================================================

[Testing Sorting Engine] Adding mixed afternoon/morning entries out of chronological order...
Resulting sorted agenda order:
  ⏱️ 07:30 -> Critical Morning Meds
  ⏱️ 16:00 -> Afternoon Park Run

[Testing Overlap Analytics] Injecting a colliding task window...
⚠️ WARNING: Conflict detected! Your proposed time blocks collide with:
  ❌ Blocker: 'Afternoon Park Run' (16:00 - 16:40)

[Testing Recurrence Systems] Tracking a Daily Care loop completion...
  Current instance date: 2026-07-05 12:00
  🔄 Success! Rolled forward next cycle to: 2026-07-06 12:00

======================================================================
```

## 🧪 Testing PawPal+
To run the full suite of automated unit tests, open your terminal and execute the following standard test runner command:
```bash
# Run the full test suite:
python -m pytest -v

# Run with coverage:
pytest --cov

Our comprehensive test framework targets the core behavioral rules and edge cases of the scheduling engine to guarantee absolute system stability:

- Chronological Task Sorting (test_chronological_task_sorting): Verifies that the scheduler automatically organizes agendas from earliest to latest start times, even when care events are inputted out of order.

- Empty Agenda Isolation (test_empty_pet_agenda): Checks the system boundary by verifying that querying a new pet profile with zero logged activities safely handles an empty array baseline without crashing.

- Time-Window Overlap Conflict Detection (test_conflict_detection_window_overlap): Tests our mathematical validation formula ($\text{Start}_A < \text{End}_B \text{ and } \text{Start}_B < \text{End}_A$) to ensure it catches overlapping task slots for a pet and flags it for the user.Automated Recurrence Rollforward (test_recurrence_logic_daily_rollforward): Confirms that clicking a Daily task successfully marks it complete and generates a brand-new task instance shifted precisely one day into the future using timedelta.
```

Sample test output:

```
# Paste your pytest output here

================================= test session starts =================================
platform darwin -- Python 3.14.2, pytest-9.1.1, pluggy-1.6.0 -- /Users/salisuibrahim/dev/machine-learning/CodePath/ai110-module2show-pawpal-starter/.venv/bin/python3
cachedir: .pytest_cache
rootdir: /Users/salisuibrahim/dev/machine-learning/CodePath/ai110-module2show-pawpal-starter
collected 4 items                                                                     

tests/test_pawpal.py::test_chronological_task_sorting PASSED                    [ 25%]
tests/test_pawpal.py::test_empty_pet_agenda PASSED                              [ 50%]
tests/test_pawpal.py::test_conflict_detection_window_overlap PASSED             [ 75%]
tests/test_pawpal.py::test_recurrence_logic_daily_rollforward PASSED            [100%]

================================== 4 passed in 0.01s ==================================
```

## 📐 Smarter Scheduling

> Fill in once you've implemented scheduling logic.

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| **Task sorting** | `Scheduler.sort_by_time()` | Orders tasks chronologically by absolute `start_time` metadata. |
| **Filtering** | `Scheduler.filter_tasks()` | Segments lists by explicit target `pet_id` or `is_completed` states. |
| **Conflict handling** | `Scheduler.detect_conflicts()` | Implements overlap logic ($\text{Start}_A < \text{End}_B \text{ and } \text{Start}_B < \text{End}_A$) to prevent physical scheduling collisions. |
| **Recurring tasks** | `Scheduler.handle_recurring_generation()` | Automatically uses `timedelta` to roll completed daily/weekly tasks forward into the next occurrence slot. |

## 💾 Extended Capability: JSON Data Persistence

To ensure system reliability beyond volatile application memory bounds, PawPal+ incorporates an automated file-based database lifecycle subsystem:

  **Persistence Architecture:** Native serialization matrices are written into `pawpal_system.py` across `to_dict()` and `from_dict()` serialization definitions. This enables precise parsing of nested classes and handling of complex properties like ISO-formatted `datetime` strings.
  **Application Lifecycle Flow:** `app.py` acts as a non-blocking gatekeeper. Upon environment boot, the system checks for `data.json`. If found, it automatically restores the complete `Owner` structural ecosystem, full profile matrices, and active schedules. Any subsequent write actions cleanly overwrite the JSON storage file.
  **Modified Components:**
    * `pawpal_system.py`: Added explicit encoding, decoding, file loading, and serialization tracking handlers.
    * `app.py`: Integrated file synchronization checks across state instantiation hooks and state update points.

## Confidence Level

⭐ ⭐ ⭐ ⭐ ⭐ (5/5 Stars) — The core algorithmic engine provides fully deterministic data structure operations, mathematically absolute timeline block tracking, and robust execution sorting boundaries.

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. **Profile Management & Onboarding:** The owner's master profile is initialized on launch. Using the "Onboard a Pet" form in the left sidebar, users can register pet profiles (such as Mochi, Jest, or Papii) with their specific species and age metrics, writing them directly into the core state structures.

2. **Dynamic Task Configuration:** In the main panel, the user chooses which pet profile to update via a dropdown menu. They specify the care step details—including description titles, category blocks, custom duration metrics, urgency priority rankings, and recurrence frequencies (Once, Daily, or Weekly).

3. **Live Chronological Timeline Sort:** As tasks are logged, the backend invocation hooks parse them via Scheduler.sort_by_time(). The interface instantly rearranges the list elements chronologically by start time, bypassing addition order.

4. **Algorithmic Schedule Collision Warnings:** If an added task's time-window parameters overlap with a previously scheduled block for that pet, the timeline instantly catches it. The Scheduler.detect_conflicts() matrix flags the item with a prominent red ⚠️ Schedule Collision warning box detailing the exact overlapping blocker task.

5. **Contextual AI Explanations & Recurrence Rollover:** Every task row displays system logic notes explaining why it is placed there based on priority constraints. Pushing the "Mark Done" button updates state tracking dynamically; if configured as a "Daily" or "Weekly" routine, a new upcoming instance is projected into the future using timedelta.

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
