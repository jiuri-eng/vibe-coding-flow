# Prompt Template Library

## Overview

A curated collection of proven prompt patterns for common Vibe Coding scenarios. These templates eliminate guesswork — use them as starting points and customize for your specific context.

**Philosophy**: Good prompts = clear intent + sufficient constraints + concrete examples + verifiable output.

---

## Category 1: Feature Implementation Prompts

### T-1: New Feature (Standard)

```
## Task
Implement [feature name] as described in docs/02-prd.md section [FR-XX].

## Context
- Tech stack: [from architecture doc]
- Related files: [list existing files that interact with this feature]
- Pattern to follow: [reference example in examples/]

## Requirements
1. [Specific requirement 1 with acceptance criterion]
2. [Specific requirement 2 with acceptance criterion]
3. [Specific requirement 3 with acceptance criterion]

## Constraints
- Must integrate with existing [component/service/store] without breaking it
- Follow the code style in [style guide or example file]
- Include error handling for [specific edge cases]

## Output Expected
- Files to create: [list]
- Files to modify: [list with specific changes]
- Tests to write: [test file path + what to test]

## Verification
Run [command] to verify the implementation works.
```

### T-2: Bug Fix

```
## Bug Report
- **What**: [description of wrong behavior]
- **Expected**: [what should happen]
- **Actual**: [what actually happens]
- **Reproduction Steps**: [steps to reproduce]

## Investigation Required
1. Read these files first: [file paths]
2. Identify root cause (do NOT just fix symptoms)
3. Check if similar bug exists elsewhere in codebase

## Fix Requirements
- Minimal change that fixes the root cause
- Add regression test so this cannot reoccur
- Do NOT refactor surrounding code unless necessary

## Verification
[command to run to confirm fix + test passes]
```

### T-3: Refactoring

```
## Refactoring Goal
[What to improve: performance / readability / maintainability / type safety]

## Scope
Files involved: [list files]
Current problem: [describe technical debt or issue]

## Constraints
- Behavior must NOT change — all existing tests must still pass
- One logical change per commit
- If refactoring is complex, break into sub-tasks

## Approach
1. First, add tests that document current behavior (safety net)
2. Make the refactoring change
3. Run full test suite
4. Remove any now-redundant tests if appropriate
5. Verify build/lint still passes
```

---

## Category 2: Architecture & Design Prompts

### T-4: Tech Stack Decision

```
## Project Requirements
- Type: [Web App / CLI / Full-stack / etc.]
- Scale expectation: [users, data volume, complexity]
- Team size: [number of developers]
- Timeline: [MVP deadline]
- Special requirements: [real-time? offline? i18n? etc.]

## Options Analysis
For each option, provide:
1. Pros for our use case
2. Cons / risks
3. Learning curve for team
4. AI coding support quality
5. Community & ecosystem health
6. Deployment complexity

## My Preferences (if any)
- [Any tech the user already knows or prefers]
- [Any tech to explicitly avoid]

## Deliverable
Recommend ONE primary option with rationale, plus a fallback option.
```

### T-5: API Design

```
## API Purpose
[What this API should do]

## Resources & Endpoints
Design RESTful endpoints covering:
- List/create/read/update/delete operations
- Filtering, pagination, sorting where needed
- Authentication requirements
- Rate limiting considerations

## Response Format
Define standard:
- Success response shape
- Error response shape (with error codes)
- Pagination metadata format

## Integration Points
- Which frontend components consume this API?
- What auth mechanism is used?
- What database/caching layer sits behind?
```

---

## Category 3: Code Generation Prompts

### T-6: Component Generation (Vue/React)

```
## Component: [ComponentName]
- **Purpose**: [one-line description of what it does]
- **Type**: [Page feature / Layout / Presentational / Container]

## Props Interface
```typescript
interface [Name]Props {
  // Define all props with types and whether required
  propOne: string;
  propTwo?: number;  // optional
  callback: () => void;
}
```

## Design Tokens (from UI Design doc)
- Use colors from design system: --color-primary, --color-bg, etc.
- Spacing tokens: --space-sm/md/lg/xl
- Typography: --text-body, --text-h2
- Border radius: --radius-md
- Transitions: --transition-fast

## Behavior
- On mount: [what happens]
- User interaction: [what user can do]
- Error state: [how errors display]
- Loading state: [how loading displays]
- Empty state: [how empty data displays]

## Accessibility
- Keyboard navigation: [what keys do what]
- Screen reader labels: [aria attributes needed]
- Focus management: [where focus goes after actions]
```

### T-7: Service / API Client

```
## Service: [ServiceName]
- **Purpose**: [API domain this service handles]
- **Base URL**: [API base URL or config key]

## Methods to Implement
| Method Name | HTTP | Endpoint | Description | Parameters | Return Type |
|-------------|------|---------|-------------|-----------|------------|
| [name] | GET | /path | [desc] | [params] | [type] |
| [name] | POST | /path | [desc] | [body] | [type] |

## Error Handling Strategy
- Network errors: [retry logic? toast? redirect?]
- Auth errors (401/403): [refresh token? redirect to login?]
- Server errors (5xx): [retry? fallback? show generic message?]
- Validation errors (422): [show field-level errors?]

## Caching Strategy
- Which endpoints to cache? [none / stale-while-revalidate / etc.]
- Cache invalidation triggers?

## Example Call Pattern
```typescript
// Show how other parts of the codebase call services
const result = await service.method(params);
// Handle result or error
```
```

### T-8: Store / State Management (Pinia/Zustand)

```
## Store: [StoreName]
- **Domain**: [what domain this store manages]

## State Shape
```typescript
interface [Name]State {
  // List all state fields with types and initial values
}

