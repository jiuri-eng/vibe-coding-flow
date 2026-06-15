# Session Handoff Protocol

## Overview

When context budget is exhausted or context collapse is detected, the current session must hand off to a new session. This protocol defines the **self-contained handoff package** format that enables a new session to continue work without loading the full vibe-coding-flow skill.

**Core principle**: The handoff package IS the mini-skill. The new session reads ONE file (~500-800 tokens) and knows exactly what to do, what's been decided, and what constraints apply — without needing the 10KB+ SKILL.md.

---

## Handoff Package Format

Save as `docs/handoff-[stage]-[task]-[timestamp].md` (e.g., `docs/handoff-S6-T12-20260615.md`).

```markdown
# Session Handoff Package
**Generated**: [timestamp] | **From**: Stage [N], Task [T-xx]
**Reason**: [Context budget 85% / Context collapse detected / User requested]
**Project**: [name] | **Tier**: [S/M/L/XL] | **Path**: [absolute project path, e.g. D:\projects\my-app]

---

## 1. Current State (一句话)
[One sentence describing exactly where we are]

## 2. Progress Map
```
Completed: T-01 ~ T-11 (11/30 done)
Current:  T-12 — User auth middleware (IN PROGRESS)
Next:     T-13 — Session management
Remaining: T-14 ~ T-30 (19 tasks)
```

## 3. Key Decisions (Max 10)
No context, no explanation — just the decision and the one-line rationale:

1. localStorage persistence → No IndexedDB (MVP simplicity)
2. bcrypt cost=12 → Balance: fast enough for dev, secure for prod
3. No OAuth for MVP → Explicitly excluded in S1
4. CSS: vanilla, no framework → From S3 architecture decision
5. API: REST, not GraphQL → Team familiarity
6. ...
7. ...
8. ...
9. ...
10. ...

## 4. Key Constraints (Max 10)
Must-follow rules extracted from CLAUDE.md / .cursorrules / previous stages:

1. Function length < 50 lines
2. Nesting depth <= 4
3. No new npm dependencies without architecture review
4. All user input → textContent (never innerHTML)
5. No console.log in production code
6. Error handling: try-catch with user-facing message
7. CSS: BEM naming convention
8. Tests: minimum 1 test per exported function
9. Commit message: "feat/fix/chore: [description]"
10. ...

## 5. Working Instructions (Mini-Skill, ~300 tokens)
Extracted from vibe-coding-flow for THIS stage and project type.
The new session follows these WITHOUT loading the full skill:

### Per-Task Loop
1. Read task from docs/05-todo.md
2. Select prompt template (T-1 for features, T-9 for tests)
3. Implement → Test → L2 Task Gate (see below)
4. Verify acceptance criteria
5. Mark task complete in TODO
6. Context Checkpoint (after every 5 tasks): evaluate budget

### L2 Task Gate (abbreviated)
- L2-A Security: Check for secrets, injection, auth bypass
- L2-B Quality: Naming conventions, function length, no debug code
- L2-C Completeness: All AC met, dependencies honored, imports clean

### When Complete
- Update docs/05-todo.md status
- Generate Summary Card if budget > 60%
- Generate new Handoff Package if budget > 80%

## 6. Module Loading Decision (Platform-Aware)

This section adapts to the current platform (see `SKILL.md` Platform Auto-Detection). The receiving AI evaluates this matrix before loading any modules:

| Condition | Load modules? | Reason |
|-----------|:---:|--------|
| Continue Stage 6 tasks, same plan | NO | Handoff package is sufficient — self-contained work instructions above |
| Stage switch (e.g., S6→S7) | Partial | Load only `references/self-check.md` for L1-7 + L3 delivery gate |
| Architecture change needed | YES | Need full S3 methodology + tech-stacks.md |
| New PRD requirement added | YES | Need S2 PRD template |
| Bug fix only (1-2 tasks) | NO | Handoff package instructions + file context enough |
| > 10 tasks remaining | NO | Handoff package designed for this — split if needed |
| User explicitly asks to follow full methodology | YES | Explicit user intent |
| Implementing UI (Stage 6, no design doc) | Partial | Load `references/prompt-templates.md` T-5 (UI components) |
| Security audit needed | Partial | Load `references/security-checklist.md` only |
| Writing tests | NO | Handoff instructions + file context enough |

**Default**: DO NOT load core modules. Only load specific reference files when the matrix says YES/Partial.

### Platform-Specific Note

| Platform | "Module" Means |
|----------|---------------|
| WorkBuddy | Load via `Skill` tool |
| Cursor / Claude Code | Read the `.md` files directly from references/ |
| Codex CLI | Read `AGENTS.md` or references/ files |
| Generic AI | Read the sections you need from the conversation context |

## 7. Context Resume Blueprint
The new session should read these files in this order (all paths relative to **project `Path`** from header):

### Must Read (essential)
1. **This handoff package** (already in context)
2. `docs/05-todo.md` — Current task list and status
3. The source files for the CURRENT task only (not the whole project)

### Read On-Demand (only if needed)
4. `docs/03-architecture.md` — If unsure about file structure or data model
5. `docs/02-prd.md` — If unsure about functional requirements
6. `CLAUDE.md` or `.cursorrules` — If constraint questions arise

### Do NOT Read (unless explicitly needed)
- Earlier stage documents (S0, S1, S4) — decisions already in Section 3
- Completed task code — "what's built" is described in Progress Map
- Previous session conversation history — decisions already extracted here

## 8. Anti-Hallucination Checklist
The new session should verify these before making ANY code changes:

- [ ] Re-read Section 4 (Key Constraints) — no violations
- [ ] Re-read Section 3 (Key Decisions) — no contradictions
- [ ] Confirm current task number matches docs/05-todo.md
- [ ] Read ONLY the files listed in Section 7 "Must Read"
- [ ] If uncertain about architecture, read docs/03-architecture.md before guessing
- [ ] If the user says "that's not what we decided" → re-read Section 3

---

**End of Handoff Package. The next session starts from Section 7.**
```

