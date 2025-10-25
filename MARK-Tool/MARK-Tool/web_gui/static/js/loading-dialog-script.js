export function showLoadingPopup() {
    const template = document.getElementById('loading-popup-template');
    let popup = template.content.cloneNode(true)
    document.body.appendChild(popup)

    const actionButton = document.getElementById('loading-popup-action-btn');
    actionButton.addEventListener('click', (e) => {
        hideLoadingPopup()
    })
}

export function hideLoadingPopup() {
    const popup = document.getElementById('loading-popup-container');
    if (popup) popup.remove();
}

export function addCustomAction(customLogic) {
    const actionButton = document.getElementById('loading-popup-action-btn');
    actionButton.addEventListener('click', customLogic)
}

export function showActionButton(action) {
    const button = document.getElementById('loading-popup-action-btn');
    button.style.display = 'default';
}

export function setContentText(text) {
    const content = document.getElementById('loading-content-text');
    content.textContent = text;
}

export function hideLoadingSpinner() {
    const spinner = document.getElementById('loading-spinner');
    spinner.style.display = 'none';
}