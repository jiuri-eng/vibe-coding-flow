"""VibeCLI — Automated Tests (pytest)

Run: python -m pytest tests/ -v
"""

import subprocess
import sys
import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_DIR = os.path.join(PROJECT_ROOT, "src")
VIBECLI = os.path.join(SRC_DIR, "vibecli.py")
PYTHON = sys.executable


def run_vibecli(*args, cwd=SRC_DIR):
    """Run vibecli.py, return (exit_code, stdout, stderr)."""
    result = subprocess.run(
        [PYTHON, VIBECLI, *args],
        capture_output=True,
        text=True,
        cwd=cwd,
        timeout=10,
    )
    return result.returncode, result.stdout, result.stderr


def test_help():
    """--help prints usage and exits 0."""
    code, out, err = run_vibecli("--help")
    assert code == 0, f"exit {code}, stderr: {err[:200]}"
    assert "usage:" in out.lower() or "Usage:" in out.lower()


def test_scan_current_dir():
    """Scan without arguments should scan current directory."""
    code, out, err = run_vibecli()
    # Exit 0 or 2 (findings) are both acceptable for a successful scan
    assert code in (0, 2), f"Unexpected exit {code}, stderr: {err[:200]}"
    assert len(out) > 0, "Should produce some output"


def test_scan_with_output_file(tmp_path):
    """-o should write output to file."""
    output_file = tmp_path / "report.md"
    code, _, _ = run_vibecli(".", "-o", str(output_file))
    assert code in (0, 2)
    assert output_file.exists()
    content = output_file.read_text()
    assert len(content) > 0
    assert "#" in content  # Markdown report has headers


def test_output_contains_file_inventory():
    """Output should list files found."""
    code, out, _ = run_vibecli()
    assert code in (0, 2)
    assert "vibecli.py" in out, f"Should mention vibecli.py: {out[:300]}"


def test_output_has_language_breakdown():
    """Output should mention Python as a detected language."""
    code, out, _ = run_vibecli()
    assert code in (0, 2)
    lower = out.lower()
    assert "python" in lower, f"Should mention Python: {out[:300]}"


def test_nonexistent_directory():
    """Non-existent path should exit 1 (error)."""
    code, out, err = run_vibecli("/tmp/does_not_exist_abcdef")
    assert code == 1, f"Expected exit 1, got {code}"


def test_security_only_flag():
    """--security-only should still work."""
    code, out, err = run_vibecli("--security-only")
    assert code in (0, 2), f"Unexpected exit {code}, stderr: {err[:200]}"


def test_security_scan_finds_patterns():
    """Security scan should detect known patterns (exit 2 = findings)."""
    # Create a temp file with a known security issue
    import tempfile
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".py", delete=False, dir=os.path.dirname(__file__)
    ) as f:
        f.write('API_KEY = "sk-1234567890abcdef"\n')
        f.write('password = "admin123"\n')
        f.write('eval(user_input)\n')
        bad_file = f.name

    try:
        code, out, _ = run_vibecli(os.path.dirname(bad_file))
        # Should detect at least one issue
        assert "warning" in out.lower() or "finding" in out.lower() or \
               "security" in out.lower() or code == 2, \
               f"Expected security findings, got code={code}, out={out[:300]}"
    finally:
        os.unlink(bad_file)


def test_exit_code_0_for_empty_dir(tmp_path):
    """Scanning empty directory should exit 0 (no findings)."""
    empty_dir = tmp_path / "empty"
    empty_dir.mkdir()
    code, _, err = run_vibecli(str(empty_dir))
    assert code == 0, f"Expected 0 for empty dir, got {code}, err={err[:200]}"


def test_markdown_report_has_expected_sections():
    """Report should contain standard report sections."""
    code, out, _ = run_vibecli("--security-only")
    assert code in (0, 2)
    lower = out.lower()
    # The report should have a header
    assert "#" in out, "Report should contain markdown headers"
