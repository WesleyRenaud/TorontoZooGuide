import { showItineraryConfirmPopup } from '../panel/components/confirmPopup.js';
import { APP_STRINGS } from '../../strings.js';

export function showSaveIssuesProceedConfirmation({
   title,
   message,
   onConfirm,
} = {}) {
   showItineraryConfirmPopup({
      title,
      message,
      confirmText: APP_STRINGS.itinerary.confirmation.proceedAnyway,
      cancelText: APP_STRINGS.itinerary.actions.cancel,
      onConfirm,
   });
}
