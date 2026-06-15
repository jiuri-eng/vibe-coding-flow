# vibe-coding-flow

> **8 阶段 Vibe Coding 工作流** — 面向 AI 编程代理的平台无关技能框架。

[English](#english) | [中文](#中文)

---

## English

### What is this?

`vibe-coding-flow` is a **skill** for AI coding agents (WorkBuddy, Cursor, Claude Code, Codex, Windsurf, etc.). It transforms a raw idea into a runnable project through a structured **8-stage workflow**:

```
Idea → PRD → Architecture → UI Design → Tasks → Code → Deliver
 ↑                                                               |
 +──────────────────── Feedback Loop (Self-Check L1-L4) ──────────+
```

### Key Features

| Feature | Description |
|---------|-------------|
| **Platform Auto-Detection** | Detects WorkBuddy/Cursor/Claude Code/Codex/Gemini and auto-adapts |
| **Project Size Router** | S / M / L / XL routing — small ideas get Fast Track, large systems get multi-session planning |
| **Self-Check System (L1-L4)** | Stage gates, task gates, context checkpoints, and anti-pattern monitoring |
| **Context Budget** | Token budget tiers with forced mitigation at 80% / 95% thresholds |
| **Session Handoff** | Self-contained handoff packages for multi-session large projects |
| **Multi-Agent Orchestration** | Parallel specialist teams with role templates |
| **Security Gates** | Pre-commit scanning + runtime safety checklist |
| **13+ Prompt Templates** | Proven patterns for features, bugs, reviews, debugging, tests |

### Installation

#### WorkBuddy

```
/install-skill vibe-coding-flow
```

Or manually: clone this repo into `~/.workbuddy/skills/vibe-coding-flow/`.

#### Cursor / Windsurf / Claude Code

Copy `SKILL.md` content into your project's rule file (`.cursorrules`, `.windsurfrules`, `CLAUDE.md`, etc.).

### Stage Overview

| Stage | Output | File |
|:---:|---------|------|
| S0 | Context Setup | `CLAUDE.md` / `.cursorrules` |
| S1 | Ideation & Scoping | `docs/01-ideation.md` |
| S2 | PRD | `docs/02-prd.md` |
| S3 | Architecture & Tech Stack | `docs/03-architecture.md` |
| S4 | UI/UX Design | `docs/04-ui-design.md` (skip for CLI) |
| S5 | Task Breakdown | `docs/05-todo.md` |
| S6 | Implementation | Source code |
| S7 | Delivery | `README.md` + deploy instructions |

### Example Projects

- **`example-project/`** — Full 8-stage Web App (VibeTodo, Vanilla JS)
- **`example-project-cli/`** — 7-stage CLI Tool (VibeCLI, Python)

### Requirements

None. Pure markdown + prompt patterns. Works with any AI agent that can read files.

### License

MIT

---

## 中文

### 这是什么？

`vibe-coding-flow` 是一个面向 AI 编程代理的**技能（Skill）**，支持 WorkBuddy、Cursor、Claude Code、Codex、Windsurf 等平台。它通过结构化的 **8 阶段工作流**，将原始想法转化为可运行的项目：

```
想法 → PRD → 架构 → UI设计 → 任务拆解 → 编码 → 交付
 ↑                                                         |
 +────────────── 反馈循环（自检 L1-L4）──────────────────────+
```

### 核心特性

| 特性 | 说明 |
|------|------|
| **平台自适应** | 自动检测 WorkBuddy/Cursor/Claude Code/Codex/Gemini 并适配 |
| **项目规模路由** | S/M/L/XL 分级 — 小项目走 Fast Track，大系统走多会话规划 |
| **自检系统（L1-L4）** | 阶段门控、任务门控、上下文检查点、反模式监控 |
| **上下文预算** | Token 预算分级，80% / 95% 强制缓解措施 |
| **会话交接** | 大型项目多会话交接包，上下文不丢失 |
| **多代理编排** | 并行专家团队 + 角色模板 |
| **安全门控** | 提交前扫描 + 运行时安全检查清单 |
| **13+ 提示词模板** | 功能/缺陷/审查/调试/测试的成熟模式 |

### 安装

#### WorkBuddy

```
/install-skill vibe-coding-flow
```

或手动：将此仓库克隆到 `~/.workbuddy/skills/vibe-coding-flow/`。

#### Cursor / Windsurf / Claude Code

将 `SKILL.md` 内容复制到项目的规则文件（`.cursorrules`、`.windsurfrules`、`CLAUDE.md` 等）。

### 阶段概览

| 阶段 | 产出 | 文件 |
|:---:|------|------|
| S0 | 上下文工程 | `CLAUDE.md` / `.cursorrules` |
| S1 | 构思与范围 | `docs/01-ideation.md` |
| S2 | 需求与 PRD | `docs/02-prd.md` |
| S3 | 架构与技术栈 | `docs/03-architecture.md` |
| S4 | UI/UX 设计 | `docs/04-ui-design.md`（CLI 项目跳过） |
| S5 | 任务拆解 | `docs/05-todo.md` |
| S6 | 实现 | 源代码 |
| S7 | 交付 | `README.md` + 部署说明 |

### 示例项目

- **`example-project/`** — 完整 8 阶段 Web 应用（VibeTodo，原生 JS）
- **`example-project-cli/`** — 7 阶段 CLI 工具（VibeCLI，Python）

### 依赖

零依赖。纯 Markdown + 提示词模式，适用于任何能读取文件的 AI 代理。

### 许可证

MIT

---

## References

All 18 reference modules are in `references/`:

| File | Purpose |
|------|---------|
| `quick-start.md` | 5-minute guide for new users |
| `context-engineering.md` | Stage 0: auto-generate project context |
| `mcp-integration.md` | MCP server setup |
| `prompt-templates.md` | 13+ prompt patterns |
| `security-checklist.md` | Pre-commit security gates |
| `multi-agent-orchestration.md` | Parallel agent teams |
| `self-check.md` | L1-L4 self-check system |
| `context-budget.md` | Token budget tiers |
| `session-handoff.md` | Multi-session handoff packages |
| `advanced-qa.md` | Meta-Mentor CPI (Chain-Pattern Interrupts) |
| `token-efficiency.md` | 8-level context compression |
| `tech-stacks.md` | Tech stack recommendations |
| `docker-sandbox.md` | Docker isolation (on-demand) |
| `windows-setup.md` | Windows setup (on-demand) |
| `rule-pack.md` | Rule package management (on-demand) |
| `design-reverse.md` | Design token extraction (on-demand) |
| `ci-cd-integration.md` | GitHub Actions (on-demand) |
