# Stage 3: Architecture & Tech Stack — 产物

## 技术栈确认

| 类别 | 选择 | 版本要求 | 理由 |
|------|------|---------|------|
| 标记语言 | HTML5 | — | 语义化标签，无框架依赖 |
| 样式 | CSS3 | — | 自定义属性做设计系统，Flexbox + Grid 布局 |
| 脚本 | JavaScript | ES6+ (ES2015+) | 原生模块模式，无需编译 |
| 构建 | 无 | — | 直接打开 HTML 文件即可运行 |
| 包管理 | 无 | — | 零外部依赖 |
| 存储 | localStorage API | — | 浏览器原生，JSON 序列化 |
| 图标/符号 | Unicode + CSS 伪元素 | — | 零依赖 |

## 系统架构

```
┌──────────────────────────────────────────────┐
│                   index.html                  │
│  ┌────────────────────────────────────────┐  │
│  │              styles.css                 │  │
│  │  :root { design tokens }               │  │
│  │  .layout {} / .component {}            │  │
│  │  @media queries (responsive)           │  │
│  └────────────────────────────────────────┘  │
│  ┌────────────────────────────────────────┐  │
│  │               app.js                    │  │
│  │  ┌─────────┬──────────┬───────────┐   │  │
│  │  │  State  │  Render  │  Storage  │   │  │
│  │  │ Manager │  Engine  │  Adapter  │   │  │
│  │  └────┬────┴─────┬────┴─────┬─────┘   │  │
│  │       │          │          │         │  │
│  │  Event Handlers ←── User Actions        │  │
│  └────────────────────────────────────────┘  │
│                      │                        │
│               localStorage                   │
│              (vibetodo-todos)                 │
└──────────────────────────────────────────────┘
```

## 文件结构

```
src/
├── index.html      # 页面结构 (~80 行)
├── styles.css      # 所有样式 (~250 行)
└── app.js          # 所有逻辑 (~200 行)
```

## 数据模型

```typescript
// Todo 对象结构
interface Todo {
  id: string;            // 唯一标识，格式: 'todo_<timestamp>_<random>'
  title: string;         // 任务标题，1-200 字符
  priority: Priority;    // 优先级枚举
  completed: boolean;    // 完成状态
  createdAt: string;     // 创建时间 ISO 格式
  completedAt: string | null; // 完成时间，未完成时为 null
}

type Priority = 'high' | 'medium' | low';

// 应用状态（内存中的完整状态）
interface AppState {
  todos: Todo[];           // 全部任务列表
  filter: FilterType;      // 当前筛选条件
}

type FilterType = 'all' | 'high' | 'medium' | 'low';
```

## 模块职责划分（app.js 内部逻辑分组）

### State Manager (`state` 模块)

```javascript
// 职责: 维护应用状态的唯一数据源
const state = {
  todos: [],       // Todo[]
  filter: 'all',   // FilterType

  // 方法:
  // - addTodo(title, priority) → void
  // - toggleTodo(id) → void
  // - deleteTodo(id) → void
  // - setFilter(filter) → void
  // - getFilteredTodos() → Todo[]
  // - getStats() => { total, completed }
};
```

### Render Engine (`render` 模块)

```javascript
// 职责: 根据 state 渲染 UI（纯渲染，不修改 state）
const render = {
  // - renderApp() → 重新渲染整个应用
  // - createTodoElement(todo) → DOM Element (使用 textContent!)
  // - updateCounter(stats) → 更新计数显示
  // - updateFilterTabs(filter, statsByPriority) → 更新 tab 高亮和计数
  // - showEmptyState() / hideEmptyState()
};
```

### Storage Adapter (`storage` 模块)

```javascript
// 职责: localStorage 的读写，带错误处理
const storage = {
  // KEY = 'vibetodo-todos'
  // - save(todos: Todo[]) → boolean (成功/失败)
  // - load() → Todo[] | null (损坏返回 null)
  // - isAvailable() → boolean
};
```

### Event Handler (`events` 模块)

```javascript
// 职责: 用户交互的事件委托
const events = {
  // - init() → 绑定所有事件监听
  // 使用事件委托: 在父容器上监听，通过 event.target 识别具体操作
  //
  // 事件映射:
  // form@submit     → addTodo
  // list@click      → toggleTodo (checkbox) 或 deleteTodo (delete btn)
  // tabs@click      → setFilter
};
```

## 数据流图

```
User Action
    │
    ▼
Event Handler (捕获用户操作，提取意图)
    │
    ▼
State Manager (更新内存状态)
    │
    ├──→ Storage Adapter (持久化到 localStorage)
    │
    ▼
Render Engine (根据新状态重新渲染 DOM)
    │
    ▼
Browser Display (用户看到变化)
```

**关键原则**: 单向数据流。事件 → 状态 → 渲染。永远不直接操作 DOM 来反映业务状态变化。

## 关键技术决策记录

| # | 决策 | 替代方案 | 选择理由 |
|---|------|---------|----------|
| TD1 | 不用框架 | React/Vue/Svelte | 示例项目应零依赖；300 行代码不需要框架 |
| TD2 | 事件委托 | 每个 element 绑 listener | 减少内存占用；动态添加的任务自动有事件响应 |
| TD3 | textContent 非 innerHTML | innerHTML 方便但危险 | PRD 要求 XSS 安全 |
| TD4 | ID 用时间戳+随机数 | UUID 库 | 零依赖；碰撞概率可接受 |
| TD5 | 全量重渲染 vs 局部更新 | Virtual DOM / 绑定更新 | 列表项 < 1000 时全量重渲染性能足够 |

## 更新后的 CLAUDE.md 片段（Stage 3 补充）

在 Stage 0 生成的 CLAUDE.md 中补充架构细节：

```markdown
## Architecture Details (Added Stage 3)
- **Data flow**: Unidirectional — Events → State → Render → Display
- **Pattern**: Module-level closures (State/Render/Storage/Events), not classes
- **Event delegation**: Single listener on task-list container
- **ID format**: `todo_${Date.now()}_${Math.random().toString(36).slice(2, 8)}`
- **Render strategy**: Full re-render of task list on every state change
```

## MCP 配置决策

对于 VibeTodo 这个项目规模：
- **Context7**: 不需要。项目只使用 Web API（localStorage），没有第三方库。
- **Serena**: 不需要。项目只有 3 个文件，代码搜索不是瓶颈。
- **结论**: 本项目跳过 MCP 配置。（MCP 在大型项目中才真正有价值）

## 用户确认

> ✅ 用户确认：技术方案清晰，文件结构简洁，可以开始设计 UI。

## 下一步 → Stage 4: UI/UX Design
