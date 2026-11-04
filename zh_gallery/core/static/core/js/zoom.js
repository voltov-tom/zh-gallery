// Увеличение картинки наведением: курсор двигается — растёт та часть, на
// которую он указывает. Кликать не нужно, поэтому работает и с клавиатуры
// (Tab — увеличение по центру).

const MAX_ZOOM = 3;
const MIN_ZOOM = 1.8;

// На тач-устройствах наведения нет: тап фокусировал бы картинку и включал зум,
// а пользователь и так увеличивает жестами. Поэтому там зум не подключаем вовсе.
const supportsHover = window.matchMedia("(hover: hover) and (pointer: fine)").matches;

function initZoom(box) {
    if (!supportsHover) {
        return;
    }

    const image = box.querySelector("img");
    if (!image) {
        return;
    }

    // Насколько сильно увеличивать: примерно «один пиксель картинки на пиксель
    // экрана», но в разумных пределах.
    const naturalZoom = () => {
        const rendered = image.clientWidth || 1;
        const natural = image.naturalWidth || rendered;
        return Math.min(MAX_ZOOM, Math.max(MIN_ZOOM, natural / rendered));
    };

    const applyOrigin = (event) => {
        const rect = box.getBoundingClientRect();
        if (!rect.width || !rect.height) {
            return;
        }
        const x = ((event.clientX - rect.left) / rect.width) * 100;
        const y = ((event.clientY - rect.top) / rect.height) * 100;
        image.style.transformOrigin = `${x}% ${y}%`;
    };

    const zoomIn = () => {
        image.style.setProperty("--zoom-scale", naturalZoom().toFixed(2));
        box.classList.add("is-zoomed");
    };

    const zoomOut = () => {
        box.classList.remove("is-zoomed");
    };

    box.addEventListener("pointerenter", (event) => {
        if (event.pointerType === "mouse") {
            applyOrigin(event);
            zoomIn();
        }
    });

    box.addEventListener("pointermove", (event) => {
        if (box.classList.contains("is-zoomed")) {
            applyOrigin(event);
        }
    });

    box.addEventListener("pointerleave", zoomOut);

    // Клавиатура: фокус на контейнере — увеличение по центру
    box.tabIndex = 0;
    box.addEventListener("focus", () => {
        image.style.transformOrigin = "50% 50%";
        zoomIn();
    });
    box.addEventListener("blur", zoomOut);
}

document.querySelectorAll("[data-media-zoom]").forEach(initZoom);
