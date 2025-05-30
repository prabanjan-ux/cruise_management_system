document.addEventListener('DOMContentLoaded', () => {
  const highlight = document.querySelector('.highlight-box');
  const form = document.querySelector('form');
  const msgBox = document.getElementById('submitMessage');

  // Animate highlight box
  setTimeout(() => {
    highlight.style.transition = 'all 0.8s ease';
    highlight.style.opacity = '1';
    highlight.style.transform = 'translateY(0)';
  }, 100);

  // Animate form
  setTimeout(() => {
    form.style.transition = 'all 1s ease';
    form.style.opacity = '1';
    form.style.transform = 'translateY(0)';
  }, 300);

  // Show message box if present
  if (msgBox) {
    msgBox.style.display = 'block';
    setTimeout(() => {
      msgBox.style.display = 'none';
    }, 3000);
  }
});
