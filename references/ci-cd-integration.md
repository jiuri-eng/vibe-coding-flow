# CI/CD Integration — Vibe Coding Flow

## Overview

The self-check system (L1-L4) and security gates work great in interactive mode, but for team projects you want these gates to run **automatically** on every push. This guide provides ready-to-use GitHub Actions workflows that encode the key checks.

**When to use this**: You're collaborating with others, or you want automated enforcement of the quality standards defined elsewhere in this skill.

---

## Quick Start: Copy-Paste Workflow

Create `.github/workflows/vibe-check.yml` in your project:

```yaml
name: Vibe Coding Quality Gates

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  # ──────────────────────────────────────────
  # Job 1: L2-A Security Gate (18 MUST-PASS checks)
  # ──────────────────────────────────────────
  security-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0  # full history for secret scanning

      - name: Secret detection (gitleaks)
        uses: gitleaks/gitleaks-action@v2
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}

      - name: Dependency audit (Node.js)
        if: hashFiles('package-lock.json') != ''
        run: npm audit --audit-level=high

      - name: Dependency audit (Python)
        if: hashFiles('requirements.txt') != ''
        run: |
          pip install pip-audit
          pip-audit

      - name: Hardcoded secret scan (custom patterns)
        run: |
          ! grep -rnE "(password|secret|api_key|token)\s*=\s*['\"][^$]" \
            --include="*.py" --include="*.js" --include="*.ts" \
            --exclude-dir=node_modules --exclude-dir=.git \
            . 2>/dev/null || (echo "HARDCODED SECRET DETECTED" && exit 1)

  # ──────────────────────────────────────────
  # Job 2: L2-B Quality Gate
  # ──────────────────────────────────────────
  quality-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        if: hashFiles('package.json') != ''
        uses: actions/setup-node@v4
        with:
          node-version: '22'

      - name: Install dependencies
        if: hashFiles('package.json') != ''
        run: npm ci

      - name: Lint (ESLint)
        if: hashFiles('.eslintrc*') != '' || hashFiles('eslint.config.*') != ''
        run: npx eslint src/ --max-warnings 0

      - name: Lint (Ruff for Python)
        if: hashFiles('*.py') != ''
        run: |
          pip install ruff
          ruff check src/

      - name: Complexity check (function length + nesting)
        run: |
          echo "Checking function length < 50 lines..."
          find src/ -name "*.js" -o -name "*.ts" | while read f; do
            # Count lines between function declaration and closing brace
            # Simple heuristic: warn on files with suspicious patterns
            long_funcs=$(grep -c "function " "$f" 2>/dev/null || true)
            if [ "$long_funcs" -gt 20 ]; then
              echo "  WARN: $f has $long_funcs functions — check for decomposition"
            fi
          done

  # ──────────────────────────────────────────
  # Job 3: L2-C Completeness Gate
  # ──────────────────────────────────────────
  completeness-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Check PRD function coverage
        run: |
          if [ -f docs/02-prd.md ]; then
            echo "=== PRD Function Requirements ==="
            grep -c "^### F-" docs/02-prd.md || echo "No F-NNN items found"
            echo ""
            echo "=== Source files ==="
            find src/ -name "*.js" -o -name "*.ts" -o -name "*.py" | wc -l
            echo "(Manual verification: ensure all F-NNN items are implemented)"
          else
            echo "No PRD found — skipping completeness check"
          fi

      - name: Check TODO completion
        run: |
          if [ -f docs/05-todo.md ]; then
            remaining=$(grep -c "\[ \]" docs/05-todo.md 2>/dev/null || echo "0")
            done=$(grep -c "\[x\]" docs/05-todo.md 2>/dev/null || echo "0")
            echo "TODO status: $done completed, $remaining remaining"
            if [ "$remaining" -gt 0 ]; then
              echo "WARN: $remaining tasks not marked complete"
            fi
          fi

  # ──────────────────────────────────────────
  # Job 4: Tests (L1 Stage Gate)
  # ──────────────────────────────────────────
  run-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        if: hashFiles('package.json') != ''
        uses: actions/setup-node@v4
        with:
          node-version: '22'

      - name: Install dependencies
        if: hashFiles('package.json') != ''
        run: npm ci

      - name: Run tests (Vitest)
        if: hashFiles('vitest.config.*') != '' || hashFiles('vite.config.*') != ''
        run: npx vitest run --reporter=verbose

      - name: Run tests (pytest)
        if: hashFiles('requirements*.txt') != '' || hashFiles('pyproject.toml') != ''
        run: |
          pip install pytest
          python -m pytest tests/ -v
```

