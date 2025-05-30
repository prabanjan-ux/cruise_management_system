document.addEventListener('DOMContentLoaded', function () {
  const highlight = document.querySelector('.highlight-box');
  const form = document.querySelector('form');
  const msgBox = document.getElementById('submitMessage');

  // Initial animation styles
  highlight.style.opacity = '0';
  highlight.style.transform = 'translateY(-20px)';
  form.style.opacity = '0';
  form.style.transform = 'translateY(30px)';

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

  // Show success message on form submit (without blocking submission)
  form.addEventListener('submit', function () {
    msgBox.style.display = 'block';

    setTimeout(() => {
      msgBox.style.display = 'none';
    }, 3000);
  });
});
