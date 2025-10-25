export function showLoadingPopup() {
    const template = document.getElementById('loading-popup-template');
    let popup = template.content.cloneNode(true)
    document.body.appendChild(popup)

    const actionButton = document.getElementById('loading-popup-action-btn');
    actionButton.style.display = 'none';
}

export function hideLoadingPopup() {
    const popup = document.getElementById('loading-popup-container');
    if (popup) popup.remove();
}

export function addCustomAction(customLogic) {
    const actionButton = document.getElementById('loading-popup-action-btn');
    actionButton.addEventListener('click', customLogic)
}

export function removeAllCustomActions(customLogic) {
    let old_element = document.getElementById("loading-popup-action-btn");
    let new_element = old_element.cloneNode(true);
    old_element.parentNode.replaceChild(new_element, old_element);
}

export function showActionButton() {
    const button = document.getElementById('loading-popup-action-btn');
    button.style.display = 'block';
}

export function setContentText(text) {
    const content = document.getElementById('loading-content-text');
    content.textContent = text;
}

export function hideLoadingSpinner() {
    const spinner = document.getElementById('loading-spinner');
    spinner.style.display = 'none';
}

export function hideActionButton() {
    const button = document.getElementById('loading-popup-action-btn');
    button.style.display = 'none';
}