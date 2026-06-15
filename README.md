# vibe-coding-flow

> **The first systematic 8-stage delivery framework for AI coding agents.**
> From raw idea to running project — making AI agents deliver like senior engineers.

<p align="center">
  <img src="https://img.shields.io/badge/version-v4.3.2-blue?style=flat-square" alt="version" />
  <img src="https://img.shields.io/badge/license-MIT-green?style=flat-square" alt="license" />
  <img src="https://img.shields.io/badge/platforms-WorkBuddy%20%7C%20Cursor%20%7C%20Claude%20Code-orange?style=flat-square" alt="platforms" />
  <img src="https://img.shields.io/badge/stages-8-blueviolet?style=flat-square" alt="stages" />
  <br/>
  <img src="https://img.shields.io/badge/zero%20dependencies-important?style=flat-square" alt="zero deps" />
  <img src="https://img.shields.io/badge/self--check-L1--L4-success?style=flat-square" alt="self-check" />
</p>

<br/>

<p align="center">
  <b>业界首个面向 AI 编程代理的完整 8 阶段工作流框架</b><br/>
  <i>从一句想法到可运行项目，让 AI 代理像资深工程师一样系统性交付</i>
</p>

<p align="center">
  <a href="#快速开始">快速开始</a> ·
  <a href="#核心特性">核心特性</a> ·
  <a href="#8-阶段详解">8 阶段</a> ·
  <a href="#参考模块索引18-个">参考模块</a> ·
  <a href="https://github.com/jiuri-eng/vibe-coding-flow/issues">报告问题</a>
</p>

<br/>

> **English Abstract** — `vibe-coding-flow` is a platform-agnostic skill framework that guides AI coding agents through a complete 8-stage software delivery workflow (Idea → PRD → Architecture → Design → Tasks → Code → Deliver). Features include: 4-level self-check gates (L1-L4), token budget management with session handoff at 95% threshold, multi-agent orchestration, and built-in security scanning. Supports WorkBuddy, Cursor, Claude Code, Codex, Windsurf, and more. Zero dependencies — pure markdown + prompt patterns.

<br/>

---

<h2 align="center">🌊 核心价值：填补 AI 编程的系统性空白</h2>

<p align="center">
<table>
<tr>
<td width="33%" align="center">
  <b>🎯 平台无关</b><br/>
  同一套工作流，适配 5+ 主流 AI 编程代理
</td>
<td width="33%" align="center">
  <b>🔒 内置自检</b><br/>
  L1-L4 四级门控，每层都有质量保障
</td>
<td width="33%" align="center">
  <b>🚀 规模感知</b><br/>
  S/M/L/XL 四级路由，小项目快、大项目稳
</td>
</tr>
</table>
</p>

<br/>

## 适用人群

| 你是... | vibe-coding-flow 能帮你... |
|---------|----------------------|
| **独立开发者** | 用 AI 代理从想法直接交付完整项目，不再只得到「代码片段」 |
| **产品/设计师** | 用结构化 PRD + UI 设计文档与 AI 对话，产出可验证、可交接 |
| **技术团队 Lead** | 统一团队成员使用 AI 代理的交付标准，减少代码 Review 成本 |
| **AI 编程研究者** | 基于 18 个参考模块快速定制适合自己场景的工作流 |

<br/>

## 为什么需要 vibe-coding-flow？

> AI 编程代理很强大，但缺乏**系统性约束**。
> 它们擅长写代码，却不擅长**管理整个软件生命周期**。

| 痛点 | vibe-coding-flow 的解法 |
|------|----------------------|
| AI 写代码容易「跑偏」，缺乏阶段性验收 | **8 阶段门控**：每阶段产出文档，必须确认才进入下一阶段 |
| 大型项目上下文窗口撑爆 | **Context Budget**：80% 预警、95% 强制交接，支持多会话续跑 |
| 不同 AI 代理行为不一致 | **平台自适应**：自动检测 WorkBuddy/Cursor/Claude Code 等，生成对应规则文件 |
| AI 生成的代码缺乏安全审查 | **Security Gates**：提交前自动扫描密钥泄露、注入风险 |
| 项目规模差异大，一套流程不适用 | **规模路由**：S 级（小工具）走 Fast Track，XL 级（大系统）自动规划多代理协作 |

