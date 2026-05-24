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
} = {}) {
   const existingPopup = document.querySelector('.tzg-popup.tzg-notice');
   existingPopup?.__tzgPopupCleanup?.();
   existingPopup?.remove();

   const {
      root,
      overlay,
      buttonEls,
   } = createItineraryPopupLayout({
      popupClassName: 'tzg-notice',
      title,
      message,
      bodyContent,
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
   });

   buttonEls.ok?.addEventListener('click', close);
}