interface [Name]Getters {
  // Derived/computed values
}

interface [Name]Actions {
  // Mutations with parameter types and return types
}
```

## Persistence
- Should this state persist across page refreshes? [yes/no]
- If yes: localStorage? sessionStorage? plugin?

## Side Effects
- Which actions trigger API calls?
- How are loading/error states managed during async operations?
- What happens on concurrent calls to the same action?
```

### T-9: Test Generation

```
## Test Target: [file or module being tested]

## Test Categories
### Unit Tests
Test each function/component in isolation:
1. Happy path: [normal input → expected output]
2. Edge case: [boundary conditions]
3. Error case: [invalid input / failure mode]
4. Default behavior: [no props / empty state / null input]

### Integration Tests
Test interactions between components/services:
1. [Scenario 1: user flow step by step]
2. [Scenario 2: error recovery flow]

## Test Framework Config
- Framework: [Vitest / Jest / Playwright]
- Testing library: [@testing-library/vue / react-testing-library]
- Mock strategy: [factory functions / MSW / mock files]

## Coverage Requirements
- Minimum coverage: [X%] for new code
- Must cover: [critical paths that must have tests]
- Exempt: [types/interfaces that don't need unit tests]

## Anti-Patterns to Avoid
- Don't test implementation details (test behavior instead)
- Don't mock everything (mock only external dependencies)
- Don't use brittle selectors (use accessible queries)
```

---

## Category 4: Review & Debugging Prompts

### T-10: Code Review Request

```
## Review Scope
- Files changed: [list file paths or link to diff]
- PR/Task reference: [task number or PR link]

## Review Criteria
1. **Correctness**: Does the code implement the requirement correctly?
2. **Edge cases**: Are there unhandled edge cases or error scenarios?
3. **Security**: Any injection risks, exposed secrets, auth bypasses?
4. **Performance**: Any N+1 queries, unnecessary re-renders, memory leaks?
5. **Style consistency**: Does it match project conventions?
6. **Test coverage**: Are there sufficient tests for the changes?
7. **Type safety**: Are types complete and correct?

## Context
- This is part of: [feature name from PRD]
- Dependencies on: [other modules or services]
- Known constraints: [from architecture decisions]

## Output Format
List issues as:
- [BLOCKER] Must fix before merge
- [WARNING] Should fix but not blocking
- [SUGGESTION] Nice to have improvement
- [NIT] Minor style observation
```

### T-11: Debug Session

```
## Problem Symptom
- **Expected behavior**: [what should happen]
- **Actual behavior**: [what happens instead]
- **Error message** (if any): [full error text]
- **Frequency**: [always / intermittent / only when...]

## Environment
- Browser/Runtime: [version]
- Node/Python version: [version]
- Relevant dependencies: [key packages + versions]

## What I've Tried
1. [Attempt 1]: result was [outcome]
2. [Attempt 2]: result was [outcome]
3. [Attempt 3]: result was [outcome]

## Relevant Code
[Paste the relevant code sections — focus on the area around the problem]

## Hypotheses (if any)
I suspect the issue might be related to: [your theory]
Please investigate and either confirm or disprove.
```

---

## Category 5: Project Management Prompts

### T-12: Progress Check

```
## Project Status Request

### Completed Tasks
[List completed task IDs with brief summary]

### Current Task
- Task ID: [T-XX]
- Status: [in progress / blocked / needs review]
- Blocker (if any): [what's blocking]

### Remaining Tasks
[List pending tasks with priorities]

### Questions for Reviewer
1. [Question about approach decision]
2. [Technical trade-off to discuss]
3. [Scope question about a requirement]
```

### T-13: Session Handoff (Context Compaction)

```
## Session Summary — [Project Name] — [Date]

### What Was Accomplished
1. [Completed item 1 with file references]
2. [Completed item 2 with file references]
3. [Completed item 3 with file references]

### Key Decisions Made
- [Decision 1]: chose X over Y because...
- [Decision 2]: adopted pattern Z because...

### Current State of Codebase
- Working branch: [branch name]
- Last successful build: [yes/no + command]
- Failing tests (if any): [list]
- Known issues: [list open problems]

### Where We Left Off
- Next task: [T-XX description]
- Incomplete work: [partial implementation notes]
- Pending questions: [questions for user]

### To Resume Next Session
1. Read AGENTS.md / CLAUDE.md
2. Read docs/05-todo.md for task list
3. Read this handoff file
4. Continue with task [T-XX]
```

---

## Prompt Quality Checklist

Before sending any prompt to AI, verify:

| Check | Question |
|-------|----------|
| **Intent clear?** | Can someone understand WHAT to build without asking follow-ups? |
| **Constraints stated?** | Are boundaries, "must NOT", and limitations explicit? |
| **Examples provided?** | Is there at least one concrete pattern to follow? |
| **Output defined?** | Is it clear exactly what files/code to produce? |
| **Verification included?** | Is there a way to prove the output is correct? |
| **Context sufficient?** | Does the AI have enough info about the project (stack, patterns, conventions)? |
| **Length appropriate?** | Long enough to be precise, short enough to fit context window (< 2000 tokens ideal) |

## Anti-Patterns (Never Do These)

| Anti-Pattern | Why It Fails | Fix |
|-------------|-------------|-----|
| "Build me a [vague thing]" | Too ambiguous, AI guesses wrong | Use T-1 template with specifics |
| "Fix the bug" (no details) | AI doesn't know which bug | Use T-2 template |
| Prompt gets longer each iteration | Context collapse, quality degrades | Reference docs instead of repeating info |
| Copy-pasting entire files | Wastes tokens, obscures intent | Describe changes, point to line ranges |
| No acceptance criteria | Can't verify if AI succeeded | Always include verification step |
