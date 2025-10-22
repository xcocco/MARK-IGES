export function showLoadingPopup() {
    const template = document.getElementById('loading-popup-template');
    let popup = template.content.cloneNode(true)
    document.body.appendChild(popup)
    // obtain the actual document element after appending it
    popup = document.getElementById('loading-popup-container')

    const topBar = document.getElementById('loading-popup-top-bar');
    topBar.style.display = 'none'
    const popupCloseButton = document.getElementById('loading-popup-top-bar-close-button');
    popupCloseButton.addEventListener('click', (e) => {
        hideLoadingPopup()
    })
}

export function hideLoadingPopup() {
    const popup = document.getElementById('loading-popup-container');
    if (popup) popup.remove();
}

export function showTopBar() {
    const topBar = document.getElementById('loading-popup-top-bar');
    topBar.style.display = 'inline-block';
}

export function setContentText(text) {
    const content = document.getElementById('loading-content-text');
    content.textContent = text;
}

export function hideLoadingSpinner() {
    const spinner = document.getElementById('loading-spinner');
    spinner.style.display = 'none';
}