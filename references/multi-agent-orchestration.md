# Multi-Agent Orchestration

## Overview

When projects grow beyond what a single AI agent can efficiently handle, **multi-agent orchestration** enables parallel workstreams, specialized roles, and coordinated execution. This module provides patterns for scaling Vibe Coding from single-agent to team-level productivity.

## When to Switch to Multi-Agent Mode

| Signal | Single Agent OK | Need Multi-Agent |
|--------|---------------|-----------------|
| Task count | < 10 tasks | 20+ tasks with dependencies |
| Codebase size | < 50 files | 100+ files across domains |
| Parallel potential | Tasks are sequential | Independent tasks can run in parallel |
| Specialization needed | Generalist is fine | Distinct domains (frontend/backend/tests/docs) |
| Iteration speed | Fast enough | Waiting for single agent is bottleneck |

## Architecture Patterns

### Pattern A: Sequential Pipeline (Simplest)

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│  Research   │ -> │  Architect  │ -> │  Builder    │
│  Agent      │    │  Agent      │    │  Agent      │
│             │    │             │    │             │
│ Gather info │    │ Create plan │    │ Write code  │
└─────────────┘    └─────────────┘    └─────────────┘
```

**Best for**: Linear workflow where each stage depends on the previous one.
**Implementation**: Use the standard Vibe Coding flow — each stage IS a specialized agent step.

### Pattern B: Parallel Workers (Most Common for MVP)

```
                    ┌──────────────┐
                    │  Lead Agent  │
                    │  (Planner)   │
                    └──────┬───────┘
                           |
              ┌────────────┼────────────┐
              v            v            v
     ┌────────────┐ ┌──────────┐ ┌──────────┐
     │ Frontend   │ │ Backend  │ │ Testing  │
     │ Agent      │ │ Agent    │ │ Agent    │
     │            │ │          │ │          │
     │ UI/UX impl │ │ API/DB   │ │ Tests    │
     └─────┬──────┘ └────┬─────┘ └────┬─────┘
           │             │            │
           v             v            v
     ┌──────────────────────────────────┐
     │        Integration Agent         │
     │  Merge + Verify + Fix Conflicts │
     └──────────────────────────────────┘
```

**Best for**: Full-stack apps where frontend, backend, and tests can be developed independently against agreed interfaces.

**How It Works**:
1. **Lead Agent** reads PRD + Architecture docs → creates interface contracts (API shapes, type definitions, shared models)
2. **Workers implement in parallel** against those contracts (not against each other's code)
3. **Integration Agent** merges results, runs full test suite, resolves conflicts

### Pattern C: Specialist Swarm (Complex Projects)

```
                      ┌──────────────────┐
                      │  Orchestrator    │
                      │                  │
                      │ - Task queue     │
                      │ - Dependency map │
                      │ - Result merge   │
                      └──┬───┬───┬───┬───┘
                         │   │   │   │
              ┌──────────┘   │   │   └──────────┐
              v              v   v              v
       ┌──────────┐  ┌──────────┐  ┌──────────┐
       │ UI Dev   │  │ API Dev  │  │ Security  │
       │          │  │          │  │ Reviewer  │
       │ Focus:   │  │ Focus:   │  │ Focus:   │
       │ Components│  │ Endpoints│  │ Auth,     │
       │ Pages    │  │ DB schema│  │ injection,│
       │ Styling  │  │ Logic    │  │ secrets   │
       └──────────┘  └──────────┘  └──────────┘
              │              │           │
              └──────────────┴───────────┘
                             v
                   ┌──────────────────┐
                   │ Quality Gate     │
                   │ - All tests pass │
                   │ - No security    │
                   │   issues         │
                   │ - Build succeeds │
                   └──────────────────┘
```

## Role Definitions

### Orchestrator / Lead Agent

**Responsibilities:**
- Read all project docs (ideation through todo)
- Decompose the TODO list into parallelizable work packages
- Define interfaces/contracts between work packages
- Assign tasks to specialist agents
- Monitor progress and reassign if stuck
- Merge outputs and resolve conflicts

**Prompt Template for Orchestrator:**
```
You are the Lead Developer for [project name].

Your job:
1. Read docs/01-ideation.md through docs/05-todo.md
2. Identify tasks that can run IN PARALLEL (no dependencies between them)
3. For parallel tasks, define clear interface contracts (API types, shared models)
4. Create a work package for each agent containing:
   - Scope (what this agent owns)
   - Interfaces (what it must conform to)
   - Deliverables (files to create/modify)
   - Acceptance criteria
