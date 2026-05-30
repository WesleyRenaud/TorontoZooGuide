import { showItineraryConfirmPopup } from './components/confirmPopup.js';
import { getItineraryPanelMountEl } from './components/popup.js';
import { APP_STRINGS } from '../../strings.js';

export function showShortVisitConfirmation({ onConfirm, onCancel } = {}) {
   const strings = APP_STRINGS.itinerary.confirmation;

   showItineraryConfirmPopup({
      title: strings.shortVisitTitle,
      message: strings.shortVisitMessage,
      cancelText: APP_STRINGS.itinerary.actions.cancel,
      mountEl: getItineraryPanelMountEl()
         ?? document.body,
      onConfirm,
      onCancel,
   });
}
