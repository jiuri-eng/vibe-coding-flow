---
name: vibe-coding-flow
version: "4.4"
description: "Vibe Coding 全流程技能(v4.3.2)：平台无关的 8 阶段闭环工作流。含平台自适应检测(WorkBuddy/Cursor/Claude/Codex/Gemini 自动适配)、项目规模路由(S/M→Fast Track)、核心11模块、高级5模块(按需加载)、多代理编排、13+ Prompt模板、Partial Re-do回退。触发词：'帮我做个项目'、'从想法到产品'、'vibe coding 流程'。"
agent_created: true
---

# Vibe Coding Flow

> **New user? Start here**: [Quick Start Guide](references/quick-start.md) — 5 minutes, copy-paste templates, covers Web/CLI/Fast Track modes. Windows user? Also check [Windows Setup](references/windows-setup.md) (advanced module, load on demand).

## Project Size Router (项目规模路由)

**Load this FIRST** — before deciding whether to run the full 8-stage workflow. One look at the user's request tells you which path to take:

| Signal | Tier | Action |
|--------|:---:|--------|
| "帮我做个...小工具/脚本/单页面" / ~5 features max | **S** | **Fast Track** — skip confirmations, produce minimal docs, build fast |
| "做个...应用/网站" / 5-15 features / has backend | **M** | **Standard** — full 8 stages, single session (see Context Budget) |
| "做一个...系统/平台" / 15-30 features / multi-module | **L** | **Standard + Multi-Agent** — plan for agent split at S5 |
| "搭建/重构/整个..." / 30+ features / team project | **XL** | **Plan multi-session** — pre-generate handoff template at S5 |

**S/M default**: If the user's request is under 30 words and sounds like a quick tool → **Fast Track by default**. Tell the user: "This looks like a Fast Track project. I'll skip confirmations and build quickly. Say 'full mode' if you want the 8-stage workflow."

**What Fast Track does**: S0-S7 still execute, but Stage confirmations are skipped. Documents are generated as lightweight checklists, not full templates. Stage 4 may be simplified. Self-Check still runs at each stage gate.

---

## Platform Auto-Detection (平台自适应)

**Load this SECOND** — right after Project Size Router. This skill is platform-agnostic. After loading, YOU (the AI) must detect your current platform, **get user confirmation**, and adapt accordingly.

---

### Step 1: Gather Platform Fingerprint

