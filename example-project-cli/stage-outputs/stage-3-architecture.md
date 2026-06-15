# Stage 3: Architecture & Tech Stack — VibeCLI

## Tech Stack

| Component | Choice | Rationale |
|-----------|--------|-----------|
| **Language** | Python 3.12+ | stdlib has everything needed (os, re, pathlib, argparse) |
| **Dependency** | None (stdlib only) | Meets NFR-1 zero-dependency requirement |
| **CLI Framework** | `argparse` (stdlib) | Sufficient for this scope; avoids click dependency |
| **Report Format** | Markdown plain text | Universal readability; no rendering needed |
| **File Scanning** | `os.walk()` + `pathlib.Path` | Recursive directory traversal |
| **Pattern Matching** | `re` module (stdlib) | Regex-based complexity/security detection |

## Architecture Decision Record

### ADR-001: Single File Architecture

**Decision**: Entire tool in one file (`vibecli.py`).

**Alternatives considered**:
- Multi-file package structure — Rejected: Over-engineering for ~300 lines of code
- Two files (cli.py + core.py) — Rejected: Adds import overhead without clear benefit

**Rationale**: This is a focused CLI tool with < 400 lines. Single file simplifies distribution (just copy one file). If it grows beyond 500 lines, split into package.

### ADR-002: Regex over AST

**Decision**: Use regex pattern matching for complexity and security scanning.

**Rationale**: AST parsing requires language-specific parsers (ast module for Python only). Regex works across languages with acceptable false-positive rate. PRD explicitly labels findings as "POTENTIAL".

### ADR-003: Streaming Output

**Decision**: Generate report as string in memory, output all at once.

**Alternatives considered**:
- Streaming to stdout line-by-line — Rejected: User may want `-o` file mode
- Template engine — Rejected: No dependencies; f-strings sufficient

## Data Model

```python
@dataclass
class FileInfo:
    path: str           # Relative file path
    ext: str            # File extension (.py, .js, etc.)
    lines: int          # Line count
    lang: str           # Language category

@dataclass
class ComplexityFinding:
    file: str
    line: int
    type: str           # "long_function" | "deep_nesting"
    value: int          # Line count or nest depth
    severity: str       # WARNING | CRITICAL

@dataclass
class SecurityFinding:
    file: str
    line: int
    pattern: str        # Pattern name (hardcoded_secret, eval_call, etc.)
    match_text: str     # Snippet of matched code (truncated)
    severity: str       # CRITICAL | HIGH | MEDIUM | LOW

@dataclass
class ScanResult:
    files: list[FileInfo]
    complexity: list[ComplexityFinding]
    security: list[SecurityFinding]
    total_files: int
    total_lines: int
```

## Module Responsibilities

Single-file function layout:

| Function | Responsibility | Depends On |
|----------|---------------|------------|
| `scan_directory()` | Orchestrate full scan pipeline | All below |
| `collect_files()` | Walk directory, filter, count lines | os, pathlib |
| `analyze_complexity()` | Detect long functions & deep nesting | re |
| `scan_security()` | Pattern-match security issues | re |
| `format_report()` | Build Markdown string from results | All result types |
| `main()` | Parse args, run scan, output/exit | argparse |

## Data Flow

```
User input (PATH)
    │
    ▼
main() ── parse args
    │
    ▼
scan_directory(target_path)
    ├── collect_files() → list[FileInfo]
    ├── analyze_complexity(files) → list[ComplexityFinding]   [skip if --security-only]
    └── scan_security(files) → list[SecurityFinding]
    │
    ▼
ScanResult (aggregate)
    │
    ▼
format_report(result) → str (Markdown)
    │
    ▼
Output (stdout or -o file)
Exit code: 0 / 1 / 2
```

## Key Technical Decisions

| # | Decision | Trade-off |
|---|---------|-----------|
| 1 | Skip binary files by trying UTF-8 decode first | Small overhead on text files; safe fallback |
| 2 | Pre-compile regex patterns at module load | Faster repeated matching; slight memory use |
| 3 | Security patterns case-insensitive where appropriate | Catches more variants; slightly more FPs |
| 4 | Line count via readlines() not wc approximation | Accurate; uses minimal memory per file |

## File Structure

```
src/
└── vibecli.py          # Single file (~280 lines)
    ├── Imports & Constants (lines 1-30)
    ├── Data Classes (lines 31-60)
    ├── collect_files() (lines 61-100)
    ├── analyze_complexity() (lines 101-150)
    ├── scan_security() (lines 151-210)
    ├── format_report() (lines 211-260)
    ├── main() (lines 261-280)
    └── entry point (line 282)
```

## MCP Considerations (Stage 3)

For this project, no MCP servers needed (zero-dependency, local-only). If extended later:
- **Context7** — Not needed (no external library APIs)
- **Serena** — Could add for symbol-level search in scanned codebase (future v2)
- **Filesystem MCP** — Not needed; tool itself provides file access

## Validation (L1-3 Self-Check)

| Check | Result |
|-------|--------|
| All required sections present | PASS (tech stack, ADRs, data model, modules, data flow, decisions) |
| Tech stack matches complexity | PASS (Python stdlib for a simple scanner is appropriate) |
| Data model covers all PRD entities | PASS (FileInfo→F1, ComplexityFinding→F2, SecurityFinding→F3, ScanResult→F4) |
| Context files updated | PASS (CLAUDE.md confirmed single-file Python architecture) |

**L1-3: PASS — Ready for Stage 5** (Stage 4 skipped for CLI)

## Next → Stage 5: Task Breakdown & TODO
