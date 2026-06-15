# Stage 1: Ideation & Scoping — VibeCLI

## User Interaction

```
User: 我想做一个命令行工具，能扫描一个代码目录，然后生成一份分析报告，
      告诉我这个项目有什么文件、代码量多少、有没有明显的安全问题。

AI: 好的，让我确认一下方向：
   1. 这是一个纯本地的代码分析工具，不需要联网？
   2. 报告格式是 Markdown 输出到终端/文件？
   3. 扫描范围是按文件扩展名判断语言类型？
   4. 安全扫描只做基础模式匹配（不做AST分析）？

User: 对，就这些。简单实用就好，不要过度设计。
```

## Direction Confirmation

### Core Idea
A **zero-dependency Python CLI tool** that scans a target directory and produces a structured Markdown analysis report covering file inventory, code complexity indicators, and basic security pattern detection.

### MVP Scope (IN)

| # | Feature | Description |
|---|---------|-------------|
| 1 | File Inventory | Count files by extension, total lines, language breakdown |
| 2 | Complexity Scan | Detect long functions (>50 lines), deep nesting (>4 levels) |
| 3 | Security Quick-Scan | Pattern match for secrets, eval(), SQL injection vectors |
| 4 | Markdown Report | Formatted report with sections, tables, severity labels |
| 5 | CLI Interface | argparse with --path, -o (output), --security-only flags |

### Explicitly Excluded (OUT)

| # | Feature | Reason for Exclusion |
|---|---------|---------------------|
| 1 | AST-based analysis | Over-engineering; regex suffices for v1 |
| 2 | Git integration | Adds dependency (gitpython); out of scope |
| 3 | JSON/HTML output formats | Markdown is sufficient; can add later |
| 4 | Configuration file (.vibeclirc) | CLI args are enough for now |
| 5 | Parallel scanning | Most directories are small; adds complexity |
| 6 | Web UI / dashboard | This is explicitly a CLI tool |

### Success Criteria

- [ ] Runs with zero `pip install` (stdlib only)
- [ ] Scans a 100-file project in under 2 seconds
- [ ] Report is readable as raw Markdown in terminal
- [ ] Exit code reflects result status correctly

### Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|-----------|
| Large directory causes slowdown | Low | Medium | Add --max-depth flag if needed |
| Binary files cause encoding errors | Medium | Low | Skip non-text files gracefully |
| False positives in security scan | High | Low | Label as "potential" only, never definitive |

## Validation (L1-1 Self-Check)

| Check | Result |
|-------|--------|
| docs/01-ideation.md exists with required sections | PASS |
| User's core intent preserved | PASS ("scan dir → analysis report") |
| Excluded items list present (6 items) | PASS |
| Success criteria measurable | PASS (all have binary yes/no criteria) |

**L1-1: PASS — Ready for Stage 2**

## Next → Stage 2: Requirements & PRD
