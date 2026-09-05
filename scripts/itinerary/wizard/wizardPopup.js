import {
   createItineraryPopupLayout,
   mountDismissablePopup,
} from '../panel/components/popup.js';
import { APP_STRINGS } from '../../strings.js';

export class WizardPopup {
   static showItineraryWizardPopup({
      mountEl,
      title = APP_STRINGS.common.headsUp,
      message = '',
      buttonText = APP_STRINGS.itinerary.noItemsSelected.button,
   } = {}) {
      if (!mountEl) return;

      const existingPopup = mountEl.querySelector('.tzg-popup');
      existingPopup?.__tzgPopupCleanup?.();
      existingPopup?.remove();

      const {
         root,
         overlay,
         buttonEls,
      } = createItineraryPopupLayout({
         title,
         message,
         actionButtons: [
            {
               key: 'ok',
               className: 'itin-next tzg-popup-ok',
               text: buttonText,
            },
         ],
      });

      const { close } = mountDismissablePopup({
         mountEl,
         root,
         overlay,
         initialFocusEl: buttonEls.ok,
      });

      buttonEls.ok?.addEventListener('click', close);
   }
}