5. Present the orchestration plan for my approval before dispatching agents
```

### Frontend Agent

**Responsibilities:**
- Implement UI components per design system tokens
- Build pages and layouts from UI/UX design doc
- Handle client-side state and user interactions
- Ensure responsive design and accessibility

**Context Package:**
```
Read these before starting:
- docs/04-ui-design.md (design system, layouts, components)
- docs/03-architecture.md (frontend architecture section)
- examples/components/ (patterns to follow)

You own:
- src/components/
- src/pages/
- src/composables/ or src/hooks/
- src/styles/

Interface contract (from backend):
- [API endpoint shapes you consume]
- [Type definitions for data models]
DO NOT modify backend code. If an API change is needed, file a request with the orchestrator.
```

### Backend Agent

**Responsibilities:**
- Implement API endpoints per architecture spec
- Database schema, migrations, queries
- Business logic and validation
- Authentication/authorization middleware

**Context Package:**
```
Read these before starting:
- docs/03-architecture.md (backend/API/database sections)
- docs/02-prd.md (functional requirements)
- examples/services/ (patterns to follow)

You own:
- src/api/ or src/routes/
- src/services/
- src/models/ or src/db/
- migrations/
- middleware/

Interface contract (to frontend):
- You MUST provide these endpoints: [list]
- Request/response types: [shapes]
DO NOT modify frontend code. If a type change affects frontend, coordinate via orchestrator.
```

### Testing Agent

**Responsibilities:**
- Write unit tests as features are implemented
- Write integration tests for API endpoints
- Write E2E tests for critical user flows
- Maintain test utilities and fixtures

**Context Package:**
```
Read these before starting:
- docs/03-architecture.md (testing strategy section)
- references/prompt-templates.md (T-9: Test Generation template)
- examples/tests/ (testing patterns to follow)

You own:
- __tests__/ or tests/
- *.test.ts / *.spec.ts files
- test fixtures and mocks
- Playwright/Cypress E2E specs

Rules:
- Every new feature gets at minimum unit tests
- Critical paths get integration tests
- User-facing flows get E2E tests
- Target: 70%+ coverage on new code
```

### Security Review Agent (Optional but Recommended)

**Responsibilities:**
- Run security checklist on every merged change
- Check for secrets, injection vulnerabilities, auth issues
- Validate dependency safety
- Report findings as blocker/warning/suggestion

**Context Package:**
```
Read references/security-checklist.md before reviewing.

For each set of changes:
1. Run the Pre-Commit Checklist (all MUST-pass items)
2. Check dependency vulnerabilities
3. Scan for common vulnerability patterns
4. Output a security report with severity ratings
```

## Coordination Protocols

### Interface Contract Format

Before agents work in parallel, the orchestrator defines:

```markdown
## Contract: Frontend ↔ Backend

### Shared Types (src/types/shared.ts)
```typescript
interface User {
  id: string;
  email: string;
  name: string;
  avatarUrl?: string;
}

interface ApiResponse {
  success: boolean;
  data?: T;
  error?: { code: string; message: string };
}
```

### API Contract
| Method | Path | Request | Response | Auth Required? |
|--------|------|---------|----------|---------------|
| GET | /api/users | {} | User[] | Yes |
| POST | /api/auth/login | {email, password} | {token} | No |
| PUT | /api/users/:id | {Partial<User>} | User | Yes |

### State Management Contract
- Frontend uses Pinia store: `useUserStore()`
- Store actions call API client (not directly fetch)
- API client handles auth token injection
```

### Handoff Protocol

When Agent A needs to hand off work to Agent B:

```markdown
## Handoff: [Agent A] → [Agent B]

### What Was Done
[Summary of completed work with file references]

### Current State
- Working branch: [branch-name]
- Last passing test: [test command output]
- Known issues: [any problems encountered]

### What You Need To Do Next
[Specific instructions for next agent]

