# Stage 0: Context Setup — 产物

## 触发条件

用户说："我想做个待办清单 App" → 立即进入 Stage 0，在开始任何构思之前先生成 AI 规则文件。

## 自动生成的文件

### CLAUDE.md

```markdown
# VibeTodo - Project Rules for AI Assistants

## Project Overview
VibeTodo is a single-page Todo application built with vanilla HTML/CSS/JavaScript.
No frameworks, no build tools, no backend. Data persists in localStorage.

## Tech Stack
- HTML5 (semantic elements)
- CSS3 (Custom Properties, Flexbox, Grid)
- JavaScript ES6+ (modules pattern, localStorage API)
- No external dependencies

## Code Conventions
- **File structure**: Single-page app with 3 files: index.html, styles.css, app.js
- **Naming**: camelCase for JS variables/functions, kebab-case for CSS classes, UPPERCASE for constants
- **HTML**: Semantic tags (header, main, section, footer). No div soup.
- **CSS**: BEM-like naming. Custom properties in :root for design tokens. Mobile-first responsive.
- **JS**: Functions over classes (this is simple enough). Pure functions preferred. Side effects isolated.
- **Comments**: JSDoc for functions. Section headers for logical code blocks.
- **Error handling**: Try/catch around localStorage operations. Graceful degradation if unavailable.

## Architecture
- `index.html`: Structure only. Inline critical CSS for FOUC prevention. Defer script loading.
- `styles.css`: All styling. Design tokens in :root. Component styles grouped by section.
- `app.js`: All logic. Event delegation pattern for UI interactions. Module-level state with closure.

## Data Model (localStorage)
Key: `vibetodo-todos`
Value: JSON array of Todo objects:
```json
{
  "id": string (uuid-like),
  "title": string,
  "priority": "high" | "medium" | "low",
  "completed": boolean,
  "createdAt": ISO date string,
  "completedAt": ISO date string | null
}
```

## Security Requirements (MANDATORY)
- NEVER hardcode secrets, tokens, or credentials — always use environment variables
- All user inputs must be validated and sanitized (XSS prevention)
- Use textContent (not innerHTML) when rendering user-supplied content
- New dependencies: N/A (no npm) but review any CDN links before adding
- When in doubt, ask about security implications before implementing

## Do's and Don'ts
- DO keep it simple — this is an MVP example project
- DO follow mobile-first responsive design
- DO validate user input on both client side (length limits, trim whitespace)
- DON'T add features not specified in the PRD without asking first
- DON'T use innerHTML with user content — always use textContent or DOM APIs
- DON'T over-engineer — no need for state management library or event bus
```

### .cursorrules

```jsonc
// VibeTodo Coding Rules
{
  "language": "JavaScript (ES6+) / HTML5 / CSS3",
  "framework": "None (vanilla)",
  "conventions": {
    "naming_js": "camelCase",
    "naming_css": "kebab-case (BEM-like)",
    "indentation": "2 spaces",
    "quotes": "single quotes for JS, double for CSS",
    "semicolons": "always"
  },
  "structure": {
    "files": ["index.html", "styles.css", "app.js"],
    "no_build_tools": true,
    "no_npm": true
  },
  "rules": [
    "Use semantic HTML elements (header, main, section, footer)",
    "Mobile-first CSS with custom properties as design tokens",
    "Event delegation for UI interactions (not per-element listeners)",
    "textContent for user data — never innerHTML",
    "Pure functions for business logic, isolated side effects",
    "JSDoc comments for all public functions",
    "Keep each function under 20 lines; split if longer"
  ],
  "security": [
    "No innerHTML with user input",
    "Validate title length (1-200 chars), strip whitespace",
    "Try/catch all localStorage operations",
    "No external CDN links without approval"
  ]
}
```

### INITIAL.md (可复用的功能请求模板)

```markdown
# Feature Request: [Feature Name]

## Context
[Why do we need this? What problem does it solve?]

## Proposed Solution
[What should the feature look like?]

## Acceptance Criteria
- [ ] Criteria 1
- [ ] Criteria 2
- [ ] Criteria 3

## Priority: High | Medium | Low

## Notes
[Any edge cases, dependencies, or concerns]
```

---

## Stage 0 关键决策

| 决策 | 原因 |
|------|------|
| 先生成规则文件再构思 | 确保后续每个阶段都有约束，AI 输出不会跑偏 |
| CLAUDE.md 包含数据模型定义 | 让 AI 在 Stage 6 实现时直接知道怎么存取数据 |
| 安全要求写进规则文件 | 而不是事后检查——预防 > 治疗 |
| .cursorrules 包含结构约定 | 防止 AI 自作主张拆分文件或引入依赖 |

## 下一步 → Stage 1: Ideation & Scoping
