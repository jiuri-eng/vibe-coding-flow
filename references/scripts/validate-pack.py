#!/usr/bin/env python3
"""Rule Pack validator — validate and generate .rulebook/pack.toml files.

Usage:
    python validate-pack.py validate path/to/pack.toml    # Validate a pack
    python validate-pack.py generate path/to/.rulebook    # Generate template pack.toml
    python validate-pack.py check path/to/project         # Check pack vs actual files
"""

import sys
import os
from datetime import datetime, timezone

REQUIRED_FIELDS = {
    "pack": ["name", "version"],
    "targets": ["workbuddy"],
    "rules": ["core"],
}

OPTIONAL_FIELDS = {
    "pack": ["created_at", "updated_at", "author"],
    "targets": ["claude_code", "cursor", "copilot"],
    "rules": ["security", "style", "patterns"],
}

PACK_TEMPLATE = """[pack]
name = "{project_name}"
version = "1.0.0"
created_at = "{now}"
updated_at = "{now}"
author = "vibe-coding-flow"

[targets]
claude_code = true
cursor = true
copilot = false
workbuddy = true

[rules]
core = "core-rules.md"
security = "security-rules.md"
style = "style-guide.md"
patterns = "patterns.md"

# Changelog entries are auto-generated when rules are modified
[[changelog.entry]]
version = "1.0.0"
timestamp = "{now}"
stage = 0
change = "Initial rule pack created from Stage 0 context setup"
reason = "Project initialization"

[version_history]
current = "1.0.0"
previous = []
rollback_support = true
"""


def parse_toml_simple(content):
    """Minimal TOML parser for pack.toml — no external dependencies."""
    result = {}
    current_section = None
    current_table = None

    for line in content.split("\n"):
        line = line.strip()
        if not line or line.startswith("#"):
            continue

        if line.startswith("[") and line.endswith("]"):
            section = line[1:-1].strip()
            if section.startswith("[["):
                table = section[2:-2].strip()
                parts = table.split(".")
                parent = parts[0] if len(parts) > 0 else table
                if parent not in result:
                    result[parent] = []
                result[parent].append({})
                current_table = result[parent][-1]
                current_section = None
            else:
                result[section] = {}
                current_section = result[section]
                current_table = None
        elif "=" in line:
            key, _, val = line.partition("=")
            key = key.strip()
            val = val.strip().strip('"')
            if current_table is not None:
                current_table[key] = val
            elif current_section is not None:
                if val.lower() in ("true", "false"):
                    current_section[key] = val.lower() == "true"
                else:
                    current_section[key] = val
    return result


def validate_pack(filepath):
    """Validate a pack.toml file."""
    errors = []
    warnings = []

    if not os.path.exists(filepath):
        print(f"ERROR: {filepath} not found")
        return False

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    parsed = parse_toml_simple(content)

    for section, fields in REQUIRED_FIELDS.items():
        if section not in parsed:
            errors.append(f"Missing required section: [{section}]")
            continue
        for field in fields:
            if field not in parsed[section]:
                errors.append(f"Missing required field: [{section}].{field}")

    for section, fields in OPTIONAL_FIELDS.items():
        if section in parsed:
            for field in fields:
                if field not in parsed[section]:
                    warnings.append(f"Missing optional field: [{section}].{field}")

    if "pack" in parsed and "version" in parsed["pack"]:
        version = parsed["pack"]["version"]
        parts = version.split(".")
        if len(parts) != 3 or not all(p.isdigit() for p in parts):
            errors.append(
                f"Invalid version format: '{version}' — must be X.Y.Z (semver)"
            )

    if "version_history" in parsed:
        vh = parsed["version_history"]
        if "current" in vh and "pack" in parsed:
            if vh["current"] != parsed["pack"]["version"]:
                warnings.append(
                    f"Version mismatch: pack.version={parsed['pack']['version']} "
                    f"but version_history.current={vh['current']}"
                )

    rule_dir = os.path.dirname(filepath)
    if "rules" in parsed:
        for key, filename in parsed["rules"].items():
            if isinstance(filename, str) and not os.path.exists(
                os.path.join(rule_dir, filename)
            ):
                warnings.append(
                    f"Rule file not found: rules.{key} = '{filename}' "
                    f"(expected at {os.path.join(rule_dir, filename)})"
                )

    if errors:
        print(f"VALIDATION FAILED — {len(errors)} error(s):")
        for e in errors:
            print(f"  [ERROR] {e}")
    if warnings:
        print(f"WARNINGS ({len(warnings)}):")
        for w in warnings:
            print(f"  [WARN]  {w}")
    if not errors and not warnings:
        print("VALIDATION PASSED — pack.toml is valid")
    elif not errors:
        print("VALIDATION PASSED with warnings")
    return len(errors) == 0


