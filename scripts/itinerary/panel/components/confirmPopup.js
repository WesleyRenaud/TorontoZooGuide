import { ConfirmPopupHelpers } from './confirmPopupHelpers.js';
import { ItineraryPanelPopup } from './itineraryPanelPopup.js';
import { Strings } from '../../../strings.js';

export class ConfirmPopup {
   static showItineraryConfirmPopup({
      title = Strings.common.headsUp,
      message = '',
      bodyContent = null,
      confirmText = Strings.itinerary.actions.confirm,
      cancelText = Strings.itinerary.actions.cancel,
      doNotShowAgainLabel = null,
      mountEl = ItineraryPanelPopup.getItineraryOverlayMountEl() ?? document.body,
      onConfirm,
      onCancel,
   } = {}) {
      const existingPopup = document.querySelector('.tzg-popup.tzg-confirm');
      existingPopup?.__tzgPopupCleanup?.();
      existingPopup?.remove();

      const confirmBody = bodyContent
         ? { body: bodyContent }
         : ConfirmPopupHelpers.createConfirmPopupBody(message, doNotShowAgainLabel);

      const {
         root,
         overlay,
         buttonEls,
      } = ItineraryPanelPopup.createItineraryPopupLayout({
         popupClassName: 'tzg-confirm',
         title,
         bodyContent: confirmBody.body ?? confirmBody,
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

      const { close, dismiss } = ItineraryPanelPopup.mountDismissablePopup({
         mountEl,
         root,
         overlay,
         initialFocusEl: buttonEls.confirm,
         onDismiss: onCancel,
      });

      buttonEls.cancel?.addEventListener('click', dismiss);
      buttonEls.confirm?.addEventListener('click', () => {
         onConfirm?.({
            doNotShowAgain: Boolean(confirmBody.checkbox?.checked),
         });
         close();
      });
   }
}
