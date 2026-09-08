import { ConfirmFragment } from './components/confirmFragment.js';
import { ItineraryPanelFragment } from './components/itineraryPanelFragment.js';
import { Strings } from '../../strings.js';

export class ShortVisitFragment {
   static showShortVisitConfirmation({ onConfirm, onCancel } = {}) {
      ConfirmFragment.showItineraryConfirmPopup({
         title: Strings.itinerary.confirmation.shortVisitTitle,
         message: Strings.itinerary.confirmation.shortVisitMessage,
         doNotShowAgainLabel: Strings.itinerary.confirmation.doNotShowAgain,
         cancelText: Strings.itinerary.actions.cancel,
         mountEl: ItineraryPanelFragment.getItineraryPanelMountEl()
            ?? document.body,
         onConfirm,
         onCancel,
      });
   }
}
