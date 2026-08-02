import { showItineraryConfirmPopup } from './components/confirmPopup.js';
import { getItineraryPanelMountEl } from './components/popup.js';
import { APP_STRINGS } from '../../strings.js';

export function showAttractionOutsideOperatingHoursConfirmation({
   onConfirm,
   onCancel,
} = {}) {
   const strings = APP_STRINGS.itinerary.confirmation;

   showItineraryConfirmPopup({
      title: strings.attractionOutsideOperatingHoursTitle,
      message: strings.attractionOutsideOperatingHoursMessage,
      confirmText: APP_STRINGS.itinerary.actions.adjust,
      cancelText: APP_STRINGS.itinerary.actions.cancel,
      mountEl: getItineraryPanelMountEl() ?? document.body,
      onConfirm,
      onCancel,
   });
}
