import { showItineraryConfirmPopup } from '../panel/components/confirmPopup.js';
import { APP_STRINGS } from '../../strings.js';

export function showScheduleOverrideSelectionConfirmation({
   onConfirm,
} = {}) {
   showItineraryConfirmPopup({
      title: APP_STRINGS.itinerary.confirmation.scheduleOverrideSelectionTitle,
      message: APP_STRINGS.itinerary.confirmation.scheduleOverrideSelectionMessage,
      confirmText: APP_STRINGS.itinerary.confirmation.saveIssuesButton,
      cancelText: APP_STRINGS.itinerary.actions.cancel,
      onConfirm,
   });
}
