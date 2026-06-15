/**
 * VibeTodo — Automated Tests
 * Zero dependencies beyond Node.js + jsdom.
 * Run: npm test  or  node tests/run.js
 */

const assert = require('assert');
const fs = require('fs');
const path = require('path');
const { JSDOM } = require('jsdom');

let passed = 0;
let failed = 0;
function check(name, ok, detail) {
  if (ok) { passed++; console.log('  [PASS] ' + name); }
  else { failed++; console.error('  [FAIL] ' + name + (detail ? '\n         ' + detail : '')); }
}

console.log('\nVibeTodo Test Suite\n');

// Read source and build a complete HTML page
const appJS = fs.readFileSync(path.join(__dirname, '..', 'src', 'app.js'), 'utf-8');

const dom = new JSDOM(
  fs.readFileSync(path.join(__dirname, '..', 'src', 'index.html'), 'utf-8'),
  { url: 'http://localhost', runScripts: 'dangerously' }
);

const doc = dom.window.document;
const win = dom.window;

// Inject app.js by creating a script element (most reliable way)
const script = doc.createElement('script');
script.textContent = appJS;
doc.body.appendChild(script);

const input = () => doc.getElementById('todo-input');
const form = () => doc.querySelector('.input-section');
const items = () => doc.querySelectorAll('.task-item');
const counter = () => doc.querySelector('.task-counter');
const empty = () => doc.querySelector('.empty-state');
const firstTitle = () => doc.querySelector('.task-title');

// Wait for scripts to execute, then run tests
setTimeout(() => {

  // === F-001: Add Todo ===
  input().value = 'Buy groceries';
  doc.getElementById('priority-select').value = 'high';
  form().dispatchEvent(new win.Event('submit', { cancelable: true, bubbles: true }));

  check('F-001: addTodo creates item in DOM',
    items().length === 1,
    'expected 1, got ' + items().length
  );

  check('F-001: title matches input',
    firstTitle() && firstTitle().textContent === 'Buy groceries'
  );

  check('F-001: priority badge shows correct label',
    doc.querySelector('.priority-badge') &&
    doc.querySelector('.priority-badge').textContent.includes('高')
  );

  // === F-001: Reject empty input ===
  input().value = '   ';
  form().dispatchEvent(new win.Event('submit', { cancelable: true, bubbles: true }));
  check('F-001: rejects empty/whitespace input',
    items().length === 1,
    'expected 1, got ' + items().length
  );

  // === F-002: Toggle Complete ===
  const cb = doc.querySelector('.checkbox');
  if (cb) {
    cb.checked = true; // First toggle: set to completed
    cb.dispatchEvent(new win.Event('click', { bubbles: true }));
    check('F-002: toggle on adds completed class',
      items()[0].classList.contains('completed')
    );
    check('F-002: checkbox is checked',
      doc.querySelector('.checkbox').checked === true
    );

    // Second toggle: uncheck (re-query after re-render)
    const cb2 = doc.querySelector('.checkbox');
    cb2.dispatchEvent(new win.Event('click', { bubbles: true }));
    const itemAfter = doc.querySelector('.task-item');
    check('F-002: toggle off removes completed class',
      itemAfter && !itemAfter.classList.contains('completed'),
      'classList: ' + (itemAfter ? itemAfter.className : 'null')
    );
  } else {
    check('F-002: checkbox exists (pre-condition)', false, 'checkbox not found');
  }

  // === F-003: Delete ===
  const delBtn = doc.querySelector('.delete-btn');
  if (delBtn) {
    delBtn.dispatchEvent(new win.Event('click', { bubbles: true }));
    setTimeout(() => {
      check('F-003: deleteTodo removes item from DOM',
        items().length === 0,
        'expected 0, got ' + items().length
      );

      runRemaining();
    }, 250);
  } else {
    check('F-003: delete button exists (pre-condition)', false);
    runRemaining();
  }

}, 200);

