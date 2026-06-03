import { showItineraryConfirmPopup } from './components/confirmPopup.js';
import { getItineraryOverlayMountEl } from './components/popup.js';
import { APP_STRINGS } from '../../strings.js';

export function showGuardiansTalkUnscheduleConfirmation({
   onConfirm,
   onCancel,
   mountEl = getItineraryOverlayMountEl() ?? document.body,
} = {}) {
   const strings = APP_STRINGS.itinerary.confirmation;

   showItineraryConfirmPopup({
      title: strings.guardiansTalkUnscheduleTitle,
      message: strings.guardiansTalkUnscheduleMessage,
      confirmText: strings.guardiansTalkUnscheduleConfirm,
      cancelText: APP_STRINGS.itinerary.actions.cancel,
      mountEl,
      onConfirm,
      onCancel,
   });
}
