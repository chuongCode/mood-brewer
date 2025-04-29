document.addEventListener('DOMContentLoaded', function () {
  const fill = document.getElementById('caffeine-fill');
  if (!fill) return;

  const intake = parseInt(fill.dataset.intake);
  const goal = parseInt(fill.dataset.goal);
  const percent = Math.min((intake / goal) * 100, 100);

  fill.style.height = percent + '%';
});