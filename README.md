# AICodeQuest

A competitive programming game where humans and AI battle to understand, inject, and detect bugs in code.

---

## Architecture

```
Game/
├── client/                 # React frontend (Vite)
│   ├── src/
│   │   ├── Pages/         # Login, Home, CodeEditor
│   │   ├── Components/    # Navbar, LeaderBoard
│   │   ├── styles/        # CSS stylesheets
│   │   └── utils/         # Helper functions
│   └── public/            # Static assets
│
└── server/                # Python Flask backend
    ├── routes/            # API endpoints (start_game, get_code, submit_turn, get_results)
    ├── db/                # MongoDB connection
    ├── models/            # Session data model
    ├── game/              # Core logic (scorer, validator, state)
    ├── ai/                # Groq LLM integration
    ├── piston/            # Code execution engine
    ├── config/            # Game constants
    ├── tests/             # Test cases per level (A1-A4)
    └── questions/         # Problem code files
```

---

## Flow

```
1. LOGIN → User enters username → Session created in MongoDB

2. HOME → View stats, leaderboard → Start game

3. GAME LOOP (5 questions: A1×2, A2×1, A3×1, A4×1):

   Turn 0 (DEFENSE):
   ├── AI injects bug into clean code
   ├── Human receives buggy code
   ├── Human fixes the bug
   ├── Code tested against test cases
   └── Winner: Human (all pass) or AI (any fail)

   Action: [INJECT] → Turn 1  |  [SKIP] → Next question

   Turn 1 (ATTACK):
   ├── Human injects subtle bug into clean code
   ├── AI attempts to detect and fix
   ├── AI's fix tested against test cases
   └── Winner: AI (all pass) or Human (any fail)

   Action: [DETECT] → Next question, reset to Turn 0

4. RESULTS → Final scores, leaderboard update
```

---

## Tech Used

| Layer | Technology |
|-------|------------|
| Frontend | React 19, Vite 7, Tailwind CSS, Monaco Editor |
| Backend | Flask (Python), Flask-CORS |
| Database | MongoDB |
| AI | Groq API (Llama 3.1/3.3/4 models) |
| Code Execution | Piston API (sandboxed execution) |
| Language | C (extensible) |

---

## Prompts Used (Condensed)

### Bug Injection Prompts

**A1 - Syntax Errors:**
> Inject simple, surface-level bugs. Examples: alter arithmetic/comparison/boolean operators, modify loop boundaries (off-by-one), change indices, replace variable names, alter return values.

**A2 - Semantic Errors:**
> Inject logic-level bugs preserving syntax. Examples: incorrect conditions that fail on edge cases, misplaced statements in/out of loops, wrong variable initialization, incorrect termination conditions.

**A3 - Algorithmic Errors:**
> Inject algorithmic bugs. Examples: wrong recurrence/invariant, broken optimal substructure, greedy where DP needed, wrong data structure, incorrect recursion reduction.

**A4 - AI-Hallucination Errors:**
> Inject LLM-style mistakes. Examples: assume unstated preconditions, handle only typical cases, apply familiar patterns incorrectly, hard-code solutions, simplify conditions aggressively.

### Bug Detection Prompt
> Fix the bug in this code. Output ONLY the corrected code without any formatting, explanations, or backticks. Fix only the bug, don't refactor.

---

## Design Principles

1. **Separation of Concerns** - Distinct modules for AI, validation, scoring, and state management
2. **Resilience** - Automatic model fallback on rate limits; sandboxed code execution
3. **Stateful Sessions** - MongoDB tracks all game progress, code history, and turns
4. **Test-Driven Validation** - Deterministic scoring via predefined test cases
5. **Progressive Difficulty** - Four levels from syntax to AI-hallucination bugs
6. **Configuration-Driven** - Levels, questions, and points defined in constants

---

## Example Gameplay Scenario

**Question:** Add two numbers (A1 Level)

**Original Code:**
```c
#include <stdio.h>
int main() {
    int num1, num2;
    scanf("%d %d", &num1, &num2);
    printf("%d", num1 + num2);
    return 0;
}
```

**Turn 0 - Defense:**
1. AI injects bug: `num1 + num2` → `num1 - num2`
2. Human receives buggy code
3. Human spots the bug and fixes it back to `+`
4. Tests run: Input `5 10` → Expected `15` → Output `15` → PASS
5. Human wins +1 point

**Turn 1 - Attack (if INJECT selected):**
1. Human receives clean code
2. Human injects subtle bug: `num1 + num2` → `num1 * num2`
3. AI analyzes and attempts fix
4. AI corrects to `num1 + num2`
5. Tests pass → AI wins +1 point

---

## Game Mechanics

| Mechanic | Description |
|----------|-------------|
| **Turns** | Alternating Defense (Turn 0) and Attack (Turn 1) |
| **Scoring** | +1 point per turn won (both Human and AI) |
| **Levels** | A1 (Syntax), A2 (Semantic), A3 (Algorithmic), A4 (AI-Hallucination) |
| **Questions** | 5 total: A1×2, A2×1, A3×1, A4×1 |
| **Validation** | Code executed via Piston API against predefined test cases |
| **Win Condition** | All test cases must pass to win a turn |
| **Actions** | INJECT (go to attack), SKIP (next question), DETECT (after attack) |

---

## AI Bug Generation

The AI uses **Groq's LLM API** with specialized prompts per difficulty level:

| Level | Bug Type | Characteristics |
|-------|----------|-----------------|
| A1 | Syntax | Obvious, surface-level (wrong operators, off-by-one) |
| A2 | Semantic | Logic errors, correct syntax but wrong behavior |
| A3 | Algorithmic | Structural issues (wrong approach, broken invariants) |
| A4 | Hallucination | LLM-typical mistakes (assumptions, overgeneralization) |

**Model Rotation:** `llama-3.1-8b-instant` → `llama-3.3-70b-versatile` → `llama-4-maverick-17b-128e-instruct` → `groq/compound`

**Parameters:** Temperature 0.2 (deterministic), Timeout 15s

**Constraints:** Output only modified code, no explanations, no markdown, no comments about changes.
