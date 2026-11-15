// Яндекс Метрика — только после согласия на аналитические cookie.
//
// Счётчик грузится не из HTML, а отсюда: пока человек не нажал «Согласен»,
// ни одного запроса на mc.yandex.ru не уходит (152-ФЗ, да и тест
// test_no_external_scripts_or_styles проверяет статику страницы).
// Согласие хранит cookie.js в localStorage, оттуда же берём его здесь.

const STORAGE_KEY = "zh-gallery:cookie-notice-accepted";
const ACCEPT_EVENT = "zh-gallery:cookie-accepted";

const tag = document.currentScript || document.querySelector("script[data-metrika-id]");
const counterId = tag ? tag.dataset.metrikaId : "";

function hasConsent() {
    try {
        return Boolean(window.localStorage.getItem(STORAGE_KEY));
    } catch (error) {
        return false;
    }
}

function loadCounter() {
    if (!counterId || window.__zhMetrikaLoaded) {
        return;
    }
    window.__zhMetrikaLoaded = true;

    (function (m, e, t, r, i, k, a) {
        m[i] =
            m[i] ||
            function () {
                (m[i].a = m[i].a || []).push(arguments);
            };
        m[i].l = Number(new Date());
        for (let j = 0; j < e.scripts.length; j++) {
            if (e.scripts[j].src === r) {
                return;
            }
        }
        k = e.createElement(t);
        a = e.getElementsByTagName(t)[0];
        k.async = true;
        k.src = r;
        a.parentNode.insertBefore(k, a);
    })(window, document, "script", `https://mc.yandex.ru/metrika/tag.js?id=${counterId}`, "ym");

    window.ym(counterId, "init", {
        ssr: true,
        webvisor: true,
        clickmap: true,
        trackLinks: true,
        accurateTrackBounce: true,
        referrer: document.referrer,
        url: window.location.href,
    });
}

if (counterId) {
    if (hasConsent()) {
        loadCounter();
    }
    window.addEventListener(ACCEPT_EVENT, loadCounter);
}