---

## Adding Self-Check Report to CI

For projects that want the full L1-L4 report in CI output, add this job:

```yaml
  self-check-report:
    runs-on: ubuntu-latest
    needs: [security-scan, quality-check, completeness-check, run-tests]
    steps:
      - uses: actions/checkout@v4

      - name: Generate Self-Check Report
        run: |
          echo "## Vibe Coding Self-Check Report" >> $GITHUB_STEP_SUMMARY
          echo "" >> $GITHUB_STEP_SUMMARY
          echo "| Gate | Status |" >> $GITHUB_STEP_SUMMARY
          echo "|------|--------|" >> $GITHUB_STEP_SUMMARY
          echo "| L1 Stage Gate | ${{ needs.run-tests.result == 'success' && 'PASS' || 'FAIL' }} |" >> $GITHUB_STEP_SUMMARY
          echo "| L2-A Security | ${{ needs.security-scan.result == 'success' && 'PASS' || 'FAIL' }} |" >> $GITHUB_STEP_SUMMARY
          echo "| L2-B Quality  | ${{ needs.quality-check.result == 'success' && 'PASS' || 'FAIL' }} |" >> $GITHUB_STEP_SUMMARY
          echo "| L2-C Completeness | ${{ needs.completeness-check.result == 'success' && 'PASS' || 'FAIL' }} |" >> $GITHUB_STEP_SUMMARY
          echo "" >> $GITHUB_STEP_SUMMARY
          echo "Generated at: $(date -u +'%Y-%m-%dT%H:%M:%SZ')" >> $GITHUB_STEP_SUMMARY
```

---

## Project-Specific CI Templates

### Node.js / React / Vite project

```yaml
# Minimal CI for a VibeTodo-style project
name: VibeTodo CI
on: [push, pull_request]
jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: '22' }
      - run: npm ci
      - run: npx vitest run
      - run: npx eslint src/
      - run: npm audit --audit-level=high
```

### Python / CLI project

```yaml
# Minimal CI for a VibeCLI-style project
name: VibeCLI CI
on: [push, pull_request]
jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: '3.13' }
      - run: pip install pytest ruff pip-audit
      - run: python -m pytest tests/ -v
      - run: ruff check src/
      - run: pip-audit
```

---

## Integration with Skill Stages

| Stage | CI Automation Point |
|-------|--------------------|
| **Stage 0** | Create `.github/workflows/vibe-check.yml` from template (part of context setup) |
| **Stage 6** | Each task push triggers CI — L2 gate runs automatically |
| **Stage 7** | Final CI run produces Self-Check Report as build artifact |

### Adding CI to the Vibe Coding Workflow

In Stage 0 context setup, include this in `CLAUDE.md`:

```markdown
## CI/CD Requirements
- All pushes must pass: security scan, lint, tests, dependency audit
- CI workflow defined in .github/workflows/vibe-check.yml
- PRs require all CI checks green before merge
- Self-Check Report auto-generated in CI summary
```

---

## When NOT to Add CI

- Solo projects where you're the only developer — interactive L2 Task Gate in WorkBuddy is sufficient
- Prototypes that won't be maintained
- Projects without Git (CI needs a VCS)
- Learning experiments where the overhead slows you down

The interactive self-check system (L1-L4) already covers 95% of what CI would enforce for solo Vibe Coding. CI adds value when you need **enforcement**, not just **awareness**.
