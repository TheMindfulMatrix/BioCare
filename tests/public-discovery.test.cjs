const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const path = require('node:path');
const source = fs.readFileSync(path.join(__dirname, '../assets/js/enhancements.js'), 'utf8');

function element(extra = {}) {
  return { listeners: {}, hidden: false, value: '', textContent: '',
    addEventListener(name, callback) { this.listeners[name] = callback; },
    focus() { this.focused = true; }, ...extra };
}

function evidenceBrowser(reducedMotion) {
  const search = element();
  const reset = element();
  const emptyReset = element();
  const empty = element();
  const status = element();
  const cards = [element({ dataset: { sourceSearch: 'magnesium', sourceCollection: 'core-four' } }),
    element({ dataset: { sourceSearch: 'sleep', sourceCollection: '' } })];
  const controls = element({ querySelector(selector) { return selector === '[data-evidence-search]' ? search : reset; }, querySelectorAll() { return []; } });
  const fields = { '[data-evidence-controls]': controls, '[data-evidence-status]': status,
    '[data-evidence-empty]': empty, '[data-evidence-empty-reset]': emptyReset };
  const root = { querySelector(selector) { return fields[selector]; }, querySelectorAll() { return cards; } };
  const location = new URL('https://example.test/evidence.html?collection=core-four');
  const window = element({ matchMedia() { return { matches: reducedMotion }; } });
  const document = { documentElement: { classList: { add() {} } },
    querySelector() { return null; }, querySelectorAll(selector) { return selector === '[data-evidence-browser]' ? [root] : []; }, addEventListener() {} };
  const history = { replaceState(_state, _title, url) { location.href = new URL(url, location).href; } };
  vm.runInNewContext(source, { document, window, location, history, URL, URLSearchParams });
  return { cards, controls, emptyReset, search, status, location, window };
}

for (const reducedMotion of [false, true]) {
  test(`Evidence clear releases Core Four restriction and browser return restores it; reduced motion=${reducedMotion}`, () => {
    const browser = evidenceBrowser(reducedMotion);
    assert.deepEqual(browser.cards.map(card => card.hidden), [false, true]);
    assert.match(browser.status.textContent, /Core Four collection/);
    let prevented = false;
    browser.controls.listeners.reset({ preventDefault() { prevented = true; } });
    assert.equal(prevented, true);
    assert.deepEqual(browser.cards.map(card => card.hidden), [false, false]);
    assert.equal(browser.location.search, '');
    assert.match(browser.status.textContent, /Showing 2 of 2/);
    assert.equal(browser.search.focused, true);
    browser.location.search = '?collection=core-four&q=unmatched';
    browser.window.listeners.popstate();
    assert.deepEqual(browser.cards.map(card => card.hidden), [true, true]);
    browser.emptyReset.listeners.click();
    assert.deepEqual(browser.cards.map(card => card.hidden), [false, false]);
    assert.equal(browser.location.search, '');
    browser.location.search = '?collection=core-four';
    browser.window.listeners.popstate();
    assert.deepEqual(browser.cards.map(card => card.hidden), [false, true]);
  });
}
