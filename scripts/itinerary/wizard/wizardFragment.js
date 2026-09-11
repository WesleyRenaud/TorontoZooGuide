import { ItineraryPanelFragment } from '../panel/components/itineraryPanelFragment.js';
import { Strings } from '../../strings.js';

export class WizardFragment {
   static showItineraryWizardPopup({
      mountEl,
      title = Strings.common.headsUp,
      message = '',
      buttonText = Strings.itinerary.actions.ok,
   } = {}) {
      if (!mountEl) return;

      const existingPopup = mountEl.querySelector('.tzg-popup');
      existingPopup?.__tzgPopupCleanup?.();
      existingPopup?.remove();

      const {
         root,
         overlay,
         buttonEls,
      } = ItineraryPanelFragment.createItineraryPopupLayout({
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

      const { close } = ItineraryPanelFragment.mountDismissablePopup({
         mountEl,
         root,
         overlay,
         initialFocusEl: buttonEls.ok,
      });

      buttonEls.ok?.addEventListener('click', close);
   }
}
