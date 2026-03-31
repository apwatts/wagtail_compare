document.addEventListener("DOMContentLoaded", function () {
    var header = document.querySelector("[data-subsite-header]");
    var footerBrand = document.querySelector("[data-footer-brand]");
    var homePopup = document.querySelector("[data-home-popup]");

    function syncHeaderState() {
        if (!header) {
            return;
        }

        header.classList.toggle("is-solid", window.scrollY > 24);
    }

    if (header) {
        syncHeaderState();
        window.addEventListener("scroll", syncHeaderState, { passive: true });
    }

    if (homePopup) {
        function closeHomePopup() {
            homePopup.hidden = true;
        }

        homePopup.hidden = false;

        homePopup.querySelectorAll("[data-home-popup-close]").forEach(function (element) {
            element.addEventListener("click", closeHomePopup);
        });

        document.addEventListener("keydown", function (event) {
            if (event.key === "Escape") {
                closeHomePopup();
            }
        });
    }

    if (!footerBrand) {
        return;
    }

    function collapseFooterBrand() {
        footerBrand.classList.remove("is-expanded");
    }

    footerBrand.addEventListener("click", function (event) {
        if (!window.matchMedia("(hover: none), (pointer: coarse)").matches) {
            return;
        }

        if (!footerBrand.classList.contains("is-expanded")) {
            event.preventDefault();
            footerBrand.classList.add("is-expanded");
        }
    });

    document.addEventListener("pointerdown", function (event) {
        if (!footerBrand.contains(event.target)) {
            collapseFooterBrand();
        }
    });

    window.addEventListener("scroll", collapseFooterBrand, { passive: true });
    window.addEventListener("blur", collapseFooterBrand);
});
