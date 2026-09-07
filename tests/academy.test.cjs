const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const { createState, makePlan, init } = require('../assets/js/academy.js');
const copies = Object.fromEntries([['everyday', 'learning.json'], ['partner', 'partner-learning.json']].map(([kind, name]) => [kind, JSON.parse(fs.readFileSync(path.join(__dirname, '../content', name))).practice]));

test('samples start incomplete, cannot navigate outside three steps, and reset', () => {
  for (const kind of ['everyday', 'partner']) {
    const state = createState(kind);
    assert.equal(state.step, 0);
    assert.equal(state.completed, false);
    assert.equal(state.move(-1), 0);
    state.move(1); state.move(1);
    assert.equal(state.move(1), 2);
    assert.equal(state.move(-1), 1);
    state.reset();
    assert.equal(state.step, 0);
    assert.equal(state.completed, false);
  }
});
test('correct answers complete only their own sample', () => {
  assert.equal(createState('everyday').answer('smaller'), true);
  assert.equal(createState('everyday').answer('pause'), false);
  assert.equal(createState('partner').answer('pause'), true);
  assert.equal(createState('partner').answer('smaller'), false);
});
test('all distractors and missing answers fail', () => {
  for (const answer of ['double', 'quit', 'pressure', 'promise', '', null, undefined]) {
    assert.equal(createState('everyday').answer(answer), false);
    assert.equal(createState('partner').answer(answer), false);
  }
});
test('changed answers clear completion; each visit gets separate memory', () => {
  const one = createState('everyday');
  one.answer('smaller'); one.invalidate();
  assert.equal(one.completed, false);
  one.answer('smaller');
  assert.equal(createState('everyday').completed, false);
});
test('unknown sample names fail closed including prototype keys', () => {
  for (const kind of ['unknown', 'constructor', '__proto__']) assert.throws(() => createState(kind));
});
test('every everyday combination has a cue, action, fallback and reflection', () => {
  for (const cue of Object.keys(copies.everyday.cues)) for (const action of Object.keys(copies.everyday.actions)) {
    const plan = makePlan('everyday', { cue, action }, copies.everyday);
    assert.ok(plan.includes(copies.everyday.cues[cue]));
    for (const phrase of copies.everyday.actions[action]) assert.ok(plan.includes(phrase));
    assert.ok(plan.includes('review'));
    assert.ok(!plan.includes('{'));
  }
});
test('every partner combination retains commercial disclosure and opt-out', () => {
  for (const topic of Object.keys(copies.partner.topics)) for (const format of Object.keys(copies.partner.formats)) {
    const plan = makePlan('partner', { topic, format }, copies.partner);
    assert.ok(plan.includes(copies.partner.topics[topic]));
    assert.ok(plan.includes(copies.partner.formats[format]));
    assert.ok(plan.includes('independent Zinzino partner'));
    assert.ok(plan.includes('benefit commercially'));
    assert.ok(plan.includes('No pressure'));
  }
});
test('unknown and inherited choice keys cannot inject text into plans', () => {
  assert.equal(makePlan('everyday', { cue: '<script>', action: '__proto__' }, copies.everyday), makePlan('everyday', {}, copies.everyday));
  assert.equal(makePlan('partner', { topic: 'constructor', format: '__proto__' }, copies.partner), makePlan('partner', {}, copies.partner));
});

