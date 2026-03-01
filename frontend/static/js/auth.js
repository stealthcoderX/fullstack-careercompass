/**
 * auth.js
 * CareerCompass – Client-side form validation for register and login pages.
 * Made by stealthcoderX | All rights reserved.
 * Server always re-validates; this is a UX enhancement only.
 */

'use strict';

// ── Helpers ──────────────────────────────────────────────────────────────────

function showError(errEl, message) {
  if (!errEl) return;
  errEl.textContent = message;
  errEl.classList.add('is-visible');
}

function clearError(errEl) {
  if (!errEl) return;
  errEl.textContent = '';
  errEl.classList.remove('is-visible');
}

function setInputState(input, state /* 'error' | 'valid' | 'neutral' */) {
  if (!input) return;
  input.classList.remove('is-error', 'is-valid');
  if (state === 'error') input.classList.add('is-error');
  if (state === 'valid') input.classList.add('is-valid');
}

function isValidEmail(email) {
  return /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(email);
}

function setButtonLoading(btn, loading) {
  if (!btn) return;
  btn.classList.toggle('is-loading', loading);
  btn.disabled = loading;
}

// ── Password strength ─────────────────────────────────────────────────────────

function evaluatePasswordStrength(password) {
  let score = 0;
  if (password.length >= 8)  score++;
  if (password.length >= 12) score++;
  if (/[A-Z]/.test(password)) score++;
  if (/[0-9]/.test(password)) score++;
  if (/[^A-Za-z0-9]/.test(password)) score++;

  const levels = [
    { label: '',        colour: '',         pct: 0   },
    { label: 'Weak',    colour: '#f05050',  pct: 20  },
    { label: 'Fair',    colour: '#f0a030',  pct: 45  },
    { label: 'Good',    colour: '#3ecf8e',  pct: 70  },
    { label: 'Strong',  colour: '#1a9b8a',  pct: 88  },
    { label: 'Very strong 💪', colour: '#0e7a6a', pct: 100 },
  ];
  return levels[Math.min(score, 5)];
}

// ── Registration form ─────────────────────────────────────────────────────────

function initRegisterForm(cfg) {
  const form      = document.getElementById(cfg.formId);
  const btn       = document.getElementById(cfg.btnId);
  const nameEl    = document.getElementById(cfg.nameId);
  const emailEl   = document.getElementById(cfg.emailId);
  const passEl    = document.getElementById(cfg.passId);
  const confirmEl = document.getElementById(cfg.confirmId);
  const agreeEl   = document.getElementById(cfg.agreeId);
  const nameErr   = document.getElementById(cfg.nameErrId);
  const emailErr  = document.getElementById(cfg.emailErrId);
  const passErr   = document.getElementById(cfg.passErrId);
  const confirmErr= document.getElementById(cfg.confirmErrId);
  const fillEl    = document.getElementById(cfg.fillId);
  const labelEl   = document.getElementById(cfg.labelId);

  if (!form) return;

  // Live password strength
  if (passEl && fillEl && labelEl) {
    passEl.addEventListener('input', () => {
      const result = evaluatePasswordStrength(passEl.value);
      fillEl.style.width      = result.pct + '%';
      fillEl.style.background = result.colour;
      labelEl.textContent     = result.label;
    });
  }

  // Live confirm check
  if (confirmEl) {
    confirmEl.addEventListener('input', () => {
      if (confirmEl.value && passEl && confirmEl.value !== passEl.value) {
        setInputState(confirmEl, 'error');
        showError(confirmErr, 'Passwords do not match.');
      } else if (confirmEl.value) {
        setInputState(confirmEl, 'valid');
        clearError(confirmErr);
      }
    });
  }

  // Submit
  form.addEventListener('submit', (e) => {
    let valid = true;

    // Name
    const name = nameEl ? nameEl.value.trim() : '';
    if (!name || name.length < 2) {
      setInputState(nameEl, 'error');
      showError(nameErr, 'Full name must be at least 2 characters.');
      valid = false;
    } else {
      setInputState(nameEl, 'valid');
      clearError(nameErr);
    }

    // Email
    const email = emailEl ? emailEl.value.trim() : '';
    if (!isValidEmail(email)) {
      setInputState(emailEl, 'error');
      showError(emailErr, 'Please enter a valid email address.');
      valid = false;
    } else {
      setInputState(emailEl, 'valid');
      clearError(emailErr);
    }

    // Password
    const pass = passEl ? passEl.value : '';
    if (pass.length < 8) {
      setInputState(passEl, 'error');
      showError(passErr, 'Password must be at least 8 characters.');
      valid = false;
    } else {
      setInputState(passEl, 'valid');
      clearError(passErr);
    }

    // Confirm
    const confirm = confirmEl ? confirmEl.value : '';
    if (!confirm || confirm !== pass) {
      setInputState(confirmEl, 'error');
      showError(confirmErr, 'Passwords do not match.');
      valid = false;
    } else {
      setInputState(confirmEl, 'valid');
      clearError(confirmErr);
    }

    // Terms
    if (agreeEl && !agreeEl.checked) {
      agreeEl.focus();
      valid = false;
      const label = agreeEl.parentElement;
      if (label) {
        label.style.color = '#f08080';
        setTimeout(() => label.style.color = '', 2000);
      }
    }

    if (!valid) {
      e.preventDefault();
      return;
    }

    setButtonLoading(btn, true);
  });
}

// ── Login form ────────────────────────────────────────────────────────────────

function initLoginForm(cfg) {
  const form    = document.getElementById(cfg.formId);
  const btn     = document.getElementById(cfg.btnId);
  const emailEl = document.getElementById(cfg.emailId);
  const passEl  = document.getElementById(cfg.passId);
  const emailErr= document.getElementById(cfg.emailErrId);
  const passErr = document.getElementById(cfg.passErrId);

  if (!form) return;

  form.addEventListener('submit', (e) => {
    let valid = true;

    const email = emailEl ? emailEl.value.trim() : '';
    if (!isValidEmail(email)) {
      setInputState(emailEl, 'error');
      showError(emailErr, 'Please enter a valid email address.');
      valid = false;
    } else {
      setInputState(emailEl, 'valid');
      clearError(emailErr);
    }

    const pass = passEl ? passEl.value : '';
    if (!pass) {
      setInputState(passEl, 'error');
      showError(passErr, 'Password is required.');
      valid = false;
    } else {
      setInputState(passEl, 'valid');
      clearError(passErr);
    }

    if (!valid) {
      e.preventDefault();
      return;
    }

    setButtonLoading(btn, true);
  });
}
