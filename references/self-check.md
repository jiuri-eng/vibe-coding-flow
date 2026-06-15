# Self-Check System: 4-Layer Automatic Quality Assurance

## Overview

The **Self-Check System** is an automatic quality gate that runs between "AI finishes work" and "presents result to user". It catches issues before they reach the user, reducing review cycles and preventing accumulated errors.

**Core principle**: The AI acts as its own QA engineer. Every deliverable passes through 4 layers of checks before being presented.

**Cost**: ~3-8 seconds of pure reasoning per check (no external tool calls needed). Does NOT increase user wait time — runs during the AI's response composition phase.

---

## Architecture

```
AI completes work output
        │
        ▼
┌───────────────────────────────────────┐
│         Self-Check Zone               │
│                                       │
│  L1 ─── Stage Gate (阶段门控)         │  ← Per stage
│  L2 ─── Task Gate (任务门控)          │  ← Per task (Stage 6)
│  L3 ─── Cross-Stage (跨阶段一致性)    │  ← Stage 5 & 7
│  L4 ─── Anti-Pattern (反模式检测)      │  ← Continuous monitoring
│                                       │
│              Decision                 │
│           ╱            ╲              │
│        PASS             FAIL          │
│     (交付+报告)      (修复/上报)       │
└───────────────────────────────────────┘
```

### When Each Layer Triggers

