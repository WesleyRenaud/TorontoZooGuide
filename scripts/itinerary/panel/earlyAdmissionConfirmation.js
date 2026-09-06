import { ConfirmPopup } from './components/confirmPopup.js';
import { Popup } from './components/popup.js';
import { Strings } from '../../strings.js';

export class EarlyAdmissionConfirmation {
   static showEarlyAdmissionConfirmation({ onConfirm, onCancel } = {}) {
      const strings = Strings.itinerary.confirmation;

      ConfirmPopup.showItineraryConfirmPopup({
         title: strings.earlyAdmissionTitle,
         message: strings.earlyAdmissionMessage,
         doNotShowAgainLabel: strings.doNotShowAgain,
         cancelText: Strings.itinerary.actions.cancel,
         mountEl: Popup.getItineraryPanelMountEl()
            ?? document.body,
         onConfirm,
         onCancel,
      });
   }
}
