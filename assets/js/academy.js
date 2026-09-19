/* Free sample state lives only in memory. No identity, tracking, or payments. */
(function (root, factory) {
  const api = factory();
  if (typeof module === 'object' && module.exports) module.exports = api;
  if (root && root.document) {
    const start = () => api.init(root.document);
    if (root.document.readyState === 'loading') root.document.addEventListener('DOMContentLoaded', start, { once: true });
    else start();
  }
})(typeof window !== 'undefined' ? window : null, function () {
  'use strict';
  const correct = { everyday: 'smaller', partner: 'pause' };
  function pick(values, key, fallback) { return values[Object.hasOwn(values, key) ? key : fallback]; }
  function makePlan(kind, choices, copy) {
    let substitutions;
    if (kind === 'partner') {
      substitutions = { topic: pick(copy.topics, choices.topic, 'products'), format: pick(copy.formats, choices.format, 'guide') };
    } else {
      const action = pick(copy.actions, choices.action, 'plan');
      substitutions = { cue: pick(copy.cues, choices.cue, 'breakfast'), action: action[0], fallback: action[1] };
    }
    return copy.template.replace(/\{(\w+)\}/g, (match, name) => Object.hasOwn(substitutions, name) ? substitutions[name] : match);
  }
  function createState(kind) {
    if (!Object.hasOwn(correct, kind)) throw new Error('Unknown course sample');
    let step = 0;
    let completed = false;
    return {
      get step() { return step; },
      get completed() { return completed; },
      move(delta) { step = Math.min(2, Math.max(0, step + Math.sign(delta))); return step; },
      answer(value) { completed = value === correct[kind]; return completed; },
      invalidate() { completed = false; },
      reset() { step = 0; completed = false; }
    };
  }
  function init(doc) {
    doc.querySelectorAll('[data-academy]').forEach((player) => {
      if (player.dataset.ready === 'true') return;
      const kind = player.dataset.academy;
      if (!Object.hasOwn(correct, kind)) return;
      let copy;
      try {
        copy = JSON.parse(player.querySelector('[data-practice-copy]').textContent);
        makePlan(kind, {}, copy);
      } catch (_) { return; } // Leave all fallback lesson content readable.
      const state = createState(kind);
      const panels = [...player.querySelectorAll('[data-panel]')];
      const back = player.querySelector('[data-back]');
      const next = player.querySelector('[data-next]');
      const quiz = player.querySelector('[data-quiz]');
      const feedback = player.querySelector('[data-feedback]');
      const complete = player.querySelector('[data-complete]');
      const check = player.querySelector('[data-check]');
      const plan = player.querySelector('[data-plan]');
      const progress = player.querySelector('[data-progress]');
      const progressLabel = player.querySelector('[data-progress-label]');
      const stepLabel = player.querySelector('[data-step]');
      const restart = player.querySelector('[data-restart]');
      if (panels.length !== 3 || ![back, next, quiz, feedback, complete, check, plan, progress, progressLabel, stepLabel, restart].every(Boolean)) return;
      const choices = [...player.querySelectorAll('[data-choice]')];
      const defaults = choices.map((field) => field.value);
      function render(focus) {
        panels.forEach((panel, index) => { panel.hidden = index !== state.step; });
        back.disabled = state.step === 0;
        next.hidden = state.step === 2;
        next.textContent = state.step === 0 ? 'Practise →' : 'Check your understanding →';
        progress.value = state.step + 1;
        progress.textContent = `${state.step + 1} of 3`;
        progressLabel.textContent = state.completed ? 'Sample complete' : `Step ${state.step + 1} of 3`;
        stepLabel.textContent = state.completed ? 'Sample complete' : `0${state.step + 1} / 03`;
        [...player.querySelectorAll('.academy-stages li')].forEach((item, index) => {
          if (index === state.step) item.setAttribute('aria-current', 'step');
          else item.removeAttribute('aria-current');
        });
        if (focus) {
          const heading = panels[state.step].querySelector('h3');
          heading.setAttribute('tabindex', '-1');
          heading.focus();
        }
      }
      function updatePlan() {
        plan.textContent = makePlan(kind, Object.fromEntries(choices.map((field) => [field.dataset.choice, field.value])), copy);
      }
      back.addEventListener('click', () => { state.move(-1); render(true); });
      next.addEventListener('click', () => { state.move(1); render(true); });
      choices.forEach((field) => field.addEventListener('change', updatePlan));
      quiz.addEventListener('change', () => {
        state.invalidate();
        complete.hidden = true;
        feedback.textContent = '';
        render(false);
      });
      check.addEventListener('click', () => {
        const selected = quiz.querySelector('input:checked');
        if (!selected) { feedback.textContent = 'Choose an answer first.'; return; }
        const passed = state.answer(selected.value);
        feedback.textContent = passed ? feedback.dataset.correct : feedback.dataset.wrong;
        complete.hidden = !passed;
        render(false);
      });
      restart.addEventListener('click', () => {
        state.reset();
        choices.forEach((field, index) => { field.value = defaults[index]; });
        quiz.querySelectorAll('input').forEach((input) => { input.checked = false; });
        feedback.textContent = '';
        complete.hidden = true;
        updatePlan();
        render(true);
      });
      updatePlan();
      render(false);
      check.hidden = false;
      player.querySelectorAll('[data-enhanced]').forEach((element) => { element.hidden = false; });
      player.dataset.ready = 'true';
    });
  }
  return { makePlan, createState, init };
});
