// Базовое поведение страниц: прелоадер, мобильное меню, кнопка «наверх».
// Раньше это были три инлайн-скрипта в base.html.

function hidePreloader() {
    document.body.classList.add('loaded_hiding');
    window.setTimeout(() => {
        document.body.classList.add('loaded');
        document.body.classList.remove('loaded_hiding');
    }, 500);
}

function initPreloader() {
    window.addEventListener('load', hidePreloader);
}

function initBurger() {
    const burgers = Array.from(document.querySelectorAll('.navbar-burger'));
    burgers.forEach((burger) => {
        burger.addEventListener('click', () => {
            const target = document.getElementById(burger.dataset.target);
            if (!target) {
                return;
            }
            burger.classList.toggle('is-active');
            target.classList.toggle('is-active');
        });
    });
}

function initTopButton() {
    const button = document.getElementById('topButton');
    if (!button) {
        return;
    }
    button.hidden = false;
    button.style.display = 'none';

    const toggle = () => {
        const scrolled = document.body.scrollTop > 20 || document.documentElement.scrollTop > 20;
        button.style.display = scrolled ? 'block' : 'none';
    };

    window.addEventListener('scroll', toggle, { passive: true });
    button.addEventListener('click', () => {
        document.body.scrollTop = 0;
        document.documentElement.scrollTop = 0;
    });
    toggle();
}

const onReady = (callback) => {
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', callback);
    } else {
        callback();
    }
};

onReady(() => {
    initPreloader();
    initBurger();
    initTopButton();
});