// Minimal event fixture exercises our bindings; it is NOT a browser/layout test.
function element(extra = {}) {
  return Object.assign({ hidden: false, disabled: false, dataset: {}, textContent: '', handlers: {}, attrs: {},
    addEventListener(name, fn) { (this.handlers[name] ||= []).push(fn); },
    fire(name) { (this.handlers[name] || []).forEach(fn => fn()); },
    setAttribute(k, v) { this.attrs[k] = v; }, removeAttribute(k) { delete this.attrs[k]; },
    focus() { this.focused = true; }
  }, extra);
}
function fixture(kind = 'everyday') {
  const headers = [element(), element(), element()];
  const panels = headers.map(h => element({ querySelector: () => h }));
  const inputs = (kind === 'partner' ? ['pause', 'pressure', 'promise'] : ['double', 'smaller', 'quit']).map(value => element({ value, checked: false }));
  const fields = (kind === 'partner' ? [['topic', 'products'], ['format', 'guide']] : [['cue', 'breakfast'], ['action', 'plan']]).map(([choice, value]) => element({ dataset: { choice }, value }));
  const singles = Object.fromEntries(['back','next','quiz','feedback','complete','check','plan','progress','progress-label','step','restart'].map(name => [`[data-${name}]`, element()]));
  singles['[data-practice-copy]'] = element({ textContent: JSON.stringify(copies[kind]) });
  singles['[data-quiz]'].querySelector = () => inputs.find(input => input.checked);
  singles['[data-quiz]'].querySelectorAll = () => inputs;
  singles['[data-feedback]'].dataset = { correct: 'Correct.', wrong: 'Try again.' };
  const stages = [element(), element(), element()];
  const enhanced = [element({hidden:true}), element({hidden:true})];
  const player = element({ dataset: { academy: kind }, querySelector: selector => singles[selector], querySelectorAll: selector => ({'[data-panel]':panels,'[data-choice]':fields,'.academy-stages li':stages,'[data-enhanced]':enhanced}[selector] || []) });
  const doc = { querySelectorAll: () => [player] };
  return { doc, player, panels, headers, singles, fields, inputs, stages, enhanced, get: name => singles[`[data-${name}]`] };
}
test('initialization reveals controls and isolates the first panel, without focus theft', () => {
  const f = fixture(); init(f.doc);
  assert.equal(f.player.dataset.ready, 'true');
  assert.deepEqual(f.panels.map(p => p.hidden), [false,true,true]);
  assert.equal(f.get('back').disabled, true);
  assert.equal(f.get('check').hidden, false);
  assert.ok(f.enhanced.every(e => !e.hidden));
  assert.equal(f.headers[0].focused, undefined);
  assert.ok(f.get('plan').textContent.startsWith('After I'));
});
test('binding is idempotent and navigation transfers focus to the active lesson', () => {
  const f = fixture(); init(f.doc); init(f.doc);
  f.get('next').fire('click');
  assert.deepEqual(f.panels.map(p => p.hidden), [true,false,true]);
  assert.equal(f.headers[1].focused, true);
  assert.equal(f.get('progress').value, 2);
  assert.equal(f.stages[1].attrs['aria-current'], 'step');
  assert.equal(f.stages[0].attrs['aria-current'], undefined);
  f.get('next').fire('click');
  assert.equal(f.get('next').hidden, true);
  f.get('back').fire('click');
  assert.equal(f.get('next').hidden, false);
});
test('missing answers, retries, completion and answer-change feedback all work', () => {
  const f = fixture(); init(f.doc);
  f.get('next').fire('click'); f.get('next').fire('click');
  f.get('check').fire('click');
  assert.equal(f.get('feedback').textContent, 'Choose an answer first.');
  f.inputs[0].checked = true; f.get('check').fire('click');
  assert.equal(f.get('feedback').textContent, 'Try again.');
  assert.equal(f.get('complete').hidden, true);
  f.inputs[0].checked = false; f.inputs[1].checked = true; f.get('check').fire('click');
  assert.equal(f.get('complete').hidden, false);
  assert.equal(f.get('progress-label').textContent, 'Sample complete');
  f.get('quiz').fire('change');
  assert.equal(f.get('complete').hidden, true);
  assert.equal(f.get('feedback').textContent, '');
});
test('partner controls update transparent draft and restart resets all selections', () => {
  const f = fixture('partner'); init(f.doc);
  f.fields[0].value = 'business'; f.fields[0].fire('change');
  assert.ok(f.get('plan').textContent.includes('costs and responsibilities'));
  f.get('next').fire('click'); f.get('next').fire('click');
  f.inputs[0].checked = true; f.get('check').fire('click');
  assert.equal(f.get('complete').hidden, false);
  f.get('restart').fire('click');
  assert.deepEqual(f.panels.map(p => p.hidden), [false,true,true]);
  assert.equal(f.fields[0].value, 'products');
  assert.ok(f.inputs.every(input => !input.checked));
  assert.equal(f.get('complete').hidden, true);
  assert.equal(f.get('feedback').textContent, '');
});
test('malformed/missing configuration leaves static lesson fallback intact', () => {
  for (const bad of ['{', '{}', 'null']) {
    const f = fixture(); f.get('practice-copy').textContent = bad; init(f.doc);
    assert.equal(f.player.dataset.ready, undefined);
    assert.ok(f.panels.every(panel => !panel.hidden));
    assert.ok(f.enhanced.every(control => control.hidden));
  }
});
test('incomplete markup is not partially initialized', () => {
  const f = fixture(); delete f.singles['[data-restart]']; init(f.doc);
  assert.equal(f.player.dataset.ready, undefined);
  assert.ok(f.panels.every(panel => !panel.hidden));
});
test('sample runtime has no network, storage, tracking, payments or motion-dependent boot', () => {
  const source = fs.readFileSync(path.join(__dirname, '../assets/js/academy.js'), 'utf8');
  assert.doesNotMatch(source, /localStorage|sessionStorage|indexedDB|fetch\(|XMLHttpRequest|sendBeacon|innerHTML|document\.cookie|matchMedia|prefers-reduced-motion|dataLayer/);
});
