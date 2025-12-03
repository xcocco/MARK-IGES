document.addEventListener("DOMContentLoaded", function() {
    const tabs = document.querySelectorAll(".tab");
    const inputForm = document.getElementById("input-form");
    const tablesWrapper = document.getElementById("tables-wrapper");

    tabs.forEach(tab => {
        tab.addEventListener("click", function() {
            selectTab(tab.dataset.tab);
        });
    });

    selectTab("Input")

    // File browse logic
    document.querySelectorAll('.browse-btn').forEach(function(btn) {
        btn.addEventListener('click', function() {
            const inputId = btn.getAttribute('data-input');
            const fileInput = btn.nextElementSibling;
            fileInput.click();
            fileInput.onchange = function() {
                if (fileInput.files.length > 0) {
                    document.getElementById(inputId).value = fileInput.files[0].path || fileInput.files[0].name;
                }
            };
        });
    });
});

export function createNewTab(tabName, contentNode) {
    if (document.querySelector(`.tab[data-tab="${tabName}"]`) === null) {
        const newTab = document.createElement('li')
        newTab.textContent = tabName
        newTab.classList.add('tab')
        newTab.addEventListener("click", function () {
                selectTab(newTab.dataset.tab);
            }
        );
        newTab.dataset.tab = tabName

        const tabs = document.querySelector(".tabs-container");
        tabs.appendChild(newTab)

        const tabWindow = document.querySelector(".tab-window")
        contentNode.dataset.tab = tabName
        tabWindow.appendChild(contentNode)
    }

    selectTab(tabName)
}

export function selectTab(tabName) {
    const tabs = document.querySelectorAll(".tab");
    tabs.forEach(tab => tab.classList.remove("tab-active"));

    document.querySelector(`.tab[data-tab="${tabName}"]`).classList.add("tab-active");
    document.querySelectorAll('.tab-window > *').forEach( (element) => {
            if (element.dataset.tab !== tabName) element.classList.add('tab-window-hidden')
            else element.classList.remove('tab-window-hidden')
        }
    )
    
    // Dispatch custom event for tab change
    const event = new CustomEvent('tabChanged', { detail: { tab: tabName } });
    document.dispatchEvent(event);
}

export function removeTab(tabName) {
    document.querySelector(`.tab[data-tab="${tabName}"]`).remove()
    document.querySelector(`.tab-window > *[data-tab="${tabName}"]`).remove()
    selectTab('Output')
}