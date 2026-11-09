/* Миниатюра выбранной работы прямо в форме категории/подкатегории. */
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

        function update() {
            box.innerHTML = "";
            if (!select.value) {
                return;
            }
            fetch("/admin/core/mediaitem/" + select.value + "/thumb/", {
                credentials: "same-origin",
            })
                .then(function (response) {
                    return response.ok ? response.json() : null;
                })
                .then(function (data) {
                    if (!data || !data.url) {
                        return;
                    }
                    var img = document.createElement("img");
                    img.src = data.url;
                    img.alt = "";
                    img.style.maxHeight = "120px";
                    img.style.borderRadius = "8px";
                    box.appendChild(img);
                });
        }

        select.addEventListener("change", update);
        update();
    }

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", init);
    } else {
        init();
    }
})();
