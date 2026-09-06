import { ConfirmPopup } from '../panel/components/confirmPopup.js';
import { Strings } from '../../strings.js';

export class ScheduleOverrideSelectionConfirmation {
   static showScheduleOverrideSelectionConfirmation({
      onConfirm,
   } = {}) {
      ConfirmPopup.showItineraryConfirmPopup({
         title: Strings.itinerary.confirmation.scheduleOverrideSelectionTitle,
         message: Strings.itinerary.confirmation.scheduleOverrideSelectionMessage,
         confirmText: Strings.itinerary.confirmation.saveIssuesButton,
         cancelText: Strings.itinerary.actions.cancel,
         onConfirm,
      });
   }
}
