export function cleanupConfirmPopup() {
   document.querySelector('.tzg-confirm')?.__tzgPopupCleanup?.();
   document.querySelector('.tzg-confirm')?.remove();
}

export function cleanupNoticePopup() {
   document.querySelector('.tzg-notice')?.__tzgPopupCleanup?.();
   document.querySelector('.tzg-notice')?.remove();
}
