document.addEventListener('DOMContentLoaded', function () {

  /* ---------- Footer year ---------- */
  var yearEl = document.getElementById('year');
  if (yearEl) yearEl.textContent = new Date().getFullYear();

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

  /* ---------- Lead form (on the /contact page) ---------- */
  var leadForm = document.getElementById('lead-form');
  var leadFormSuccess = document.getElementById('lead-form-success');

  /* ---------- Lead form submit ----------
     This form doesn't send anywhere yet -- it's a placeholder until
     you connect it to a real destination. Two common options:

     1) Google Forms: create your form, then map each <input name="...">
        below to the matching entry.XXXXXXX field name from your Google
        Form's HTML, and POST to its .../formResponse URL.
     2) Your own backend: add a Flask route in app.py that accepts
        this data (e.g. POST /submit-lead) and call it here with fetch().

     For now, submitting just shows a success message so you can see
     the full flow working end to end.
  ---------------------------------------------------------------- */
  function submitLeadForm(formData) {
    // TODO: replace with a real request once you have a destination.
    console.log('Lead form submitted (not yet connected):', Object.fromEntries(formData));
    return Promise.resolve();
  }

  if (leadForm) {
    leadForm.addEventListener('submit', function (e) {
      e.preventDefault();
      if (!leadForm.reportValidity()) return;

      var formData = new FormData(leadForm);
      submitLeadForm(formData).then(function () {
        leadForm.hidden = true;
        if (leadFormSuccess) leadFormSuccess.hidden = false;
      });
    });
  }

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

});