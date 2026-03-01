/**
 * main.js
 * CareerCompass – Global JavaScript utilities
 * Made by stealthcoderX | All rights reserved.
 */

'use strict';

// ── Intersection Observer for scroll animations ──────────────────────────────
(function initScrollAnimations() {
  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          const delay = parseInt(entry.target.dataset.delay || '0', 10);
          setTimeout(() => entry.target.classList.add('is-visible'), delay);
          observer.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.12, rootMargin: '0px 0px -40px 0px' }
  );

  document.querySelectorAll('[data-animate]').forEach((el) => observer.observe(el));
})();

// ── Password show/hide toggle ────────────────────────────────────────────────
(function initPasswordToggles() {
  document.querySelectorAll('.input-toggle[data-target]').forEach((btn) => {
    btn.addEventListener('click', () => {
      const input = document.getElementById(btn.dataset.target);
      if (!input) return;
      const isPassword = input.type === 'password';
      input.type = isPassword ? 'text' : 'password';
      btn.textContent = isPassword ? 'Hide' : 'Show';
    });
  });
})();

// ── Auto-dismiss flash messages ──────────────────────────────────────────────
(function initFlashDismiss() {
  document.querySelectorAll('.flash').forEach((el) => {
    setTimeout(() => {
      el.style.transition = 'opacity 0.4s';
      el.style.opacity = '0';
      setTimeout(() => el.remove(), 400);
    }, 6000);
  });
})();