<br/>

## 工作流全景

```
                    ┌──────────────────────────────────────────────────────┐
                    │                vibe-coding-flow 8 阶段              │
                    └──────────────────────────────────────────────────────┘

  阶段 0          阶段 1          阶段 3          阶段 5          阶段 7
  Context ─────► Ideation ─────► Architecture ─────► Task ─────► Delivery
  Setup          & Scoping       & Tech Stack    Breakdown      (交付)
     │              │              │              │
     ▼              ▼              ▼              ▼
  CLAUDE.md    01-ideation   03-architecture  05-todo      README
  .cursorrules      │              │              │           deploy docs
     │              ▼              ▼              ▼
     └─────────► 阶段 2        阶段 4         Source Code
                   PRD &        UI/UX Design     │
                   Reqs          (CLI 跳过)      │
                                    │              │
                                    ▼              ▼
                                04-ui-design   Stage 6: Implementation
                                                  (编码 + 每任务自检)
```

<br/>

## 核心特性

| 特性 | 说明 | 独特价值 |
|------|------|---------|
| **平台自适应检测** | 自动识别 WorkBuddy/Cursor/Claude Code/Codex/Gemini，生成对应规则文件 | 支持 5+ 主流平台 |
| **项目规模路由** | S/M/L/XL 四级，S 级自动跳过确认、轻量文档；XL 级自动规划多会话 | ✅ 兼顾效率与严谨 |
| **自检系统 L1-L4** | 阶段门控 + 任务门控 + 上下文检查点 + 反模式监控 | ✅ 四层质量保障 |
| **上下文预算管理** | Token 预算分级，80% 预警生成摘要卡，95% 强制生成交接包 | ✅ 解决上下文窗口瓶颈 |
| **会话交接包** | 自包含交接文档，新会话加载后可无缝续跑 | ✅ 支持无限规模项目 |
| **多代理编排** | 并行专家团队模板（前端/后端/测试/DevOps 角色） | ✅ 大型项目提速 3-5x |
| **安全门控** | 提交前扫描：密钥泄露、SQL 注入、XSS、依赖漏洞 | ✅ 内置安全左移 |
| **13+ 提示词模板** | 功能开发 / 缺陷修复 / 代码审查 / 调试 / 测试等成熟模式 | ✅ 开箱即用 |

<br/>

## 支持平台

| 平台 | 状态 | 规则文件 |
|------|:---:|---------|
| **WorkBuddy** | ✅ 完整支持 | `CLAUDE.md` + Skill 加载 |
| **Cursor** | ✅ 完整支持 | `.cursorrules` |
| **Claude Code** | ✅ 完整支持 | `CLAUDE.md` |
| **Codex CLI** | ✅ 完整支持 | `AGENTS.md` |
| **Windsurf** | ✅ 完整支持 | `.windsurfrules` |
| **Gemini CLI** | ✅ 完整支持 | 对话式引导 |
| **GitHub Copilot** | 🔜 计划中 | — |

<br/>

## 快速开始

### WorkBuddy 用户

```bash
# 方式一：一句话安装（推荐）
/install-skill vibe-coding-flow

# 方式二：手动克隆
git clone https://github.com/jiuri-eng/vibe-coding-flow.git ~/.workbuddy/skills/vibe-coding-flow/
```

### Cursor / Windsurf / Claude Code 用户

将 `SKILL.md` 的完整内容复制到项目的规则文件中：

| 平台 | 规则文件 |
|------|---------|
| Cursor | `.cursorrules` |
| Windsurf | `.windsurfrules` |
| Claude Code | `CLAUDE.md` |
| Codex CLI | `AGENTS.md` |

<br/>

## 8 阶段详解

