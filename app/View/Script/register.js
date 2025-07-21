// Toggle visibility for password and confirm fields
document.querySelectorAll('.password-toggle').forEach(btn => {
  btn.addEventListener('click', () => {
    const fieldId = btn.getAttribute('data-target');
    const icon = btn.querySelector('i');
    const input = document.getElementById(fieldId);
    if (input.type === 'password') {
      input.type = 'text';
      icon.classList.replace('fa-eye', 'fa-eye-slash');
    } else {
      input.type = 'password';
      icon.classList.replace('fa-eye-slash', 'fa-eye');
    }
  });
});

// Form submission handler
const registerForm = document.getElementById('register-form');
registerForm.addEventListener('submit', async (e) => {
  e.preventDefault();
  const btn = registerForm.querySelector('button[type="submit"]');
  btn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Creating...';
  btn.disabled = true;

  // Build payload
  const payload = {
    username: document.getElementById('reg-username').value,
    email: document.getElementById('reg-email').value,
    password: document.getElementById('reg-password').value,
    confirm_password: document.getElementById('reg-confirm').value
  };

  try {
    const response = await fetch(registerForm.action, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    const result = await response.json();
    if (result.success) {
      window.location.href = '/auth/login';
    } else {
      throw new Error(result.error || 'Registration failed');
    }
  } catch (err) {
    alert(err.message);
    btn.disabled = false;
    btn.innerHTML = '<i class="fas fa-user-plus me-2"></i>Create Account';
  }
});