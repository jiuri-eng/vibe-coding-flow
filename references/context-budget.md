# Context Budget Management

## Overview

Large projects cause context window overload, leading to hallucinations and context collapse. This module provides proactive **token budget management** across all stages — preventing the problem before it happens, rather than only detecting it after (L4 AP-2).

**Core principle**: Every project has a finite context budget. Budget exceeded = forced mitigation (compress, split, or handoff). No exceptions.

---

## Project Size Tiers

| Tier | Scope | Token Budget | Stage 6 Tasks | Strategy |
|------|-------|-------------|:---:|----------|
| **S** | Single page / CLI tool | ~5000 | < 10 | Single session, full context OK |
| **M** | Small web app (3-5 pages) | ~8000 | 10-25 | Single session + summary cards |
| **L** | Medium app (5-10 pages, backend) | ~12000 | 25-50 | Multi-agent split recommended |
| **XL** | Large app (10+ pages, complex backend) | ~15000 | 50+ | Mandatory: multi-session + handoff |

**Budget scope**: Cumulative context from Stage 0 start to current point. Files read on-demand do not count — only what's in active conversation context.

---

## Per-Stage Budget Allocation

Percentage of total budget, allocated at Stage 1/2 planning:

| Stage | S | M | L | XL |
|-------|---|---|---|---|
| S0: Context | 10% | 8% | 5% | 5% |
| S1: Ideation | 8% | 7% | 5% | 3% |
| S2: PRD | 15% | 12% | 8% | 5% |
| S3: Architecture | 15% | 12% | 10% | 7% |
| S4: UI Design | 12% | 10% | 7% | 5% |
| S5: TODO | 10% | 8% | 5% | 5% |
| S6: Implementation | 20% | 33% | 50% | 60% |
| S7: Delivery | 10% | 10% | 10% | 10% |

**Rationale**: Stage 6 is the token hog. For XL projects, 60% of budget still needs multi-session.

---

## Context Checkpoint (Stage 6)

At the end of every **5 tasks** (or every task for XL), evaluate:

```
[Context Checkpoint] Tasks done: 12/30 | Est. tokens consumed: ~8000/12000 | Budget: 67%
```

### Decision Tree

```
Checkpoint triggered (every N tasks)
  │
  ├── Budget usage < 60%
  │     → Continue normally
  │
  ├── Budget usage 60-80%
  │     → Generate Summary Card (compact current state)
  │     → Present Summary Card at start of next task
  │     → Continue
  │
  ├── Budget usage 80-95%
  │     → FORK: Multi-Agent available? → Split remaining tasks to agents
  │     → FORK: No Multi-Agent? → Generate Session Handoff Package
  │     → Recommend: "Start new session with handoff package"
  │
  └── Budget usage > 95%
        → MANDATORY: Generate Session Handoff Package
        → STOP. Do not continue current session.
        → "Context budget exhausted. Please start new session with handoff package."
```

### Checkpoint Placement in Stage 6 Loop

```
For each task in TODO:
  └─ Intent → Template → Code → Test → L2 Gate → Verify → Commit
                                                        │
                                                    [Context Checkpoint]
                                                    (every N tasks)
                                                        │
                                              Continue / Compress / Handoff
```

---

## Summary Card Format

When budget hits 60-80%, generate this compact card as a **preamble** to the next task:

```markdown
## Context Summary Card (Budget: 72%)
**Project**: [name] | **Stage**: 6 | **Tasks**: 15/30 done
**Current**: Implementing T-16 (user auth middleware)
**Key Decisions** (last 10):
1. Using JWT with 24h expiry
2. Password hashing via bcrypt (cost=12)
3. No OAuth for MVP
...
**Key Constraints**:
- Function length < 50 lines
- No new npm dependencies without architecture review
- All inputs sanitized before DB write
**Next**: T-16 → T-17 → T-18
```

The receiving AI reads this card first, then the relevant source files — skipping all prior conversation history.

---

## Session Handoff Trigger

When budget exceeds 80% OR L4 AP-2 Context Collapse is detected:

1. **Pause** current task immediately
2. **Generate** full Session Handoff Package (see `references/session-handoff.md`)
3. **Save** to `docs/handoff-[timestamp].md`
4. **Output**: "Context budget critical. Handoff package saved to docs/handoff-[timestamp].md. Please start new session and reference this file."

---

## Budget Tracking (Internal)

The AI should maintain an internal budget counter during Stage 6. This is approximate — no need for exact token counting:

| Signal | Rough Token Estimate |
|--------|---------------------|
| Stage document read (PRD, Arch, etc.) | ~500-1000 each |
| Recent code changes (last 3 files) | ~300-800 each |
| Conversation history (per exchange) | ~200-500 each |
| Agent output (per response) | ~300-800 each |

**Rule of thumb**: After 15+ exchanges in Stage 6 with 3+ documents in context, you're likely at 60-70% budget.

---

## Integration with Other Modules

| Module | Integration Point |
|--------|------------------|
| `self-check.md` | L4 monitor includes budget tracking; Context Checkpoint added to Stage 6 loop |
| `session-handoff.md` | Budget > 80% triggers handoff package generation |
| `multi-agent-orchestration.md` | Budget 80-95% with agents available → split to agents |
| `token-efficiency.md` | Use compression BEFORE triggering handoff (reduce, don't avoid) |

---

## Quick Reference for AI

```
IF project_tier == "XL" AND stage == 6 AND tasks_remaining > 15:
    → Plan for 2-3 sessions minimum
    → Set checkpoint interval to 3 tasks
    → Pre-generate handoff template at task 10

IF budget > 80% AND user asks to continue:
    → Refuse. "Context budget critical. To avoid hallucinations, 
      please start new session with handoff package."
    → This is a PROFESSIONAL OBLIGATION, not optional.

IF budget > 60%:
    → Always present Summary Card before next task.
```
