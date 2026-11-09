/* Миниатюра выбранной работы в форме категории/подкатегории.
 *
 * Django-админка использует select2 (django.jQuery), который по выбору
 * элемента вызывает jQuery-события change / select2:select, а нативный
 * addEventListener("change") при этом не срабатывает. Поэтому подписываемся
 * и на jQuery, и на нативный обработчик — на случай отключённого select2.
 */
(function () {
    "use strict";

    function init() {
        var select = document.getElementById("id_preview_item");
        if (!select) {
            return;
        }

        var box = document.getElementById("preview-thumb");
        if (!box) {
            box = document.createElement("div");
            box.id = "preview-thumb";
            box.style.marginTop = "8px";
            var row = select.closest(".form-row") || select.parentElement;
            row.appendChild(box);
        }

        var lastId = null;

        function show(id) {
            if (id === lastId) {
                return;
            }
            lastId = id;
            box.innerHTML = "";

            if (!id) {
                return;
            }

            var img = document.createElement("img");
            img.alt = "";
            img.style.maxHeight = "120px";
            img.style.borderRadius = "8px";
            img.style.opacity = "0.4";
            box.appendChild(img);

            fetch("/admin/core/mediaitem/" + id + "/thumb/", {
                credentials: "same-origin",
            })
                .then(function (response) {
                    return response.ok ? response.json() : null;
                })
                .then(function (data) {
                    if (!data || !data.url || lastId !== id) {
                        img.remove();
                        return;
                    }
                    img.src = data.url;
                    img.style.opacity = "1";
                })
                .catch(function () {
                    img.remove();
                });
        }

        function update() {
            show(select.value);
        }

        select.addEventListener("change", update);

        var jq = (window.django && window.django.jQuery) || window.jQuery;
        if (jq) {
            jq(select).on(
                "change select2:select select2:clear select2:unselect",
                update
            );
        }

        update();
    }

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", init);
    } else {
        init();
    }
})();
