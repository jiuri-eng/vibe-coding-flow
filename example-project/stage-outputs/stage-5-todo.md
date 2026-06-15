# Stage 5: Task Breakdown & TODO — 产物

## 任务列表

> 使用 Prompt Template T-1 (New Feature) 编写每个任务描述。

---

### Phase 1: 项目骨架 (T-01 ~ T-03)

#### T-01: 创建 index.html 基础结构
- **意图**: 搭建 HTML 骨架，包含语义化标签结构和基本 meta 信息
- **验收标准**:
  - [ ] `<!DOCTYPE html>` + `<html lang="zh-CN">`
  - [ ] `<head>` 含 charset, viewport, title "VibeTodo", link to styles.css
  - [ ] `<body>` 含 `<header>`, `<main>`, 正确的结构嵌套
  - [ ] `<script src="app.js" defer></script>`
  - [ ] 所有内容区域都有语义化的 id/class 占位
- **约束**: 只写结构，不加样式或脚本逻辑
- **参考**: Stage 3 Architecture 文件结构定义
- **复杂度**: 低 (预计 10 min)

#### T-02: 实现 CSS 设计系统和基础布局
- **意图**: 将 Stage 4 的 Design Tokens 转换为实际 CSS，实现整体页面布局
- **验收标准**:
  - [ ] :root 定义全部 design tokens (colors, spacing, typography, radii, shadows, transitions)
  - [ ] CSS Reset / Normalize (box-sizing, margin/padding reset)
  - [ ] Body 背景色、字体、min-height 全屏
  - [ ] Header 布局 (flex: space-between)
  - [ ] Main 容器 (max-width: 720px, 居中, padding)
  - [ ] Input Section 布局
  - [ ] Filter Tabs 布局
  - [ ] Task List 容器
  - [ ] Empty State 样式
- **约束**: Mobile-first; 不使用任何外部资源; BEM-like 命名
- **参考**: Stage 4 UI Design - Design Tokens + 线框图
- **复杂度**: 中 (预计 20 min)

#### T-03: 实现 JavaScript 核心架构 (State + Storage + Render)
- **意图**: 搭建 JS 四大模块骨架，实现数据和渲染的基础能力
- **验收标准**:
  - [ ] `state` 模块: todos[], filter, add/toggle/delete/setFilter/getFilteredTodos/getStats
  - [ ] `storage` 模块: save/load/isAvailable, try/catch 错误处理
  - [ ] `render` 模块: renderApp/createTodoElement/updateCounter/updateFilterTabs/showEmptyState
  - [ ] `events` 模板: init() 绑定事件委托
  - [ ] 初始化流程: storage.load → state.init → renderApp → events.init
  - [ ] 使用 textContent 渲染标题（安全要求）
- **约束**: 纯函数优先; 单向数据流; 每个函数 < 20 行
- **参考**: Stage 3 Architecture - 模块职责 + 数据流图
- **复杂度**: 中高 (预计 30 min)

---

### Phase 2: 核心功能实现 (T-04 ~ T-06)

#### T-04: 实现添加任务功能 (F1)
- **意图**: 用户可以通过输入框 + 优先级选择器添加新任务
- **验收标准**:
  - [ ] 输入框回车或点击添加按钮触发添加
  - [ ] 空内容或纯空格不添加（输入框抖动效果）
  - [ ] 标题自动 trim，限制 200 字符
  - [ ] 新任务出现在列表顶部
  - [ ] 添加后清空输入框，保持焦点
  - [ ] 自动保存到 localStorage
  - [ ] 计数器实时更新
- **约束**: ID 格式: `todo_${Date.now()}_${random}`; 默认优先级 "medium"
- **参考**: PRD F1 功能需求; Prompt Template T-1
- **复杂度**: 中 (预计 15 min)
- **依赖**: T-02, T-03

#### T-05: 实现标记完成和删除功能 (F2, F3)
- **意图**: 用户可以切换任务完成状态和删除任务
- **验收标准**:
  - [ ] 点击 checkbox 或标题区域切换完成状态
  - [ ] 已完成任务: 删除线 + opacity 0.6 + 完成 CSS class
  - [ ] 取消完成: 恢复正常样式
  - [ ] 点击删除按钮移除任务
  - [ ] 删除时有 200ms fadeOut 动画效果
  - [ ] 删除后自动保存并重新渲染
  - [ ] 删除按钮 hover 时显现
- **约束**: 使用事件委托; 删除动画结束后再移除 DOM; textContent 安全
- **参考**: PRD F2/F3 功能需求; Stage 4 交互状态定义
- **复杂度**: 中 (预计 15 min)
- **依赖**: T-03, T-04

#### T-06: 实现优先级筛选和计数功能 (F4, F5)
- **意图**: 按 Tab 筛选不同优先级的任务，显示统计计数
- **验收标准**:
  - [ ] 4 个 Tab: 全部 / 高 / 中 / 低
  - [ ] 点击 Tab 切换筛选条件，列表即时更新
  - [ ] 当前选中 Tab 有高亮样式
  - [ ] 每个 Tab 显示对应优先级的任务数量
  - [ ] Header 区域显示 "共 X 项，已完成 Y 项"
  - [ ] 空筛选结果时显示 empty state 提示
