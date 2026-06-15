# Context Engineering Module

## Overview

Context Engineering is the foundation of reliable Vibe Coding. Instead of relying on clever prompts, it systematically designs the environment (rules, examples, documentation, validation gates) so AI coding assistants can execute work consistently across tasks and team members.

**Core formula**: Precise Rules + Rich Examples + Structured Requests + Validation Gates = Consistent AI Output

## When to Use

This module runs **before Stage 1 (Ideation & Scoping)** as a "Stage 0: Context Setup". It produces project-level instruction files that all subsequent stages reference.

## Outputs

The Context Setup phase generates these files in the project root:

```
project-root/
├── CLAUDE.md              # Global rules for Claude-based assistants
├── .cursorrules           # Rules for Cursor IDE
├── .copilot-instructions  # Rules for GitHub Copilot (optional)
├── INITIAL.md             # Template for feature requests (reusable)
├── .ai/
│   └── memory/            # Persistent agent memory (optional)
└── examples/              # Code patterns to follow (populated later)
    └── README.md
```

---

## File 1: CLAUDE.md — Project-Level Rules

### Purpose
AI coding assistants read this file at the start of every session. It is your "project constitution" — the single source of truth for how code should be written in this project.

### Template

```markdown
# [Project Name] — AI Assistant Rules

## Project Overview
- **What**: [One-line description]
- **Stack**: [Tech stack summary, e.g., Vue 3 + TypeScript + Vite + FastAPI]
- **Architecture**: [Monorepo? SPA? Microservices?]

## Code Structure Rules
- Max file length: [e.g., 300 lines] — split if exceeded
- Module organization: [e.g., feature-based / layer-based]
- Import order: external → internal relative → internal absolute
- Naming convention: [camelCase for variables, PascalCase for components, kebab-case for files]

## Style Conventions
- Language: [e.g., TypeScript strict mode enabled]
- Formatting: [e.g., Prettier with config in .prettierrc]
- Component pattern: [e.g., Composition API with <script setup>]
- State management: [e.g., Pinia stores, one store per domain]
- Error handling: [e.g., use Result/Either pattern, never swallow errors silently]

## Testing Requirements
- Test framework: [e.g., Vitest for unit tests, Playwright for E2E]
- Coverage target: [e.g., minimum 70% on core logic]
- Test location: [e.g., __tests__/ next to source files, or tests/ directory]
- Mocking style: [e.g., prefer factory functions over mock objects]

## Workflow Rules
- Before writing code: read relevant docs/ files and existing code patterns
- Before modifying: understand the existing implementation first
- After completing: run tests/lint before marking task done
- Commit format: [e.g., type(scope): description with PRD/TASK ref]

## Common Pitfalls (DO NOT)
- [Specific anti-patterns for this stack, e.g., "Don't use v-if and v-for on same element"]
- [Known issues, e.g., "State mutations outside Pinia actions cause reactivity bugs"]
- [Security rules, e.g., "Never commit secrets; use environment variables"]
```

### Generation Rules
1. Auto-generate from Stage 1 ideation + Stage 2 architecture outputs
2. Always customize for the actual tech stack — never use generic templates blindly
3. Update whenever architecture or conventions change
4. Keep under 200 lines — if longer, split into domain-specific rule files

---

## File 2: .cursorrules — Cursor IDE Rules

### Purpose
Cursor reads this file on project open. It provides coding conventions and behavior instructions specific to Cursor's AI features.

### Template

```markdown
# [Project Name] — Cursor Rules

## Tech Stack
You are working in a [stack description] project. Key technologies:
- [List 5-8 key dependencies with versions]

## Code Style
- Use [specific patterns, e.g., Composition API <script setup> for all Vue components]
- Prefer [specific choices, e.g., async/await over .then() chains]
- File naming: [convention]
- Import alias: [if any, e.g., @/ for src/]

## AI Behavior Rules
- When generating new components, follow patterns in [path/to/existing/components]
- When editing existing code, preserve the existing style unless explicitly asked to change
- Always import from barrel files when available ([e.g., components/index.ts])
- For API calls, use the service layer in [path/to/services]
- State changes must go through [store/service], never mutate directly

## Tab Complete & Chat Guidelines
- Prefer concise implementations over verbose ones
- Suggest TypeScript types for all function parameters
- When suggesting imports, check if they already exist in the file
- For Vue: use auto-imported composables where available
```

### Generation Rules
1. Generate alongside CLAUDE.md — content overlaps but format differs per tool
2. Focus on what Cursor specifically needs (tab-complete hints, chat behavior)
3. Keep under 100 lines — Cursor truncates long rules files

---

## File 3: INITIAL.md — Feature Request Template

### Purpose
A reusable template for users to describe new features. This replaces vague "build me X" requests with structured, actionable specifications that AI can reliably implement.

### Template

