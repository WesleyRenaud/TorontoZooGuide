import { ConfirmPopup } from '../panel/components/confirmPopup.js';
import { APP_STRINGS } from '../../strings.js';

export class SaveIssuesProceedConfirmation {
   static showSaveIssuesProceedConfirmation({
      title,
      message,
      onConfirm,
   } = {}) {
      ConfirmPopup.showItineraryConfirmPopup({
         title,
         message,
         confirmText: APP_STRINGS.itinerary.confirmation.proceedAnyway,
         cancelText: APP_STRINGS.itinerary.actions.cancel,
         onConfirm,
      });
   }
}
