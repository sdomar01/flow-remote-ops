(function () {
  var dot = document.getElementById('cursorGlow');
  var trail = document.getElementById('cursorGlowTrail');
  if (!dot || !trail) return;
  if (!window.matchMedia('(hover: hover) and (pointer: fine)').matches) return;

  var mouseX = 0, mouseY = 0;
  var dotX = 0, dotY = 0;
  var trailX = 0, trailY = 0;

  window.addEventListener('mousemove', function (e) {
    mouseX = e.clientX;
    mouseY = e.clientY;
  });

  function animate() {
    dotX += (mouseX - dotX) * 0.35;
    dotY += (mouseY - dotY) * 0.35;
    trailX += (mouseX - trailX) * 0.12;
    trailY += (mouseY - trailY) * 0.12;

    dot.style.transform = 'translate(' + dotX + 'px,' + dotY + 'px) translate(-50%,-50%)';
    trail.style.transform = 'translate(' + trailX + 'px,' + trailY + 'px) translate(-50%,-50%)';

    requestAnimationFrame(animate);
  }
  requestAnimationFrame(animate);

  var selector = 'a, button, .btn, summary, input, select, textarea, .dropdown-trigger, .menu-toggle, .who-card, .team-card, .funnel-item';
  document.addEventListener('mouseover', function (e) {
    if (e.target.closest(selector)) {
      dot.classList.add('is-active');
      trail.classList.add('is-active');
    }
  });
  document.addEventListener('mouseout', function (e) {
    if (e.target.closest(selector)) {
      dot.classList.remove('is-active');
      trail.classList.remove('is-active');
    }
  });
})();