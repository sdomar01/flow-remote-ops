document.addEventListener('DOMContentLoaded', function () {

  /* ---------- Footer year ---------- */
  var yearEl = document.getElementById('year');
  if (yearEl) yearEl.textContent = new Date().getFullYear();

  /* ---------- Hero typewriter effect (two lines) ---------- */
  var line1El = document.getElementById('typewriter-line1');
  var line2El = document.getElementById('typewriter-line2');
  var cursor1 = document.getElementById('cursor-line1');
  var cursor2 = document.getElementById('cursor-line2');

  if (line1El && line2El) {
    var line1Text = 'WE RUN THE BACK END';
    var line2Text = 'YOU BUILD THE BUSINESS';
    var typeSpeed = 42; // ms per character
    var idx1 = 0;
    var idx2 = 0;

    function typeLine1() {
      if (idx1 <= line1Text.length) {
        line1El.textContent = line1Text.slice(0, idx1);
        idx1++;
        setTimeout(typeLine1, typeSpeed);
      } else {
        if (cursor1) cursor1.style.display = 'none';
        if (cursor2) cursor2.style.display = 'inline-block';
        setTimeout(typeLine2, 150);
      }
    }

    function typeLine2() {
      if (idx2 <= line2Text.length) {
        line2El.textContent = line2Text.slice(0, idx2);
        idx2++;
        setTimeout(typeLine2, typeSpeed);
      }
    }

    typeLine1();
  }

  /* ---------- Mobile menu ---------- */
  var menuToggle = document.getElementById('menu-toggle');
  var mobileNav = document.getElementById('mobile-nav');

  if (menuToggle && mobileNav) {
    menuToggle.addEventListener('click', function () {
      var isOpen = menuToggle.getAttribute('aria-expanded') === 'true';
      menuToggle.setAttribute('aria-expanded', String(!isOpen));
      mobileNav.classList.toggle('open', !isOpen);
    });

    mobileNav.querySelectorAll('a').forEach(function (link) {
      link.addEventListener('click', function () {
        menuToggle.setAttribute('aria-expanded', 'false');
        mobileNav.classList.remove('open');
      });
    });
  }

  /* ---------- Mobile nav accordion groups (About, Employers, Talents, Explore) ---------- */
  document.querySelectorAll('.mobile-nav-toggle').forEach(function (toggle) {
    var panel = toggle.nextElementSibling;
    if (!panel) return;

    toggle.addEventListener('click', function () {
      var isOpen = toggle.getAttribute('aria-expanded') === 'true';

      // Close any other open group first
      document.querySelectorAll('.mobile-nav-toggle').forEach(function (other) {
        if (other !== toggle) {
          other.setAttribute('aria-expanded', 'false');
          var otherPanel = other.nextElementSibling;
          if (otherPanel) otherPanel.style.maxHeight = null;
        }
      });

      toggle.setAttribute('aria-expanded', String(!isOpen));
      panel.style.maxHeight = isOpen ? null : panel.scrollHeight + 'px';
    });
  });

  /* ---------- Nav dropdowns (Services, About) ---------- */
  function initDropdown(triggerId, dropdownId) {
    var trigger = document.getElementById(triggerId);
    var dropdown = document.getElementById(dropdownId);
    if (!trigger || !dropdown) return;

    function close() {
      trigger.setAttribute('aria-expanded', 'false');
      dropdown.setAttribute('aria-hidden', 'true');
      dropdown.classList.remove('open');
    }

    function open() {
      trigger.setAttribute('aria-expanded', 'true');
      dropdown.setAttribute('aria-hidden', 'false');
      dropdown.classList.add('open');
    }

    trigger.addEventListener('click', function (e) {
      e.stopPropagation();
      var isOpen = trigger.getAttribute('aria-expanded') === 'true';
      isOpen ? close() : open();
    });

    dropdown.querySelectorAll('a').forEach(function (link) {
      link.addEventListener('click', close);
    });

    document.addEventListener('click', function (e) {
      if (!dropdown.contains(e.target) && e.target !== trigger) close();
    });

    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') close();
    });
  }

  initDropdown('about-trigger', 'about-dropdown');
  initDropdown('employers-trigger', 'employers-dropdown');
  initDropdown('talents-trigger', 'talents-dropdown');
  initDropdown('explore-trigger', 'explore-dropdown');

  /* ---------- FAQ accordion ---------- */
  var triggers = document.querySelectorAll('.accordion-trigger');
  triggers.forEach(function (trigger) {
    var panel = trigger.closest('.accordion-item').querySelector('.accordion-panel');

    trigger.addEventListener('click', function () {
      var isOpen = trigger.getAttribute('aria-expanded') === 'true';

      // Close all other panels (single-open accordion)
      triggers.forEach(function (otherTrigger) {
        if (otherTrigger !== trigger) {
          otherTrigger.setAttribute('aria-expanded', 'false');
          var otherPanel = otherTrigger.closest('.accordion-item').querySelector('.accordion-panel');
          otherPanel.style.maxHeight = null;
        }
      });

      trigger.setAttribute('aria-expanded', String(!isOpen));
      panel.style.maxHeight = isOpen ? null : panel.scrollHeight + 'px';
    });
  });

  /* ---------- Forms (Contact page + Talents forms) ----------
     All 4 forms (lead form, job application, candidate inquiry,
     candidate referral) share one Google Sheets webhook. Each form
     includes a hidden "form_type" field so the Apps Script knows which
     sheet tab to write the row to.

     Paste your Apps Script Web App URL below once you've deployed it
     (see the setup steps -- Google Sheet with 4 tabs: Leads, Job
     Applications, Candidate Inquiries, Candidate Referrals -- plus the
     Apps Script doPost() code that routes by form_type).
  ---------------------------------------------------------------- */
  var GOOGLE_SHEET_WEBHOOK_URL = 'https://script.google.com/macros/s/AKfycbwsjD-85BsRPYwl94ad-_eDjsTF0GpI7WpuJx_V6Hmn8pAAU2xuKy-DUjXkNY_W6jwZ/exec';

  function submitLeadForm(formData) {
    var isPlaceholder = GOOGLE_SHEET_WEBHOOK_URL.indexOf('https://docs.google.com/spreadsheets/d/1e6Bb6IdjifT2YJdon5jxLexdrjinN25H5USGvSnuT2Q/edit?usp=sharing') !== -1;

    if (isPlaceholder) {
      // Not connected yet -- log to console so you can still see the
      // full flow working end to end.
      console.log('Form submitted (Google Sheet not connected yet):', Object.fromEntries(formData));
      return Promise.resolve();
    }

    // Apps Script Web Apps don't return CORS headers we can read from
    // the browser, so we POST with mode: 'no-cors'. The submission
    // still reaches the sheet -- we just can't read the response body,
    // which is fine since we already show our own success message.
    return fetch(GOOGLE_SHEET_WEBHOOK_URL, {
      method: 'POST',
      mode: 'no-cors',
      body: formData
    }).catch(function (err) {
      console.error('Lead form submission failed:', err);
    });
  }

  document.querySelectorAll('form.lead-form').forEach(function (form) {
    // Success element is either a specific #lead-form-success (contact
    // page) or the nearest .lead-form-success sibling (Talents forms).
    var success = document.getElementById(form.id + '-success')
      || (form.parentElement ? form.parentElement.querySelector('.lead-form-success') : null)
      || document.getElementById('lead-form-success');

    form.addEventListener('submit', function (e) {
      e.preventDefault();
      if (!form.reportValidity()) return;

      var formData = new FormData(form);
      submitLeadForm(formData).then(function () {
        form.hidden = true;
        if (success) success.hidden = false;
      });
    });
  });

  /* ---------- Sticky header shadow on scroll ---------- */
  var header = document.getElementById('site-header');
  var lastScrolled = false;
  function handleScroll() {
    var scrolled = window.scrollY > 8;
    if (scrolled !== lastScrolled) {
      header.style.boxShadow = scrolled ? '0 1px 0 rgba(15,23,42,0.06)' : 'none';
      lastScrolled = scrolled;
    }
  }
  window.addEventListener('scroll', handleScroll, { passive: true });
  handleScroll();

  /* ---------- Scroll-reveal animations ---------- */
  var revealSelector = '.why-item, .service-group, .who-card, .funnel-item, .role-item, .process-line li, .category-items, .founder-note, .vm-block';
  var revealEls = document.querySelectorAll(revealSelector);

  if ('IntersectionObserver' in window && revealEls.length) {
    revealEls.forEach(function (el, i) {
      el.classList.add('reveal');
      el.style.transitionDelay = (i % 6) * 0.06 + 's';
    });

    var revealObserver = new IntersectionObserver(function (entries, observer) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('revealed');
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });

    revealEls.forEach(function (el) { revealObserver.observe(el); });
  }

});