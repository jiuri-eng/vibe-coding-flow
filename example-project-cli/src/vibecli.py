#!/usr/bin/env python3
"""VibeCLI: Codebase Analysis Tool.

Scans a directory and generates a Markdown report covering:
- File inventory (by extension/language)
- Complexity indicators (long functions, deep nesting)
- Security pattern detection (secrets, eval(), SQL vectors)

Usage:
    python vibecli.py <path> [-o output.md] [--security-only]

Exit codes: 0=success, 1=error, 2=findings detected.
"""

import os
import re
import sys
import argparse
from pathlib import Path
from datetime import datetime, timezone
from dataclasses import dataclass, field

# Constants
SKIP_DIRS = {'.git', 'node_modules', '__pycache__', '.tox', 'venv', '.venv',
             'dist', 'build', '.next', '.cache'}
LANG_MAP = {
    '.py': 'Python', '.js': 'JavaScript', '.ts': 'TypeScript',
    '.html': 'HTML', '.css': 'CSS', '.md': 'Markdown',
    '.json': 'JSON', '.yaml': 'YAML', '.yml': 'YAML',
    '.sh': 'Shell', '.sql': 'SQL', '.java': 'Java',
    '.go': 'Go', '.rs': 'Rust', '.rb': 'Ruby', '.php': 'PHP',
    '.c': 'C', '.cpp': 'C++', '.h': 'C/C++ Header',
    '.tsx': 'TSX', '.jsx': 'JSX', '.vue': 'Vue', '.svelte': 'Svelte',
}
TEXT_EXTS = set(LANG_MAP.keys()) | {'.txt', '.xml', '.toml', '.cfg',
                                   '.ini', '.env', '.dockerignore'}

# Pre-compiled patterns
RE_FUNC_PY = re.compile(r'^(\s*)def\s+\w+\([^)]*\)\s*:', re.MULTILINE)
RE_FUNC_JS = re.compile(r'^(\s*)(?:function\s+\w+|\w+)\s*\([^)]*\)\s*(?:\{|$)', re.MULTILINE)
RE_CLASS = re.compile(r'^(\s*)class\s+', re.MULTILINE)
RE_SECRET = re.compile(
    r'(password|passwd|pwd|secret|api_key|apikey|token|auth|credential)'
    r'\s*[=:]\s*[("\']([^"\']{3,})[("\')]',
    re.IGNORECASE)
RE_EVAL = re.compile(r'\beval\s*\(|\bexec\s*\(|subprocess.*shell\s*=\s*True', re.IGNORECASE)
RE_SQL_INJECT = re.compile(
    r'(?:SELECT|INSERT|UPDATE|DELETE|FROM)\s+.*(?:f["\']|%\s|\.format\()',
    re.IGNORECASE)


@dataclass
class FileInfo:
    path: str
    ext: str
    lines: int
    lang: str


@dataclass
class ComplexFinding:
    file: str
    line: int
    ftype: str
    value: int
    sev: str


@dataclass
class SecFinding:
    file: str
    line: int
    pat: str
    snippet: str
    sev: str


@dataclass
class ScanResult:
    files: list[FileInfo] = field(default_factory=list)
    complex_findings: list[ComplexFinding] = field(default_factory=list)
    sec_findings: list[SecFinding] = field(default_factory=list)
    total_f: int = 0
    total_l: int = 0


def _count_lines(fp: str) -> tuple[int, list[str]]:
    """Count lines and return content lines."""
    try:
        with open(fp, encoding='utf-8', errors='replace') as fh:
            lines = fh.readlines()
        return len(lines), [l.rstrip('\n') for l in lines]
    except OSError:
        return 0, []


def _is_text_file(fp: str, ext: str) -> bool:
    if ext in TEXT_EXTS:
        return True
    try:
        with open(fp, encoding='utf-8', errors='strict') as _:
            return True
    except (OSError, UnicodeDecodeError):
        return False


