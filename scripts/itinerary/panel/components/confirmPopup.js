import { el } from '../dom.js';
import {
   createItineraryPopupLayout,
   getItineraryOverlayMountEl,
   mountDismissablePopup,
} from './popup.js';
import { APP_STRINGS } from '../../../strings.js';

const { actions } = APP_STRINGS.itinerary;

function createConfirmPopupBody(message, doNotShowAgainLabel) {
   const body = el('div', 'tzg-popup-confirm-body');

   body.appendChild(
      el('div', 'tzg-popup-message', message)
   );

   if (!doNotShowAgainLabel) {
      return body;
   }

   const label = el('label', 'toggle-row tzg-popup-do-not-show-again');
   const checkbox = el('input');
   checkbox.type = 'checkbox';

   label.append(checkbox, ` ${doNotShowAgainLabel}`);
   body.appendChild(label);

   return {
      body,
      checkbox,
   };
}

export function showItineraryConfirmPopup({
   title = APP_STRINGS.common.headsUp,
   message = '',
   bodyContent = null,
   confirmText = actions.confirm,
   cancelText = actions.cancel,
   doNotShowAgainLabel = null,
   mountEl = getItineraryOverlayMountEl() ?? document.body,
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
   } = createItineraryPopupLayout({
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

   const { close, dismiss } = mountDismissablePopup({
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
