# MCP Integration Guide

## Overview

MCP (Model Context Protocol) extends AI coding agents with external tools — code search, documentation retrieval, database access, and more. This chapter explains how to configure MCP servers for Vibe Coding projects, reducing context window pressure and improving output quality.

> **Windows user?** Paths and commands differ on Windows (e.g., `npx.cmd` instead of `npx`, `C:\\Users\\...` instead of `/home/...`). See [windows-setup.md](windows-setup.md) for the full Windows MCP config guide.

## When to Use MCP

| Project Scale | MCP Necessity | Recommended Setup |
|---------------|--------------|-------------------|
| Small (< 20 files) | Optional | Context7 for docs only |
| Medium (20-100 files) | Recommended | Context7 + file system MCP |
| Large (100+ files) | Essential | Context7 + Serena + custom MCPs |
| Monorepo / Multi-package | Critical | Full stack: Serena + Context7 + domain MCPs |

## Core MCP Servers for Vibe Coding

### 1. Context7 — Live Documentation Provider

**Purpose**: Inject up-to-date library/framework documentation into AI context. Solves the "hallucinated APIs" problem where LLMs generate code based on outdated training data.

**Stars**: 57.3k+ | **License**: MIT

#### What It Provides
| Tool | Function |
|------|----------|
| `resolve-library-id` | Map a library name to its Context7 ID |
| `query-docs` | Fetch docs + code examples for a specific library |

#### Setup

```bash
# One-command setup (recommended)
npx ctx7 setup --claude    # For Claude Code
npx ctx7 setup --cursor    # For Cursor
npx ctx7 setup             # Auto-detect client
```

Or manual MCP config:

```json
{
  "mcpServers": {
    "context7": {
      "url": "https://mcp.context7.com/mcp",
      "headers": {
        "CONTEXT7_API_KEY": "your-api-key-from-context7-com-dashboard"
      }
    }
  }
}
```

#### Usage Pattern in Prompts
```
Use context7 to fetch latest [library-name] docs for:
[specific feature or API needed]
```

#### Best Practices
- Get a free API key from context7.com/dashboard for higher rate limits
- Specify version numbers when you need version-specific docs: "Next.js 14 middleware"
- Always prefer over letting the LLM guess API signatures

---

### 2. Serena — Semantic Code Toolkit

**Purpose**: IDE-level semantic code operations (search, rename, refactor, navigate) via MCP. Turns fragile text surgery into atomic symbol-level operations.

**Stars**: 25.3k+ | **License**: MIT | **Languages**: 40+ (LSP backend)

#### What It Provides

| Category | Tools | Impact |
|----------|-------|--------|
| **Retrieval** | find-symbol, find-references, symbol-overview, diagnostics | Navigate large codebases instantly |
| **Refactoring** | rename-symbol, move-file, inline, safe-delete | Cross-file changes in one atomic call |
| **Symbolic Editing** | replace-symbol-body, insert-before/after-symbol | Safer and more token-efficient than text replace |
| **Foundation** | search-pattern, list-dir, read-file, execute-shell | Basic filesystem operations |
| **Memory** | Cross-session persistent memory | Maintain context across sessions |

#### Setup

```bash
# Prerequisite: install uv (Python package manager)
# Then:
uv tool install -p 3.13 serena-agent
serena init                    # Uses free LSP backend (40+ languages)
serena init -b JetBrains       # Uses paid JetBrains plugin backend
```

MCP configuration (add to your MCP client config):

```json
{
  "mcpServers": {
    "serena": {
      "command": "serena",
      "args": ["mcp"]
    }
  }
}
```

#### Why Serena Matters for Vibe Coding

Traditional AI code editing reads entire files, finds line numbers, and does text replacement — which breaks when code changes. Serena operates at the **symbol level**:

| Operation | Without Serena | With Serena |
|-----------|---------------|-------------|
| Rename a component used in 12 files | 8-12 error-prone steps | 1 atomic call |
| Find all callers of a function | Grep + manual filter | `find-references` (exact) |
| Change function body | Read file → locate → text replace | `replace-symbol-body` (symbol-aware) |
| Token cost of cross-file edit | High (reads full files) | Low (operates on symbols only) |

---

### 3. Filesystem MCP — Built-in Access

Most AI coding clients include a built-in filesystem MCP. Ensure it is configured with proper scope:

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/path/to/project"]
    }
  }
}
```

**Scope rule**: Only allow access to project directories. Never grant access to home directory or system paths.

### 4. Domain-Specific MCP Servers

For specialized projects, consider these:

| MCP Server | Use Case | Install |
|-----------|----------|---------|
| `postgres` | Database schema queries + SQL execution | `npx @modelcontextprotocol/server-postgres` |
| `github` | Issue management, PR creation, code review | Official GitHub MCP |
| `sequential-thinking` | Complex reasoning chains before coding | `npx @modelcontextprotocol/server-sequential-thinking` |
| `brave-search` | Web research during implementation | Brave Search API key required |
| `puppeteer` | Visual testing / screenshot capture | Browser automation |

## MCP Configuration for Vibe Coding Projects

### Standard MCP Config Template

Create `.mcp.json` in your project root:

```json
{
  "mcpServers": {
    "context7": {
      "url": "https://mcp.context7.com/mcp",
      "headers": {
        "CONTEXT7_API_KEY": "${CONTEXT7_API_KEY}"
      }
    },
    "serena": {
      "command": "serena",
      "args": ["mcp"],
      "env": {}
    },
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "${PROJECT_DIR}"]
    }
  }
}
```

### Per-Stage MCP Usage Guide

| Stage | MCP Tools to Leverage | Purpose |
|-------|---------------------|---------|
| Stage 0 (Context Setup) | Serena: symbol-overview, list-dir | Understand existing codebase structure |
| Stage 1 (Ideation) | Context7: query-docs | Research feasibility of tech choices |
| Stage 3 (Architecture) | Context7 + Serena | Design patterns from real codebase + latest docs |
| Stage 5 (Task Breakdown) | Serena: find-references, diagnostics | Map dependencies and impact areas |
| Stage 6 (Implementation) | All MCP tools | Code generation with live docs + semantic editing |
| Stage 7 (Integration) | Serena: diagnostics, find-symbol | Final quality checks |

## Integration Checklist

- [ ] Identify which MCP servers this project needs (use table above)
- [ ] Create `.mcp.json` in project root with selected servers
- [ ] Set environment variables for API keys (never hardcode)
- [ ] Test each MCP server connectivity before starting Stage 6
- [ ] Document MCP-specific instructions in CLAUDE.md under "Available Tools"
- [ ] If using Serena, run `serena init` and verify language server starts correctly
- [ ] If using Context7, get API key from dashboard for higher rate limits

## Troubleshooting

| Symptom | Likely Cause | Fix |
|---------|-------------|-----|
| MCP server not found | Not installed or wrong command path | Run install command, verify binary exists |
| Permission denied | Filesystem MCP scoped too broadly | Narrow to specific project directories |
| Rate limited (429) | No API key for Context7 | Register at context7.com/dashboard |
| Symbol not found (Serena) | Language server not started | Run `serena init`, check LSP installation |
| Stale docs (Context7) | Cached response | Add version specifier to query prompt |
