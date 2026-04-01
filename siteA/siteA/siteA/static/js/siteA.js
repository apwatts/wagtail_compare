document.addEventListener("DOMContentLoaded", function () {
    var header = document.querySelector("[data-subsite-header]");
    var footerBrand = document.querySelector("[data-footer-brand]");
    var homePopup = document.querySelector("[data-home-popup]");
    var tkOverview = document.querySelector("[data-tk-overview]");
    var tkHeroClouds = document.querySelector("[data-tk-hero-clouds]");

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

    if (tkOverview) {
        function syncTkOverview() {
            var scrollProgress = Math.min(window.scrollY, 100);
            var offset = 100 - scrollProgress;

            tkOverview.style.transform = "translateY(" + offset.toFixed(1) + "px)";
        }

        syncTkOverview();
        window.addEventListener("scroll", syncTkOverview, { passive: true });
        window.addEventListener("resize", syncTkOverview);
    }

    if (tkHeroClouds) {
        function syncTkHeroClouds() {
            var scrollProgress = Math.min(window.scrollY, 100);
            var bottomOffset = -100 + scrollProgress;

            tkHeroClouds.style.bottom = bottomOffset.toFixed(1) + "px";
        }

        syncTkHeroClouds();
        window.addEventListener("scroll", syncTkHeroClouds, { passive: true });
        window.addEventListener("resize", syncTkHeroClouds);
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
