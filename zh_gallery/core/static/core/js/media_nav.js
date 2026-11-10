// Перелистывание работ стрелками клавиатуры: ← предыдущая, → следующая.
// Работает только когда фокус не в поле ввода.
document.querySelectorAll("[data-media-nav]").forEach(function (nav) {
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
            window.location.href = nav.dataset.prev;
        } else if (event.key === "ArrowRight" && nav.dataset.next) {
            window.location.href = nav.dataset.next;
        }
    });
});
