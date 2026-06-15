# Module A: Meta-Mentor Layer (元导师层)

> **Part of Advanced QA suite**: This file covers the Meta-Mentor CPI module. See also:
> - [rule-pack.md](rule-pack.md) — Module B: Rule Package Version Management
> - [design-reverse.md](design-reverse.md) — Module C: Design System Reverse Engineering
>
> **Source**: [vibe-check-mcp-server](https://github.com/PV-Bhat/vibe-check-mcp-server) (490 stars)

## Concept

The Meta-Mentor is an external "sanity check" layer that sits between the AI Agent and the user. Think of it as a **rubber-duck debugger for LLMs** — a quick sanity check before the agent goes down the wrong path.

### Why It Matters

Research data (153 runs evaluated):

| Metric | Without Meta-Mentor | With Meta-Mentor | Change |
|--------|---------------------|------------------|--------|
| Task success rate | ~27% | ~54% | **+27% (almost 2x)** |
| Harmful operations | ~83% | ~42% | **-41% (almost halved)** |

The meta-mentor prevents:
- **Tunnel Vision** — Agent fixates on one approach and ignores alternatives
- **Over-engineering** — Agent builds more than the user asked for
- **Reasoning Lock-In** — Agent confidently executes a flawed plan
- **Goal Drift** — Agent gradually shifts away from original intent

### Chain-Pattern Interrupts (CPI)

The core mechanism: at key risk inflection points, inject brief reflective pauses.

```
Normal flow:   Plan -> Execute -> Deliver
CPI-enhanced:  Plan -> [CPI CHECK] -> Execute -> [CPI CHECK] -> Deliver
                            ^                        ^
                  Challenge assumptions    Validate alignment
```

#### When to Trigger CPI

| Phase | Risk | CPI Question to Ask Self |
|-------|------|--------------------------|
| After Stage 1 (Ideation) | Scope creep starting? | "Is this still what the user originally asked for?" |
| After Stage 3 (Architecture) | Over-engineering? | "Is there a simpler way to achieve the same goal?" |
| Before each major implementation task | Wrong approach? | "What could go wrong with my current plan?" |
| After Stage 6 (Implementation) | Quality issues missed? | "Would I be embarrassed if a senior engineer reviewed this?" |
| At any point after 3+ failed attempts | Doom Loop forming? | "Am I stuck in a loop? Should I try a completely different approach?" |

#### Optimal Dosage

Research shows optimal interruption rate: **10-20% of steps**. Too few = no effect; too many = annoying overhead.

For our 8-stage workflow with ~9 tasks per project:

```
Recommended CPI points for typical project:
1. After Stage 1 ideation (scope check)
2. After Stage 3 architecture (simplicity check)
3. Mid-Stage 6 (after task 4-5 of 9) (progress sanity check)
4. Before Stage 7 delivery (final quality gut-check)
= 4 CPI checks per project (~15% of total decision points) <- optimal range
```

#### CPI Implementation Pattern

When triggered, run this internal self-questioning protocol:

```markdown
## CPI Checkpoint: {stage_name}

### 1. Alignment Check
- Original user request (verbatim): "{...}"
- Current working direction: "{...}"
- Keyword overlap: {X}%
- Verdict: ALIGNED / DRIFT DETECTED

### 2. Simplicity Check
- What am I building right now?
- What is the MINIMAL version of this?
- Am I adding things the user didn't ask for?
- Verdict: APPROPRIATE / OVER-ENGINEERED

### 3. Assumption Audit
- Top 3 assumptions I'm making:
  1. {assumption} -> Valid? Yes/No/Uncertain
  2. {assumption} -> Valid? Yes/No/Uncertain
  3. {assumption} -> Valid? Yes/No/Uncertain
- Action needed based on invalid assumptions: {...}

### 4. Decision
- CONTINUE (all checks pass) / ADJUST (fix drift or over-engineering) / PAUSE (ask user)
```

### Integration with Existing Self-Check System

Our L4 Anti-Pattern Detection already covers Drift detection. The Meta-Mentor layer adds:

| Existing L4 | Meta-Mentor Adds |
|-------------|-----------------|
| Detects drift AFTER it happens | Prevents drift BEFORE it solidifies |
| Automatic threshold-based triggers | Reflective, qualitative self-questioning |
| Reactive (fix problems) | Proactive (prevent problems) |

**Combined architecture**:

```
L4 Anti-Pattern (continuous, automatic):
  +-- Monitors signals (retries, contradictions, keyword overlap)
  +-- Triggers when thresholds exceeded

Meta-Mentor CPI (strategic checkpoints):
  +-- Scheduled reflective pauses at key milestones
  +-- Qualitative self-challenge questions
  +-- Complements L4 with human-like "gut check"

Together: Automatic monitoring + Strategic reflection = Comprehensive QA
```

### Practical Setup (for WorkBuddy integration)

The Meta-Mentor does NOT require a separate MCP server or external tool. It's a **pattern of thinking** integrated into the workflow:

1. Add CPI checkpoint descriptions to SKILL.md at each relevant stage
2. The AI agent runs the self-questioning protocol as part of its normal reasoning
3. If any CPI check fails, the agent adjusts course BEFORE presenting to user
4. Cost: Zero additional tools or API calls; pure reasoning

---

## See Also

- [rule-pack.md](rule-pack.md) — Module B: Rule Package Version Management (pack.toml format, validation script, sync/rollback)
- [design-reverse.md](design-reverse.md) — Module C: Design System Reverse Engineering (extract tokens from existing products)
- [scripts/validate-pack.py](scripts/validate-pack.py) — Python script to generate and validate pack.toml files
- [self-check.md](self-check.md) — L1-L4 Self-Check System (complementary automatic QA layer)
