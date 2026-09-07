import { ConfirmPopup } from './components/confirmPopup.js';
import { ItineraryPanelPopup } from './components/itineraryPanelPopup.js';
import { Strings } from '../../strings.js';

export class ShortVisitConfirmation {
   static showShortVisitConfirmation({ onConfirm, onCancel } = {}) {
      ConfirmPopup.showItineraryConfirmPopup({
         title: Strings.itinerary.confirmation.shortVisitTitle,
         message: Strings.itinerary.confirmation.shortVisitMessage,
         doNotShowAgainLabel: Strings.itinerary.confirmation.doNotShowAgain,
         cancelText: Strings.itinerary.actions.cancel,
         mountEl: ItineraryPanelPopup.getItineraryPanelMountEl()
            ?? document.body,
         onConfirm,
         onCancel,
      });
   }
}
