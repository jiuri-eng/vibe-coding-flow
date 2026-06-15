# Stage 4: UI/UX Design — 产物

## 设计系统 (Design Tokens)

### Color Palette (CSS Custom Properties)

```css
:root {
  /* === Primary Colors === */
  --color-primary: #6366f1;         /* Indigo - 主色调 */
  --color-primary-hover: #4f46e5;
  --color-primary-light: #eef2ff;

  /* === Priority Colors === */
  --color-high: #ef4444;            /* Red - 高优先级 */
  --color-high-bg: #fef2f2;
  --color-medium: #f59e0b;          /* Amber - 中优先级 */
  --color-medium-bg: #fffbeb;
  --color-low: #3b82f6;             /* Blue - 低优先级 */
  --color-low-bg: #eff6ff;

  /* === Neutral Colors === */
  --color-bg: #f8fafc;              /* Page background */
  --color-surface: #ffffff;         /* Card/container background */
  --color-border: #e2e8f0;
  --color-text: #1e293b;
  --color-text-secondary: #64748b;
  --color-text-muted: #94a3b8;

  /* === Status Colors === */
  --color-success: #22c55e;
  --color-danger: #ef4444;

  /* === Typography === */
  --font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  --font-size-xs: 0.75rem;    /* 12px */
  --font-size-sm: 0.875rem;   /* 14px */
  --font-size-base: 1rem;     /* 16px */
  --font-size-lg: 1.125rem;   /* 18px */
  --font-size-xl: 1.5rem;     /* 24px */
  --font-weight-normal: 400;
  --font-weight-medium: 500;
  --font-weight-bold: 600;

  /* === Spacing Scale === */
  --space-xs: 0.25rem;   /* 4px */
  --space-sm: 0.5rem;    /* 8px */
  --space-md: 1rem;      /* 16px */
  --space-lg: 1.5rem;    /* 24px */
  --space-xl: 2rem;      /* 32px */

  /* === Radii === */
  --radius-sm: 0.375rem; /* 6px */
  --radius-md: 0.5rem;   /* 8px */
  --radius-lg: 0.75rem;  /* 12px */
  --radius-full: 9999px;

  /* === Shadows === */
  --shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.05);
  --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1);

  /* === Transitions === */
  --transition-fast: 150ms ease;
  --transition-normal: 200ms ease;
  --transition-slow: 300ms ease;
}
```

## 组件树

```
<App>
  <Header>
    <Logo /> "VibeTodo"
    <TaskCounter />
  </Header>

  <main>
    <InputSection>
      <TextInput placeholder="添加新任务..." />
      <PrioritySelector>
        <PriorityOption value="high" label="高" />
        <PriorityOption value="medium" label="中" selected />
        <PriorityOption value="low" label="低" />
      </PrioritySelector>
      <AddButton>+ 添加</AddButton>
    </InputSection>

    <FilterTabs>
      <Tab active count={total}>全部</Tab>
      <Tab count={highCount}>高</Tab>
      <Tab count={medCount}>中</Tab>
      <Tab count={lowCount}>低</Tab>
    </FilterTabs>

    <TaskList>
      <!-- Task Item (repeat for each filtered todo) -->
      <TaskItem priority={priority} completed={completed}>
        <Checkbox checked={completed} />
        <Title>{title}</Title>
        <PriorityBadge>{priorityLabel}</PriorityBadge>
        <DeleteButton>×</DeleteButton>
      </TaskItem>

      <!-- Empty State -->
      <EmptyState>还没有任务，添加一个吧！</EmptyState>
    </TaskList>
  </main>
</App>
```

## 线框图描述

### Mobile (< 640px)

```
┌─────────────────────┐
│  VibeTodo            │
│  共 3 项，已完成 1 项 │
├─────────────────────┤
│ ┌─────────────────┐ │
│ │ 添加新任务...    │ │
│ └─────────────────┘ │
│ [高] [中✓] [低] [+] │
├─────────────────────┤
│ [全部] [高] [中] [低]│
├─────────────────────┤
│ ☐ 买牛奶      [高] ×│
│ ☐ 写周报      [中] ×│
│ ☑ 学习 Vibe   [低] ×│
│                     │
│ ─────────────────── │
│ 还没有更多任务了      │
└─────────────────────┘
```