function runRemaining() {
  // === F-004: Filter ===
  input().value = 'High task'; doc.getElementById('priority-select').value = 'high';
  form().dispatchEvent(new win.Event('submit', { cancelable: true, bubbles: true }));

  input().value = 'Medium task'; doc.getElementById('priority-select').value = 'medium';
  form().dispatchEvent(new win.Event('submit', { cancelable: true, bubbles: true }));

  input().value = 'Low task'; doc.getElementById('priority-select').value = 'low';
  form().dispatchEvent(new win.Event('submit', { cancelable: true, bubbles: true }));

  check('F-004: 3 items added', items().length === 3, 'got ' + items().length);

  const highTab = doc.querySelector('[data-filter="high"]');
  if (highTab) {
    highTab.dispatchEvent(new win.Event('click', { bubbles: true }));
    check('F-004: high filter shows 1 item',
      items().length === 1,
      'got ' + items().length
    );
    check('F-004: filtered item is High task',
      items()[0].querySelector('.task-title').textContent === 'High task'
    );

    doc.querySelector('[data-filter="all"]').dispatchEvent(new win.Event('click', { bubbles: true }));
    check('F-004: all filter shows 3 items',
      items().length === 3,
      'got ' + items().length
    );
  } else {
    check('F-004: filter tab exists', false);
  }

  // === F-005: Counter ===
  check('F-005: counter shows total',
    counter().textContent.includes('3')
  );
  check('F-005: counter shows 0 completed',
    counter().textContent.includes('0')
  );

  // Also toggle the first one for F-005 counting
  const firstCb = doc.querySelector('.checkbox');
  firstCb.dispatchEvent(new win.Event('click', { bubbles: true }));
  check('F-005: counter shows 1 completed after toggle',
    counter().textContent.includes('1')
  );

  // === F-006: localStorage ===
  const stored = JSON.parse(win.localStorage.getItem('vibetodo-todos'));
  check('F-006: stored data is array',
    Array.isArray(stored)
  );
  check('F-006: stored 3 items',
    stored.length === 3,
    'got ' + (stored ? stored.length : 'null')
  );
  check('F-006: each todo has required fields',
    stored[0] && typeof stored[0].id === 'string' &&
    typeof stored[0].title === 'string' &&
    typeof stored[0].completed === 'boolean'
  );

  // === F-008: Empty State ===
  doc.querySelectorAll('.delete-btn').forEach(b =>
    b.dispatchEvent(new win.Event('click', { bubbles: true }))
  );
  setTimeout(() => {
    check('F-008: empty state visible when no items',
      empty().classList.contains('visible')
    );
    finalize();
  }, 600);
}

function finalize() {
  // === XSS Prevention ===
  input().value = '<img src=x onerror=alert(1)>';
  form().dispatchEvent(new win.Event('submit', { cancelable: true, bubbles: true }));

  const titles = doc.querySelectorAll('.task-title');
  const lastTitle = titles[titles.length - 1];
  check('XSS: textContent renders literal HTML',
    lastTitle && lastTitle.textContent === '<img src=x onerror=alert(1)>'
  );

  // === Title Truncation ===
  input().value = 'x'.repeat(250);
  form().dispatchEvent(new win.Event('submit', { cancelable: true, bubbles: true }));

  const finalStored = JSON.parse(win.localStorage.getItem('vibetodo-todos'));
  // addTodo uses unshift — newest items are at index 0
  const firstAdded = finalStored[0];
  check('Title: truncates to 200 characters',
    firstAdded && firstAdded.title.length === 200,
    'got length ' + (firstAdded ? firstAdded.title.length : 'null') + ', title starts with: ' + (firstAdded ? firstAdded.title.slice(0, 5) : 'N/A')
  );

  // Summary
  console.log('\n' + '='.repeat(50));
  console.log('Results: ' + passed + ' passed, ' + failed + ' failed');
  console.log('Total:   ' + (passed + failed) + ' tests');
  console.log('='.repeat(50) + '\n');
  process.exit(failed > 0 ? 1 : 0);
}
