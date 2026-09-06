/* Progressive enhancements. No network requests, storage, or health profiling. */
(() => {
  'use strict';
  document.querySelectorAll('[data-pathfinder]').forEach(root => {
    const controls = root.querySelector('[data-path-controls]');
    const buttons = [...root.querySelectorAll('[data-path-choice]')];
    const panels = [...root.querySelectorAll('[data-path-panel]')];
    if (!controls || !buttons.length || panels.length !== buttons.length) return;
    const select = value => {
      if (!panels.some(panel => panel.dataset.pathPanel === value)) return;
      panels.forEach(panel => { panel.hidden = panel.dataset.pathPanel !== value; });
      buttons.forEach(button => button.setAttribute('aria-pressed', String(button.dataset.pathChoice === value)));
    };
    buttons.forEach(button => button.addEventListener('click', () => select(button.dataset.pathChoice)));
    select(buttons[0].dataset.pathChoice);
    controls.hidden = false;
  });
})();
