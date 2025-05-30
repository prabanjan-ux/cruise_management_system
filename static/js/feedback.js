document.addEventListener('DOMContentLoaded', () => {
  const highlight = document.querySelector('.highlight-box');
  const form = document.querySelector('form');
  const msgBox = document.getElementById('submitMessage');

  // Fade in highlight box
  setTimeout(() => {
    if (highlight) {
      highlight.style.transition = 'all 0.8s ease';
      highlight.style.opacity = '1';
      highlight.style.transform = 'translateY(0)';
    }
  }, 100);

  // Fade in form
  setTimeout(() => {
    if (form) {
      form.style.transition = 'all 1s ease';
      form.style.opacity = '1';
      form.style.transform = 'translateY(0)';
    }
  }, 300);

  // Optional: No need to intercept submit unless doing AJAX
  // form.addEventListener('submit', function(event) {
  //   // Don't prevent default, so form submits to backend normally
  // });
});