def generate_pack(dirpath, project_name=None):
    """Generate a template pack.toml in the given directory."""
    if not os.path.exists(dirpath):
        os.makedirs(dirpath, exist_ok=True)

    filepath = os.path.join(dirpath, "pack.toml")
    if os.path.exists(filepath):
        print(f"ERROR: {filepath} already exists. Delete it first to regenerate.")
        return False

    name = project_name or os.path.basename(os.path.dirname(dirpath.rstrip("/\\")))
    if not name or name == ".":
        name = "my-project"

    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    content = PACK_TEMPLATE.format(project_name=name, now=now)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"Generated: {filepath}")
    print(f"  Project: {name}")
    print(f"  Version: 1.0.0")
    print(f"  Next: fill in rule files (core-rules.md, security-rules.md, ...)")
    return True


def check_consistency(project_dir):
    """Check if pack.toml is consistent with actual project files."""
    pack_path = os.path.join(project_dir, ".rulebook", "pack.toml")
    claude_path = os.path.join(project_dir, "CLAUDE.md")
    cursor_path = os.path.join(project_dir, ".cursorrules")

    issues = []

    if not os.path.exists(pack_path):
        issues.append("No .rulebook/pack.toml found — run 'generate' first")
    else:
        with open(pack_path, "r", encoding="utf-8") as f:
            parsed = parse_toml_simple(f.read())
        version = parsed.get("pack", {}).get("version", "unknown")

        if os.path.exists(claude_path):
            with open(claude_path, "r", encoding="utf-8") as f:
                claude_content = f.read()
            if version not in claude_content:
                issues.append(
                    f"CLAUDE.md does not reference pack version {version}"
                )

        if os.path.exists(cursor_path):
            with open(cursor_path, "r", encoding="utf-8") as f:
                cursor_content = f.read()
            if version not in cursor_content:
                issues.append(
                    f".cursorrules does not reference pack version {version}"
                )

    if issues:
        print(f"CONSISTENCY CHECK — {len(issues)} issue(s):")
        for i in issues:
            print(f"  [!] {i}")
    else:
        print("CONSISTENCY CHECK PASSED — pack is in sync with project files")
    return len(issues) == 0


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(0)

    command = sys.argv[1]

    if command == "validate":
        if len(sys.argv) < 3:
            print("Usage: validate-pack.py validate path/to/pack.toml")
            sys.exit(1)
        ok = validate_pack(sys.argv[2])
        sys.exit(0 if ok else 1)

    elif command == "generate":
        target = sys.argv[2] if len(sys.argv) > 2 else ".rulebook"
        name = sys.argv[3] if len(sys.argv) > 3 else None
        ok = generate_pack(target, name)
        sys.exit(0 if ok else 1)

    elif command == "check":
        target = sys.argv[2] if len(sys.argv) > 2 else "."
        ok = check_consistency(target)
        sys.exit(0 if ok else 1)

    else:
        print(f"Unknown command: {command}")
        print("Available: validate, generate, check")
        sys.exit(1)


if __name__ == "__main__":
    main()