def collect_files(target: Path) -> list[FileInfo]:
    """Walk directory, filter, categorize, count lines."""
    results = []
    try:
        entries = list(target.iterdir())
    except PermissionError:
        print(f"[WARN] Permission denied: {target}", file=sys.stderr)
        return results

    for entry in entries:
        name = entry.name
        if name.startswith('.') and entry.is_dir():
            continue
        if name in SKIP_DIRS:
            continue
        if entry.is_dir():
            results.extend(collect_files(entry))
            continue
        ext = entry.suffix.lower()
        if not _is_text_file(str(entry), ext):
            continue
        n, _ = _count_lines(str(entry))
        results.append(FileInfo(
            path=str(entry.relative_to(target)),
            ext=ext or '(none)',
            lines=n,
            lang=LANG_MAP.get(ext, 'Other'),
        ))
    return results


def analyze_complexity(files: list[FileInfo]) -> list[ComplexFinding]:
    """Detect long functions (>50 lines) and deep nesting (>4 levels)."""
    findings = []
    for fi in files:
        _, contents = _count_lines(
            Path.cwd().joinpath(fi.path) if not Path(fi.path).is_absolute()
            else fi.path)
        if not contents:
            continue
        src = '\n'.join(contents)

        for pattern in [RE_FUNC_PY, RE_FUNC_JS, RE_CLASS]:
            for m in pattern.finditer(src):
                indent = len(m.group(1))
                start = src[:m.start()].count('\n') + 1
                func_lines = 0
                base_indent = indent
                depth = indent // 4 if indent else 0

                for li in range(start - 1, min(start + 200, len(contents))):
                    cur_ind = len(contents[li]) - len(contents[li].lstrip())
                    if li == start - 1:
                        continue
                    if cur_ind <= base_indent and func_lines > 0:
                        break
                    func_lines += 1

                if func_lines > 50:
                    sev = 'CRITICAL' if func_lines > 100 else 'WARNING'
                    findings.append(ComplexFinding(
                        file=fi.path, line=start,
                        ftype='long_function', value=func_lines, sev=sev))

                if depth > 4:
                    findings.append(ComplexFinding(
                        file=fi.path, line=start,
                        ftype='deep_nesting', value=depth, sev='WARNING'))
                break
    return findings


def scan_security(files: list[FileInfo]) -> list[SecFinding]:
    """Regex-based security pattern detection."""
    findings = []
    for fi in files:
        _, contents = _count_lines(
            Path.cwd().joinpath(fi.path) if not Path(fi.path).is_absolute()
            else fi.path)
        for i, line in enumerate(contents, 1):
            m = RE_SECRET.search(line)
            if m:
                snippet = line.strip()[:80]
                findings.append(SecFinding(
                    file=fi.path, line=i, pat='hardcoded_secret',
                    snippet=snippet, sev='CRITICAL'))
            m = RE_EVAL.search(line)
            if m:
                findings.append(SecFinding(
                    file=fi.path, line=i, pat='eval_or_exec_call',
                    snippet=line.strip()[:80], sev='HIGH'))
            m = RE_SQL_INJECT.search(line)
            if m:
                findings.append(SecFinding(
                    file=fi.path, line=i, pat='potential_sql_injection',
                    snippet=line.strip()[:80], sev='MEDIUM'))
    return findings


