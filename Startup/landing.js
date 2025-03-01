document.addEventListener('DOMContentLoaded', () => {
    // Existing modal elements
    const registerModal = document.getElementById('registerModal');
    const loginModal = document.getElementById('loginModal');
    const registerBtn = document.querySelector('.register-btn');
    const loginBtn = document.querySelector('.login-btn');
    const closeRegisterBtn = document.querySelector('#registerModal .close');
    const closeLoginBtn = document.querySelector('#loginModal .close');
    const registerForm = document.getElementById('registrationForm');
    const loginForm = document.getElementById('loginForm');

    // Modal Controls
    registerBtn.addEventListener('click', () => {
        registerModal.classList.add('show');
        document.body.style.overflow = 'hidden';
    });

    loginBtn.addEventListener('click', () => {
        loginModal.classList.add('show');
        document.body.style.overflow = 'hidden';
    });

    closeRegisterBtn.addEventListener('click', () => closeModal(registerModal));
    closeLoginBtn.addEventListener('click', () => closeModal(loginModal));

    // Close modals when clicking outside
    window.addEventListener('click', (e) => {
        if (e.target === registerModal) closeModal(registerModal);
        if (e.target === loginModal) closeModal(loginModal);
    });

    function closeModal(modal) {
        modal.classList.remove('show');
        document.body.style.overflow = 'visible';
    }

    // Login Form Handler
    loginForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        const username = document.getElementById('loginUsername').value;
        const password = document.getElementById('loginPassword').value;

        try {
            const response = await fetch('http://localhost:5000/api/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ username, password })
            });

            const data = await response.json();

            if (response.ok && data.success) {
                // Store user data and redirect
                localStorage.setItem('userData', JSON.stringify(data.user));
                window.location.href = 'dashboard.html';
            } else {
                showError(loginForm, data.message || 'Invalid username or password');
            }
        } catch (error) {
            console.error('Error:', error);
            showError(loginForm, 'Error during login. Please try again.');
        }
    });

    // Registration Form Handler (update existing code)
    registerForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        const formData = {
            name: document.getElementById('name').value,
            username: document.getElementById('username').value,
            email: document.getElementById('email').value,
            phone: document.getElementById('phone').value,
            password: document.getElementById('password').value,
            experience: Number(document.getElementById('experience').value),
            designation: document.getElementById('designation').value,
            age: Number(document.getElementById('age').value)
        };

        console.log(formData);

        try {
            const response = await fetch('http://localhost:5000/api/register', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData)
            });

            const data = await response.json();

            if (response.ok && data.success) {
                localStorage.setItem('userData', JSON.stringify(data.user));
                window.location.href = 'dashboard.html';
            } else {
                showError(registerForm, data.message || 'Error creating account');
            }
        } catch (error) {
            console.error('Error:', error);
            showError(registerForm, 'Error creating account. Please try again.');
        }
    });

    // Error handling function
    function showError(form, message) {
        let errorDiv = form.querySelector('.error-message');
        if (!errorDiv) {
            errorDiv = document.createElement('div');
            errorDiv.className = 'error-message';
            form.appendChild(errorDiv);
        }
        errorDiv.textContent = message;
        errorDiv.classList.add('show-error');
        setTimeout(() => {
            errorDiv.classList.remove('show-error');
        }, 3000);
    }
});