### Important Context
- Decision made: [X] because [reason]
- Workaround used: [description of any temporary solution]
- Do NOT touch: [files that are out of scope]
```

### Conflict Resolution

When parallel agents produce conflicting changes:

1. **Schema conflicts** (type definitions differ): Or arbitrates, picks canonical version
2. **Import path conflicts**: Standardize on barrel exports
3. **Dependency version conflicts**: Use lockfile resolution, pin to compatible version
4. **Logic conflicts** (same function modified differently): Human review required

## Implementation Guide for WorkBuddy

### Core Primitives

WorkBuddy multi-agent uses 3 primitives:

| Primitive | Tool | Purpose |
|-----------|------|---------|
| **Spawn** | `Agent` tool with `name` + `prompt` | Launch a new sub-agent to work on a specific task |
| **Coordinate** | `SendMessage` to agent name | Send instructions or data to a running agent |
| **Aggregate** | `TaskList` / agent returns result | Collect outputs from completed agents |

### Example: 4-Agent VibeTodo Build

A real multi-agent execution plan for building VibeTodo (the example Web project). The orchestrator (you, the main conversation) spawns 3 specialist agents in parallel after Stage 5 task breakdown:

**Step 1 — Stage 5 outputs this task split**:
```
Task 1: HTML structure (index.html)      ← FE-Structure
Task 2: CSS design system (styles.css)   ← FE-Styles
Task 3: JS app logic (app.js)            ← FE-Logic
Task 4: Quality + security audit         ← Auditor
```

**Step 2 — Orchestrator spawns 3 agents in parallel**:

```
Orchestrator (main conversation):
  → Spawn "fe-html" agent:  "Write index.html based on the wireframe
     from stage-outputs/stage-4-ui-design.md and the PRD from
     stage-outputs/stage-2-prd.md. Output ONLY the HTML file content.
     Do NOT add any CSS or JS — those are handled by other agents."
  
  → Spawn "fe-css" agent:  "Write styles.css based on the Design Tokens
     in stage-outputs/stage-4-ui-design.md (color: #378ADD, font: system-ui).
     Cover all interaction states (hover, focus, active, disabled).
     Output ONLY the CSS file content."
  
  → Spawn "fe-js" agent:   "Write app.js based on the functional requirements
     in stage-outputs/stage-2-prd.md (F-001 through F-008). Use IIFE pattern,
     localStorage for persistence, textContent for safe rendering.
     Output ONLY the JS file content."
```

**Step 3 — Each agent works independently**:

Agent `fe-html` gets this prompt:
```
Task: Build VibeTodo index.html

Context files to read:
- ../stage-outputs/stage-4-ui-design.md (component tree + wireframe)
- ../stage-outputs/stage-2-prd.md (F-001: Add todo, F-002: Toggle complete)

Rules:
- Semantic HTML only (<header>, <main>, <section>, <footer>)
- NO inline styles or <style> tags
- NO <script> tags
- Include data-testid attributes for testing
- Output ONLY the file content, no explanations

Output: src/index.html
```

Agent `fe-css` gets this prompt:
```
Task: Build VibeTodo styles.css

Context files to read:
- ../stage-outputs/stage-4-ui-design.md (Design Tokens section)

Tokens to implement:
- Primary: #378ADD, Surface: #F8F9FA, Text: #212529
- Font: system-ui, 16px base
- Border-radius: 8px (inputs), 12px (cards)
- Spacing: 8px grid system

States to cover:
- Button: default, hover (darken 10%), active (darken 15%), disabled
- Input: default, focus (2px primary border), error (red border)
- Card: default, hover (subtle shadow via outline)

Output: src/styles.css
```

Agent `fe-js` gets this prompt:
```
Task: Build VibeTodo app.js

Context files to read:
- ../stage-outputs/stage-2-prd.md (F-001 through F-008 with AC)

Requirements:
- F-001 Add todo: text input + Enter key/add button
- F-002 Toggle complete: click checkbox to mark done
- F-003 Delete todo: X button with confirmation
- F-004 Filter: All/Active/Completed tabs
- F-005 Count: "3 items left" counter
- F-006 Persist: localStorage read on init, write on change
- F-007 Clear completed: button to remove all done items
- F-008 Empty state: friendly message when no todos

Constraints:
- IIFE pattern: (function() { ... })();
- textContent for ALL user-generated content (XSS prevention)
- NO innerHTML, NO dangerouslySetInnerHTML, NO v-html equivalent
- localStorage key: "vibetodo-tasks"

Output: src/app.js
```

**Step 4 — Orchestrator collects results**:

After all 3 agents finish, the orchestrator:

```
→ Spawn "auditor" agent:
  "Run L2 Task Gate on these 3 files:
   - Security: check all 18 MUST-PASS items from security-checklist.md
   - Quality: verify naming conventions, function length <50 lines, nesting <=4
   - Completeness: verify all F-001 through F-008 acceptance criteria are covered
   Report PASS/WARN/FAIL for each dimension. Auto-fix WARN items."
```

**Step 5 — Integration test**:

The orchestrator reads all 3 output files, verifies cross-references:
- HTML `class` attributes match CSS selectors
- JS `element.classList.add('active')` has a `.active` definition in CSS
- HTML `data-testid` attributes match what the JS queries

---

### Agent Communication Patterns

#### Pattern 1: Send Task + Wait for Result (Fire and Forget)

```
Orchestrator spawns agent with complete self-contained prompt.
Agent reads context files, produces output, writes file, returns.
Orchestrator reads the result and validates.
```

Best for: Independent tasks with well-defined inputs/outputs.

#### Pattern 2: Send Task + Iterate (Chat Loop)

```
Orchestrator spawns "fe-dev".
Orchestrator → fe-dev: "Build the header component"
fe-dev finishes, reports back.
Orchestrator → fe-dev: "Now build the footer component"
fe-dev finishes, reports back.
Orchestrator → fe-dev: "Wire them together in App.tsx"
```

Best for: Tasks that build on each other, same domain.

#### Pattern 3: Coordinator + Workers (Hub and Spoke)

```
┌──────────────┐
│ Orchestrator │
└──┬───┬───┬───┘
   │   │   │
   v   v   v
  FE  BE  DB      ← All spawned in parallel
   │   │   │
   └───┼───┘
       v
   Integration    ← Spawned after all 3 complete
```

Best for: Full-stack projects with clear domain boundaries.

---

### Coordination Protocol (WorkBuddy Agent Syntax)

When spawning agents, use this annotated template:

```
Spawn agent with:
  name: "role-based-name"  (e.g., "fe-styles", "be-api", "test-crud")
  prompt: |
    CONTEXT FILES TO READ:
    - ../path/to/prd.md  (section: F-001 to F-005)
    - ../path/to/architecture.md  (section: API routes)
    
    TASK:
    [Clear, one-sentence description of what to produce]
    
    CONSTRAINTS:
    - Output ONLY [file type / format]
    - Do NOT modify [out-of-scope files]
    - Follow [naming convention / pattern]
    - Max [X] lines / files
    
    DELIVERABLE:
    Write to: [exact file path]
    
    SIGN-OFF:
    When done, report: "[agent-name] complete: [what was produced]"
  
  run_in_background: true  (for parallel execution)
  subagent_type: "general-purpose"  (or "Explore" for read-only tasks)
```

### Agent Role Templates (Ready to Copy)

#### Frontend Component Agent

```
name: "fe-component"
prompt: |
  CONTEXT: Read ../docs/04-ui-design.md for component specs.
  TASK: Build the [ComponentName] component.
  CONSTRAINTS:
  - React + TypeScript, no class components
  - Tailwind CSS for styling, match design tokens exactly
  - Include loading, empty, error states
  - Add aria-labels for accessibility
  - Output: src/components/[ComponentName].tsx
  SIGN-OFF: Report component name + states covered + line count.
```

#### Backend API Agent

```
name: "be-api"
prompt: |
  CONTEXT: Read ../docs/03-architecture.md for API design.
  TASK: Build the [route group] API endpoints.
  CONSTRAINTS:
  - FastAPI + Pydantic, async handlers
  - Input validation with Pydantic models
  - Error responses: { "error": "message" }, never expose stack traces
  - Database: parameterized queries only, NO string interpolation
  - Output: src/api/[module].py
  SIGN-OFF: Report endpoints built + request/response shapes.
```

#### Testing Agent

```
name: "test-coverage"
prompt: |
  CONTEXT: Read ../docs/02-prd.md (all F-NNN items).
  TASK: Write tests for the [module/feature].
  CONSTRAINTS:
  - Vitest + @testing-library/react (frontend) or pytest (backend)
  - Cover: happy path, edge cases, error states, auth bypass attempts
  - Security tests: XSS injection, SQL injection, IDOR
  - Output: src/__tests__/[module].test.{ts,py}
  SIGN-OFF: Report test count + coverage targets met.
```

---

### Multi-Agent Execution Checklist

Before spawning agents, verify:
- [ ] Task list has clear dependency graph (no circular deps)
- [ ] Each agent has a well-defined scope (no overlapping file writes)
- [ ] Interface contracts are specified (API types, CSS class names, file paths)
- [ ] Agent prompts include ALL context they need (no run-time questions)
- [ ] Output file paths are unique (no two agents writing to same file)
- [ ] Integration agent is planned (to verify cross-agent consistency)

### Scaling Factors

| Project Complexity | Agent Setup | Coordination Overhead |
|-------------------|------------|---------------------|
| Small (< 10 tasks) | Single agent | None |
| Medium (10-30 tasks) | 2 agents (FE + BE) | Low — interface contracts |
| Large (30-100 tasks) | 4+ agents (specialists) | Medium — need orchestrator |
| Enterprise (100+ tasks) | Agent teams + kanban | High — use vibe-kanban pattern |

### When NOT to Use Multi-Agent

- Simple CRUD app or landing page (single agent faster)
- Tight coupling between all parts (parallelism impossible)
- Learning/exploration phase (still figuring out architecture)
- Team size = 1 (coordination overhead not worth it)
- Tasks are sequential by nature (Step 2 MUST run after Step 1)
