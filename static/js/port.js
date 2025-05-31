document.addEventListener('DOMContentLoaded', () => {
  const highlight = document.querySelector('.highlight-box');
  const form = document.querySelector('#main-form'); // safer selector for your form
  const msgBox = document.getElementById('submitMessage');

  // Set initial animation styles (if elements exist)
  if (highlight) {
    highlight.style.opacity = '0';
    highlight.style.transform = 'translateY(30px)';
  }

  if (form) {
    form.style.opacity = '0';
    form.style.transform = 'translateY(30px)';
  }

  // Animate highlight box after slight delay
  if (highlight) {
    setTimeout(() => {
      highlight.style.transition = 'all 0.8s ease';
      highlight.style.opacity = '1';
      highlight.style.transform = 'translateY(0)';
    }, 100);
  }

  // Animate form after a bit longer delay
  if (form) {
    setTimeout(() => {
      form.style.transition = 'all 1s ease';
      form.style.opacity = '1';
      form.style.transform = 'translateY(0)';
    }, 300);

    // Show success message on form submit (without blocking submission)
    if (msgBox) {
      form.addEventListener('submit', () => {
        msgBox.style.display = 'block';
        setTimeout(() => {
          msgBox.style.display = 'none';
        }, 3000);
      });
    }
  }
});