| Layer | Trigger Point | Frequency | Blocking? |
|-------|--------------|-----------|-----------|
| L1 Stage Gate | End of every Stage (0-7) | 6-8 times/project | Yes — fix before presenting |
| L2 Task Gate | After each task completion in Stage 6 | N times (N = #tasks) | Yes — fix before next task |
| L3 Cross-Stage | Stage 5 (TODO generation) + Stage 7 (delivery) | 2 times/project | Warning only |
| L4 Anti-Pattern | Continuous — after every user interaction | Ongoing | Adaptive — escalate if severe |

---

## L1: Stage Gate (阶段门控)

**Purpose**: Ensure each stage's deliverable is complete, template-compliant, and aligned with user intent before presenting for approval.

### Checklist by Stage

#### Stage 0: Context Setup Gate
```markdown
## L1-0 Check: Context Files Generated?
- [ ] CLAUDE.md exists and contains: project overview, tech stack placeholder,
      coding conventions, security requirements, file structure rules
- [ ] .cursorrules exists and is < 100 lines (Cursor limit)
- [ ] INITIAL.md exists with structured fields (title, description, priority, etc.)
- [ ] examples/ directory created with README.md placeholder
- [ ] Security section present in CLAUDE.md (from references/security-checklist.md)

Auto-fix: If any file missing → generate it now with best-guess content.
If CLAUDE.md > 200 lines → suggest splitting into domain-specific rule files.
```

#### Stage 1: Ideation Gate
```markdown
## L1-1 Check: Ideation Output Complete?
- [ ] docs/01-ideation.md exists
- [ ] Contains: original idea quote, clarified scope, MVP definition,
      explicitly excluded items list (what we're NOT doing), success criteria
- [ ] User's core intent preserved (compare keywords with original request)
- [ ] No feature creep detected (excluded list is non-empty or justified empty)
- [ ] Success criteria are measurable (not vague like "make it good")

Auto-fix: Add excluded items if missing. Re-quote user's original words at top.
```

#### Stage 2: PRD Gate
```markdown
## L1-2 Check: PRD Complete and Structured?
- [ ] docs/02-prd.md exists
- [ ] Contains ALL required sections:
      - Product overview (name, positioning, target users, value prop)
      - Functional requirements (F1, F2, ... each with table of fields/constraints/validation)
      - Non-functional requirements (NF1, NF2, ... with measurable metrics)
      - Information architecture (tree structure of UI elements)
      - User stories (US-1, US-2, ...)
      - Acceptance criteria (checkbox list)
- [ ] Every functional requirement has acceptance criteria
- [ ] No orphaned requirements (each F-number maps to a US-number)
- [ ] PRD is internally consistent (no contradictions between sections)

Auto-fix: Add missing sections using SKILL.md templates.
Flag contradictions to user.
```

#### Stage 3: Architecture Gate
```markdown
## L1-3 Check: Architecture Document Complete?
- [ ] docs/03-architecture.md exists
- [ ] Contains: tech stack selection with rationale, file/directory structure,
      data models (entities + fields + relationships),
      module responsibilities (table), API design (if applicable),
      key technical decisions with trade-off analysis,
      MCP configuration (if applicable)
- [ ] Tech stack matches project complexity (not over-engineered)
- [ ] Data model covers all entities mentioned in PRD
- [ ] File structure matches module responsibility assignments
- [ ] Stage 0 files (CLAUDE.md / .cursorrules) updated with confirmed architecture

Auto-fill: Update context files with confirmed tech stack decisions.
```

#### Stage 4: UI Design Gate (skip for non-visual projects)
```markdown
## L1-4 Check: UI Design Document Complete?
- [ ] docs/04-ui-design.md exists
- [ ] Contains: design token system (colors, spacing, typography, radii, shadows, transitions),
      component tree (hierarchy of all UI components),
      wireframe descriptions (text-based layout per screen/state),
      interaction states (normal/hover/focus/disabled/error/success/loading),
      responsive strategy (breakpoints + layout changes per breakpoint)
- [ ] All PRD features have corresponding UI representation
- [ ] Design tokens are concrete values (not "primary color" but "#378ADD")
- [ ] Component tree covers all information architecture nodes from PRD

Auto-fix: Generate missing tokens from a coherent palette if absent.
Map any uncovered IA nodes to UI components.
```

#### Stage 5: TODO Gate
```markdown
## L1-5 Check: TODO List Complete and Well-Structured?
- [ ] docs/05-todo.md exists
- [ ] Contains: task list with T-ID, description, acceptance criteria,
      constraints, prompt template reference, complexity estimate,
      dependencies, status tracking format
- [ ] Dependency graph is acyclic (no circular dependencies)
- [ ] Every PRD functional requirement maps to >= 1 task
- [ ] Tasks are atomic (each does ONE thing)
- [ ] Total estimated effort is reasonable (< 2 weeks for MVP)
- [ ] Multi-agent evaluation performed and documented (sequential vs parallel decision)

Auto-fix: Break down tasks that do > 1 thing.
Add tasks for uncovered PRD requirements.
Fix circular dependencies by reordering.
```

#### Stage 6: Implementation Gate (runs AFTER all tasks done, before Stage 7)
```markdown
## L1-6 Check: Implementation Complete?
- [ ] All tasks in docs/05-todo.md marked as completed [-x]
- [ ] Code follows conventions defined in CLAUDE.md / .cursorrules
- [ ] No TODO / FIXME / HACK comments remain in code
- [ ] All tests pass (if tests were planned)
- [ ] Build succeeds (if build step exists)
- [ ] examples/ directory populated with key patterns used during implementation

Auto-fix: Address remaining TODOs or convert to tracked issues.
Update examples/ with representative code snippets.
```

#### Stage 7: Delivery Gate
```markdown
## L1-7 Check: Delivery Package Complete?
- [ ] docs/07-delivery.md exists (or final report)
- [ ] README.md updated with usage instructions
- [ ] Final verification checklist all checked
- [ ] Security audit passed
- [ ] Dependency vulnerability scan clean (if applicable)
- [ ] Deployment instructions provided (even if "just open index.html")
- [ ] Known limitations documented
- [ ] Extension roadmap provided (optional but recommended)

Auto-fix: Generate missing documentation from code analysis.
```

### L1 Scoring Rubric

| Score | Meaning | Action |
|-------|---------|--------|
| **PASS** (100%) | All items checked ✅ | Present to user |
| **WARN** (>80%, minor gaps) | Core complete, some optional items missing | Fix auto-fixable items, note rest to user |
| **FAIL** (<80%, critical gaps) | Required sections missing or inconsistent | Do NOT present. Fix all critical gaps first. |

---

## L2: Task Gate (任务门控) — Extended Security Gate

**Purpose**: After completing EACH task in Stage 6, run a multi-dimensional quality check beyond just security.

### L2 = Security Gate + Quality Gate + Completeness Gate

```
Task T-xx completed (code written, tested locally)
        │
        ├── L2-A: Security Gate (from references/security-checklist.md)
        │   MUST-PASS: secrets, injection, auth, input validation
        │   SHOULD-PASS: dependency audit, error messages, CSP/CORS
        │
        ├── L2-B: Quality Gate (NEW)
        │   Naming conventions match CLAUDE.md?
        │   Function length < threshold?
        │   Sufficient comments for complex logic?
        │   No dead code or debug leftovers?
        │
        └── L2-C: Completeness Gate (NEW)
            All acceptance criteria from T-xx satisfied?
            Task dependencies honored?
            Related files updated (imports, exports, types)?
            
        │
        ▼
   All 3 gates PASS → Mark T-xx as completed ✅
   Any gate FAIL → Fix before marking complete
```

### L2-B: Quality Gate Checklist

```markdown
## Quality Gate (per task)

### Naming Convention Check
- [ ] Variables/functions/classes follow CLAUDE.md naming rules
- [ ] No generic names (data, temp, item) without descriptive prefix/context
- [ ] File names follow project convention (kebab-case / PascalCase / etc.)
- [ ] CSS class names follow agreed pattern (BEM / camelCase / atomic)

### Complexity Check
- [ ] Single function body < 50 lines (warning if > 30)
- [ ] Nesting depth <= 4 (alert if > 3)
- [ ] Cyclomatic complexity < 10 per function (estimated)
- [ ] No functions with > 5 parameters (use object parameter instead)

### Documentation Check
- [ ] Public functions have docstring/JSDoc comment
- [ ] Non-obvious business logic has inline comment explaining WHY
- [ ] No commented-out code blocks (remove them or make conditional)
- [ ] Magic numbers replaced with named constants

### Cleanliness Check
- [ ] No console.log / print / debugger statements left in production code
- [ ] No unused imports or variables
- [ ] No duplicate code that should be extracted to shared utility
- [ ] Error handling follows project pattern (not bare try-catch swallowing errors)

### Auto-fix Rules
- console.log → remove or replace with proper logging utility
- unused import → remove
- magic number → extract to constant with descriptive name
- function too long → split into smaller functions
- nesting too deep → extract early return or helper function
```

### L2-C: Completeness Gate Checklist

```markdown
## Completeness Gate (per task)

### Acceptance Criteria Coverage
- [ ] Review the task's acceptance criteria from docs/05-todo.md
- [ ] For each criterion: verify it is met by the implemented code
- [ ] If a criterion was impossible to satisfy, document why and flag to user

### Dependency Honor
- [ ] If this task depends on T-yy: confirm T-yy is already completed
- [ ] If this task is a prerequisite: confirm downstream tasks can proceed
- [ ] No out-of-order execution that breaks the plan

### Ripple Effect Check
- [ ] New files created: listed and explained
- [ ] Existing files modified: changes are minimal and focused
- [ ] Import/export chains updated (no broken references)
- [ ] Type definitions updated (if using TypeScript / JSDoc types)
- [ ] Tests updated (if test files exist for modified modules)

### Auto-fix Rules
- Missing acceptance criterion → implement it or add to known-limitations
- Broken import → add missing export or fix path
- Type mismatch → align types across boundary
```

### L2 Decision Matrix

| Gate | Severity | Action on Fail |
|------|----------|---------------|
| Security MUST-PASS | Critical | Block. Must fix before proceeding. |
| Security SHOULD-PASS | Warning | Note in delivery report. Fix if quick. |
| Quality - Naming | Low | Auto-fix (rename). Proceed. |
| Quality - Complexity | Medium | Refactor if > thresholds significantly. Note if borderline. |
| Quality - Docs | Low | Auto-add comments. Proceed. |
| Quality - Cleanliness | Medium | Remove debug code. Flag suspicious patterns. |
| Completeness - AC | High | Missing criteria must be implemented. |
| Completeness - Dep | Critical | Cannot proceed until deps met. |
| Completeness - Ripple | Medium | Fix immediate breakages. Note others. |

---

## L2.5: Context Checkpoint (上下文检查点) — Stage 6 Only

**Purpose**: Proactively monitor context budget during Stage 6 implementation. Prevent context collapse BEFORE it happens, rather than only detecting it after (L4 AP-2).

**Trigger**: After every **5 tasks** completed in Stage 6 (or every task for XL projects).

**Reference**: Full budget model in `references/context-budget.md`.

### Checkpoint Decision Tree

```
[Context Checkpoint] Tasks done: N/M | Est. budget used: X%
  │
  ├── Budget < 60%
  │     → Continue normally. No action needed.
  │
  ├── Budget 60-80%
  │     → Generate Context Summary Card (see context-budget.md)
  │     → Present card as preamble to next task
  │     → Continue
  │
  ├── Budget 80-95%
  │     → Multi-Agent available? → Split remaining tasks to agents (see multi-agent-orchestration.md)
  │     → Multi-Agent NOT available? → Generate Session Handoff Package (see session-handoff.md)
  │     → Recommend new session. DO NOT auto-continue.
  │
  └── Budget > 95%
        → MANDATORY: Generate Session Handoff Package
        → STOP. Refuse to continue.
        → Output: "Context budget exhausted. Handoff package saved. Start new session."
```

### Checkpoint Checklist

```markdown
## Context Checkpoint (Task T-xx completed, N tasks since last checkpoint)

### Budget Assessment
- [ ] Estimate current context token usage (rough: ~300-500 per exchange + doc sizes)
- [ ] Compare against project tier budget (S=5000, M=8000, L=12000, XL=15000)
- [ ] Budget usage %: ___

### Decision
- [ ] < 60% → Continue (no action)
- [ ] 60-80% → Summary Card generated and saved
- [ ] 80-95% → Handoff Package OR Multi-Agent split executed
- [ ] > 95% → Handoff Package generated, session STOPPED

### Actions Taken
- [ ] Summary Card: docs/summary-[stage]-[task].md
- [ ] Handoff Package: docs/handoff-[stage]-[task]-[date].md
- [ ] Multi-Agent split: N agents spawned for remaining tasks
- [ ] N/A — below threshold
```

### Context Checkpoint Placement in Stage 6 Loop

```
For each task in TODO:
  └─ Intent → Template → Code → Test → L2 Gate → Verify → Commit
                                                        │
                                                    [Context Checkpoint]
                                                    (every 5 tasks / every task for XL)
                                                        │
                                              Continue / Summary / Handoff / Split
```

---

## L3: Cross-Stage Consistency (跨阶段一致性)

**Purpose**: Detect drift between what was planned (early stages) and what was built (later stages). The most common failure mode in Vibe Coding is gradual requirement creep that goes unnoticed.

### Trigger Points

1. **Stage 5 (TODO Generation)**: Before breaking down into tasks, verify PRD ↔ Architecture alignment
2. **Stage 7 (Delivery)**: Before final handoff, verify everything against all previous stages

### Consistency Checks

#### C1: PRD-to-Code Coverage Matrix

```
For each F-[N] in docs/02-prd.md:
  ├─ Find corresponding code implementation(s)
  ├─ Find corresponding test case(s)
  ├─ Find corresponding UI element(s)
  └─ Status: IMPLEMENTED / PARTIAL / MISSING

Output: Coverage matrix table
```

| PRD Item | Code Location | Test | UI Element | Status |
|----------|-------------|------|------------|--------|
| F1: Add Task | app.js:state.addTodo() | manual TC-1 | .input-section | IMPLEMENTED |
| F2: Toggle Complete | app.js:state.toggleTodo() | manual TC-2 | .task-item click | IMPLEMENTED |
| ... | ... | ... | ... | ... |

**Threshold**: 100% of P0/P1 requirements MUST be IMPLEMENTED. P2+ can be PARTIAL with explanation.

#### C2: Architecture Decision Tracking

```
For each decision recorded in docs/03-architecture.md:
  ├─ Is the decision followed in the actual code?
  ├─ If deviated: was there a conscious reason documented?
  └─ Status: FOLLOWED / DEVIATED (reasoned) / VIOLATED (unexplained)

Output: Decision compliance table
```

| Decision | Stated In Architecture | Actual In Code | Status |
|----------|---------------------|----------------|--------|
| Module pattern: closures | "Use module-level closures" | IIFE wrapper around all JS | FOLLOWED |
| Storage: localStorage | "Use localStorage" | localStorage API used | FOLLOWED |
| Rendering: textContent | "No innerHTML for user content" | textContent everywhere | FOLLOWED |
| ... | ... | ... | ... |

**Threshold**: Unexplained VIOLATIONS = 0 allowed. DEVIATED must have inline comment explaining why.

#### C3: Document Sync Check

```
For each document produced:
  ├─ Does it reflect the CURRENT state of the project?
  ├─ Are cross-references between documents still valid?
  └─ Outdated info flagged for update
```

| Document | Last Updated At | Current Accuracy | Action Needed |
|----------|----------------|-----------------|---------------|
| CLAUDE.md | Stage 0 | May need update (actual patterns evolved during impl.) | Review & update |
| .cursorrules | Stage 0 | Same as above | Review & update |
| PRD (docs/02) | Stage 2 | Should be stable unless scope changed | Verify |
| Architecture (docs/03) | Stage 3 | Should match actual file structure | Verify |
| UI Design (docs/04) | Stage 4 | Should match actual CSS | Verify |
| TODO (docs/05) | Stage 5 | All tasks completed? | Update statuses |

#### C4: Design Token Fidelity

Only applies to visual projects:

```
For each design token in docs/04-ui-design.md:
  ├─ Find its usage in CSS / styled-components / styles
  ├─ Is the VALUE exactly matching? (allow rounding for relative units)
  └─ Flag: MISMATCH / UNUSED / EXTRA (value not in tokens)
```

**Threshold**: MISMATCH = 0 (tokens define truth). UNUSED tokens = OK (future use). EXTRA values = flag for possible tokenization opportunity.

### L3 Output Format

When L3 triggers (Stage 5 or Stage 7), produce this report:

```markdown
## Cross-Stage Consistency Report

### Summary
- PRD Coverage: 8/8 requirements (100%)
- Architecture Compliance: 5/5 decisions followed (100%)
- Document Sync: 5/6 current (CLAUDE.md needs update)
- Design Token Fidelity: 23/25 matched (92%)

### Issues Found
| # | Severity | Description | Recommended Action |
|---|----------|-------------|--------------------|
| 1 | LOW | CLAUDE.md mentions "React-like" patterns but we use vanilla JS | Update CLAUDE.md coding conventions |
| 2 | INFO | Token `--shadow-sm` defined but never used | Keep for future use |

### Conclusion
✅ Project is consistent. Minor updates recommended for Stage 0 files.
```

---

## L4: Anti-Pattern Detection (反模式检测)

**Purpose**: Continuously monitor for known Vibe Coding anti-patterns that degrade quality over time. Unlike L1-L3 which check at specific points, **L4 runs after every user interaction** throughout the entire workflow.

### Detected Patterns

#### AP-1: Doom Loop (死循环修复)

**Definition**: The same task or issue is being fixed repeatedly without resolution.

**Detection signals**:
- Same task T-xx has been re-opened > 2 times after being marked complete
- Same error message appears > 3 times across different fix attempts
- Consecutive outputs produce diminishing changes (tweaking rather than solving)

**Threshold**: Trigger when ANY signal exceeds threshold

**Auto-action**:
```
DOOM LOOP DETECTED (signal: task T-04 re-opened 3 times)
→ STOP working on this task immediately
→ Generate diagnostic summary:
  - What was attempted (summary of each attempt)
  - What failed each time
  - Hypothesis: why attempts aren't converging
→ PRESENT TO USER with options:
  A) Redescribe the requirement from scratch
  B) Try a completely different approach (suggest alternatives)
  C) Defer this task and continue with others
```

#### AP-2: Context Collapse (上下文崩溃)

**Definition**: As conversation grows long, the AI starts losing track of earlier decisions and constraints, leading to outputs that contradict previously established facts.

**Detection signals**:
- Current output contradicts a fact established in an earlier stage document
- User says "I already told you..." or "that's not what we decided"
- Key details from PRD/Architecture are omitted in recent outputs
- AI asks about something that was already answered in a prior stage

**Threshold**: Contradiction detected OR user expresses frustration about repetition

**Auto-action**:
```
CONTEXT COLLAPSE RISK DETECTED
→ Immediately pause current work
→ Read back the following files IN FULL:
  - docs/02-prd.md (requirements ground truth)
  - docs/03-architecture.md (technical ground truth)
  - Most recent stage output (current state)
→ Generate a "Context Summary Card":
  - Key constraints (max 10 bullets)
  - Decisions already made (max 10 items)
  - What we're currently working on (1 sentence)
  - What was just completed (1 sentence)
→ Insert summary at start of next response
→ Continue with refreshed context
```

#### AP-3: Prompt Debt (提示词债务)

**Definition**: Instead of writing rules into persistent instruction files (CLAUDE.md, .cursorrules), the AI relies on increasingly long prompts repeating the same instructions every turn. This wastes context window and degrades over time.

**Detection signals**:
- Same instructional phrase appears in > 3 consecutive prompts/responses
- CLAUDE.md or .cursorrules has not been updated despite new patterns emerging
- Prompt length growing monotonically while output quality stays flat or declines
- Examples/ directory remains empty despite repeated similar code patterns

**Threshold**: Same instruction repeated 3+ times without being codified

**Auto-action**:
```
PROMPT DEBT DETECTED (pattern "always use textContent" repeated 4x)
→ Identify the recurring instruction
→ Convert it into a rule in the appropriate file:
  - Coding convention → CLAUDE.md or .cursorrules
  - Security rule → CLAUDE.md Security section
  - Pattern/example → examples/filename.ext with explanation
→ Update the instruction file NOW
→ Replace future prompt repetitions with a short reference:
  "Follow security rules in CLAUDE.md" instead of listing them each time
→ Record the debt payment in a running log (optional)
```

#### AP-4: Tech Debt Acceleration (技术债加速)

**Definition**: Accumulating shortcuts, workarounds, and "fix later" items faster than they are being addressed.

**Detection signals**:
- Comments containing: "TODO", "FIXME", "HACK", "workaround", "temporary", "later"
- Pattern of choosing quicker-but-worse solution when better option exists
- Skipping tests or error handling "for now"
- Copy-paste code instead of extracting shared logic

**Threshold**: > 5 debt indicators in a single stage

**Auto-action**:
```
TECH DEBT ACCELERATION WARNING (7 debt indicators in Stage 6)
→ Generate Tech Debt Ledger:
  | ID | Location | Description | Effort to Fix | Priority |
  |----|----------|-------------|--------------|---------|
  | TD-1 | app.js:45 | Duplicated sort logic (copied from :32) | 5 min | Low |
  | TD-2 | app.js:89 | TODO: add loading state | 15 min | Med |
  | ... | ... | ... | ... | ... |
→ For HIGH priority items (> 15 min effort): address NOW before continuing
→ For LOW priority items: add to docs/05-todo.md as explicit tasks
→ Present ledger to user with recommendation:
  "Found N items of tech debt. M items should be fixed now,
   K items can go into backlog."
```

#### AP-5: Drift / Requirement Creep (需求漂移)

**Definition**: The work gradually shifts away from what the user originally asked for, adding features or changing direction without explicit approval.

**Detection signals**:
- Current work content shares low keyword overlap with user's original request
- Features appearing that were in the "explicitly excluded" list from Stage 1
- Scope expanding without user requesting it ("I'll also add...")
- User hasn't confirmed the new direction

**Threshold**: Keyword overlap < 60% with original request OR excluded-list item violated

**Auto-action**:
```
DRIFT DETECTED (keyword overlap: 45% with original request)
→ Generate Drift Report:
  Original Request: "做一个待办清单，添加、完成、删除"
  Current Work: "...also adding drag-drop reorder, categories, due dates..."
  Added (not requested): drag-drop, categories, due dates
  Excluded (but now included): (none yet)
→ PAUSE and present to user:
  "I noticed we've expanded beyond the original scope.
   These features were added but not in your original request:
   - [list]
   Should I: A) Continue with expanded scope
             B) Return to original scope
             C) Let you pick which additions to keep?"
→ Wait for user decision before proceeding
```

### L4 Monitoring Dashboard

After every significant interaction, emit a compact status line (internal, not shown to user):

```
[L4 Monitor] DoomLoop=0/3 | ContextCollapse=0/1 | PromptDebt=1/3 | TechDebt=3/5 | Drift=85% | Budget=67%
```

Values represent current count / threshold. Any at-or-above threshold triggers the corresponding auto-action.

---

## Self-Report Format

Every time the Self-Check Zone runs, append (or include) a compact report:

```markdown
## Self-Check Report (Stage N / Task T-xx)

### Results
| Layer | Status | Details |
|-------|--------|---------|
| L1 Stage Gate | PASS/WARN/FAIL | X/Y items passed |
| L2 Task Gate | PASS/WARN/FAIL | Sec: X/Y · Qual: X/Y · Comp: X/Y |
| L3 Cross-Stage | N/A/RUN | Coverage: X% · Compliance: X% |
| L4 Anti-Pattern | CLEAR/WARNING | All patterns within thresholds |

### Actions Taken (auto-fixes applied)
- [ ] Fixed X (description)
- [ ] Updated Y (file)

### Issues Requiring Attention (presented to user)
- [ ] Issue Z (severity: LOW/MED/HIGH) — recommendation
```

---

## Integration with Existing Workflow

### Where Self-Check Fits in SKILL.md

| Workflow Step | Self-Check Integration |
|--------------|----------------------|
| End of Stage N (before "Decision Check") | Run L1-N Stage Gate + L4 scan |
| After each Task in Stage 6 (before mark complete) | Run L2 Task Gate (A+B+C) + L4 scan |
| After every 5 tasks in Stage 6 | Run L2.5 Context Checkpoint (budget evaluation) |
| Stage 5 TODO generation | Run L3 Cross-Stage (PRD↔Arch alignment) |
| Stage 7 Final delivery | Run L1-7 + L2.5 final + L3 full + L4 full scan |
| Any user message received | Quick L4 scan (anti-pattern monitoring + budget) |

### Performance Budget

| Check Type | Est. Time | Method |
|-----------|----------|--------|
| L1 Stage Gate | 3-5 sec | Read产物文件 + 对比模板checklist |
| L2 Task Gate | 2-3 sec | 审查当前代码 + 对照acceptance criteria |
| L2.5 Context Checkpoint | 1-2 sec | 评估token消耗 + 决策(每5个任务运行) |
| L3 Cross-Stage | 5-8 sec | 跨文档对比（只在 Stage 5/7 运行）|
| L4 Anti-Pattern | 1-2 sec | 检查最近交互的模式信号(含Budget追踪) |
| **Full suite (worst case)** | **~20 sec** | Only at Stage 7 delivery |

---

## Summary: Why This Matters

| Problem Without Self-Check | With Self-Check |
|----------------------------|-----------------|
| Incomplete deliverables presented to user | L1 catches before presentation |
| Security bugs found late (or never) | L2-A catches per-task |
| Code quality degrades quietly | L2-B enforces standards every task |
| Requirements silently drift | L3 detects coverage gaps |
| AI gets stuck in unproductive loops | L4 interrupts doom loops |
| Context loss causes contradictory outputs | L4 forces context refresh |
| Technical debt invisible until painful | L4 tracks and surfaces debt |
| Prompt repetition wastes context | L4 converts patterns to rules |
| User must catch all errors manually | Multi-layer safety net reduces user burden |
