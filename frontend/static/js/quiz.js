/**
 * quiz.js
 * CareerCompass – Quiz page engine.
 * Made by stealthcoderX | All rights reserved.
 *
 * Reads QUIZ_DATA, QUIZ_TOTAL, QUIZ_SUBMIT_URL from the page (set by Flask template).
 */

'use strict';

(function () {
  // ── State ──────────────────────────────────────────────────────────────────
  const questions = QUIZ_DATA;   // injected by Flask template
  const total     = QUIZ_TOTAL;
  let   current   = 0;
  const answers   = {};          // { questionId: answerIndex }
  const LABELS    = ['A', 'B', 'C', 'D'];

  // ── DOM references ─────────────────────────────────────────────────────────
  const stage      = document.getElementById('questionStage');
  const progFill   = document.getElementById('progressFill');
  const navCount   = document.getElementById('navCount');
  const submitForm = document.getElementById('quizForm');

  // ── Render ─────────────────────────────────────────────────────────────────
  function render(direction /* 'forward' | 'back' */ = 'forward') {
    const q        = questions[current];
    const selected = answers[q.id];
    const isLast   = current === total - 1;

    // Build card HTML
    const optionsHTML = q.options.map((opt, i) => `
      <button
        class="option-btn${selected === i ? ' is-selected' : ''}"
        type="button"
        data-index="${i}"
        aria-pressed="${selected === i}"
      >
        <span class="opt-label">${LABELS[i]}</span>
        <span class="opt-text">${escapeHTML(opt)}</span>
      </button>
    `).join('');

    const dotsHTML = questions.map((_, i) => `
      <div class="dot${i < current ? ' is-done' : i === current ? ' is-current' : ''}"></div>
    `).join('');

    const cardHTML = `
      <div class="q-card q-enter${direction === 'back' ? '-back' : ''}" id="qCard">
        <div class="q-category">${escapeHTML(q.category)}</div>
        <div class="q-num">Question ${String(current + 1).padStart(2, '0')} of ${total}</div>
        <h2 class="q-text">${escapeHTML(q.text)}</h2>
        <div class="options-grid" id="optionsGrid">${optionsHTML}</div>
        <div class="q-footer">
          <button class="btn-quiz-back" id="btnBack"
            ${current === 0 ? 'disabled aria-disabled="true"' : ''}>
            ← Back
          </button>
          <div class="dots-row" aria-hidden="true">${dotsHTML}</div>
          <button class="btn-quiz-next" id="btnNext"
            ${selected === undefined ? 'disabled aria-disabled="true"' : ''}>
            ${isLast ? 'Submit Quiz' : 'Next'} →
          </button>
        </div>
      </div>
    `;

    stage.innerHTML = cardHTML;

    // Update progress and counter
    const pct = ((current + 1) / total) * 100;
    progFill.style.width   = pct.toFixed(2) + '%';
    navCount.textContent   = current + 1;

    // Attach events
    document.getElementById('optionsGrid').addEventListener('click', onOptionClick);
    document.getElementById('btnBack').addEventListener('click', goBack);
    document.getElementById('btnNext').addEventListener('click', goNext);
  }

  // ── Option selection ───────────────────────────────────────────────────────
  function onOptionClick(e) {
    const btn = e.target.closest('.option-btn');
    if (!btn) return;

    const idx = parseInt(btn.dataset.index, 10);
    const q   = questions[current];
    answers[q.id] = idx;

    // Update all buttons
    document.querySelectorAll('.option-btn').forEach((b, i) => {
      const active = i === idx;
      b.classList.toggle('is-selected', active);
      b.setAttribute('aria-pressed', active);
      b.querySelector('.opt-label').style.background = active ? 'var(--teal)' : '';
      b.querySelector('.opt-label').style.color      = active ? '#fff' : '';
    });

    // Enable next button
    const nextBtn = document.getElementById('btnNext');
    if (nextBtn) {
      nextBtn.disabled = false;
      nextBtn.removeAttribute('aria-disabled');
    }
  }

  // ── Navigation ─────────────────────────────────────────────────────────────
  function goNext() {
    const q = questions[current];
    if (answers[q.id] === undefined) return;

    if (current === total - 1) {
      submitQuiz();
      return;
    }

    animateOut(() => {
      current++;
      render('forward');
    });
  }

  function goBack() {
    if (current === 0) return;
    animateOut(() => {
      current--;
      render('back');
    }, true);
  }

  function animateOut(callback, reverse = false) {
    const card = document.getElementById('qCard');
    if (!card) { callback(); return; }

    card.classList.add('q-exit');
    card.addEventListener('animationend', callback, { once: true });
  }

  // ── Submit ─────────────────────────────────────────────────────────────────
  function submitQuiz() {
    if (!submitForm) return;

    // Disable the submit button to prevent double-submit
    const nextBtn = document.getElementById('btnNext');
    if (nextBtn) {
      nextBtn.disabled = true;
      nextBtn.textContent = 'Submitting…';
    }

    // Clear any stale inputs
    submitForm.innerHTML = '';

    // Inject all answers as hidden inputs
    Object.entries(answers).forEach(([qId, answerIdx]) => {
      const input = document.createElement('input');
      input.type  = 'hidden';
      input.name  = `q${qId}`;
      input.value = String(answerIdx);
      submitForm.appendChild(input);
    });

    submitForm.submit();
  }

  // ── Utility ────────────────────────────────────────────────────────────────
  function escapeHTML(str) {
    const div = document.createElement('div');
    div.textContent = str;
    return div.innerHTML;
  }

  // ── Keyboard navigation ────────────────────────────────────────────────────
  document.addEventListener('keydown', (e) => {
    const q = questions[current];
    if (['a', 'b', 'c', 'd'].includes(e.key.toLowerCase())) {
      const idx = ['a', 'b', 'c', 'd'].indexOf(e.key.toLowerCase());
      if (idx < q.options.length) {
        const btn = document.querySelectorAll('.option-btn')[idx];
        if (btn) btn.click();
      }
    }
    if (e.key === 'ArrowRight' || e.key === 'Enter') {
      const nextBtn = document.getElementById('btnNext');
      if (nextBtn && !nextBtn.disabled) nextBtn.click();
    }
    if (e.key === 'ArrowLeft') {
      const backBtn = document.getElementById('btnBack');
      if (backBtn && !backBtn.disabled) backBtn.click();
    }
  });

  // ── Init ───────────────────────────────────────────────────────────────────
  render('forward');

})();
