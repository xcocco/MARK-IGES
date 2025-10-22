export function showLoadingPopup() {
    const template = document.getElementById('loading-popup-template');
    let popup = template.content.cloneNode(true)
    document.body.appendChild(popup)
    // obtain the actual document element after appending it
    popup = document.getElementById('loading-popup-container')

    const topBar = document.getElementById('loading-popup-top-bar');
    topBar.style.display = 'default'
    const popupCloseButton = document.getElementById('loading-popup-top-bar-close-button');
    popupCloseButton.addEventListener('click', (e) => {
        hideLoadingPopup()
    })
}

export function hideLoadingPopup() {
    const popup = document.getElementById('loading-popup-container');
    if (popup) popup.remove();
}