```markdown
## FEATURE
[Describe what you want to build — be specific about functionality, inputs, outputs, and user interactions]

## CONSTRAINTS
- Must work with: [existing tech choices, e.g., Vue 3, Pinia, FastAPI]
- Must NOT break: [existing features or contracts]
- Performance: [any latency, size, or scalability requirements]
- Compatibility: [browsers, devices, or environments to support]

## EXAMPLES TO FOLLOW
- Reference file: [path/to/example/file.ext] — shows [what pattern to follow]
- Reference file: [path/to/another/example.ext] — shows [another pattern]

## DOCUMENTATION
- Relevant docs: [links to API docs, library guides, etc.]
- Internal docs: [paths to docs/ files from earlier stages]
- Schema/API specs: [if applicable]

## ACCEPTANCE CRITERIA
- [ ] [Testable criterion 1]
- [ ] [Testable criterion 2]
- [ ] [Testable criterion 3]

## KNOWN RISKS & PITFALLS
- [Common mistakes AI makes in this domain]
- [Tricky integrations or edge cases]
- [Dependencies that may cause issues]
```

### Usage
1. User copies this template for each new feature request
2. Fills in the fields before handing to AI
3. AI uses the structured input to generate a PRP (see below)

---

## PRP Blueprint (Product Requirements Prompt)

### What is a PRP?
A PRP is an **implementation blueprint designed for AI coding agents**. It combines research findings, documentation references, step-by-step plans, and verification gates into a single document that guides AI through complex implementations.

### PRP Lifecycle

```
INITIAL.md (structured feature request)
        │
        ▼
   ┌──────────────┐
   │ Research     │ ← Analyze codebase patterns, find similar code
   │ Documentation │ ← Gather API docs, library guides
   │ Blueprint    │ ← Create step-by-step plan with validation gates
   │ Confidence   │ ← Score confidence 1-10 before proceeding
   └──────┬───────┘
          ▼
   PRPs/[feature-name].md
          │
          ▼
   ┌──────────────┐
   │ Execute      │ ← Implement each step from the blueprint
   │ Validate     │ ← Run verification gates after each step
   │ Iterate      │ ← Fix failures until all gates pass
   │ Complete     │ ← Confirm all acceptance criteria met
   └──────────────┘
```

### PRP Template

```markdown
# PRP: [Feature Name]

## Context
[Why this feature exists. What problem it solves. Links to PRD/ideation docs.]

## Research Findings
### Existing Patterns
- Found similar implementation in: [file path] — key pattern: [description]
- Database schema reference: [file or migration]
- API contract reference: [file or OpenAPI spec]

### External Dependencies
- Library: [name] — version constraint, key API used
- API: [service] — auth method, rate limits, response format
- Known issues: [from library docs or GitHub issues]

## Implementation Plan
### Step 1: [Foundation Work]
- **Action**: [What to create/modify]
- **Files**: [specific file paths]
- **Pattern to follow**: [example reference]
- **Verification**: [command or test to prove it works]
- **Gate**: ❌ Fail → [rollback strategy]

### Step 2: [Core Logic]
- **Action**: ...
- **Files**: ...
- **Pattern to follow**: ...
- **Verification**: ...
- **Gate**: ...

[Continue for each step...]

## Error Handling Strategy
| Scenario | Handling | User Feedback |
|----------|----------|---------------|
| Network failure | Retry 3x with backoff | Toast: "Connection lost, retrying..." |
| Invalid input | Client-side validate + server reject | Inline field error |
| Auth expired | Redirect to login | Modal: "Session expired" |

## Testing Plan
- Unit tests: [list test files to create/modify]
- Integration tests: [key scenarios]
- E2E tests: [critical user flows]
- Coverage gate: `npm run coverage` must pass [X]%

## Success Criteria
- [ ] All verification gates pass
- [ ] Tests pass with green builds
- [ ] No console errors in target browsers
- [ ] Acceptance criteria from INITIAL.md all satisfied

## Confidence Score: [N]/10
[Reasoning for score. If below 7, flag risks and consider more research.]
```

### Validation Gates
Every PRP step MUST include a verification gate. Gate types:

| Type | Example | When to Use |
|------|---------|-------------|
| **Compile gate** | `tsc --noEmit` | After type-heavy changes |
| **Test gate** | `vitest run src/__tests__/feature.spec.ts` | After logic changes |
| **Lint gate** | `eslint src/new-file.ts` | After any new file |
| **Build gate** | `vite build` | After dependency changes |
| **Manual gate** | Visual inspection of UI | After CSS/layout changes |
| **Security gate** | Audit for secrets, SQL injection, XSS | After any I/O change |

### Examples Directory Pattern

```
examples/
├── README.md              # Describe what each example demonstrates
├── components/            # UI component patterns
│   ├── form-example.vue   # Form handling with validation
│   └── table-example.vue  # Data table with pagination
├── services/              # Service layer patterns
│   └── api-client.ts      # Authenticated API call pattern
├── stores/                # State management patterns
│   └── example-store.ts   # Pinia store with actions/getters
└── tests/                 # Testing patterns
    ├── component.test.ts  # How to mount and test components
    └── api-mock.ts        # How to mock API responses
```

> **Rule**: Every time you discover a useful pattern during development, add it to `examples/`. This compounds over time — the more examples, the better AI performs.
