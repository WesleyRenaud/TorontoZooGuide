import { Dom } from '../dom.js';
import { Popup } from './popup.js';
import { Strings } from '../../../strings.js';

function createConfirmPopupBody(message, doNotShowAgainLabel) {
   const body = Dom.el('div', 'tzg-popup-confirm-body');

   body.appendChild(
      Dom.el('div', 'tzg-popup-message', message)
   );

   if (!doNotShowAgainLabel) {
      return body;
   }

   const label = Dom.el('label', 'toggle-row tzg-popup-do-not-show-again');
   const checkbox = Dom.el('input');
   checkbox.type = 'checkbox';

   label.append(checkbox, ` ${doNotShowAgainLabel}`);
   body.appendChild(label);

   return {
      body,
      checkbox,
   };
}

export class ConfirmPopup {
   static showItineraryConfirmPopup({
      title = Strings.common.headsUp,
      message = '',
      bodyContent = null,
      confirmText = Strings.itinerary.actions.confirm,
      cancelText = Strings.itinerary.actions.cancel,
      doNotShowAgainLabel = null,
      mountEl = Popup.getItineraryOverlayMountEl() ?? document.body,
      onConfirm,
      onCancel,
   } = {}) {
      const existingPopup = document.querySelector('.tzg-popup.tzg-confirm');
      existingPopup?.__tzgPopupCleanup?.();
      existingPopup?.remove();

      const confirmBody = bodyContent
         ? { body: bodyContent }
         : createConfirmPopupBody(message, doNotShowAgainLabel);

      const {
         root,
         overlay,
         buttonEls,
      } = Popup.createItineraryPopupLayout({
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

      const { close, dismiss } = Popup.mountDismissablePopup({
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