| 阶段 | 名称 | 核心产出 | 自检门控 |
|:---:|---------|---------|---------|
| **S0** | Context Setup | `CLAUDE.md` / `.cursorrules` / `INITIAL.md` | L1-0：文件存在、大小合规、安全段落完整 |
| **S1** | Ideation & Scoping | `docs/01-ideation.md`（一句话定义、问题陈述、范围 IN/OUT） | L1-1：意图保留、排除项列出、标准可衡量 |
| **S2** | PRD | `docs/02-prd.md`（用户故事、功能需求 + 验收标准、非功能需求） | L1-2：全章节完整、每项功能有 AC、无孤立需求 |
| **S3** | Architecture | `docs/03-architecture.md`（技术栈、系统架构、数据模型、决策记录） | L1-3：技术栈复杂度匹配、数据模型覆盖全部 PRD 实体 |
| **S4** | UI/UX Design | `docs/04-ui-design.md`（信息架构、组件树、Design Token、线框图）| L1-4：Token 为具体值、全部 PRD 功能有 UI 对应 |
| **S5** | Task Breakdown | `docs/05-todo.md`（有序任务列表、依赖 DAG、复杂度估算） | L1-5：任务原子化、DAG 无环、全部功能编号覆盖 |
| **S6** | Implementation | 源代码（逐任务循环：意图→模板→上下文→生成→测试→门控→提交） | **L2 任务门控**（安全 + 质量 + 完整性）每任务必过 |
| **S7** | Delivery | `README.md` + 部署说明 + 最终自检报告 | **L1-7 交付门控** + **L3 全量对齐** + **L4 反模式终扫** |

### 自检系统说明

```
L1  阶段门控      每阶段产出必须验收通过才进入下一阶段
L2  任务门控      每任务完成后：安全扫描 → 质量检查 → 完整性验证
L2.5  上下文检查点  每 5 个任务（XL 项目每任务）：预算检查 → 摘要卡 → 交接包
L3  跨阶段对齐      PRD→架构→代码全覆盖矩阵
L4  反模式监控      全程监控：死循环、上下文坍塌、提示词债务、技术债、漂移
```

<br/>

## 示例项目

### VibeTodo（Web App）

完整 8 阶段演示，技术栈：原生 HTML5 + CSS3 + Vanilla JS（零依赖）

```
example-project/
├── src/
│   ├── index.html       # 主页面
│   ├── styles.css       # 样式（响应式）
│   └── app.js          # 应用逻辑
├── stage-outputs/       # 各阶段完整产出文档
│   ├── stage-0-context-setup.md
│   ├── stage-1-ideation.md
│   ├── ...
│   └── stage-7-delivery.md
└── tests/              # 测试用例
```

### VibeCLI（CLI Tool）

7 阶段演示（跳过 S4 UI 设计），技术栈：Python + `rich` CLI 库

```
example-project-cli/
├── src/vibecli.py      # CLI 入口
├── stage-outputs/       # 各阶段完整产出文档
└── tests/              # pytest 测试用例
```

<br/>

## 参考模块索引（18 个）

### 核心模块（自动加载）

| 文件 | 用途 |
|------|------|
| `quick-start.md` | 新手 5 分钟快速上手指南 |
| `context-engineering.md` | Stage 0 方法论：自动生成项目上下文 |
| `mcp-integration.md` | MCP 服务器配置（Context7、Serena 等） |
| `prompt-templates.md` | 13+ 提示词模板（功能/缺陷/审查/调试/测试） |
| `security-checklist.md` | 提交前安全门控、漏洞模式、密钥管理 |
| `multi-agent-orchestration.md` | 3 种并行模式 + 角色模板 + WorkBuddy Agent 示例 |
| `self-check.md` | L1-L4 自检系统完整定义、决策矩阵、报告格式 |
| `context-budget.md` | v4.3 Token 预算分级、各阶段分配、强制缓解触发条件 |
| `session-handoff.md` | v4.3 交接包格式、技能加载决策矩阵、续跑蓝图 |
| `advanced-qa.md` | Module A：Meta-Mentor CPI（链式模式中断，成功率 +27%） |
| `token-efficiency.md` | 8 级上下文压缩策略、分层命名、窗口管理 |

### 高级模块（按需加载）

