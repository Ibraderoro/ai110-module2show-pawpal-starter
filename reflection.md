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

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
