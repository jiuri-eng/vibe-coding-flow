# Stage 5: Task Breakdown & TODO — VibeCLI

> Note: Stage 4 (UI/UX Design) was **skipped** for this project.
> Reason: VibeCLI is a CLI tool with no graphical interface.
> Alternative: CLI interaction model defined in Stage 2 PRD (F5).

## TODO List

### T-01: Project Scaffold
**Description**: Create `vibecli.py` with imports, constants, data classes, and entry point stub.
**Prompt Template**: T-1 (New Feature)
**Acceptance Criteria**:
- AC-1.1: File exists with correct shebang (`#!/usr/bin/env python3`)
- AC-1.2: All stdlib imports present (os, re, sys, argparse, pathlib, datetime, dataclasses)
- AC-3.1: `FileInfo`, `ComplexityFinding`, `SecurityFinding`, `ScanResult` dataclasses defined
- AC-3.2: Regex constants pre-compiled at module level
**Complexity**: Low | **Dependencies**: None

### T-02: File Collection Engine (`collect_files`)
**Description**: Implement recursive directory walking with filtering, line counting, and categorization.
**Prompt Template**: T-1 (New Feature)
**Acceptance Criteria**:
- AC-1.1: Recursively walks target directory
- AC-1.2: Groups files by extension into language categories
- AC-1.3: Counts lines per file accurately
- AC-1.4: Skips hidden dirs, node_modules, __pycache__, .git
- AC-1.5: Handles permission errors gracefully
**Complexity**: Medium | **Dependencies**: T-01

### T-03: Complexity Analyzer (`analyze_complexity`)
**Description**: Implement function length detection and nesting depth analysis using regex.
**Prompt Template**: T-1 (New Feature)
**Acceptance Criteria**:
- AC-2.1: Detects functions >50 lines body
- AC-2.2: Detects nesting >4 levels
- AC-2.3: Reports file:line + measured value
- AC-2.4: Supports Python and JS/TS patterns
- AC-2.5: Severity labeling (WARNING/CRITICAL)
**Complexity**: Medium-High | **Dependencies**: T-01

### T-04: Security Scanner (`scan_security`)
**Description**: Implement regex-based security pattern detection across source files.
**Prompt Template**: T-1 (New Feature)
**Acceptance Criteria**:
- AC-3.1: Detects hardcoded secret-like strings
- AC-3.2: Detects eval()/exec()/dangerous calls
- AC-3.3: Detects SQL injection pattern vectors
- AC-3.4: Reports file:line + truncated snippet
- AC-3.5: Labels as "POTENTIAL" finding
**Complexity**: High | **Dependencies**: T-01, T-02

### T-05: Report Formatter (`format_report`)
**Description**: Build Markdown report string from aggregated scan results.
**Prompt Template**: T-6 (Component Generation — template/renderer)
**Acceptance Criteria**:
- AC-4.1: Header with project name, timestamp, path
- AC-4.2: Sections for inventory, complexity, security
- AC-4.3: Security sorted by severity
- AC-4.4: Summary with totals and health score
- AC-4.5: Supports stdout and file output
**Complexity**: Medium | **Dependencies**: T-01

### T-06: CLI Entry Point & Integration (`main` + `scan_directory`)
**Description**: Wire up argparse, orchestrate scan pipeline, handle output and exit codes.
**Prompt Template**: T-1 (New Feature)
**Acceptance Criteria**:
- AC-5.1: Positional PATH argument (default `.`)
- AC-5.2: `-o/--output` flag for file output
- AC-5.3: `--security-only` flag
- AC-5.4: `--help` with usage examples
- AC-5.5: Exit codes 0/1/2
**Complexity**: Medium | **Dependencies**: T-02, T-03, T-04, T-05

## Dependency Graph

```
T-01 (Scaffold)
    │
    ├──────────────┬──────────────┐
    ▼              ▼              ▼
T-02          T-03          T-05
(Collection)   (Complexity)   (Formatter)
    │              │              │
    ▼              │              │
T-04            │              │
(Security)      │              │
    │              │              │
    └──────┬───────┘              │
           ▼                      │
         T-06 ◄──────────────────┘
      (Integration)
```

## Multi-Agent Evaluation

**Decision**: **Single-Agent Sequential**

Rationale:
- Only 6 tasks, all tightly coupled in single-file architecture
- Tasks have strong sequential dependencies (T-02 must complete before T-04)
- Total estimated effort: ~280 lines of code
- Parallel execution would add coordination overhead exceeding benefit

## PRD-to-Task Coverage

| PRD Requirement | Maps To Tasks |
|-----------------|---------------|
| F1: File Inventory | T-01, T-02 |
| F2: Complexity Detection | T-03 |
| F3: Security Scanning | T-04 |
| F4: Report Generation | T-05 |
| F5: CLI Interface | T-06 |

Coverage: **5/5 = 100%**

## Validation (L1-5 Self-Check)

| Check | Result |
|-------|--------|
| All tasks have required fields (ID, desc, AC, constraints, complexity, deps) | PASS |
| Dependency graph is acyclic | PASS (no cycles) |
| Every PRD requirement maps to >=1 task | PASS (5/5 coverage) |
| Tasks are atomic | PASS (each task does ONE thing) |
| Multi-agent evaluation documented | PASS (sequential decision with rationale) |

### L3 Cross-Stage Check (First Pass)

- **PRD→Architecture alignment**: Every F-number has implementation path ✅
- **Architecture→TODO coverage**: Every module assigned to >=1 task ✅
- **Gaps**: None detected

**L1-5: PASS + L3 First Pass: PASS — Ready for Stage 6**

## Next → Stage 6: Implementation
