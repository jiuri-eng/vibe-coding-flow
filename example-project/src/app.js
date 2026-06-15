/**
 * VibeTodo — Application Logic
 *
 * Architecture: Module-level closures with unidirectional data flow
 * Pattern: Events → State → Render → Display
 * Security: All user content rendered via textContent (no innerHTML)
 */

;(function () {
  'use strict';

  // ================================================================
  // Constants
  // ================================================================
  const STORAGE_KEY = 'vibetodo-todos';
  const MAX_TITLE_LENGTH = 200;
  const DELETE_ANIMATION_MS = 200;

  // ================================================================
  // State Manager (Single source of truth)
  // ================================================================
  const state = {
    todos: [],
    filter: 'all',

    addTodo(title, priority) {
      const todo = {
        id: generateId(),
        title: title.slice(0, MAX_TITLE_LENGTH),
        priority,
        completed: false,
        createdAt: new Date().toISOString(),
        completedAt: null,
      };
      this.todos.unshift(todo); // 新任务插入顶部
    },

    toggleTodo(id) {
      const todo = this.todos.find((t) => t.id === id);
      if (!todo) return;
      todo.completed = !todo.completed;
      todo.completedAt = todo.completed ? new Date().toISOString() : null;
    },

    deleteTodo(id) {
      this.todos = this.todos.filter((t) => t.id !== id);
    },

    setFilter(filter) {
      this.filter = filter;
    },

    getFilteredTodos() {
      if (this.filter === 'all') return [...this.todos];
      return this.todos.filter((t) => t.priority === this.filter);
    },

    getStats() {
      const total = this.todos.length;
      const completed = this.todos.filter((t) => t.completed).length;
      const byPriority = {
        high: this.todos.filter((t) => t.priority === 'high').length,
        medium: this.todos.filter((t) => t.priority === 'medium').length,
        low: this.todos.filter((t) => t.priority === 'low').length,
      };
      return { total, completed, ...byPriority };
    },
  };

  // ================================================================
  // ID Generator
  // ================================================================
  function generateId() {
    return (
      'todo_' +
      Date.now().toString(36) +
      '_' +
      Math.random().toString(36).slice(2, 8)
    );
  }

  // ================================================================
  // Storage Adapter (localStorage with error handling)
  // ================================================================
  const storage = {
    save(todos) {
      try {
        localStorage.setItem(STORAGE_KEY, JSON.stringify(todos));
        return true;
      } catch (e) {
        console.warn('[VibeTodo] 无法保存到 localStorage:', e.message);
        showStorageWarning();
        return false;
      }
    },

    load() {
      try {
        const raw = localStorage.getItem(STORAGE_KEY);
        if (!raw) return null;
        const parsed = JSON.parse(raw);
        if (!Array.isArray(parsed)) return null;
        return parsed;
      } catch (e) {
        console.warn('[VibeTodo] 数据损坏，从空白开始:', e.message);
        return null;
      }
    },

    isAvailable() {
      try {
        const test = '__vibetodo_test__';
        localStorage.setItem(test, test);
        localStorage.removeItem(test);
        return true;
      } catch (e) {
        return false;
      }
    },
  };

  // ================================================================
  // Priority Label Map
  // ================================================================
  const PRIORITY_LABELS = {
    high: '高',
    medium: '中',
    low: '低',
  };

  // ================================================================
  // Render Engine (Pure rendering — never modifies state)
  // ================================================================
  const render = {
    renderApp() {
      this.renderList();
      this.updateCounter(state.getStats());
      this.updateFilterTabs(state.getStats());
      this.toggleEmptyState();
    },

    renderList() {
      const listEl = document.querySelector('.task-list');
      const filtered = state.getFilteredTodos();

      // Clear and rebuild (acceptable for < 1000 items)
      listEl.innerHTML = '';

      filtered.forEach((todo) => {
        listEl.appendChild(this.createTodoElement(todo));
      });
    },

    /**
     * Create a DOM element for a single todo item.
     * SECURITY: Uses textContent for title — NEVER innerHTML.
     */
    createTodoElement(todo) {
      const li = document.createElement('li');
      li.className = 'task-item' + (todo.completed ? ' completed' : '');
      li.dataset.id = todo.id;

      // Checkbox
      const checkbox = document.createElement('input');
      checkbox.type = 'checkbox';
      checkbox.className = 'checkbox';
      checkbox.checked = todo.completed;
      checkbox.setAttribute('aria-label', '标记' + (todo.completed ? '未完成' : '完成'));

      // Title (SECURITY: textContent prevents XSS)
      const title = document.createElement('span');
      title.className = 'task-title';
      title.textContent = todo.title; // ← 安全：自动转义 HTML

      // Priority Badge
      const badge = document.createElement('span');
      badge.className = 'priority-badge ' + todo.priority;
      badge.textContent = PRIORITY_LABELS[todo.priority];

      // Delete Button
      const deleteBtn = document.createElement('button');
      deleteBtn.className = 'delete-btn';
      deleteBtn.textContent = '\u00D7'; // × symbol
      deleteBtn.setAttribute('aria-label', '删除任务');

      li.append(checkbox, title, badge, deleteBtn);
      return li;
    },

    updateCounter(stats) {
      const counter = document.querySelector('.task-counter');
      counter.textContent =
        '共 ' + stats.total + ' 项，已完成 ' + stats.completed + ' 项';
    },

    updateFilterTabs(stats) {
      const tabs = document.querySelectorAll('.filter-tab');
      tabs.forEach(function (tab) {
        const tabFilter = tab.dataset.filter;
        tab.classList.toggle('active', tabFilter === state.filter);
        tab.setAttribute(
          'aria-selected',
          String(tabFilter === state.filter)
        );

        var count;
        if (tabFilter === 'all') {
          count = stats.high + stats.medium + stats.low;
        } else {
          count = stats[tabFilter] || 0;
        }
        tab.querySelector('.tab-count').textContent = '(' + count + ')';
      });
    },

    toggleEmptyState() {
      const emptyState = document.querySelector('.empty-state');
      const hasItems = state.getFilteredTodos().length > 0;
      emptyState.classList.toggle('visible', !hasItems);
    },
  };

  // ================================================================
  // Event Handlers (Delegation pattern — single listener per zone)
  // ================================================================

  /** Handle form submit → Add Todo */
  function handleSubmit(e) {
    e.preventDefault();

    var input = document.getElementById('todo-input');
    var prioritySelect = document.getElementById('priority-select');
    var title = input.value.trim();

    // Validation: reject empty input
    if (!title) {
      input.classList.add('error');
      setTimeout(function () {
        input.classList.remove('error');
      }, 500);
      input.focus();
      return;
    }

    // Add to state
    state.addTodo(title, prioritySelect.value);

    // Persist
    storage.save(state.todos);

    // Re-render
    render.renderApp();

    // Reset form
    input.value = '';
    input.focus();
  }

  /** Handle task list clicks → Toggle complete or Delete */
  function handleListClick(e) {
    var item = e.target.closest('.task-item');
    if (!item) return;

    var id = item.dataset.id;

    // Click on checkbox or title → Toggle complete
    if (e.target.closest('.checkbox') || e.target.closest('.task-title')) {
      state.toggleTodo(id);
      storage.save(state.todos);
      render.renderApp();
      return;
    }

    // Click on delete button → Remove with animation
    if (e.target.closest('.delete-btn')) {
      item.classList.add('deleting');

      // Wait for animation finish, then remove from state
      setTimeout(function () {
        state.deleteTodo(id);
        storage.save(state.todos);
        render.renderApp();
      }, DELETE_ANIMATION_MS);
    }
  }

  /** Handle filter tab click → Change filter */
  function handleFilterClick(e) {
    var tab = e.target.closest('.filter-tab');
    if (!tab) return;

    state.setFilter(tab.dataset.filter);
    render.renderApp();
  }

  // ================================================================
  // Storage Warning
  // ================================================================
  function showStorageWarning() {
    var existing = document.querySelector('.storage-warning');
    if (existing) return; // Already showing

    var banner = document.createElement('div');
    banner.className = 'storage-warning';
    banner.textContent =
      '存储空间可能已满，数据将不会在刷新后保留。请清理浏览器数据。';
    document.body.insertBefore(banner, document.body.firstChild);
  }

  // ================================================================
  // Initialization
  // ================================================================
  function init() {
    // Load saved data into state
    var saved = storage.load();
    if (saved && Array.isArray(saved)) {
      state.todos = saved;
    }

    // Warn if localStorage is unavailable
    if (!storage.isAvailable()) {
      showStorageWarning();
    }

    // Initial render
    render.renderApp();

    // Bind events (delegation pattern)
    document.querySelector('.input-section').addEventListener('submit', handleSubmit);
    document.querySelector('.task-list').addEventListener('click', handleListClick);
    document.querySelector('.filter-tabs').addEventListener('click', handleFilterClick);
  }

  // Start when DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
