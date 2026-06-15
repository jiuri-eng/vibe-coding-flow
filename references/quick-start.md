# Quick Start — 5 分钟上手 Vibe Coding Flow

> **语言偏好**：技能文档为英文（技术术语国际通用），但 AI 对话支持中/英文，用你最舒服的语言描述想法即可。

## 你需要准备什么

- 一个想法（哪怕只是一个模糊的方向）
- WorkBuddy 或任何支持 AI 对话的编码工具
- 5 分钟读完这份指南，30 分钟跑完第一个项目

---

## 第一步：告诉 AI 你的想法（30 秒）

直接说，不需要任何格式。例如：

```
帮我做一个番茄钟计时器，网页版就行
```

或者：

```
我要一个命令行工具，能扫描代码里的安全问题
```

**关键原则**：描述你想做什么（What），而不是怎么做（How）。AI 会引导你完成后续步骤。

---

## 第二步：路线自动选择（AI 处理）

根据你的项目类型，流程会自动适配：

```
你的想法
  ├── Web 应用 / 网站
  │   → Stage 0→1→2→3→4(UI设计)→5→6→7  ← 完整 8 阶段
  │
  ├── CLI 工具 / 脚本
  │   → Stage 0→1→2→3→5→6→7           ← 跳过 Stage 4 (UI)
  │
  └── "直接帮我做好"
      → Fast Track 模式                   ← 跳过确认，直奔代码
```

---

## 第三步：跟着流程走（30 分钟）

每个阶段 AI 会产出一份文档，**你只需要说"继续"**：

| 阶段 | 产出 | 你做什么 |
|------|------|---------|
| S0 Context | CLAUDE.md / 项目上下文 | 快速扫一眼 |
| S1 Ideation | 项目范围文档 | 确认方向 |
| S2 PRD | 需求文档 | 检查功能列表 |
| S3 Architecture | 技术选型 + 架构 | 确认技术栈 |
| S4 UI (可选) | 设计稿 | 看看配色/布局 |
| S5 TODO | 任务分解 | 确认优先级 |
| S6 Coding | 逐任务写代码 | 每任务自动检查安全/质量 |
| S7 Delivery | 可运行项目 | 拿到最终成果 |

**你的投入**：每个阶段看 1-3 分钟文档，说"继续"或提出修改意见。

---

## 最小化投入路径（Copy-Paste 模板）

如果你想最省力，复制下面这段话直接发：

```
帮我做一个 [你的想法]。走 vibe coding 全流程，每阶段产出一份文档。
Web 应用用 React + TypeScript + Tailwind CSS + Vite。
自动检查代码安全和质量。做完给我最终文件和部署说明。
```

---

## 决策分支速查

### 场景 A：项目很大（预计 > 10K 行代码）

AI 会自动启用 **Token 效率优化**（[详见 token-efficiency.md](token-efficiency.md)）：
- 变量名从 `numberOfActiveUsersInCurrentSession` 缩短为 `nrActUsers`
- 5 个以上重复代码段自动提取函数
- 每 8 次对话检查上下文是否膨胀

### 场景 B：需求不清晰

AI 会进入 **Ideation 阶段**帮你理清：
- 问 3-5 个澄清问题
- 输出 Scope IN / OUT 表格
- 给出 2 个可替代方案

### 场景 C：想跳过某些阶段

直接说 "跳过 Stage 4，不需要 UI 设计"，AI 自动跳过。

### 场景 D：中间想改需求

说 "回到 Stage 1，我要改 XXX"，AI 从该阶段重新开始，保留后续阶段的所有产出作为参考。

---

## 进阶阅读顺序

有 13+ 个 reference 文件不知从何读起？按场景选路径：

### 路径 A：我就是想用，不用懂原理（3 个文件）

1. **本文件 (quick-start.md)** ← 你在这
2. [windows-setup.md](windows-setup.md) — 仅 Windows 用户需要
3. [SKILL.md](../SKILL.md) — 速览 8 阶段摘要就够了

### 路径 B：我想深入理解每个阶段（5 个文件）

1. [SKILL.md](../SKILL.md) — 完整工作流定义
2. [context-engineering.md](context-engineering.md) — Stage 0 基础设施
3. [mcp-integration.md](mcp-integration.md) — Stage 3 工具链扩展
4. [prompt-templates.md](prompt-templates.md) — Stage 5-6 提示词模板
5. [self-check.md](self-check.md) — 全流程质量门控

### 路径 C：我在做大型/团队项目（7 个文件）

1. 先读完路径 B 的 5 个文件
2. [security-checklist.md](security-checklist.md) — 安全门控（MUST-PASS 18 项）
3. [docker-sandbox.md](docker-sandbox.md) — 隔离执行环境
4. [multi-agent-orchestration.md](multi-agent-orchestration.md) — 多代理并行
5. [token-efficiency.md](token-efficiency.md) — Token 压缩策略
6. [ci-cd-integration.md](ci-cd-integration.md) — GitHub Actions 自动化
7. [rule-pack.md](rule-pack.md) — 跨助手规则同步

### 路径 D：我是设计师/前端关注 UI（5 个文件）

1. [SKILL.md](../SKILL.md) Stage 4 部分
2. [design-reverse.md](design-reverse.md) — 从现有产品提取 Design Token
3. [token-efficiency.md](token-efficiency.md) — 分层命名与压缩
4. [prompt-templates.md](prompt-templates.md) — T-3(组件)/T-4(审查)模式

### 路径 E：我关注质量与安全（4 个文件）

1. [self-check.md](self-check.md) — L1-L4 自检体系
2. [security-checklist.md](security-checklist.md) — 安全门控
3. [advanced-qa.md](advanced-qa.md) — Meta-Mentor CPI（成功率 +27%）
4. [ci-cd-integration.md](ci-cd-integration.md) — 自动化质量门控

---

## 核心注意点

| 事项 | 说明 |
|------|------|
| 每阶段结束**必须等待你确认** | 你不会错过任何决策点 |
| Stage 6 每完成一个任务**自动安全检查** | 不会让漏洞代码流入 |
| 最终会输出 **Self-Report Card** | 透明展示所有检查结果 |
| 如果卡住了 | 说 "跳过这个阶段，继续" |
| 不想要文档 | 说 "Fast track，直奔代码" |

---

## 快速参考卡

| 你想... | 告诉 AI |
|---------|--------|
| 开始新项目 | "帮我做 [想法]" |
| 恢复之前项目 | "继续 [项目名]" |
| 只看建议不改代码 | "Plan 模式分析 [想法]" |
| 只写文档不写代码 | "做到 Stage 5 就停" |
| 只写代码不写文档 | "Fast track，直接写代码" |
| 多人协作（多 Agent） | "用多代理模式" |
| 检查代码安全性 | "运行安全审计" |
| 优化 Token 用量 | "启用 Token 压缩" |

---

## 接下来

- 准备开始？跳到 [下一步](#) — 直接给 AI 一个想法就行
- 想深入了解？阅读 [SKILL.md](../SKILL.md) 看完整工作流
- 想看完整案例？打开 `../example-project/`（Web 示例）或 `../example-project-cli/`（CLI 示例）
- Windows 用户？查看 [windows-setup.md](windows-setup.md) 了解 Windows 特有配置
