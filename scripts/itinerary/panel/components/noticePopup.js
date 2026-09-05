import { Popup } from './popup.js';
import { APP_STRINGS } from '../../../strings.js';

export class NoticePopup {
   static showItineraryNoticePopup({
      title = APP_STRINGS.common.headsUp,
      message = '',
      bodyContent = null,
      buttonText = APP_STRINGS.itinerary.noItemsSelected.button,
      mountEl = Popup.getItineraryOverlayMountEl() ?? document.body,
      onConfirm = null,
      showCloseButton = false,
      onClose = null,
   } = {}) {
      const existingPopup = mountEl.querySelector?.('.tzg-popup.tzg-notice')
         ?? document.querySelector('.tzg-popup.tzg-notice');
      existingPopup?.__tzgPopupCleanup?.();
      existingPopup?.remove();

      const {
         root,
         overlay,
         buttonEls,
         closeButton,
      } = Popup.createItineraryPopupLayout({
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

      const { close } = Popup.mountDismissablePopup({
         mountEl,
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
}
