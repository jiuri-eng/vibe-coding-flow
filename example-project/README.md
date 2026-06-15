# VibeTodo — Vibe Coding Flow 完整示例项目

> 一个极简但完整的 Todo 应用，用于演示 **vibe-coding-flow 技能的全部 8 个阶段**。
> 从"我想做个待办清单"这个模糊想法开始，到最终交付可运行的 Web 应用。

---

## 项目概览

| 属性 | 值 |
|------|-----|
| 项目名 | **VibeTodo** |
| 类型 | 单页 Web 应用 (SPA) |
| 技术栈 | Vanilla HTML5 + CSS3 + JavaScript (ES6+) |
| 复杂度 | 入门级（~300 行代码） |
| 耗时估算 | 有经验的 AI 辅助开发约 15-20 分钟 |
| 演示目的 | 展示每个阶段的输入 → 处理 → 产出 |

## 为什么选这个项目？

1. **足够简单** — 不需要后端/数据库/构建工具，聚焦流程本身
2. **足够完整** — 包含 CRUD、状态管理、UI 交互、持久化、响应式设计
3. **足够真实** — 不是 "Hello World"，是一个真正有用的应用
4. **每阶段都有产出** — 从 Stage 0 的规则文件到 Stage 7 的最终代码

---

## 用户原始需求（Stage 1 的起点）

> "我想做一个待办清单 App，可以添加任务、标记完成、删除任务，最好能按优先级分类，数据保存在浏览器里不丢失。"

---

## 各阶段产物索引

```
example-project/
├── README.md                          ← 你正在读的这个文件
├── stage-outputs/
│   ├── stage-0-context-setup.md       ← Stage 0: AI 规则文件
│   ├── stage-1-ideation.md            ← Stage 1: 构思与范围
│   ├── stage-2-prd.md                 ← Stage 2: 需求文档
│   ├── stage-3-architecture.md        ← Stage 3: 架构设计
│   │   └── CLAUDE.md                  ← (更新后的上下文文件)
│   ├── stage-4-ui-design.md           ← Stage 4: UI/UX 设计
│   ├── stage-5-todo.md                ← Stage 5: 任务拆解
│   ├── stage-6-implementation.md      ← Stage 6: 实现记录
│   └── stage-7-delivery.md            ← Stage 7: 集成交付
└── src/                               ← 最终实现代码
    ├── index.html
    ├── styles.css
    └── app.js
```

### 快速跳转

- [Stage 0: Context Setup](stage-outputs/stage-0-context-setup.md) — 生成 AI 规则文件
- [Stage 1: Ideation & Scoping](stage-outputs/stage-1-ideation.md) — 确认方向
- [Stage 2: Requirements & PRD](stage-outputs/stage-2-prd.md) — 确认需求
- [Stage 3: Architecture & Tech Stack](stage-outputs/stage-3-architecture.md) — 确认技术方案
- [Stage 4: UI/UX Design](stage-outputs/stage-4-ui-design.md) — 确认视觉设计
- [Stage 5: Task Breakdown & TODO](stage-outputs/stage-5-todo.md) — 确认实施计划
- [Stage 6: Implementation](stage-outputs/stage-6-implementation.md) — 逐步实现
- [Stage 7: Integration & Polish](stage-outputs/stage-7-delivery.md) — 最终交付

---

## 运行最终产物

```bash
# 方式一：直接在浏览器打开
open src/index.html

# 方式二：使用本地服务器（推荐，避免 localStorage CSP 问题）
cd src && python -m http.server 8080
# 然后访问 http://localhost:8080
```

## 功能截图预览

运行 `src/index.html` 后你将看到：

- ✅ 添加新任务（带标题和优先级选择）
- ✅ 标记完成 / 取消完成
- ✅ 删除单个任务
- ✅ 按优先级筛选（高/中/低/全部）
- ✅ 任务计数统计（总数 / 已完成）
- ✅ 数据自动保存到 localStorage
- ✅ 响应式布局（手机 / 平板 / 桌面）

---

## 关键决策记录（Why This Way?）

| 决策 | 选择 | 替代方案 | 理由 |
|------|------|---------|------|
| 技术栈 | Vanilla HTML/CSS/JS | React / Vue / Svelte | 示例项目应零依赖，聚焦流程而非框架 |
| 状态管理 | localStorage | IndexedDB / SQLite | 待办数据量小，localStorage 足够且更简单 |
| CSS 方法 | 自定义属性 + Flexbox/Grid | Tailwind / Bootstrap | 展示完整的设计 token 系统 |
| 构建 | 无构建步骤 | Vite / webpack | 示例应即开即用，无需 npm install |
| 测试 | 手动验证 | Jest / Vitest | 入门级示例，测试作为进阶扩展 |

## 与 Vibe Coding Flow 技能的对应关系

本示例严格遵循 `vibe-coding-flow/SKILL.md` 定义的 8 阶段工作流：

| 阶段 | SKILL.md 定义 | 本示例实践 | 产出的关键学习点 |
|------|--------------|-----------|---------------|
| **0** | Context Setup | 自动生成 CLAUDE.md 等 | 规则文件如何驱动后续所有阶段 |
| **1** | Ideation | MVP vs Full 范围决策 | 学会砍需求，先做核心 |
| **2** | PRD | 结构化需求文档 | 功能需求 + 非功能需求的写法 |
| **3** | Architecture | 文件结构 + 数据模型 + 模块职责 | 架构文档不只是画图，是编码契约 |
| **4** | UI Design | 设计系统 + 组件树 + 线框图描述 | 设计先行减少实现返工 |
| **5** | TODO | 结构化任务列表 + 依赖关系 | 任务拆解的质量决定实现效率 |
| **6** | Implementation | Prompt → Code → Verify → Security Gate | 每个任务的执行节奏和检查标准 |
| **7** | Integration | 全量测试 + 安全审计 + 文档收尾 | 交付不是写完代码就结束 |

---

## 扩展建议（走通基础后的下一步）

如果你想用这个示例继续练习 Vibe Coding：

1. **加后端**: 用 Node.js + Express + JSON File DB 替代 localStorage
2. **加用户系统**: 登录注册 + 多用户待办列表
3. **加动画**: 任务添加/删除的过渡动画
4. **拖拽排序**: 用原生 Drag & Drop API 实现优先级调整
5. **PWA 化**: 加 Service Worker 支持离线使用
6. **部署**: 上传到 GitHub Pages 或 Vercel

每一个扩展都可以重新走一遍 8 阶段流程来规划——这正是 Vibe Coding 的精髓。
