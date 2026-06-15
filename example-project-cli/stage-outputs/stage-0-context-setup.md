# Stage 0: Context Setup — VibeCLI

## Generated Files

### CLAUDE.md (Project-Level Rules)

```markdown
# VibeCLI Project Rules

## Project Overview
- Type: CLI tool (codebase analysis)
- Language: Python 3.12+, zero external dependencies
- Entry point: src/vibecli.py
- Output format: Markdown report to stdout or file

## Code Conventions
- Use `argparse` for CLI argument parsing
- All functions must have type hints
- Exit code 0 = success, 1 = error, 2 = findings/warnings
- Errors go to stderr, normal output to stdout
- Maximum function body: 40 lines (CLI tools should be concise)
- Naming: snake_case for functions/variables, UPPER_CASE for constants
- Docstrings on all exported functions (Google style, brief)

## File Structure Convention
- Single-file architecture (this is a small CLI tool)
- Functions ordered by dependency: helpers → core → CLI entry → main
- Constants at top of file, after imports

## Security Requirements (from security-checklist.md)
- No eval() / exec() / subprocess with user input
- Path traversal protection: reject paths containing `..`
- File read-only: never write/delete user files
- Secret patterns: scan but never extract/display full matches

## Token Efficiency
- Target compression level: L3-L4 (medium project)
- Internal variables abbreviated; exports descriptive
- Comments: docstrings only, no inline comments unless non-obvious logic
```

### .cursorrules

```json
{
  "conventions": {
    "language": "Python",
    "style": "snake_case type hints argparse single-file",
    "maxFunctionLines": 40,
    "naming": "exports descriptive, internals abbreviated",
    "exitCodes": { "success": 0, "error": 1, "findings": 2 }
  },
  "security": [
    "no eval/exec/subprocess on user input",
    "reject path traversal (..)",
    "read-only file access"
  ]
}
```

### INITIAL.md (Feature Request Template)

```markdown
# Feature Request: {title}

## Summary
One-line description of what this feature should do.

## Motivation
Why is this needed? What problem does it solve?

## Proposed Behavior
Step-by-step description of expected behavior.

## Acceptance Criteria
- [ ] AC-1: ...
- [ ] AC-2: ...

## Edge Cases to Consider
- What happens when ...?
```

### Examples Directory

Created placeholder for discovered patterns during implementation:
- `examples/input-patterns.md` — Common directory structures and how tool handles them
- `examples/output-samples.md` — Sample report outputs for reference

## Validation (L1-0 Self-Check)

| Check | Result |
|-------|--------|
| All required files exist | PASS (CLAUDE.md, .cursorrules, INITIAL.md, examples/) |
| CLAUDE.md contains security section | PASS |
| File sizes within limits | PASS (CLAUDE.md ~35 lines < 200, .cursorrules ~15 lines < 100) |

**L1-0: PASS — Ready for Stage 1**