Before guessing, collect a **fingerprint** — a short list of observed facts from your system prompt and tools. This is for debugging (Problem #5) and for the confirmation message shown to the user.

```
Platform Fingerprint:
- Model name: [e.g., claude-sonnet-4-20250514]
- OS reported: [e.g., win32 / darwin / linux]
- Tools available: [list 3-5 most distinctive tools, e.g., Agent, Skill, Bash, WebFetch]
- Special blocks found: [e.g., product_identity, .cursorrules reference, sandbox reference]
- Best-guess platform: [platform name]
- Confidence: [HIGH / MEDIUM / LOW]
```

### Step 2: Match Against Detection Profiles

Compare the fingerprint against these profiles. Use **fuzzy matching** — a platform matches if it hits >= 2 of its signals, not just one exact keyword. If only 1 signal fires, lower confidence to LOW.

| Platform | Strong Signals (>= 2 to match) | Typical Fingerprint |
|----------|-------------------------------|---------------------|
| **WorkBuddy** | `product_identity` block + `Skill` tool + `Agent` tool | High-tool-count, identity-aware |
| **Cursor** | `.cursorrules` reference + `codebase_search` tool + agent-like compose mode | High-tool-count, code-search-heavy |
| **Claude Code** | Claude model name + `Bash` tool + no `Agent`/`Skill` tools | Mid-tool-count, terminal-oriented |
| **Codex CLI** | `codex`/`openai` reference + `sandbox` tool + `AGENTS.md` | Sandbox-oriented, OpenAI ecosystem |
| **Windsurf** | `windsurf` keyword + Cascade agent mode + `codebase_search` | Similar to Cursor but different keyword |
| **Gemini CLI** | `gemini` in model name + Google tool signatures | Google ecosystem |
| **Generic** | No specific signals, or only `Bash` + `WebFetch` | Low-tool-count, minimal |

**Fuzzy matching rule**: If `windsurf` is in system prompt → Windsurf, even if profile ALSO looks like Cursor. Specific keyword beats generic pattern.

### Step 3: Determine Capability Tier

| Tier | Platforms | What It Means |
|------|-----------|---------------|
| **Full** | WorkBuddy | All 8 stages with Multi-Agent, MCP, Sandbox, Confirmation loop. Full Self-Check. |
| **Standard** | Cursor, Codex CLI, Claude Code | 8 stages but some capabilities degraded. Sequential mode where Multi-Agent unavailable. Self-Check runs. |
| **Shell-Only** | Gemini CLI, bare terminal agents | Can read/write files and run commands. Multi-Agent and MCP unavailable. Simplified Self-Check. |
| **Advisory** | Generic AI Chat, Claude.ai (no tools) | NO file system access. You are a coach, not a builder. All output is conversation text. Self-Check is verbal only. |

**Tier gap warning**: If detected tier is ADVISORY, tell the user upfront: "I'm running in Advisory mode — I can plan and guide you through the 8 stages, but I cannot write files or run code. You'll need to do the implementation yourself following my instructions. This experience will be very different from using me in a coding IDE."

### Step 4: Mandatory Confirmation (CRITICAL — fixes Problem #1 and #2)

**After detection, you MUST present this confirmation message to the user before proceeding:**

```
Platform detected: [platform name] (Confidence: [HIGH/MEDIUM/LOW])
Capability tier: [Full/Standard/Shell-Only/Advisory]
Key capabilities: [bullet list of what's available]
Key limitations: [bullet list of what's degraded/absent]

Is this correct? Reply:
  "yes" → Proceed with auto-adapted flow
  "[platform name]" → Manually set platform (e.g., "Windsurf")
  "diagnostic" → Show full platform fingerprint for debugging
```

**User override**: If the user specifies a different platform, accept it immediately. The user knows better than auto-detection. Update the fingerprint's best-guess and confidence accordingly.

**If user doesn't respond**: Assume "yes" after 2 exchanges. But for HIGH confidence detection, you may proceed immediately with a one-line note: "Detected [platform]. Using [tier] mode. Say 'override [name]' to switch."

### Step 5: Apply Capability Profile

Each platform has a **capability profile** — this is HOW it does things, not just a binary yes/no. Use this profile to guide your behavior:

| Capability | Full (WorkBuddy) | Standard (Cursor) | Standard (Claude) | Standard (Codex) | Advisory |
|------------|-----------------|-------------------|-------------------|-----------------|----------|
| **Stage 0 output** | CLAUDE.md + .cursorrules via file write | `.cursorrules` via file write | `CLAUDE.md` via file write | `AGENTS.md` via file write | Output as chat text |
| **Multi-Agent** | `Agent` tool with team patterns | ✗ (force Sequential) | ✗ (force Sequential) | `sandbox` instances | ✗ |
| **MCP servers** | Config in `~/.workbuddy/mcp.json` | Config in Cursor MCP settings | Config in `.mcp.json` | ✗ | ✗ |
| **Session handoff** | `Skill` tool loads modules | Read `references/*.md` files | Read `references/*.md` files | Read `references/*.md` files | Read from chat context |
| **Confirmation** | System-native confirmation | Explicit "Continue? (y/n)" | Explicit "Continue? (y/n)" | Explicit "Continue? (y/n)" | Wait for user message |
| **Preview** | `preview_url` | `preview_url` | ✗ (user opens manually) | ✗ (user opens manually) | ✗ |
| **Sandbox** | Docker via `docker-sandbox.md` | ✗ (native environment) | Docker via Bash | `sandbox` tool | ✗ |

### Step 6: Auto-Adaptation Rules

Based on the capability profile, apply these rules:

| If profile says... | Then... |
|-------------------|---------|
| **Multi-Agent = ✗** | Force Sequential mode. Skip all Multi-Agent references. Mark S5 as "N/A — platform limited". |
| **Handoff = read files** | Section 6 of handoff package says "Module Loading Decision" instead of "Skill Loading Decision". |
| **MCP = ✗** | Skip `references/mcp-integration.md`. Skip MCP config mention in S3. |
| **Sandbox = ✗** | Skip `references/docker-sandbox.md`. Code runs in platform's native environment. |
| **Confirmation = system-native** | Use platform's built-in confirmation mechanism. |
| **Confirmation = explicit y/n** | End every stage with "Continue to next stage? (y/n)" |
| **Confirmation = chat wait** | End every stage with summary. User's next message triggers next stage. |
| **Preview = ✗** | After generating HTML/CSS, tell user: "Open [file path] in your browser to preview." |
| **Tier = Advisory** | CRITICAL: Announce capability gap upfront. All documents are chat output. No file writes. |

### Step 7: Diagnostic Report (for Problem #5 debugging)

If the user says "diagnostic" during confirmation, or if something goes wrong, output this:

```markdown
## Platform Diagnostic Report
- Fingerprint: [collected in Step 1]
- Matched profile: [platform name]
- Confidence: [HIGH/MEDIUM/LOW]
- Capability tier: [Full/Standard/Shell-Only/Advisory]
- Adaptation decisions:
  - Multi-Agent: [enabled / forced-sequential]
  - MCP: [enabled / skipped]
  - Sandbox: [enabled / skipped]
  - Handoff method: [Skill / file-read / chat-context]
  - Confirmation method: [system / explicit-y-n / chat-wait]
  - Preview: [enabled / disabled]
- User override: [none / manual: platform-name]
```

### Platform Extension Hook (for Problem #6 — future community contributions)

In the future, platform-specific profiles will live in `platforms/[name].md` files. When a `platforms/` directory exists, load the matching profile file INSTEAD of using the built-in capability matrix. Until then, use the profiles in this section.

**Future file format** (preview — not yet implemented):
```markdown
# platforms/windsurf.md
## Detection
- signals: ["windsurf", "cascade"]
- fuzzy_priority: high
## Capability Profile
- tier: Standard
- multi_agent: false
- mcp: true
- sandbox: false
- confirmation: explicit_y_n
- handoff: file_read
## Behavior Notes
- Stage 0 output: .windsurfrules
- Multi-agent alternative: Cascade agent mode for sub-tasks
- MCP config: Windsurf MCP settings panel
```

Community contributors only need to write ONE file for a new platform. No need to understand the entire detection system.

---

## Overview

---

## Overview

8-stage vibe coding workflow that transforms a raw idea into a runnable project with documentation and code. Each stage produces a concrete deliverable and requires user confirmation before proceeding.

**Core formula**: `Precise Intent + Sufficient Context + Strict Verification + Proper Tooling = Quality Output`

## Core Modules (11 — Always Load)

| Module | Reference | One-Line Summary |
|--------|-----------|------------------|
| Quick Start | `quick-start.md` | 5-minute first-run path for new users |
| Context Engineering | `context-engineering.md` | Stage 0: Auto-generate CLAUDE.md / .cursorrules / INITIAL.md |
| MCP Integration | `mcp-integration.md` | Extend AI with Context7 / Serena / domain tools |
| Prompt Templates | `prompt-templates.md` | 13+ proven prompt patterns for common scenarios |
| Security Gates | `security-checklist.md` | Pre-commit scanning + runtime safety |
| Multi-Agent Orchestration | `multi-agent-orchestration.md` | Parallel specialist teams + WorkBuddy Agent examples |
| Self-Check System | `self-check.md` | L1 Stage Gate + L2 Task Gate + L2.5 Context Checkpoint + L3 Cross-Stage + L4 Anti-Pattern |
| Token Efficiency | `token-efficiency.md` | 8-level compression for large projects |
| **Context Budget** | `context-budget.md` | **v4.3** — Token budget tiers + per-stage allocation + forced mitigation |
| **Session Handoff** | `session-handoff.md` | **v4.3** — Self-contained handoff packages + skill-loading decision matrix |
| Meta-Mentor CPI | `advanced-qa.md` | Chain-Pattern Interrupts for proactive QA (Module A) |

## Advanced Modules (5 — Load On Demand)

These are specialized modules. Do NOT load them unless the specific condition is met:

| Module | Reference | When to Load |
|--------|-----------|--------------|
| Docker Sandbox | `docker-sandbox.md` | User explicitly requests isolated execution / untrusted code |
| Windows Setup | `windows-setup.md` | User is on Windows + needs Docker/WSL2/MCP path help |
| Rule Pack Management | `rule-pack.md` | Syncing coding rules across teams or machines |
| Design Reverse Engineering | `design-reverse.md` | Matching an existing product's look-and-feel |
| CI/CD Integration | `ci-cd-integration.md` | Setting up GitHub Actions for the project (Stage 7 only) |

## Workflow Decision Tree

```
User gives an idea
  -> Stage 0: Context Setup          [references/context-engineering.md]
    -> Stage 1: Ideation & Scoping
      -> Stage 2: Requirements & PRD
        -> Stage 3: Architecture & Tech Stack + MCP Config  [references/mcp-integration.md]
          -> Stage 4: UI/UX Design       [SKIP for CLI/non-visual projects]
            -> Stage 5: Task Breakdown   [references/prompt-templates.md]
              -> Stage 6: Implementation  [references/security-checklist.md + self-check.md]
                -> Stage 7: Delivery      [references/self-check.md]

Branch points:
  - Stage 5: Multi-Agent? -> [references/multi-agent-orchestration.md]
  - Stage 6: Context collapse / budget > 80%? -> [references/session-handoff.md] + [references/context-budget.md]
  - Any stage: Fast track? -> Auto-advance mode (skip confirmations)
  - Large project (>10K lines)? -> [references/token-efficiency.md]
  - XL project (>50 Stage 6 tasks)? -> Plan multi-session from start [references/context-budget.md]
  - Need quality boost? -> CPI checkpoints [references/advanced-qa.md#Module-A]
```

CRITICAL: After each stage, present the deliverable and WAIT for user confirmation.

---

## Stages (Summary)

### Stage 0: Context Setup → `references/context-engineering.md`
**Output**: CLAUDE.md, .cursorrules, INITIAL.md, examples/
**Key rules**: Generate before any ideation; update after architecture confirmed; keep CLAUDE.md <200 lines
**Self-Check**: L1-0 checklist (files exist, sizes within limits, security section present)

### Stage 1: Ideation & Scoping → Output: `docs/01-ideation.md`
**Purpose**: Clarify raw idea into concrete project definition with boundaries.
**Sections**: One-liner, problem statement, target users, project type, scope IN/OUT, success criteria
**Self-Check**: L1-1 (intent preserved, exclusions listed, criteria measurable)

### Stage 2: Requirements & PRD → Output: `docs/02-prd.md`
**Purpose**: Structured PRD with user stories, functional requirements (with acceptance criteria), non-functional requirements.
**Template**: See full PRD template in SKILL.md or generate from `references/prompt-templates.md` T-12 pattern.
**Self-Check**: L1-2 (all sections present, every F has AC, no orphaned requirements)

### Stage 3: Architecture & Tech Stack → Output: `docs/03-architecture.md`
**Purpose**: Tech stack selection, system architecture, project structure, data model, key decisions with trade-offs.
**Also**: Configure MCP servers (`references/mcp-integration.md`), update Stage 0 files with confirmed stack.
**Tech stacks**: Load recommendations from `references/tech-stacks.md`.
**Self-Check**: L1-3 (stack appropriate complexity, data model covers all PRD entities)

### Stage 4: UI/UX Design → Output: `docs/04-ui-design.md` — **[SKIP for CLI projects]**
**Purpose**: Information architecture, component tree, Design Tokens (concrete values), wireframes, interaction states, responsive strategy.
**Alternative**: For design-matching needs, use reverse engineering (`references/advanced-qa.md#Module-C`)
**Self-Check**: L1-4 (tokens are concrete values, all PRD features have UI rep, component tree covers IA)

### Stage 5: Task Breakdown & TODO → Output: `docs/05-todo.md`
**Purpose**: Ordered task list with acceptance criteria, dependencies, complexity estimates.
**Prompt templates**: Use `references/prompt-templates.md` (T-1 for features, T-9 for tests)
**Decision point**: Single-Agent Sequential vs Multi-Agent Parallel (load `references/multi-agent-orchestration.md`)
**Self-Check**: L1-5 (tasks atomic, DAG acyclic, all F-numbers covered) + **L3 First Pass** (PRD→Arch alignment, Arch→TODO coverage)

### Stage 6: Implementation → Source Code
**Loop per task**: Intent → Template Selection → Context Construction → Code Generation → Test → **L2 Task Gate** → Verify → Commit → Mark Complete

**L2 Task Gate (MANDATORY)** — see `references/self-check.md`:
- **L2-A Security** (`references/security-checklist.md`): secrets, injection, auth, input validation
- **L2-B Quality**: naming conventions, function length <50, nesting <=4, no debug leftovers
- **L2-C Completeness**: all AC satisfied, dependencies honored, imports updated

**Auto-fix rules**: Critical failures block; warnings noted; auto-fix naming/cleanup issues silently.

**L2.5 Context Checkpoint** (every 5 tasks / every task for XL projects) — see `references/context-budget.md` + `references/self-check.md`:
- Budget < 60% → Continue
- Budget 60-80% → Generate Summary Card, continue
- Budget 80-95% → Split to Multi-Agent OR generate Session Handoff Package → **New session recommended**
- Budget > 95% → **MANDATORY**: Generate Handoff Package, STOP session
- Handoff package format: see `references/session-handoff.md`

**L4 Monitoring** (continuous throughout): Doom Loop, Context Collapse, Prompt Debt, Tech Debt, Drift, Budget tracking with thresholds.

### Stage 7: Integration & Polish → Final Deliverable
**Actions**: Integration test → Full Security Audit → Code review → Documentation → Deploy instructions

**Final Self-Check Suite**:
- **L1-7 Delivery Gate**: All tasks done, README complete, security passed, deploy instructions provided
- **L3 Full Run**: C1 PRD→Code coverage matrix, C2 Arch decision tracking, C3 Document sync, C4 Token fidelity
- **L4 Final Scan**: Complete anti-pattern status across entire project lifecycle

**Output format**: Self-Report Card table (see example in `example-project/stage-outputs/stage-7-delivery.md`)

---

## Restart & Skip Rules

| Rule | Description |
|------|-------------|
| **Skip a stage** | User has existing doc? Validate against template, then continue |
| **Partial Re-do** | User rejects ONLY current stage output (e.g., "改技术栈选型") → Re-do current stage only, do NOT roll back to S0 |
| **Restart major pivot** | User rejects the project direction or core decisions from S1-S2 → Go back to Stage 1 (or Stage 0 if tech stack changes) |
| **Fast track** | "Just build it" or S-tier auto-routed → auto-advance mode (still produce docs, skip confirmations) |
| **Multi-agent switch** | At Stage 5 decision point for complex projects |
| **Session handoff** | Budget > 80% or context collapse → Generate handoff package, continue in new session |
| **CLI shortcut** | Stage 4 skipped automatically for non-visual projects |

---

## Example Projects

| Project | Type | Path | Demonstrates |
|---------|------|------|-------------|
| **VibeTodo** | Web App (Vanilla JS) | `example-project/` | Full 8 stages with UI, self-check reports |
| **VibeCLI** | CLI Tool (Python) | `example-project-cli/` | 7 stages (Stage 4 skipped), CLI-specific patterns |

Both include: complete stage output documents, source code, L1-L4 self-check reports, test case matrices.

---

## Resources Index

### `references/` (18 files)

#### Core (auto-loaded with skill)

| File | Size | Purpose |
|------|------|---------|
| `quick-start.md` | ~130 lines | 5-minute guide + reading order + copy-paste templates |
| `tech-stacks.md` | ~105 lines | Tech stack recommendations per project type |
| `context-engineering.md` | ~287 lines | Stage 0 methodology: CLAUDE.md, .cursorrules, INITIAL.md, PRP Blueprints |
| `mcp-integration.md` | ~205 lines | MCP server setup: Context7, Serena, config templates |
| `prompt-templates.md` | ~424 lines | 13+ prompt templates (features, bugs, review, debug, tests) |
| `security-checklist.md` | ~200 lines | Pre-commit security gates, vulnerability patterns, secret management |
| `multi-agent-orchestration.md` | ~500 lines | 3 patterns + WorkBuddy Agent examples, role templates, coordination |
| `self-check.md` | ~700 lines | L1-L4 + L2.5 Context Checkpoint, decision matrices, report formats |
| `token-efficiency.md` | ~420 lines | 8-level compression, hierarchical naming, context window management |
| **`context-budget.md`** | **~130 lines** | **v4.3** — Token budget tiers, per-stage allocation, forced mitigation triggers |
| **`session-handoff.md`** | **~160 lines** | **v4.3** — Handoff package format, skill-loading decision matrix, resume blueprint |
| `advanced-qa.md` | ~140 lines | Module A: Meta-Mentor CPI (Chain-Pattern Interrupts, success +27%) |

#### Advanced (load on demand — see Advanced Modules table for trigger conditions)

| File | Size | Purpose |
|------|------|---------|
| `docker-sandbox.md` | ~573 lines | Docker isolation: 3 sandboxes, seccomp profiles, safety scripts |
| `windows-setup.md` | ~150 lines | Windows: WSL2/Docker, PowerShell, MCP paths, Sandbox alternative |
| `rule-pack.md` | ~120 lines | Module B: Rule package versioning, pack.toml format, validation |
| `design-reverse.md` | ~110 lines | Module C: Design token extraction from existing products |
| `ci-cd-integration.md` | ~150 lines | GitHub Actions workflows: security scans, quality gates, test automation |
| `scripts/validate-pack.py` | ~160 lines | Python CLI: generate + validate + check pack.toml files |

### `example-project/` (Web App)
- 8 stage documents + README + running source (index.html + styles.css + app.js)

### `example-project-cli/` (CLI Tool)
- 6 stage documents (Stage 4 skipped) + README + running source (vibecli.py)
