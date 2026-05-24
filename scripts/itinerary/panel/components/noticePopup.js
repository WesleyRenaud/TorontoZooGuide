import {
   createItineraryPopupLayout,
   mountDismissablePopup,
} from './popup.js';
import { APP_STRINGS } from '../../../strings.js';

export function showItineraryNoticePopup({
   title = 'Heads up',
   message = '',
   bodyContent = null,
   buttonText = APP_STRINGS.itinerary.noItemsSelected.button,
   onConfirm = null,
   showCloseButton = false,
   onClose = null,
} = {}) {
   const existingPopup = document.querySelector('.tzg-popup.tzg-notice');
   existingPopup?.__tzgPopupCleanup?.();
   existingPopup?.remove();

   const {
      root,
      overlay,
      buttonEls,
      closeButton,
   } = createItineraryPopupLayout({
      popupClassName: 'tzg-notice',
      title,
      message,
      bodyContent,
      showCloseButton,
      actionsClassName: 'tzg-popup-actions',
      actionButtons: [
         {
            key: 'ok',
            className: 'itin-next tzg-popup-confirm',
            text: buttonText,
         },
      ],
   });

   const { close } = mountDismissablePopup({
      mountEl: document.body,
      root,
      overlay,
      initialFocusEl: buttonEls.ok,
      dismissOnOverlayClick: false,
      dismissOnEscape: false,
   });

   buttonEls.ok?.addEventListener('click', async () => {
      buttonEls.ok.disabled = true;

      try {
         const shouldClose = await onConfirm?.({ close });

         if (shouldClose !== false) {
            close();
         }
      }
      catch (error) {
         buttonEls.ok.disabled = false;
         throw error;
      }

      buttonEls.ok.disabled = false;
   });

   closeButton?.addEventListener('click', () => {
      onClose?.({ close });
   });
}
