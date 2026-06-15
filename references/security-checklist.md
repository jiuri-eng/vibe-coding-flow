# Security Checklist & Safe Execution Guide

## Overview

Security is not an afterthought — it must be built into every stage of Vibe Coding. This module provides pre-commit code review checklists, runtime safety guidelines, and environment hardening rules.

**Core principle**: AI-generated code is untrusted code until verified. Every output passes through security gates before merging.

## Security Gates by Stage

| Stage | Security Gate | Trigger |
|-------|--------------|---------|
| Stage 0 (Context Setup) | Define security requirements in CLAUDE.md | Always |
| Stage 3 (Architecture) | Threat model for auth/data/io | Always |
| Stage 6 (Implementation) | Pre-commit security scan per task | Every task completion |
| Stage 7 (Integration) | Full security audit before delivery | Before deployment |

---

## Pre-Commit Code Review Checklist

### MUST Pass (Blocker — Do Not Merge If Any Fail)

Run this checklist **after every task completion** in Stage 6:

#### Secrets & Credentials
- [ ] **No hardcoded secrets**: No API keys, passwords, tokens, or connection strings in source code
- [ ] **No secrets in config files**: Check `.env.example` doesn't contain real values
- [ ] **No secrets in git history**: Run `git log -p --all -S "api_key" -- "*.ts" "*.js" "*.py"` for sensitive patterns
- [ ] **Environment variables used correctly**: Secrets loaded from `process.env`, never string literals
- [ ] **`.env` in `.gitignore`**: Confirm it's listed

```bash
# Automated secret scanning command:
git diff --cached --name-only | xargs grep -n -iE "(password|secret|api_key|token|credential)" 2>/dev/null \
  || echo "No secrets found in staged changes"
```

#### Injection Prevention
- [ ] **SQL injection**: All database queries use parameterized queries / ORM methods. No string concatenation in SQL.
- [ ] **XSS (Cross-Site Scripting)**: User input is sanitized/escaped before rendering in DOM
  - In Vue: user content uses `v-text` or `{{ }}` (auto-escaped), NOT `v-html`
  - In React: user content in JSX text (auto-escaped), NOT `dangerouslySetInnerHTML`
- [ ] **Command injection**: No unsanitized user input passed to `exec()`, `spawn()`, `os.system()`, or shell commands
- [ ] **Path traversal**: File operations validate and sanitize paths, use allow-lists for safe directories

```python
# BAD — SQL injection risk
query = f"SELECT * FROM users WHERE name = '{user_input}'"

# GOOD — parameterized query
cursor.execute("SELECT * FROM users WHERE name = %s", (user_input,))
```

#### Authentication & Authorization
- [ ] **Auth checks present**: Protected endpoints/routes verify authentication state
- [ ] **Authorization enforced**: Users can only access their own data (no IDOR — Insecure Direct Object Reference)
- [ ] **Token storage**: Auth tokens stored in httpOnly cookies (not localStorage) when possible
- [ ] **Session management**: Proper timeout and invalidation logic exists
- [ ] **Rate limiting**: Authentication-sensitive endpoints have rate limits

#### Input Validation
- [ ] **Server-side validation**: All inputs validated on the server, not just client-side
- [ ] **Type checking**: Data types match expected schema (use Zod / Yup / Pydantic)
- [ ] **Length limits**: String inputs have max length bounds to prevent DoS via oversized payloads
- [ ] **File uploads**: File type validation (magic bytes, not just extension), size limits, virus scan for sensitive apps

### SHOULD Pass (Warning — Review Before Merging)

- [ ] **Dependency audit**: No known vulnerable dependencies (run `npm audit` / `pip-audit`)
- [ ] **Error messages**: Error responses to clients don't expose stack traces, file paths, or internal details
- [ ] **CSP headers**: Content-Security-Policy headers configured (for web apps)
- [ ] **CORS policy**: CORS is restricted to allowed origins, not wildcard (`*`)
- [ ] **HTTPS only**: Production URLs use HTTPS, no mixed content
- [ ] **Logging**: Sensitive data (passwords, tokens, PII) not written to logs

### NICE TO HAVE (Suggestion)

- [ ] Subresource Integrity (SRI) for external CDN resources
- [ ] HSTS header enabled
- [ ] CSRF protection for state-changing operations
- [ ] Security-related unit tests exist (auth bypass tests, injection test cases)
- [ ] Dependencies pinned to exact versions (lockfile committed)

---

## Runtime Safety Guidelines

### Environment Isolation

