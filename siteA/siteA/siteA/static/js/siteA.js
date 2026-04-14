document.addEventListener("DOMContentLoaded", function () {
    var header = document.querySelector("[data-subsite-header]");
    var footerBrand = document.querySelector("[data-footer-brand]");
    var tkHero = document.querySelector("[data-tk-hero]");
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

    if (tkHero || tkOverview || tkHeroClouds) {
        function syncTkLayout() {
            var isMobile = window.matchMedia("(max-width: 640px)").matches;
            var scrollProgress = Math.min(window.scrollY, 100);
            var heroOffset = isMobile ? scrollProgress * 0.45 : scrollProgress;
            var overviewOffset = isMobile ? 18 - (scrollProgress * 0.18) : 50 - (scrollProgress * 0.5);
            var bottomOffset = isMobile ? -34 + (scrollProgress * 0.34) : -70 + (scrollProgress * 0.7);

            if (tkHero) {
                tkHero.style.transform = "translateY(" + heroOffset.toFixed(1) + "px)";
            }

            if (tkOverview) {
                tkOverview.style.transform = "translateY(" + overviewOffset.toFixed(1) + "px)";
            }

            if (tkHeroClouds) {
                tkHeroClouds.style.bottom = bottomOffset.toFixed(1) + "px";
            }
        }

        syncTkLayout();
        window.addEventListener("scroll", syncTkLayout, { passive: true });
        window.addEventListener("resize", syncTkLayout);
    }

    if (homePopup) {
        var popupStorageKey = homePopup.dataset.homePopupKey;

        function markHomePopupDismissed() {
            if (!popupStorageKey) {
                return;
            }

            try {
                window.localStorage.setItem(popupStorageKey, "dismissed");
            } catch (error) {
                return;
            }
        }

        function isHomePopupDismissed() {
            if (!popupStorageKey) {
                return false;
            }

            try {
                return window.localStorage.getItem(popupStorageKey) === "dismissed";
            } catch (error) {
                return false;
            }
        }

        function closeHomePopup() {
            homePopup.hidden = true;
            markHomePopupDismissed();
        }

        if (!isHomePopupDismissed()) {
            homePopup.hidden = false;
        }

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