### Desktop (>= 1024px)

```
┌──────────────────────────────────────────────────┐
│  VibeTodo                          共 3 项，已完成 1 项 │
├──────────────────────────────────────────────────┤
│                                                    │
│  ┌──────────────────────────────────┐ ┌────┐      │
│  │ 添加新任务...                     │ │高 ▼│      │
│  └──────────────────────────────────┘ └────┘      │
│                                        [＋ 添加]    │
├──────────────────────────────────────────────────┤
│  [全部 (3)]   [高 (1)]   [中 (1)]   [低 (1)]       │
├──────────────────────────────────────────────────┤
│                                                    │
│  ☐  买牛奶                           🔴 高     🗑️  │
│  ─────────────────────────────────────────────── │
│  ☐  写周报                           🟠 中     🗑️  │
│  ─────────────────────────────────────────────── │
│  ☑  学习 Vibe Coding                🔵 低     🗑️  │
│  ─────────────────────────────────────────────── │
│                                                    │
└──────────────────────────────────────────────────┘
```

## 交互状态定义

### Task Item 状态

| 状态 | 视觉表现 | CSS 类名 |
|------|---------|----------|
| Default (未完成) | 正常文字，正常透明度 | `.task-item` |
| Hover | 左侧出现淡色背景条，删除按钮显现 | `.task-item:hover` |
| Completed (已完成) | 文字加删除线，颜色变淡 (opacity: 0.6) | `.task-item.completed` |
| Deleting (删除中) | 向左滑出 + fadeOut (200ms) | `.task-item.deleting` |
| Empty (空列表) | 显示提示文案，居中，浅灰色 | `.empty-state` (visible) |

### Button 状态

| 元素 | Normal | Hover | Disabled |
|------|--------|-------|----------|
| Add Button | 主色调背景，白字 | 深一点的主色调 | 灰色，不可点击 (输入为空时) |
| Delete Button | 隐藏 (opacity: 0) | 显现 (opacity: 1)，红色 | — |
| Tab (未选中) | 透明背景，灰色文字 | 浅灰背景 | — |
| Tab (选中) | 主色调背景，白字，底部高亮条 | — | — |

### Input 状态

| 状态 | 表现 |
|------|------|
| Normal | 边框 var(--color-border) |
| Focus | 边框 var(--color-primary)，外发光阴影 |
| Error (空提交) | 边框红色，抖动动画 |
| Placeholder | "添加新任务..." |

## 响应式断点策略

```css
/* Mobile first approach */

/* Base: 320px+ (mobile) */
/* Input + priority on separate rows */
/* Filter tabs: horizontal scroll or wrap */

/* Tablet: 640px+ */
/* Input and priority on same row */
/* Max-width container centered */

/* Desktop: 1024px+ */
/* Input section: input wide, selector compact, button inline */
/* Task items wider with more padding */
/* Optional: two-column layout for future */

/* Large desktop: 1440px+ */
/* Container max-width: 720px centered */
/* No full-width stretch */
```

## 设计原则

1. **清晰优先**: 信息层级分明——标题 > 优先级 > 操作按钮
2. **操作可见**: 重要操作（添加、切换完成）总是可达；破坏性操作（删除）hover 才显现
3. **即时反馈**: 每个操作都有视觉反馈（颜色变化、动画、数字更新）
4. **宽容设计**: 输入框容错（空格、超长文本）；误删可通过清除 localStorage 恢复
5. **移动友好**: 大触控目标 (min 44px)，避免悬停依赖的交互

## 用户确认

> ✅ 用户确认：UI 设计清爽美观，布局合理，可以实现。

## 下一步 → Stage 5: Task Breakdown & TODO
