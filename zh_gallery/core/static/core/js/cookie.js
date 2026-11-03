// Информационная плашка про технические cookie.
// Согласие хранится в localStorage: никаких дополнительных cookie не ставим,
// поэтому баннер не блокирует сайт и не требует отдельного согласия.

const STORAGE_KEY = "zh-gallery:cookie-notice-accepted";

function storageGet(key) {
    try {
        return window.localStorage.getItem(key);
    } catch (error) {
        return null;
    }
}

function storageSet(key, value) {
    try {
        window.localStorage.setItem(key, value);
    } catch (error) {
        // приватный режим — просто не запоминаем
    }
}

const notice = document.querySelector("[data-cookie-notice]");
if (notice && !storageGet(STORAGE_KEY)) {
    notice.hidden = false;

    const accept = notice.querySelector("[data-cookie-accept]");
    if (accept) {
        accept.addEventListener("click", () => {
            storageSet(STORAGE_KEY, new Date().toISOString());
            notice.hidden = true;
        });
    }
}