def format_report(r: ScanResult, target: str) -> str:
    """Build Markdown report from scan results."""
    now = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')
    lines = []
    lines.append(f'# VibeCLI Report')
    lines.append(f'')
    lines.append(f'**Target:** `{target}`  ')
    lines.append(f'**Scanned:** {now}  ')
    lines.append(f'**Files:** {r.total_f} | **Lines:** {r.total_l}')
    lines.append(f'')

    # Inventory section
    lines.append('## File Inventory')
    lines.append('')
    lines.append('| Extension | Language | Files | Lines | % |')
    lines.append('|---|---|---|---|---|')
    by_ext = {}
    for fi in r.files:
        k = (fi.ext, fi.lang)
        if k not in by_ext:
            by_ext[k] = {'f': 0, 'l': 0}
        by_ext[k]['f'] += 1
        by_ext[k]['l'] += fi.lines
    for (ext, lang), v in sorted(by_ext.items(),
                                    key=lambda x: -x[1]['l']):
        pct = round(v['l'] / max(r.total_l, 1) * 100, 1)
        lines.append(f'| `{ext}` | {lang} | {v["f"]} | {v["l"]} | {pct}% |')
    lines.append('')

    # Complexity
    if r.complex_findings:
        lines.append('## Complexity Findings')
        lines.append('')
        lines.append('| File | Line | Type | Value | Severity |')
        lines.append('|---|---|---|---|---|')
        for cf in sorted(r.complex_findings, key=lambda x: (-1 if x.sev == 'CRITICAL' else 0, x.value)):
            lines.append(f'| `{cf.file}` | {cf.line} | {cf.ftype} | {cf.value} | {cf.sev} |')
        lines.append('')

    # Security
    if r.sec_findings:
        sev_order = {'CRITICAL': 0, 'HIGH': 1, 'MEDIUM': 2, 'LOW': 3}
        sec_sorted = sorted(r.sec_findings, key=lambda x: (sev_order.get(x.sev, 9), x.file))
        lines.append('## Security Findings (POTENTIAL)')
        lines.append('')
        lines.append('| File | Line | Pattern | Snippet | Severity |')
        lines.append('|---|---|---|---|---|')
        for sf in sec_sorted:
            esc = sf.snippet.replace('|', '\\|').replace('\n', ' ')
            lines.append(f'| `{sf.file}` | {sf.line} | {sf.pat} | `{esc[:60]}` | {sf.sev} |')
        lines.append('')

    # Summary
    health = 100
    health -= min(len(r.sec_findings) * 10, 70)
    health -= min(len([c for c in r.complex_findings if c.sev == 'CRITICAL']) * 15, 40)
    health = max(health, 0)
    recs = []
    if r.sec_findings:
        recs.append('- Review and remove hardcoded secrets/credentials immediately')
    if any(c.ftype == 'long_function' and c.value > 100 for c in r.complex_findings):
        recs.append('- Consider splitting functions exceeding 100 lines')
    if not recs:
        recs.append('- No critical issues found. Project looks healthy.')

    lines.append('## Summary')
    lines.append('')
    lines.append(f'| Metric | Value |')
    lines.append(f'|---|---|')
    lines.append(f'| Total files scanned | {r.total_f} |')
    lines.append(f'| Total lines of code | {r.total_l} |')
    lines.append(f'| Complexity warnings | {len(r.complex_findings)} |')
    lines.append(f'| Security findings | {len(r.sec_findings)} |')
    lines.append(f'| Health score | **{health}/100** |')
    lines.append('')
    lines.append('### Recommendations')
    lines.append('')
    for rec in recs:
        lines.append(rec)
    lines.append('')
    return '\n'.join(lines)


def scan_directory(target: Path, security_only: bool = False) -> ScanResult:
    """Run full scan pipeline."""
    r = ScanResult()
    r.files = collect_files(target)
    r.total_f = len(r.files)
    r.total_l = sum(fi.lines for fi in r.files)

    if not security_only:
        r.complex_findings = analyze_complexity(r.files)
    r.sec_findings = scan_security(r.files)
    return r


def main():
    parser = argparse.ArgumentParser(
        description='VibeCLI: Codebase analysis tool.',
        epilog='Example: python vibecli.py ./my-project -o report.md')
    parser.add_argument('path', nargs='?', default='.',
                        help='Target directory (default: current)')
    parser.add_argument('-o', '--output', dest='output',
                        help='Write report to file instead of stdout')
    parser.add_argument('--security-only', action='store_true',
                        help='Run only security scan')
    args = parser.parse_args()

    target = Path(args.path)
    if not target.is_dir():
        print(f'[ERROR] Not a directory: {target}', file=sys.stderr)
        sys.exit(1)

    if '..' in str(target):
        print('[ERROR] Path traversal detected. Use absolute paths.',
              file=sys.stderr)
        sys.exit(1)

    result = scan_directory(target, security_only=args.security_only)
    report = format_report(result, str(target))

    if args.output:
        out_path = Path(args.output)
        out_path.write_text(report, encoding='utf-8')
        print(f'Report written to: {out_path}', file=sys.stderr)
    else:
        print(report)

    sys.exit(2 if result.sec_findings or result.complex_findings else 0)


if __name__ == '__main__':
    main()
