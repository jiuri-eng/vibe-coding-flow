# Token Efficiency Optimization for Vibe Coding

> Reference: [AI-Coding-Style-Guides](https://github.com/lidangzzz/AI-Coding-Style-Guides) (484 stars)
>
> Core philosophy: **In AI-assisted programming, "good code" shifts from human-readability-first to token-efficiency-first**, with LLM serving as the translation bridge between compressed and readable forms.

## The Problem

When vibe coding scales beyond small projects:

| Project Size | Source Code (lines) | Token Count (approx) | Context Window Fit |
|---|---|---|---|
| Small (demo) | 200-500 | 2K-5K tokens | Easy — fits in any window |
| Medium (app) | 2,000-5,000 | 20K-50K tokens | Fits in most 128K+ windows |
| Large (platform) | 10,000-50,000 | 100K-500K tokens | **Exceeds typical limits** |
| Enterprise | 100,000+ | 1M+ tokens | **Far exceeds any single context** |

**Key insight**: Context windows will always feel insufficient, regardless of whether they are 32K, 128K, or 1M. Token efficiency is a permanent concern.

## Solution: 8-Level Compression System

### Compression Levels

| Level | Description | Whitespace Removal | Code Compaction | Variable Shortening | Export Names | Comments | Advanced Refactoring | Readability | Use Case |
|:---:|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|---|
| **L1** | Remove extra whitespace/blank lines | Basic | No | No | Keep all | Keep all | No | Full | Default baseline |
| **L2** | Light line merging | Basic | Light merge | No | Keep all | Keep all | No | High | Minor space savings |
| **L3** | Shorten local variables only | Basic | Yes | Local vars only | Keep all | Keep all | No | High | Internal code cleanup |
| **L4** | Shorten local + non-export names | Basic | Yes | Local + non-export | Keep all | Keep all | No | Medium-High | Standard AI coding style |
| **L5** | Remove all whitespace + shorten identifiers | Complete | Max compact | Local + non-export | Keep all | Export comments only | No | Low | Aggressive compression |
| **L6** | Export-only comments | Complete | Max | Local + non-export | Keep all | Export section only | No | Low | API-preserving mode |
| **L7** | Remove all comments | Complete | Max | Local + non-export | Keep all | Remove all | No | Very Low | Maximum density |
| **L8** | Language-specific minification | Complete | Max + refactor | Local + non-export | Keep all | Remove all | **Yes** (ternaries, sugar) | Minimal | Extreme edge case |

### Compression Effect (Real Data)

Original TypeScript KMP algorithm implementation:
| Version | Characters | % of Original | Technique |
|---------|-----------|:---:|---|
| Original code | 1,216 | 100% | Standard formatting |
| Light compression (L2) | 795 | 65.4% | Remove extra whitespace |
| Deep compression (L5) | 443 | 36.4% | Short vars + remove comments |
| **AI-optimized (L8)** | **283** | **23.3%** | Semantic refactoring + language features |

**Key finding**: AI-style compression outperforms traditional tools (JSCompress: 28.6%, jsonminify: 79.2%) because it includes **semantic-level renaming and restructuring**, not just syntax-level changes.

## Strategy 1: Hierarchical Naming

The most impactful single technique for token reduction.

### Rules

```javascript
// BAD: All names verbose (wastes ~40% of identifier tokens)
function processUserAuthenticationCredentials(userAuthenticationCredentials) {
  const isAuthenticatedUser = checkUserAuthenticationStatus(userAuthenticationCredentials);
  const userSessionToken = generateUserSessionToken(isAuthenticatedUser);
  return { isAuthenticatedUser, userSessionToken };
}

// GOOD: Exports descriptive, internals minimal
function auth(creds) {           // export: short but clear
  const ok = checkAuth(creds);     // local: minimal
  const t = makeToken(ok);         // temp: single char
  return { ok, t };               // object props: abbreviated
}
```

### Naming Convention

| Scope | Style | Example | Rationale |
|-------|-------|---------|-----------|
| **Exported functions/classes** | Descriptive, camelCase | `auth()`, `buildLPS()` | API surface must be self-documenting |
| **Internal functions** | Abbreviated | `chk()`, `mk()` | AI can infer from usage context |
| **Loop variables** | Single letter | `i`, `j`, `k` | Universal convention |
| **Temporary variables** | Single letter / abbrev | `t`, `n`, `s` | Short-lived, scope is obvious |
| **Parameters** | Abbreviated | `req`, `res`, `cb` | Well-known patterns |
| **Object properties in returns** | Abbreviated | `{ ok, err }` | Destructuring makes names visible at call site |

### When NOT to shorten
- **Type definitions** — keep full names for type safety and documentation
- **Constants with domain meaning** — `MAX_RETRY_COUNT` > `mr`
- **Test descriptions** — keep readable for test output
- **Security-related variables** — `passwordHash` > `ph` (avoid confusion)

## Strategy 2: File Consolidation

Reduce file count to minimize import overhead and inter-file reference tokens.

### Guidelines

| Scenario | Recommendation | Rationale |
|----------|---------------|-----------|
| Tightly coupled functions | Merge into one file | Eliminates import statements between them |
| Independent modules | Separate files | Clear boundaries, lazy loading possible |
| Utility functions used everywhere | One `utils.js` / `helpers.py` | Single import point |
| Types/interfaces | One `types.ts` | Centralized type definitions |

### Anti-pattern to avoid
```bash
# TOO MANY FILES — each file adds import overhead + file header noise
src/
  auth/
    login.ts          # 15 lines
    logout.ts         # 8 lines
    session.ts        # 22 lines
    token.ts          # 18 lines
    validate.ts       # 25 lines
    hash.ts           # 12 lines
```

Better:
```bash
# CONSOLIDATED — related logic together
src/
  auth.ts             # 100 lines, all auth logic
```

Token savings from consolidation: typically **15-25%** on import/boilerplate overhead alone.

## Strategy 3: Comment Optimization

### Rule: External docs ON, internal docs OFF

```python
# GOOD: Export has docstring (AI needs this to understand purpose)
def build_lps(pattern: str) -> list[int]:
    """Build Longest Prefix Suffix array for KMP algorithm.
    Args: pattern - the pattern string to search for.
    Returns: LPS array where lps[i] = longest proper prefix which is also suffix."""
    p = len(pattern)
    lps = [0] * p
    length = 0
    i = 1
    while i < p:
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        elif length:
            length = lps[length - 1]
        else:
            lps[i] = 0
            i += 1
    return lps
    # Note: NO inline comments inside — AI understands the algorithm
```

Comment budget rule of thumb:
- **Top-level exports**: 1-3 lines explaining what + inputs + outputs
- **Inside functions**: Zero comments unless the logic is genuinely non-obvious AND non-standard
- **Complex business rules**: 1-line comment WHY (not WHAT)

## Strategy 4: Abstraction & Deduplication

Eliminate repeated patterns that waste tokens:

| Pattern | Token-wasteful | Token-efficient |
|---------|---------------|-----------------|
| Repeated validation | Copy-paste checks everywhere | Higher-order validator function |
| Similar error handling | Try-catch blocks duplicated | Error handler utility |
| Repeated type conversions | Cast everywhere | Type coercion utility |
| Similar data transformations | Map/filter chains repeated | Generic transform pipeline |

## Strategy 5: Library Selection

Prefer libraries with smaller surface area when functionality is equivalent:

| Need | Heavy Option | Tokens (approx) | Light Option | Tokens (approx) |
|------|-------------|:-:|-------------|:-:|
| Date handling | moment.js | 15K+ imports | date-fns (tree-shake) | 200 per function |
| HTTP requests | axios (full) | 3K | fetch (native) | 0 |
| DOM manipulation | jQuery | 10K+ | native DOM APIs | 0 |
| State management | Redux Toolkit | 2K+ boilerplate | Zustand | 200 |
| UI components | MUI (full) | 50K+ | Custom CSS | Variable |

## Integration with Vibe Coding Flow

### When to Apply Token Optimization

| Stage | Action |
|-------|--------|
| **Stage 0 (Context Setup)** | Add token efficiency rules to CLAUDE.md under "Coding Conventions" section |
| **Stage 3 (Architecture)** | Decide target compression level based on project size |
| **Stage 6 (Implementation)** | Write code following naming conventions; apply selected level |
| **Stage 7 (Delivery)** | Run token audit; report compression metrics |

### Choosing the Right Level for Your Project

```
Project Size Guide:
┌─────────────────┬──────────────┬──────────────────────────────┐
│ Size            │ Recommended   │ Notes                        │
├─────────────────┼──────────────┼──────────────────────────────┤
│ < 500 lines     │ L1-L2        │ Readability priority         │
│ 500-3000 lines  │ L3-L4        │ Balanced (recommended default)│
│ 3000-10000 lines│ L4-L5        │ Efficiency starts mattering  │
│ > 10000 lines   │ L5-L7        │ Must compress for context fit│
│ Special case    │ L8           │ Only when absolutely needed  │
└─────────────────┴──────────────┴──────────────────────────────┘
```

### Adding to CLAUDE.md Template

Add this section to Stage 0's generated CLAUDE.md:

```markdown
## Token Efficiency (for large projects)

Target compression level: L{N}
Naming convention: Exports descriptive, internals abbreviated
File strategy: {consolidated | modular}
Comment policy: Export docstrings only
Library preference: Lightweight / native APIs preferred
```

### Token Audit Script (Stage 7)

Run this during delivery to measure actual token efficiency:

```bash
# Count approximate token ratio (rough estimate: 1 token ≈ 4 chars for code)
echo "=== Token Efficiency Audit ==="
TOTAL_CHARS=$(find src/ -type f \( -name "*.ts" -o -name "*.js" -o -name "*.py" \) -exec cat {} \; | wc -c)
EXPORT_CHARS=$(grep -r "export\|def \|class " src/ --include="*.ts" --include="*.js" --include="*.py" | wc -c)
TOTAL_TOKENS=$((TOTAL_CHARS / 4))
RATIO=$(echo "scale=1; $EXPORT_CHARS * 100 / $TOTAL_CHARS" | bc)

echo "Total chars: $TOTAL_CHARS"
echo "Est. tokens: $TOTAL_TOKENS"
echo "Export/interface ratio: ${RATIO}% (higher = more efficient)"
echo "Target: Export ratio > 60%"
```

### Decompression: When Humans Need to Read

If a human developer needs to understand highly compressed code:

```
[Compressed code L5-L8] → Send to LLM → [Detailed explanation + Readable reconstruction]
```

The LLM acts as bidirectional translator:
- Compressing for its own consumption (token efficiency)
- Expanding for human review (readability)

This is safe because:
- Unit tests verify functional correctness regardless of readability
- Export names remain unchanged (API stability)
- LLM can always explain/reconstruct on demand

## Safety Guarantees

Token optimization does NOT compromise quality because:

| Concern | Mitigation |
|---------|-----------|
| Bugs hidden in compressed code? | Unit tests catch behavior regressions |
| Can't debug compressed code? | LLM explains/expands on demand |
| Team can't read it? | In pure Vibe Coding, humans read outputs not sources |
| Refactoring harder? | LLM handles refactoring natively |
| Export API unstable? | Export names NEVER shortened |

## Cost Impact

```
Cost = Input_Tokens × Price_In + Output_Tokens × Price_Out

If source code is 50K tokens (unoptimized):
  Input:  50K × $X per 1M tokens
  Output: varies by task complexity

If source code is 20K tokens (optimized to L4):
  Input:  20K × $X per 1M tokens  (60% cost reduction!)
  Output: same or less (less context confusion)
```

For projects processed through many iterations (typical Vibe Coding involves 10-50 AI turns), the cumulative savings are significant.

## References

- [AI-Coding-Style-Guides](https://github.com/lidangzzz/AI-Coding-Style-Guides) — Original methodology
- Compression benchmarks verified against JSCompress, jsonminify
- TOML prompt configuration format available in original repo for automated compression prompting
