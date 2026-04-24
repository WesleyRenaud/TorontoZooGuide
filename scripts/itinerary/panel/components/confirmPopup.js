import {
   createItineraryPopupLayout,
   mountDismissablePopup,
} from './popup.js';

export function showItineraryConfirmPopup({
   title = 'Heads up',
   message = '',
   confirmText = 'Confirm',
   cancelText = 'Cancel',
   onConfirm,
   onCancel,
} = {}) {
   const existingPopup = document.querySelector('.tzg-popup.tzg-confirm');
   existingPopup?.__tzgPopupCleanup?.();
   existingPopup?.remove();

   const {
      root,
      overlay,
      buttonEls,
   } = createItineraryPopupLayout({
      popupClassName: 'tzg-confirm',
      title,
      message,
      actionsClassName: 'tzg-popup-actions',
      actionButtons: [
         {
            key: 'cancel',
            className: 'itin-prev tzg-popup-cancel',
            text: cancelText,
         },
         {
            key: 'confirm',
            className: 'itin-next tzg-popup-confirm',
            text: confirmText,
         },
      ],
   });

   const { close, dismiss } = mountDismissablePopup({
      mountEl: document.body,
      root,
      overlay,
      initialFocusEl: buttonEls.confirm,
      onDismiss: onCancel,
   });

   buttonEls.cancel?.addEventListener('click', dismiss);
   buttonEls.confirm?.addEventListener('click', () => {
      onConfirm?.();
      close();
   });
}
