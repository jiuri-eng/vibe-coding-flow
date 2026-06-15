# Docker Sandbox Execution Template

## Overview

This module provides **production-grade Docker sandbox configurations** for safely executing AI-generated code during Vibe Coding development. Inspired by [vibekit](https://github.com/superagent-ai/vibekit) (1.8k stars), [CubeSandbox](https://cloud.tencent.com/developer/article/2675906) (Tencent), and industry hardening practices.

**Core principle**: All AI-generated code is **untrusted by default** and must execute in an isolated environment before being promoted to your local dev setup.

> **Windows user?** This guide assumes Linux/Docker. For Windows-specific setup (WSL2, Windows Sandbox, PowerShell alternatives), see [windows-setup.md](windows-setup.md).

---

## Why You Need This

| Scenario | Risk Without Sandbox |
|----------|---------------------|
| AI installs `npm install` with malicious package | Crypto-miner, data exfiltration, keylogger |
| AI runs `rm -rf` with wrong path | Deletes your home directory or critical files |
| AI generates network calls to unknown endpoints | Exfiltrates secrets, API keys, source code |
| AI writes to system directories | Modifies PATH, crontab, SSH config |
| AI spawns long-running processes | Exhausts CPU/memory, freezes your machine |

---

## Architecture: 4-Layer Isolation Model

```
Layer 4: Observability (监控层)
    Real-time logs, resource metrics, exit code tracking
         ↑
Layer 3: Resource Control (资源控制层)
    CPU/Memory limits, timeout enforcement, process count caps
         ↑
Layer 2: Kernel-Level Hardening (内核强化层)
    Seccomp syscall filter, read-only rootfs, no-new-privileges, AppArmor/SELinux
         ↑
Layer 1: Namespace Isolation (命名空间隔离层)
    PID / Network / Mount / UTS / IPC namespaces — standard Docker defaults
         ↑
Your Host Machine (宿主机)
```

---

## Quick Start: 3 Sandboxes for Different Needs

### Sandbox A: Development Runner (推荐日常使用)

**Purpose**: Run AI-generated dev servers, build scripts, test suites in isolation.

```dockerfile
# .docker/sandbox/Dockerfile.dev
FROM node:22-alpine AS base

# Non-root user
RUN addgroup -S appgroup && adduser -S appuser -G appgroup

# Install minimal runtime deps
RUN apk add --no-cache git curl

WORKDIR /app

# Default command
CMD ["sh", "-c", "echo 'Sandbox ready. Mount your project to /app/workspace'"]
```

```yaml
# docker-compose.sandbox.yml
version: "3.8"

services:
  dev-runner:
    build:
      context: .
      dockerfile: .docker/sandbox/Dockerfile.dev
    container_name: vibe-dev-runner
    user: "1000:1000"                          # Non-root execution
    volumes:
      - ./:/app/workspace:rw                    # Project mounted here
      - node_modules_cache:/app/workspace/node_modules  # Isolated node_modules
      - sandbox_tmp:/tmp:rw                     # Isolated temp dir
    environment:
      - NODE_ENV=development
      - SANDBOX_MODE=true                       # Code can detect it's in sandbox
      - DISABLE_TELEMETRY=true                  # No phone-home
      - HOME=/tmp                               # No access to real home
    working_dir: /app/workspace
    # === SECURITY HARDENING ===
    read_only: false                            # Need rw for dev; see B for stricter mode
    security_opt:
      - no-new-privileges:true                  # Prevent privilege escalation
      - seccomp:.docker/sandbox/seccomp-dev.json # Syscall filter
    networks:
      - sandbox-net                             # Isolated network (no host access)
    dns:
      - 8.8.8.8
    # === RESOURCE LIMITS ===
    deploy:
      resources:
        limits:
          cpus: "2.0"
          memory: 2G
          pids: 500                             # Max 500 processes
    restart: "no"                               # Never auto-restart
    stdin_open: true
    tty: true

networks:
  sandbox-net:
    driver: bridge
    internal: true                              # No external internet access!
    # Remove `internal: true` if you need npm install (use B for that)

volumes:
  node_modules_cache:
  sandbox_tmp:
```

### Sandbox B: Package Installer (网络隔离 + 只读)

**Purpose**: Safely run `npm install`, `pip install`, etc. — the highest-risk operation.

```yaml
# docker-compose.install.yml
services:
  pkg-installer:
    build:
      context: .
      dockerfile: .docker/sandbox/Dockerfile.dev
    container_name: vibe-pkg-installer
    user: "1000:1000"
    volumes:
      - ./:/app/workspace:ro                    # READ ONLY! Can't modify source
      - node_modules_cache:/app/workspace/node_modules:rw  # Only writable spot
      - cache_home:/root/.npm:rw               # npm cache (isolated)
      - cache_pip:/root/.cache/pip:rw           # pip cache (isolated)
    environment:
      - npm_config_audit=true                   # Force audit on install
      - npm_config_prefer-offline=false
      - PIP_NO_DEPS=false
      - PIP_CHECK_HASH_MATCHING=1
    working_dir: /app/workspace
    # === MAXIMUM HARDENING ===
    read_only: true                              # Root filesystem read-only
    tmpfs:
      - /tmp:size=512M,noexec,mode=1777         # Tmpfs instead of disk
    security_opt:
      - no-new-privileges:true
      - seccomp:.docker/sandbox/seccomp-install.json  # Stricter syscall filter
    networks:
      - install-net                              # Has internet (for registry)
    deploy:
      resources:
        limits:
          cpus: "1.0"
          memory: 1G
          pids: 200
    command: ["npm", "install"]                 # Override with pip install etc.
    restart: "no"

networks:
  install-net:
    driver: bridge
    # NOT internal — needs internet for package registries
    # But still isolated from host network

volumes:
  node_modules_cache:
  cache_home:
  cache_pip:
```

### Sandbox C: Test Executor (严格只读源码)

**Purpose**: Run test suites with full output capture and coverage reporting.

```yaml
# docker-compose.test.yml
services:
  test-executor:
    build:
      context: .
      dockerfile: .docker/sandbox/Dockerfile.dev
    container_name: vibe-test-executor
    user: "1000:1000"
    volumes:
      - ./:/app/workspace:ro                    # Source: read-only
      - test_output:/app/test-output:rw         # Test results go here
      - node_modules_cache:/app/workspace/node_modules:rw
    environment:
      - CI=true                                  # CI mode (no interactive prompts)
      - NODE_ENV=test
    working_dir: /app/workspace
    read_only: true
    tmpfs:
      - /tmp:size=256M,noexec,mode=1777
    security_opt:
      - no-new-privileges:true
    networks:
      - sandbox-net
    deploy:
      resources:
        limits:
          cpus: "1.5"
          memory: 1.5G
          pids: 300
    command: ["npm", "test", "--", "--coverage"]
    restart: "no"

volumes:
  node_modules_cache:
  test_output:

networks:
  sandbox-net:
    driver: bridge
    internal: true
```

---

## Seccomp Profiles (系统调用过滤)

These JSON files define which Linux syscalls the container is allowed to use. **This is the single most effective defense against kernel-level attacks.**

### seccomp-dev.json (Development — Balanced)

```json
{
  "defaultAction": "SCMP_ACT_ERRNO",
  "architectures": ["SCMP_ARCH_X86_64", "SCMP_ARCH_AARCH64"],
  "syscalls": [
    {"names": ["read", "write", "openat", "close", "fstat",
               "mmap", "mprotect", "munmap", "brk", "ioctl",
               "access", "dup2", "pipe2", "eventfd2",
               "epoll_create1", "epoll_ctl", "epoll_wait",
               "futex", "sched_yield", "clone3", "execve",
               "exit_group", "rt_sigreturn", "rt_sigprocmask",
               "getrandom", "clock_nanosleep", "getpid",
               "statx", "newfstatat", "lseek", "fcntl"],
     "action": "SCMP_ACT_ALLOW"},
    {"names": ["socket", "connect", "bind", "listen", "accept",
               "sendto", "recvfrom", "shutdown", "getsockopt",
               "setsockopt", "getsockname", "getpeername"],
     "action": "SCMP_ACT_ALLOW",
     "args": null,
     "comment": "Network operations (restricted by Docker network)"},
    {"names": ["mkdirat", "unlinkat", "renameat2", "fchmodat",
               "chdir", "getcwd", "getdents64"],
     "action": "SCMP_ACT_ALLOW",
     "comment": "Filesystem operations within workspace"}
  ]
}
```

> **Note**: For production use, generate complete profiles using:
> ```bash
> docker run --rm -v $(pwd):/out ghcr.io/containers/seccompiler:latest \
>   --input /out/seccomp-dev.yaml --output /out/seccomp-dev.json
> ```

### seccomp-install.json (Package Install — Stricter)

Blocks all network except to known package registry domains, blocks shell execution commands.

```json
{
  "defaultAction": "SCMP_ACT_ERRNO",
  "syscalls": [
    {"names": ["read", "write", "openat", "close", "fstat",
               "mmap", "mprotect", "munmap", "brk",
               "access", "dup2", "pipe2",
               "epoll_create1", "epoll_ctl", "epoll_wait",
               "futex", "clone3", "execve",
               "exit_group", "rt_sigreturn", "rt_sigprocmask",
               "getrandom", "clock_nanosleep",
               "statx", "newfstatat", "lseek", "fcntl",
               "mkdirat", "unlinkat", "renameat2", "fchmodat",
               "chdir", "getcwd", "getdents64"],
     "action": "SCMP_ACT_ALLOW"},
    {"names": ["socket", "connect", "sendto", "recvfrom",
               "getsockname", "getpeername", "shutdown"],
     "action": "SCMP_ACT_ALLOW",
     "comment": "Network only (DNS filtered at Docker level)"},
    {"names": ["bind", "listen", "accept"],
     "action": "SCMP_ACT_ERRNO",
     "comment": "No listening sockets during install"}
  ]
}
```

---

## VibeKit Integration (可选增强)

If you want **automatic secret redaction** + **observability** on top of Docker:

```bash
# Install VibeKit CLI globally
npm install -g @vibe-kit/cli

# Run Claude Code inside VibeKit's managed sandbox
vibekit claude

# Or use the SDK programmatically
npm install @vibe-kit/sdk
```

```typescript
// Example: Programmatic sandbox control with VibeKit SDK
import { VibeSandbox } from '@vibe-kit/sdk';

const sandbox = new VibeSandbox({
  image: 'node:22-alpine',
  workdir: '/workspace',
  mounts: [{ source: './', target: '/workspace', readonly: false }],
  limits: { cpu: 2, memoryMB: 2048, timeoutSec: 300 },
  // Auto-redact secrets from input/output
  redactSecrets: true,
  // Capture logs/metrics/traces
  observability: {
    enableLogs: true,
    enableMetrics: true,
    enableTraces: true,
  }
});

// Execute a command in the sandbox
const result = await sandbox.run('npm test');
console.log(result.exitCode);   // 0 = success
console.log(result.stdout);
console.log(result.stderr);
console.log(result.metrics);    // CPU%, memory, duration
```

**VibeKit vs Pure Docker comparison**:

| Feature | Pure Docker | VibeKit |
|---------|------------|---------|
| Container management | Manual | Automatic lifecycle |
| Secret redaction | Manual (env vars) | Built-in automatic |
| Observability | Manual (docker stats) | Logs + Traces + Metrics built-in |
| Multi-agent support | Manual | Native orchestration |
| Setup complexity | Medium (Docker files) | Low (one-line install) |
| Customization | Full control | Configurable but opinionated |

**Recommendation**: Start with pure Docker templates above (A/B/C). Add VibeKit when you need observability across multiple parallel agents.

---

## Usage Workflow in Vibe Coding Stages

### Stage 6 Implementation — Per-Task Execution Pattern

```
For each task T-xx in docs/05-todo.md:

  1. Review task → identify execution risk level
     ├── LOW:  Read-only operation (linting, type-check)
     │    → Run on host (safe enough)
     ├── MEDIUM: Dev server, unit tests, build scripts
     │    → Run in Sandbox A (dev-runner)
     └── HIGH:  npm/pip install, scripts with network/file ops
         → Run in Sandbox B (pkg-installer) or C (test executor)

  2. If HIGH/MEDIUM:
     ├── docker compose -f docker-compose.sandbox.yml run --rm dev-runner <command>
     ├── OR: docker compose -f docker-compose.install.yml run --rm pkg-installer
     └── Check exit code + review output

  3. Pass Security Gate (from references/security-checklist.md)

  4. Mark task complete ✅
```

### Pre-Execution Checklist

Before running any AI-generated code:

```bash
#!/bin/bash
# pre_exec_check.sh — Run before every sandbox execution

set -euo pipefail

PROJECT_DIR="${1:-.}"
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo "=== Pre-Execution Security Scan ==="

# 1. Check for suspicious patterns in staged/new files
SUSPICIOUS=$(git diff --cached --name-only 2>/dev/null \
  | xargs grep -ln -iE \
    '(rm\s+-rf\s+/|curl.*\|\s*sh|eval\s*\(|base64.*-d|wget.*\|\s*(bash|sh)|\bexec\s*\(|__import__\("os"\)\.system)' \
  2>/dev/null || true)

if [ -n "$SUSPICIOUS" ]; then
  echo -e "${RED}[BLOCKED] Suspicious patterns detected:${NC}"
  echo "$SUSPICIOUS"
  echo -e "${YELLOW}Review these files before executing.${NC}"
  exit 1
fi

# 2. Check for new dependencies added
NEW_PKGS=$(git diff --cached --name-only 2>/dev/null | grep -E '(package\.json|requirements\.txt|Cargo\.toml|go\.mod)' || true)
if [ -n "$NEW_PKGS" ]; then
  echo -e "${YELLOW}[WARNING] New dependency files changed:${NC}"
  echo "$NEW_PKGS"
  echo -e "${YELLOW}Use Sandbox B (pkg-installer) for installation.${NC}"
fi

# 3. Check file count changes (detect bulk file generation)
FILE_COUNT=$(git diff --cached --diff-filter=A --num-only 2>/dev/null | wc -l || echo 0)
if [ "$FILE_COUNT" -gt 50 ]; then
  echo -e "${YELLOW}[INFO] $FILE_COUNT new files — verify this is expected${NC}"
fi

# 4. Network check (is the project trying to connect externally?)
NET_PATTERNS=$(grep -rn -E '(fetch\(|axios\.|http[s]?://(?!localhost|127\.0\.0\.1))' \
  "$PROJECT_DIR/src" 2>/dev/null | head -5 || true)
if [ -n "$NET_PATTERNS" ]; then
  echo -e "${YELLOW}[INFO] Outbound network calls detected in source:${NC}"
  echo "$NET_PATTERNS"
fi

echo -e "${GREEN}[PASS] Pre-execution scan complete${NC}"
exit 0
```

### Post-Execution Validation

```bash
#!/bin/bash
# post_exec_validate.sh — Run after sandbox execution

CONTAINER_ID="$1"

echo "=== Post-Execution Validation ==="

# 1. Exit code check
EXIT_CODE=$(docker inspect --format='{{.State.ExitCode}}' "$CONTAINER_ID")
if [ "$EXIT_CODE" -ne 0 ]; then
  echo "[WARN] Container exited with code $EXIT_CODE"
fi

# 2. Resource usage
STATS=$(docker stats --no-stream --format 'CPU: {{.CPUPerc}} | MEM: {{.MemUsage}} | NET: {{.NetIO}}' "$CONTAINER_ID")
echo "Resource usage: $STATS"

# 3. File changes (what did the container create/modify?)
CHANGES=$(docker diff "$CONTAINER_ID" 2>/dev/null | head -20 || true)
if [ -n "$CHANGES" ]; then
  echo "Files modified in container:"
  echo "$CHANGES"
fi

# 4. Network connections made (if not internal network)
if ! docker inspect --format='{{range .NetworkSettings.Networks}}{{.ID}}{{end}}' "$CONTAINER_ID" | grep -q "."; then
  echo "[INFO] Container had network access — review outbound connections if needed"
fi

echo "=== Validation Complete ==="
```

---

## Python Projects: Specific Configuration

```dockerfile
# .docker/sandbox/Dockerfile.python
FROM python:3.13-slim AS base

RUN groupadd -r appgroup && useradd -r -g appgroup appuser

# Minimal system deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc git curl && rm -rf /var/lib/apt/lists/*

WORKDIR /app

USER appuser
```

```bash
# Run Python script in sandbox
docker compose -f docker-compose.sandbox.yml run --rm \
  -e PYTHONUNBUFFERED=1 \
  -e PYTHONDONTWRITEBYTECODE=1 \
  dev-runner python your_script.py
```

**Python-specific risks to watch**:

| Risk | Pattern | Mitigation |
|------|---------|-----------|
| Arbitrary code exec | `eval()`, `exec()`, `__import__('os').system()` | Static analysis before execution |
| Unsafe deserialization | `pickle.load()`, `yaml.load(full_load)` | Use `json` or `yaml.safe_load` |
| Dependency confusion | `pip install` from PyPI without pinning | Use Sandbox B + requirements.txt lockfile |
| Path traversal | `open(user_input, 'w')` | Validate paths, restrict to workspace subdirs |

---

## When to Use Each Sandbox

| Operation | Sandbox | Why |
|-----------|---------|-----|
| `npm install` / `pip install` | **B (Pkg Installer)** | Highest risk op; read-only source + isolated cache |
| `npm run dev` / dev server | **A (Dev Runner)** | Needs rw + network (internal only) |
| `npm test` | **C (Test Executor)** | Read-only source, captures test output separately |
| `npm run build` | **C (Test Executor)** | Build artifacts written to isolated volume |
| Linting (`eslint`, `ruff`) | Host OK | Read-only, low risk |
| Type checking (`tsc --noEmit`) | Host OK | Read-only, low risk |
| Database migrations | **A (Dev Runner)** | Needs DB connection (via internal net) |
| Running generated scripts | **A (Dev Runner)** | Unknown behavior — isolate first |
| Production deployment | Dedicated infra | Not a sandbox concern |

---

## Non-Docker Alternatives (If Docker Unavailable)

| Tool | Approach | Pros | Cons |
|------|---------|------|------|
| **Firecracker** (AWS) | MicroVM isolation | Near-metal performance, strong isolation | AWS-centric, complex setup |
| **gVisor** (Google) | User-space kernel | Strong syscall filtering | Some compat issues |
| **nsjail** | Lightweight namespace jail | Fast, simple | Linux only, manual config |
| **landlock** (Linux 5.13+) | Filesystem access rules | Built into kernel, zero overhead | Files-only, no network/process |
| **Windows Sandbox** | Windows native | Works on Windows | Heavy, slower startup |

**Minimum viable non-Docker setup** (works on any OS):

```bash
# Use a dedicated unprivileged user for AI code execution
# Create this user once:
# Linux/macOS:  sudo useradd -m -s /bin/bash ai-runner
# Windows:     net user ai-runner /add

# Then run AI-generated code as this user:
sudo -u ai-runner bash -c "cd /path/to/project && npm run dev"
# The ai-runner has NO sudo, limited home dir, no access to your files
```

---

## Integration with SKILL.md Main Workflow

Add this to **Stage 6 Implementation Rules** in SKILL.md:

> **Sandbox Policy**: Before running any AI-generated command that modifies state (install, build, migrate, server start):
> 1. Determine risk level (LOW/MEDIUM/HIGH) using the table above
> 2. For MEDIUM/HIGH: execute in appropriate Docker sandbox (A/B/C)
> 3. Run pre-execution scan (`pre_exec_check.sh`)
> 4. Review output and post-execution validation
> 5. Only after passing both security gate AND sandbox validation → mark task complete

---

## File Structure After Adding This Module

```
project-root/
├── .docker/
│   └── sandbox/
│       ├── Dockerfile.dev            # Base image definition
│       ├── Dockerfile.python         # Python variant
│       ├── seccomp-dev.json          # Syscall filter (dev)
│       └── seccomp-install.json      # Syscall filter (install — stricter)
├── docker-compose.sandbox.yml        # Sandbox A: Dev runner
├── docker-compose.install.yml        # Sandbox B: Package installer
├── docker-compose.test.yml           # Sandbox C: Test executor
├── pre_exec_check.sh                 # Pre-execution safety scan
└── post_exec_validate.sh             # Post-execution validation
```
