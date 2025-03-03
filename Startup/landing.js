document.addEventListener('DOMContentLoaded', () => {
    // Check if user is logged in and update buttons accordingly
    const userData = localStorage.getItem('userData');
    const ctaButtons = document.querySelector('.cta-buttons');

    // Update buttons based on login status
    updateButtons(userData);

    // Get modal elements
    const registerModal = document.getElementById('registerModal');
    const loginModal = document.getElementById('loginModal');
    const closeRegisterBtn = document.querySelector('#registerModal .close');
    const closeLoginBtn = document.querySelector('#loginModal .close');
    const registerForm = document.getElementById('registrationForm');
    const loginForm = document.getElementById('loginForm');

    // Function to update buttons based on login status
    function updateButtons(userData) {
        if (userData) {
            ctaButtons.innerHTML = `
                <button class="btn dashboard-btn" onclick="window.location.href='dashboard.html'">Dashboard</button>
                <button class="btn logout-btn">Logout</button>
            `;

            // Add event listener for logout
            const logoutBtn = document.querySelector('.logout-btn');
            if (logoutBtn) {
                logoutBtn.addEventListener('click', () => {
                    localStorage.removeItem('userData');
                    window.location.reload();
                });
            }
        } else {
            ctaButtons.innerHTML = `
                <button class="btn login-btn">Login</button>
                <button class="btn register-btn">Sign Up</button>
            `;

            // Add event listeners for the new buttons
            const loginBtn = document.querySelector('.login-btn');
            const registerBtn = document.querySelector('.register-btn');

            if (loginBtn) {
                loginBtn.addEventListener('click', () => {
                    loginModal.classList.add('show');
                    document.body.style.overflow = 'hidden';
                });
            }

            if (registerBtn) {
                registerBtn.addEventListener('click', () => {
                    registerModal.classList.add('show');
                    document.body.style.overflow = 'hidden';
                });
            }
        }
    }

    // Function to close modals
    function closeModal(modal) {
        modal.classList.remove('show');
        document.body.style.overflow = 'visible';
    }

    // Add event listeners for close buttons
    if (closeRegisterBtn) {
        closeRegisterBtn.addEventListener('click', () => closeModal(registerModal));
    }

    if (closeLoginBtn) {
        closeLoginBtn.addEventListener('click', () => closeModal(loginModal));
    }

    // Close modals when clicking outside
    window.addEventListener('click', (e) => {
        if (e.target === registerModal) closeModal(registerModal);
        if (e.target === loginModal) closeModal(loginModal);
    });

    // Function to format current date time
    function getCurrentDateTime() {
        const now = new Date();
        return now.toISOString().replace('T', ' ').slice(0, 19);
    }

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

    // Login Form Handler
    if (loginForm) {
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
    }

    // Registration Form Handler
    if (registerForm) {
        registerForm.addEventListener('submit', async (e) => {
            e.preventDefault();

            const formData = {
                name: document.getElementById('name').value,
                username: document.getElementById('username').value,
                email: document.getElementById('email').value,
                phone: document.getElementById('phone').value,
                password: document.getElementById('password').value,
                experience: document.getElementById('experience').value,
                designation: document.getElementById('designation').value,
                age: Number(document.getElementById('age').value),
                registrationDateTime: getCurrentDateTime(),
                registeredBy: 'bibhabasuiitkgp'
            };

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
    }
});