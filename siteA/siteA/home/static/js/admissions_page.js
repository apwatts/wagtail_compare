document.addEventListener("DOMContentLoaded", function () {
    var tabsRoot = document.querySelector("[data-admissions-tabs]");

    if (!tabsRoot) {
        return;
    }

    var tabs = Array.from(tabsRoot.querySelectorAll("[data-admissions-tab]"));
    var panels = Array.from(tabsRoot.querySelectorAll(".admissions-panel[role='tabpanel']"));

    function setActivePanel(targetId) {
        tabs.forEach(function (tab) {
            var isActive = tab.getAttribute("data-target") === targetId;
            tab.classList.toggle("is-active", isActive);
            tab.setAttribute("aria-selected", isActive ? "true" : "false");
            tab.setAttribute("tabindex", isActive ? "0" : "-1");
        });

        panels.forEach(function (panel) {
            var isActive = panel.id === targetId;
            panel.classList.toggle("is-active", isActive);
            panel.hidden = !isActive;
            panel.setAttribute("aria-hidden", isActive ? "false" : "true");
        });
    }

    if (tabs.length > 0) {
        setActivePanel(tabs[0].getAttribute("data-target"));
    }

    tabs.forEach(function (tab) {
        tab.addEventListener("click", function () {
            setActivePanel(tab.getAttribute("data-target"));
        });
    });
});
