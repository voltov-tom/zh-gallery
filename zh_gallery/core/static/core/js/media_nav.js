// Перелистывание работ.
//
// Компьютер: стрелки ← и → на клавиатуре.
// Телефон/планшет: свайп влево/вправо по изображению, а также тап по левому
// или правому краю картинки (по центру — ничего, чтобы не мешать зуму).
document.querySelectorAll("[data-media-nav]").forEach(function (nav) {
    function go(url) {
        if (url) {
            window.location.href = url;
        }
    }

    document.addEventListener("keydown", function (event) {
        if (event.metaKey || event.ctrlKey || event.altKey || event.shiftKey) {
            return;
        }

        var active = document.activeElement;
        if (active) {
            var tag = active.tagName;
            if (tag === "INPUT" || tag === "TEXTAREA" || tag === "SELECT" || active.isContentEditable) {
                return;
            }
        }

        if (event.key === "ArrowLeft" && nav.dataset.prev) {
            go(nav.dataset.prev);
        } else if (event.key === "ArrowRight" && nav.dataset.next) {
            go(nav.dataset.next);
        }
    });

    var coarse = window.matchMedia("(hover: none) and (pointer: coarse)").matches;
    var compact = window.matchMedia("(max-width: 640px)").matches;
    var box = document.querySelector("[data-media-zoom]");
    if ((!coarse && !compact) || !box) {
        return;
    }

    var startX = 0;
    var startY = 0;
    var startTime = 0;
    var moved = false;

    // Узкий экран без тача: листаем кликом по левому/правому краю
    if (!coarse && compact) {
        box.addEventListener("click", function (event) {
            var rect = box.getBoundingClientRect();
            var position = (event.clientX - rect.left) / rect.width;
            if (position < 0.3) {
                go(nav.dataset.prev);
            } else if (position > 0.7) {
                go(nav.dataset.next);
            }
        });
        return;
    }

    box.addEventListener(
        "touchstart",
        function (event) {
            if (event.touches.length !== 1) {
                return;
            }
            var touch = event.touches[0];
            startX = touch.clientX;
            startY = touch.clientY;
            startTime = Date.now();
            moved = false;
        },
        { passive: true }
    );

    box.addEventListener(
        "touchmove",
        function () {
            moved = true;
        },
        { passive: true }
    );

    box.addEventListener(
        "touchend",
        function (event) {
            var touch = event.changedTouches[0];
            var dx = touch.clientX - startX;
            var dy = touch.clientY - startY;
            var elapsed = Date.now() - startTime;

            // свайп: горизонтальный и достаточно длинный
            if (Math.abs(dx) > 60 && Math.abs(dx) > Math.abs(dy) * 1.4) {
                go(dx < 0 ? nav.dataset.next : nav.dataset.prev);
                return;
            }

            // тап по краю картинки
            if (!moved && elapsed < 400 && Math.abs(dx) < 10 && Math.abs(dy) < 10) {
                var rect = box.getBoundingClientRect();
                var position = (touch.clientX - rect.left) / rect.width;
                if (position < 0.3) {
                    go(nav.dataset.prev);
                } else if (position > 0.7) {
                    go(nav.dataset.next);
                }
            }
        },
        { passive: true }
    );
});
