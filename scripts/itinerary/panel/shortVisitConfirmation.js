import { ConfirmPopup } from './components/confirmPopup.js';
import { Popup } from './components/popup.js';
import { APP_STRINGS } from '../../strings.js';

export class ShortVisitConfirmation {
   static showShortVisitConfirmation({ onConfirm, onCancel } = {}) {
      const strings = APP_STRINGS.itinerary.confirmation;

      ConfirmPopup.showItineraryConfirmPopup({
         title: strings.shortVisitTitle,
         message: strings.shortVisitMessage,
         doNotShowAgainLabel: strings.doNotShowAgain,
         cancelText: APP_STRINGS.itinerary.actions.cancel,
         mountEl: Popup.getItineraryPanelMountEl()
            ?? document.body,
         onConfirm,
         onCancel,
      });
   }
}
