# VibeCLI — Codebase Analysis Tool

> A complete CLI example project demonstrating the **vibe-coding-flow** 8-stage workflow for **non-UI / command-line tools**.
>
> **Project Type**: CLI / Developer Tool | **Language**: Python 3.12+ | **Dependencies**: None (stdlib only)

## What This Project Does

`vibecli.py` is a zero-dependency CLI tool that analyzes a codebase and outputs:

1. **File inventory** — count by extension, language breakdown
2. **Complexity scan** — identifies long functions (>50 lines), deep nesting (>4 levels)
3. **Security quick-scan** — finds hardcoded secrets, eval() calls, SQL injection patterns
4. **Markdown report** — generates a formatted analysis report in Markdown

### Usage

```bash
# Analyze current directory
python src/vibecli.py .

# Analyze with output to file
python src/vibecli.py ./my-project -o report.md

# Show only security issues
python src/vibecli.py ./my-project --security-only
```

## Workflow Demonstration: 8 Stages for a CLI Project

| Stage | Output File | Key Difference from Web Project |
|-------|------------|----------------------------------|
| Stage 0 | `stage-outputs/stage-0-context-setup.md` | CLAUDE.md includes CLI conventions (argparse, exit codes) |
| Stage 1 | `stage-outputs/stage-1-ideation.md` | Scope focuses on terminal UX, not visual design |
| Stage 2 | `stage-outputs/stage-2-prd.md` | Non-functional: exit code behavior, stderr handling |
| Stage 3 | `stage-outputs/stage-3-architecture.md` | Module pattern: single-file CLI with subcommands |
| Stage 4 | **SKIPPED** | — | No UI/UX design needed for CLI |
| Stage 5 | `stage-outputs/stage-5-todo.md` | Tasks organized by subcommand (scan / report / security) |
| Stage 6 | `stage-outputs/stage-6-implementation.md` | Implementation + L2 Task Gate per task + L4 monitoring |
| Stage 7 | `stage-outputs/stage-7-delivery.md` | Delivery with self-check report + CLI-specific tests |

### Key Learning: Stage 4 Skip Rule

This project demonstrates when and how to **skip Stage 4 (UI/UX Design)**:

```markdown
Skip Reason: Project is a CLI tool with no graphical user interface.
All user interaction happens via:
  - Command-line arguments (--path, -o, --security-only)
  - Terminal stdout/stderr output
  - Exit codes (0 = success, 1 = error, 2 = findings)

Alternative to Stage 4: Define "CLI Interaction Model" as part of Stage 2 PRD,
covering argument parsing, output format, help text, and error handling behavior.
```

## Self-Check Results (Summary)

```
L1 Stage Gate:     7/7 PASS (Stage 4 correctly skipped)
L2 Task Gate:      5/5 tasks PASS (3 auto-fixes applied)
L3 Cross-Stage:    PASS — All PRD features mapped to code
L4 Anti-Pattern:   ALL CLEAR — Drift=96%, no doom loops
```

## Source Code

- `src/vibecli.py` (~280 lines) — Complete implementation, zero dependencies
- Runs on any Python 3.12+ installation

## Quick Start

```bash
cd example-project-cli/src
python vibecli.py --help
python vibecli.py .. -o ../analysis-report.md
cat ../analysis-report.md
```
