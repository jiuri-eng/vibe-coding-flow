# Stage 2: Requirements & PRD — VibeCLI

## Product Overview

**VibeCLI** is a command-line codebase analysis tool. Given a target directory path, it scans all recognized source files and generates a Markdown report containing:

1. **File Inventory**: File counts by extension, line counts per language, total size
2. **Complexity Analysis**: Functions/methods exceeding length thresholds, deep nesting warnings
3. **Security Quick-Scan**: Pattern-based detection of common vulnerability patterns
4. **Summary Statistics**: Totals, ratios, and health scores

---

## Functional Requirements

### F1: File Inventory Scanning

**Description**: Recursively scan target directory, categorize files by extension, count lines of code.

**Acceptance Criteria**:
- AC-1.1: Recursively walks directory tree (default depth: unlimited)
- AC-1.2: Groups files by extension into categories (`.py`, `.js`, `.ts`, `.html`, `.css`, `.md`, `.json`, other)
- AC-1.3: Counts total lines per file and sums per category
- AC-1.4: Skips hidden directories (`.` prefix), `node_modules/`, `__pycache__/`, `.git/`
- AC-1.5: Handles permission errors gracefully (log warning, continue)

**User Story**: As a developer, I want to see what languages/files my project contains so I understand its composition.

---

### F2: Complexity Detection

**Description**: Analyze source files for code complexity indicators using heuristic pattern matching.

**Acceptance Criteria**:
- AC-2.1: Detects function/method definitions with bodies exceeding 50 lines
- AC-2.2: Detects indentation nesting deeper than 4 levels
- AC-2.3: Reports file path, line number, and measured value for each finding
- AC-2.4: Supports Python (def/class) and JavaScript/TypeScript (function/=>/class) patterns
- AC-2.5: Severity labeling: WARNING (>50 lines), CRITICAL (>100 lines or >6 nested)

**User Story**: As a developer, I want to know which parts of my code are overly complex so I can refactor them.

---

### F3: Security Pattern Scanning

**Description**: Scan source files for known insecure patterns using regex-based matching.

**Acceptance Criteria**:
- AC-3.1: Detects hardcoded secret-like patterns (password, api_key, secret, token with string values)
- AC-3.2: Detects dangerous function calls (eval(), exec(), subprocess with shell=True)
- AC-3.3: Detects potential SQL injection patterns (f-strings/format %s in SQL context)
- AC-3.4: Reports match context (file:line + surrounding code snippet)
- AC-3.5: Labels findings as "POTENTIAL" (not definitive — this is regex, not AST)

**User Story**: As a developer, I want a quick security sanity check so I don't accidentally commit secrets.

---

### F4: Markdown Report Generation

**Description**: Compile all analysis results into a formatted Markdown document.

**Acceptance Criteria**:
- AC-4.1: Report has header section with project name, scan timestamp, target path
- AC-4.2: Each analysis category is a separate `##` section with data table
- AC-4.3: Security findings sorted by severity (CRITICAL > HIGH > MEDIUM > LOW)
- AC-4.4: Includes summary section with totals and health score (0-100)
- AC-4.5: Outputs to stdout by default, or to file via `-o` flag

**User Story**: As a developer, I want a readable report I can view in terminal or any Markdown viewer.

---

### F5: CLI Interface

**Description**: Provide command-line interface via argparse.

**Acceptance Criteria**:
- AC-5.1: Positional argument `PATH` (target directory, default: `.`)
- AC-5.2: Optional `-o/--output` for writing report to file
- AC-5.3: Optional `--security-only` to run only security scan (skip inventory/complexity)
- AC-5.4: `--help` shows usage with examples
- AC-5.5: Exit codes: 0=success, 1=error, 2=findings detected

---

## Non-Functional Requirements

| ID | Requirement | Detail |
|----|-------------|---------|
| NFR-1 | Zero dependencies | Python stdlib only (os, re, sys, argparse, pathlib, datetime) |
| NFR-2 | Performance | < 2 seconds for 100-file project on modern hardware |
| NFR-3 | Encoding | Handle UTF-8 and Latin-1; skip undecodable files with warning |
| NFR-4 | Safety | Read-only operation; never modify or delete user files |
| NFR-5 | Path traversal protection | Reject paths containing `..` sequences |
| NFR-6 | Terminal output | Pure Markdown, no ANSI colors (maximum compatibility) |

## Information Architecture

```
VibeCLI Report Structure:
# VibeCLI Report: {project_name}
## Metadata (path, timestamp, file count)
## File Inventory (table: ext | count | lines | %)
## Complexity Findings (table: file | line | type | severity)
## Security Findings (table: file | line | pattern | severity)
## Summary (totals, health score, recommendations)
```

## User Stories Summary

| US-ID | As a... | I want to... | So that... | Maps to F |
|-------|---------|-------------|------------|----------|
| US-1 | Developer | See file composition | Understand project structure | F1 |
| US-2 | Developer | Find complex code | Refactor proactively | F2 |
| US-3 | Developer | Quick security check | Avoid committing secrets | F3 |
| US-4 | Developer | Get formatted report | Share or archive findings | F4 |
| US-5 | DevOps engineer | Run from CI/CD | Automate quality gates | F5 |

## Validation (L1-2 Self-Check)

| Check | Result |
|-------|--------|
| All required sections present | PASS (overview, functional reqs with AC, non-functional, IA, US, acceptance checklist) |
| Every functional requirement has acceptance criteria | PASS (F1-F5 each has AC-x.y entries) |
| No orphaned requirements | PASS (each F maps to >=1 US) |
| PRD internally consistent | PASS (NFR-4 "read-only" aligns with F3.5 "POTENTIAL" labeling) |

**L1-2: PASS — Ready for Stage 3**

## Next → Stage 3: Architecture & Tech Stack
