function togglePassword() {
  const passwordInput = document.getElementById('password');
  const toggleIcon = document.getElementById('toggleIcon');
  if (passwordInput.type === 'password') {
    passwordInput.type = 'text';
    toggleIcon.classList.replace('fa-eye', 'fa-eye-slash');
  } else {
    passwordInput.type = 'password';
    toggleIcon.classList.replace('fa-eye-slash', 'fa-eye');
  }
}

// Form submit feedback
const form = document.querySelector('form');
const btn = document.querySelector('.btn-login');
form.addEventListener('submit', () => {
  btn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Signing in...';
  btn.disabled = true;
});

// Input focus animations
document.querySelectorAll('.form-control').forEach(input => {
  input.addEventListener('focus', () => {
    input.parentElement.style.transform = 'translateY(-2px)';
  });
  input.addEventListener('blur', () => {
    input.parentElement.style.transform = 'translateY(0)';
  });
});