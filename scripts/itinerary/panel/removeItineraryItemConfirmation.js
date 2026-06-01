import { showItineraryConfirmPopup } from './components/confirmPopup.js';
import { getItineraryPanelMountEl } from './components/popup.js';
import { APP_STRINGS } from '../../strings.js';

export function showRemoveItineraryItemConfirmation({
   onConfirm,
   onCancel,
} = {}) {
   const strings = APP_STRINGS.itinerary.confirmation;

   showItineraryConfirmPopup({
      title: strings.removeItemTitle,
      message: strings.removeItemMessage,
      confirmText: APP_STRINGS.itinerary.dayPlanner.remove,
      cancelText: APP_STRINGS.itinerary.actions.cancel,
      mountEl: getItineraryPanelMountEl() ?? document.body,
      onConfirm,
      onCancel,
   });
}