---

## Handoff Package Size Budget

The package MUST fit within **800 tokens** (excluding template markup). This is ~10% of a typical context window — leaving 90% for actual work.

| Section | Token Budget |
|---------|:---:|
| Current State + Progress Map | ~50 |
| Key Decisions (10 items) | ~200 |
| Key Constraints (10 items) | ~150 |
| Working Instructions | ~300 |
| Skill Loading Decision | ~80 |
| Context Resume Blueprint | ~80 |
| Anti-Hallucination Checklist | ~40 |

**If package exceeds 800 tokens**: Reduce Key Decisions/Constraints to top 8, trim Working Instructions.

---

## When to Generate Handoff Package

| Trigger | Action |
|---------|--------|
| Context budget > 80% (from context-budget.md) | **Mandatory** — generate and STOP |
| L4 AP-2 Context Collapse detected | Generate and recommend new session |
| User says "let's continue in a new chat" | Generate on demand |
| Stage 6: > 15 tasks remaining for XL project | **Pre-generate** at task 10 as insurance |
| User expresses frustration about repetition | Generate proactively |

---

## Handoff Package Location & Naming

```
docs/
  handoff-S6-T12-20260615.md    ← Current active handoff
  handoff-S6-T05-20260614.md    ← Previous (keep for audit)
  handoff-S5-20260613.md        ← Previous stage handoff
```

**Naming convention**: `handoff-[stage]-[task]-[YYYYMMDD].md`
- Omit `[task]` for non-Stage-6 handoffs
- Keep previous handoffs for audit trail

---

## Receiving a Handoff (New Session Protocol)

When a new session opens and the user (or system) references a handoff package:

1. **Read the handoff file** — this is your entry point
2. **Set workspace to project path** — use the `Path` from header metadata as working directory
3. **Evaluate Skill Loading Decision** (Section 6) — decide what to load
4. **Read Must-Read files** (Section 7) — only these, relative to project path
5. **Run Anti-Hallucination Checklist** (Section 8) — before ANY code
6. **Pick up from Current State** (Section 1) — continue, don't redo
7. **Follow Working Instructions** (Section 5) — these are your rules

---

## Handoff Package Example (for reference)

See `example-project/docs/handoff-S6-T05-example.md` for a filled-in example.
