import { ConfirmPopup } from './components/confirmPopup.js';
import { ItineraryPanelPopup } from './components/itineraryPanelPopup.js';
import { Strings } from '../../strings.js';

export class EarlyAdmissionConfirmation {
   static showEarlyAdmissionConfirmation({ onConfirm, onCancel } = {}) {
      ConfirmPopup.showItineraryConfirmPopup({
         title: Strings.itinerary.confirmation.earlyAdmissionTitle,
         message: Strings.itinerary.confirmation.earlyAdmissionMessage,
         doNotShowAgainLabel: Strings.itinerary.confirmation.doNotShowAgain,
         cancelText: Strings.itinerary.actions.cancel,
         mountEl: ItineraryPanelPopup.getItineraryPanelMountEl()
            ?? document.body,
         onConfirm,
         onCancel,
      });
   }
}
