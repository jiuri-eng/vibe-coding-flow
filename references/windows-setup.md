# Windows Setup Guide — Vibe Coding Flow

## Overview

The vibe-coding-flow skill was designed to be cross-platform, but some advanced features (Docker sandboxing, MCP server paths) require Windows-specific configuration. This guide covers everything you need to run the full skill on Windows 10/11.

---

## Quick Decision: Do I Need This?

| Your Scenario | Action |
|---------------|--------|
| Simple web/CLI project, no Docker needed | Skip to [MCP Config on Windows](#mcp-config-on-windows) only |
| Want full Docker sandbox isolation | Read [Option A: WSL2 + Docker](#option-a-wsl2--docker) |
| Can't/don't want WSL2 | Read [Option B: Windows Sandbox](#option-b-windows-sandbox-alternative) |
| Just testing, no isolation needed | Read [Option C: Python venv + Node npx](#option-c-localtemp-isolation) |

---

## Option A: WSL2 + Docker

**Best for**: Full isolation, production-grade sandboxing, identical to Linux experience.

### Pre-requisites

1. Windows 10 2004+ or Windows 11
2. Virtualization enabled in BIOS
3. Admin access

### Install (one-time setup)

```powershell
# Step 1: Install WSL2 (run in PowerShell as Admin)
wsl --install -d Ubuntu-24.04

# Step 2: Restart computer if prompted

# Step 3: Install Docker Desktop for Windows
# Download from: https://www.docker.com/products/docker-desktop/

# Step 4: Enable WSL2 integration in Docker Desktop
# Settings → Resources → WSL Integration → Enable "Ubuntu-24.04"

# Step 5: Verify
wsl docker run hello-world
# Should print: "Hello from Docker!"
```

### Using Docker from Git Bash / PowerShell

```bash
# Git Bash (paths use Linux format):
wsl docker compose -f /mnt/c/Users/$USER/project/docker-compose.yml up

# PowerShell:
wsl -- docker compose -f /mnt/c/Users/$env:USERNAME/project/docker-compose.yml up

# Create alias for convenience (add to ~/.bashrc):
alias docker='wsl docker'
alias docker-compose='wsl docker compose'
```

### File Path Mapping

| Host (Windows) | WSL2 (Linux) |
|----------------|-------------|
| `C:\Users\YourName\project` | `/mnt/c/Users/YourName/project` |
| `D:\AIdome\1\project` | `/mnt/d/AIdome/1/project` |

**IMPORTANT**: Docker volumes perform best when source code is inside WSL2's native filesystem (`~/project/`), not `/mnt/c/`. If you experience slow I/O, move your project into WSL:

```bash
wsl
cp -r /mnt/c/Users/$USER/project ~/project
cd ~/project
docker compose up
```

### Seccomp Profiles on Windows

Linux seccomp profiles (referenced in `docker-sandbox.md`) work **directly** with WSL2 Docker:

```yaml
# docker-compose.yml — same as Linux
services:
  dev:
    security_opt:
      - seccomp:./profiles/dev.seccomp.json
```

No changes needed. The Linux kernel inside WSL2 supports seccomp natively.

---

## Option B: Windows Sandbox (Alternative)

**Best for**: Quick isolated testing without Docker/WSL2. Built into Windows 10/11 Pro/Enterprise.

### Enable Windows Sandbox

```powershell
# Run as Admin
Enable-WindowsOptionalFeature -Online -FeatureName "Containers-DisposableClientVM" -All
# Restart if prompted
```

### Create Sandbox Config

```xml
<!-- sandbox.wsb — save in project root -->
<Configuration>
  <VGpu>Enable</VGpu>
  <Networking>Disable</Networking>
  <MappedFolders>
    <MappedFolder>
      <HostFolder>C:\Users\YourName\project</HostFolder>
      <SandboxFolder>C:\project</SandboxFolder>
      <ReadOnly>false</ReadOnly>
    </MappedFolder>
  </MappedFolders>
  <LogonCommand>
    <Command>explorer C:\project</Command>
  </LogonCommand>
</Configuration>
```

Launch: Double-click `sandbox.wsb`.

**Limitations vs Docker**:
- No Linux kernel features (seccomp, namespaces)
- Windows-only execution environment
- Sandbox resets on close (no persistent state)
- No network isolation options as granular as Docker

---

## Option C: Local/Temp Isolation (Zero Setup)

**Best for**: Rapid prototyping when you don't need full sandboxing.

### Python: Managed venv

```powershell
# WorkBuddy managed Python already creates isolated env
# If using system Python:
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python main.py
```

### Node.js: Use npx where possible

```powershell
# Instead of global installs, use npx (always latest, no residue):
npx eslint src/
npx vitest run

# For dependencies — install in project-local node_modules:
npm ci        # uses lockfile, no surprises
npm run dev
```

### Pre-flight Checks (before running AI code)

```powershell
# Before any AI-generated script runs, scan for:
Select-String -Path "*.py","*.js" -Pattern "os\.remove|shutil\.rmtree|fs\.unlink|rm -rf" -SimpleMatch
Select-String -Path "*.py","*.js" -Pattern "exec\(|eval\(|subprocess\.call|child_process\.exec" -SimpleMatch
```

---

## MCP Config on Windows

### Path Format

MCP server configuration uses **platform-native paths**. In WorkBuddy's `mcp.json` (~/.workbuddy/mcp.json):

```json
{
  "mcpServers": {
    "context7": {
      "command": "C:\\Program Files\\nodejs\\npx.cmd",
      "args": ["-y", "@upstash/context7-mcp"],
      "env": {
        "CONTEXT7_API_KEY": "your-key-here"
      }
    },
    "filesystem": {
      "command": "C:\\Program Files\\nodejs\\npx.cmd",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "C:\\Users\\YourName\\project"
      ]
    }
  }
}
```

Key Windows differences:
- Use **double backslashes** `\\` or **forward slashes** `/` in JSON paths
- Use **.cmd** extension for npm binaries (`npx.cmd`, not `npx`)
- File paths: `C:\\Users\\YourName\\...` or `C:/Users/YourName/...`

### Finding the Correct npx/node Path

```powershell
# Find npx location
where.exe npx
# Typical output: C:\Program Files\nodejs\npx.cmd

# Find node location
where.exe node
# Typical output: C:\Program Files\nodejs\node.exe
```

### Windows-Specific MCP Servers

| Server | Windows Notes |
|--------|--------------|
| **Context7** | Works out of box, same as Linux/Mac |
| **Serena** | Works out of box |
| **Filesystem** | Use `C:\\Users\\...` paths, ensure drive letter |
| **PostgreSQL** | If using WSL2 Postgres, connect via `localhost` (WSL2 auto-forwards) |
| **Playwright** | Requires `npx playwright install` (installs Chromium) |

---

## PowerShell Quick Reference

### Replacements for Common Bash Commands

| Bash | PowerShell |
|------|-----------|
| `grep -r "pattern" .` | `Select-String -Path * -Pattern "pattern" -Recurse` |
| `find . -name "*.js"` | `Get-ChildItem -Recurse -Filter "*.js"` |
| `cat file.txt` | `Get-Content file.txt` |
| `rm -rf dir/` | `Remove-Item -Recurse -Force dir\` |
| `export VAR=value` | `$env:VAR = "value"` |
| `echo $PATH` | `$env:PATH -split ';'` |
| `chmod +x script.sh` | Not applicable (use .bat or .ps1) |
| `source .env` | `Get-Content .env \| ForEach-Object { ... }` |

### Dangerous Commands — Windows Equivalents to Avoid

```powershell
# NEVER run AI-generated code that contains:
del /S /Q C:\              # Deletes C: drive recursively
rmdir /S /Q %USERPROFILE%  # Deletes user home directory
format C:                   # Formats C: drive
diskpart                    # Disk partitioning (destructive)
reg delete HKLM\...         # Deletes registry keys
Add-LocalGroupMember ...    # Modifies user groups
```

### WorkBuddy on Windows

WorkBuddy desktop on Windows uses **Git Bash** for `Bash` tool and native **PowerShell** for `PowerShell` tool. File operations prefer dedicated tools (Write/Edit/Read) over shell commands to avoid encoding issues with Chinese paths.

---

## Cross-Reference

| For... | See... |
|--------|--------|
| Full Docker sandbox configs | [docker-sandbox.md](docker-sandbox.md) |
| MCP server details | [mcp-integration.md](mcp-integration.md) |
| Security checklists | [security-checklist.md](security-checklist.md) |
| Quick start for new users | [quick-start.md](quick-start.md) |
