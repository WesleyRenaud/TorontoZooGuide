import { ConfirmFragment } from '../panel/components/confirmFragment.js';
import { Strings } from '../../strings.js';

export class ScheduleOverrideSelectionFragment {
   static showScheduleOverrideSelectionConfirmation({
      onConfirm,
   } = {}) {
      ConfirmFragment.showItineraryConfirmPopup({
         title: Strings.itinerary.confirmation.scheduleOverrideSelectionTitle,
         message: Strings.itinerary.confirmation.scheduleOverrideSelectionMessage,
         confirmText: Strings.itinerary.confirmation.saveIssuesButton,
         cancelText: Strings.itinerary.actions.cancel,
         onConfirm,
      });
   }
}