| 文件 | 触发条件 |
|------|---------|
| `docker-sandbox.md` | 用户明确要求隔离执行 / 不可信代码 |
| `windows-setup.md` | 用户在 Windows 上需要 Docker/WSL2/MCP 路径帮助 |
| `rule-pack.md` | 跨机器 / 跨团队同步编码规则 |
| `design-reverse.md` | 需要匹配现有产品的视觉风格 |
| `ci-cd-integration.md` | Stage 7 需要配置 GitHub Actions |

<br/>

## 与其他方案的对比

| 维度 | vibe-coding-flow | 纯提示词工程 | Ponytail | Cursor Rules |
|------|-----------------|-------------|-----------|--------------|
| **完整生命周期管理** | ✅ 8 阶段覆盖全流程 | ❌ 单轮对话 | ❌ 仅约束编码行为 | ❌ 仅编码规范 |
| **平台无关** | ✅ 5+ 平台 | ⚠️ 部分 | ✅ 13 种 | ❌ 平台绑定 |
| **自检系统** | ✅ L1-L4 四级 | ❌ 无 | ⚠️ 依赖人工 | ❌ 无 |
| **大项目支持** | ✅ 上下文预算 + 会话交接 | ❌ 易撑爆 | ❌ 无 | ❌ 无 |
| **安全门控** | ✅ 内置 | ⚠️ 需手动 | ⚠️ 部分 | ⚠️ 需配置 |
| **多代理编排** | ✅ 完整方案 | ❌ 无 | ❌ 无 | ❌ 无 |

<br/>

## 贡献

欢迎提交 Issue 和 Pull Request！

- **Bug 报告**：使用 [GitHub Issues](https://github.com/jiuri-eng/vibe-coding-flow/issues)
- **功能建议**：同样通过 Issues，标签选 `enhancement`
- **提交 PR**：请确保更新对应的 `references/` 模块文档

<br/>

## 许可证

[MIT License](LICENSE) — 最短能用的许可证，自由使用、修改、分发。

<br/>

## ⭐ Star History

如果这个项目对你有帮助，欢迎 Star 支持！

[![Star History Chart](https://api.star-history.com/svg?repos=jiuri-eng/vibe-coding-flow)](https://star-history.com/#jiuri-eng/vibe-coding-flow)

<br/>

## ☕ 打赏与赞助

如果 `vibe-coding-flow` 在你的项目中派上了用场，或者它的某个模块帮你节省了时间——

一杯咖啡的打赏，就是对我持续维护和迭代的最大鼓励。每一份支持都会被认真对待。

<p align="center">
  <table>
  <tr>
  <td align="center" width="45%">
    <b>微信支付</b><br/>
    <img src="assets/wechat-pay.jpg" width="200" alt="微信支付" />
  </td>
  <td align="center" width="45%">
    <b>支付宝</b><br/>
    <img src="assets/alipay.jpg" width="200" alt="支付宝" />
  </td>
  </tr>
  </table>
</p>

<br/>

## 联系方式

- **QQ**：2492656146
- **GitHub**：[@jiuri-eng](https://github.com/jiuri-eng)
- **仓库**：[github.com/jiuri-eng/vibe-coding-flow](https://github.com/jiuri-eng/vibe-coding-flow)

<br/>

---

<details>
<summary><b>📚 完整文档索引（点击展开）</b></summary>

### 阶段文档模板

各阶段产出文档的完整模板均在 `references/` 中定义，可直接复制使用：

- `context-engineering.md` → S0 模板
- `prompt-templates.md` → S2 PRD 模板（T-12 模式）
- `tech-stacks.md` → S3 技术栈推荐
- `self-check.md` → 全阶段自检报告格式

### 自检报告示例

完整项目的自检报告格式参见 `example-project/stage-outputs/stage-7-delivery.md` 中的「Self-Report Card」表格。

</details>

<p align="center">
  <i>让 AI 代理不再「写代码」，而是「交付项目」。</i><br/>
  <b>vibe-coding-flow</b> — Systematic AI-assisted software delivery.
</p>