- **约束**: 筛选是纯展示层过滤，不影响实际数据
- **参考**: PRD F4/F5 功能需求; Stage 4 Filter Tabs 设计
- **复杂度**: 中 (预计 15 min)
- **依赖**: T-03, T-04

---

### Phase 3: 打磨与收尾 (T-07 ~ T-09)

#### T-07: 响应式适配与视觉打磨
- **意图**: 确保应用在不同屏幕尺寸下都美观可用
- **验收标准**:
  - [ ] Mobile (320px+): Input 和 priority 竖排，tab 可横滑或换行
  - [ ] Tablet (640px+): Input 和 priority 横排
  - [ ] Desktop (1024px+): 宽屏布局优化，max-width 720px 居中
  - [ ] Task item hover 效果正确
  - [ ] Input focus 状态有视觉反馈
  - [ ] Error shake 动画实现
  - [ ] 过渡动画流畅 (transition tokens)
- **约束**: 仅用 CSS media queries; 不用 JS 做响应式检测
- **参考**: Stage 4 响应式断点策略; Stage 4 交互状态
- **复杂度**: 中 (预计 20 min)
- **依赖**: T-02, T-04, T-05, T-06

#### T-08: Security Gate 与代码审查
- **意图**: 通过安全检查清单，确保无安全隐患
- **验收标准** (from references/security-checklist.md):
  - [ ] **MUST**: 无硬编码密钥/凭证 ✓ (本项目无密钥)
  - [ ] **MUST**: 无 SQL 注入 ✓ (无数据库)
  - [ ] **MUST**: 无命令注入 ✓ (无 exec/spawn)
  - [ ] **MUST**: Auth 检查 N/A ✓ (单用户)
  - [ ] **MUST**: 输入验证 (title 1-200字符, trim) ✅ 待确认
  - [ ] **MUST**: XSS 预防 — 全部使用 textContent ✅ 待确认
  - [ ] **SHOULD**: 无依赖漏洞 ✓ (无 npm 依赖)
  - [ ] **SHOULD**: 错误信息不泄露内部详情 ✅ 待确认
- **操作**: 运行 grep 检查 innerHTML 使用情况
- **约束**: 发现问题必须修复才能进入 Stage 7
- **参考**: references/security-checklist.md MUST-PASS 清单
- **复杂度**: 低 (预计 10 min)
- **依赖**: T-04, T-05, T-06

#### T-09: 集成测试与最终验证
- **意图**: 全流程测试，确保所有功能协同工作
- **验收标准**:
  - [ ] 添加 3 个不同优先级的任务 → 全部正确显示
  - [ ] 切换其中一个完成 → 样式变化 + 计数更新
  - [ ] 删除一个任务 → 从列表消失 + 计数更新
  - [ ] 分别点击 4 个 Tab → 筛选结果正确
  - [ ] 刷新页面 → 所有数据保留
  - [ ] 输入空内容尝试添加 → 被拒绝
  - [ ] 输入超长内容 (>200字) → 被截断
  - [ ] 手机尺寸下布局不乱
  - [ ] 控制台无 JS 错误
  - [ ] README.md 更新完成
- **约束**: 手动测试每个场景；记录发现的 bug 并修复
- **参考**: Stage 2 PRD 验收标准; SKILL.md Final Verification Checklist
- **复杂度**: 中 (预计 15 min)
- **依赖**: T-07, T-08

---

## 依赖关系图

```
T-01 (HTML 结构)
  └─→ T-02 (CSS 基础布局)
       ├─→ T-04 (添加任务) ──┬─→ T-05 (完成/删除) ──┬─→ T-07 (响应式打磨)
       │                     │                       ├─→ T-08 (安全审查)
       └─→ T-03 (JS 架构) ──┤                       │
                            └─→ T-06 (筛选/计数) ─────┘
                                                          └─→ T-09 (集成测试)
```

## 复杂度估算汇总

| 任务 | 复杂度 | 预计耗时 | 累计 |
|------|--------|---------|------|
| T-01 | 低 | 10 min | 10 min |
| T-02 | 中 | 20 min | 30 min |
| T-03 | 中高 | 30 min | 60 min |
| T-04 | 中 | 15 min | 75 min |
| T-05 | 中 | 15 min | 90 min |
| T-06 | 中 | 15 min | 105 min |
| T-07 | 中 | 20 min | 125 min |
| T-08 | 低 | 10 min | 135 min |
| T-09 | 中 | 15 min | **150 min** |

**总预估: ~2.5 小时** (AI 辅助开发可压缩至 15-20 分钟)

## 多代理评估

本项目共 9 个任务，任务间有较强串行依赖，且总体复杂度低。

**结论**: 使用 **Single-Agent Sequential 模式**。
理由:
- 任务数 < 15（仅 9 个）
- 依赖链较深（不能大量并行）
- 总代码量小（~500 行），单个 agent 完全够用
- 切换多代理的协调开销 > 并行收益

（参见 references/multi-agent-orchestration.md 中的选择指南）

## 用户确认

> ✅ 用户确认：任务拆解合理，计划可行，开始实现！

## 下一步 → Stage 6: Implementation