#### Development Environment
```
┌─────────────────────────────────────┐
│         Your Machine                │
│  ┌───────────────────────────────┐  │
│  │   Project Sandbox             │  │
│  │  ┌─────────┐ ┌─────────────┐  │  │
│  │  │ Code    │ │ Dev DB      │  │  │
│  │  │ Runner  │ │ (local)     │  │  │
│  │  └─────────┘ └─────────────┘  │  │
│  └───────────────────────────────┘  │
│  Network: localhost only            │
│  Env: .env.local (dev secrets)      │
└─────────────────────────────────────┘
```

**Rules for dev sandbox:**
1. All services bind to `localhost` / `127.0.0.1` only (not `0.0.0.0`)
2. Database credentials differ from production (never share)
3. Third-party API calls use sandbox/staging keys when available
4. File operations restricted to project directory

#### Production Considerations (for later stages)
- Use Docker containers with read-only filesystem where possible
- Run processes as non-root user
- Set resource limits (CPU, memory) to prevent runaway processes
- Enable audit logging for all external interactions

### Secret Management Pattern

```bash
# .env.template — Committed to repo (template only)
DATABASE_URL=postgresql://user:pass@localhost:5432/dbname
API_KEY=your-api-key-here
JWT_SECRET=your-jwt-secret-here

# .env.local — Gitignored, for local development
# Contains real values, never committed

# Production: Use platform secret manager
# (Vercel env vars, AWS Parameter Store, Docker secrets, etc.)
```

**AI Coding Rules for Secrets** (add to CLAUDE.md):
> When generating code that requires configuration values:
> 1. Use `process.env.VAR_NAME` or equivalent
> 2. Add the variable name to `.env.template`
> 3. NEVER invent or hardcode a value
> 4. If a default is needed for dev, make it obvious (e.g., `dev-change-me`)

### AI Code Execution Safety

When AI-generated code runs during development (dev server, scripts, tests):

| Risk Category | Mitigation |
|---------------|-----------|
| **Malicious package install** | Review `package.json` / `requirements.txt` diffs before `npm install` / `pip install` |
| **Destructive file operations** | Check for `rm -rf`, `fs.unlink`, `shutil.rmtree` in generated code; scope to project dir |
| **Network exfiltration** | Dev server binds to localhost; monitor outbound connections if suspicious |
| **Crypto-mining / resource abuse** | Monitor CPU/memory during dev server runs; unusual spikes = investigate |
| **Dependency confusion** | Pin dependency versions; verify package sources |

### Safety Commands to Run After Each Task

```bash
# Node.js projects
npm audit          # Check for vulnerable dependencies
npx eslint src/    # Lint for potential issues (configure security rules)

# Python projects
pip-audit           # Check for vulnerable packages
ruff check src/     # Lint + security checks

# General
git diff --stat     # Review what files changed — anything unexpected?
git status          # Any untracked files that look suspicious?
```

---

## Common Vulnerability Patterns in AI-Generated Code

| Vulnerability | How AI Introduces It | Detection | Fix |
|--------------|---------------------|-----------|-----|
| **Hardcoded secrets** | AI generates placeholder values that look realistic | Secret scanner regex | Replace with env vars |
| **SQL injection** | Uses f-strings / template literals for queries | Code review + linter rules | Parameterized queries |
| **Missing auth check** | Focuses on feature logic, forgets access control | Manual code review | Add auth middleware/guard |
| **XSS** | Uses `v-html` / `dangerouslySetInnerHTML` for convenience | Linter + CSP test reports | Use auto-escaped rendering |
| **IDOR** | Assumes authenticated = authorized | Trace data flow per endpoint | Add ownership verification |
| **Overly permissive CORS** | Sets `Access-Control-Allow-Origin: *` to "make it work" | Check response headers | Restrict to specific origins |
| **Error info leak** | Returns full exception details for debugging | Test error responses | Return generic error to client |
| **Unvalidated redirects** | Takes URL from user input without validation | Check redirect destinations | Allow-list or validate URL scheme |

---

## Security-First CLAUDE.md Section

Add this section to your generated `CLAUDE.md`:

```markdown
## Security Requirements (MANDATORY)
- NEVER hardcode secrets, tokens, or credentials — always use environment variables
- All user inputs must be validated and sanitized server-side
- Database queries MUST use parameterized queries / ORM — no string concatenation
- Authenticated endpoints MUST verify both authentication AND authorization (ownership)
- File upload: validate type (magic bytes), limit size (< 10MB), store outside web root
- Error responses: generic message to client; details to server logs only
- New dependencies: run security audit before committing (npm audit / pip-audit)
- When in doubt, ask about security implications before implementing
```
