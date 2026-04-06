/* ============================================
   RoboMarket — Enhanced JavaScript
   Intersection Observer · Smooth interactions
   ============================================ */

document.addEventListener('DOMContentLoaded', function () {

    // ---------- Header scroll effect ----------
    const header = document.getElementById('header');
    if (header) {
        let lastScroll = 0;
        window.addEventListener('scroll', function () {
            const currentScroll = window.scrollY;
            if (currentScroll > 20) {
                header.classList.add('scrolled');
            } else {
                header.classList.remove('scrolled');
            }
            lastScroll = currentScroll;
        }, { passive: true });
    }

    // ---------- Мобильное меню с анимацией ----------
    const burger = document.getElementById('burger');
    const mobileMenu = document.getElementById('mobile-menu');

    if (burger && mobileMenu) {
        burger.addEventListener('click', function () {
            burger.classList.toggle('active');
            mobileMenu.classList.toggle('open');
        });

        // Закрытие при клике на ссылку
        mobileMenu.querySelectorAll('.nav-link').forEach(function (link) {
            link.addEventListener('click', function () {
                burger.classList.remove('active');
                mobileMenu.classList.remove('open');
            });
        });
    }

    // ---------- Intersection Observer для appear-анимаций ----------
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry, index) {
            if (entry.isIntersecting) {
                // Stagger анимация — каждый элемент с задержкой
                const delay = Array.from(entry.target.parentElement.children)
                    .filter(el => el.classList.contains('appear'))
                    .indexOf(entry.target) * 100;

                setTimeout(function () {
                    entry.target.classList.add('visible');
                }, delay);

                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    document.querySelectorAll('.appear').forEach(function (el) {
        observer.observe(el);
    });

    // ---------- Автоскрытие алертов ----------
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(function (alert) {
        setTimeout(function () {
            alert.style.opacity = '0';
            alert.style.transform = 'translateY(-10px)';
            alert.style.transition = 'all 0.4s ease';
            setTimeout(function () {
                alert.remove();
            }, 400);
        }, 5000);
    });

    // ---------- Валидация формы регистрации ----------
    const registerForm = document.getElementById('register-form');
    if (registerForm) {
        registerForm.addEventListener('submit', function (e) {
            const password = registerForm.querySelector('#password').value;
            const confirm = registerForm.querySelector('#password_confirm').value;

            if (password.length < 6) {
                e.preventDefault();
                showNotification('Пароль должен содержать минимум 6 символов', 'error');
                return;
            }

            if (password !== confirm) {
                e.preventDefault();
                showNotification('Пароли не совпадают', 'error');
                return;
            }
        });
    }

    // ---------- Валидация формы контактов ----------
    const contactForm = document.getElementById('contact-form');
    if (contactForm) {
        contactForm.addEventListener('submit', function (e) {
            const name = contactForm.querySelector('#name').value.trim();
            const email = contactForm.querySelector('#email').value.trim();
            const subject = contactForm.querySelector('#subject').value.trim();
            const message = contactForm.querySelector('#message').value.trim();

            if (!name || !email || !subject || !message) {
                e.preventDefault();
                showNotification('Пожалуйста, заполните все обязательные поля', 'error');
                return;
            }

            if (!isValidEmail(email)) {
                e.preventDefault();
                showNotification('Введите корректный email', 'error');
                return;
            }
        });
    }

    // ---------- Input focus glow effect ----------
    document.querySelectorAll('.form-group input, .form-group textarea, .form-group select').forEach(function (input) {
        input.addEventListener('focus', function () {
            this.parentElement.classList.add('focused');
        });
        input.addEventListener('blur', function () {
            this.parentElement.classList.remove('focused');
        });
    });

    // ---------- Подтверждение удаления ----------
    const deleteForms = document.querySelectorAll('.delete-confirm');
    deleteForms.forEach(function (form) {
        form.addEventListener('submit', function (e) {
            if (!confirm('Вы уверены?')) {
                e.preventDefault();
            }
        });
    });

    // ---------- Smooth scroll для якорных ссылок ----------
    document.querySelectorAll('a[href^="#"]').forEach(function (anchor) {
        anchor.addEventListener('click', function (e) {
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                e.preventDefault();
                target.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }
        });
    });

});

// ---------- Изменение количества в корзине ----------
function changeQuantity(btn, delta) {
    const form = btn.closest('form');
    const input = form.querySelector('.qty-input');
    let value = parseInt(input.value) + delta;
    if (value < 1) value = 1;
    input.value = value;
    form.submit();
}

// ---------- Уведомления — Premium стиль ----------
function showNotification(message, type) {
    const existing = document.querySelectorAll('.notification');
    existing.forEach(function (el) { el.remove(); });

    const div = document.createElement('div');
    div.className = 'notification notification-' + type;
    div.innerHTML = '<span class="notification-text">' + message + '</span>';
    div.style.cssText = 'position:fixed;top:90px;right:24px;padding:16px 28px;border-radius:14px;color:white;font-weight:600;font-size:.9rem;z-index:9999;max-width:420px;animation:slideIn .4s cubic-bezier(.4,0,.2,1);backdrop-filter:blur(10px);-webkit-backdrop-filter:blur(10px);';

    if (type === 'error') {
        div.style.background = 'linear-gradient(135deg, #ef4444, #dc2626)';
        div.style.boxShadow = '0 8px 32px rgba(239,68,68,.3)';
    } else if (type === 'success') {
        div.style.background = 'linear-gradient(135deg, #10b981, #059669)';
        div.style.boxShadow = '0 8px 32px rgba(16,185,129,.3)';
    } else {
        div.style.background = 'linear-gradient(135deg, #6366f1, #a855f7)';
        div.style.boxShadow = '0 8px 32px rgba(99,102,241,.3)';
    }

    document.body.appendChild(div);

    setTimeout(function () {
        div.style.opacity = '0';
        div.style.transform = 'translateX(30px)';
        div.style.transition = 'all 0.4s ease';
        setTimeout(function () { div.remove(); }, 400);
    }, 4000);
}

// ---------- Валидация email ----------
function isValidEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

// ---------- Keyframes ----------
const style = document.createElement('style');
style.textContent = '@keyframes slideIn{from{transform:translateX(100%);opacity:0}to{transform:translateX(0);opacity:1}}';
document.head.appendChild(style);
