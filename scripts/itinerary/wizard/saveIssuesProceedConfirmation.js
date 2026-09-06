import { ConfirmPopup } from '../panel/components/confirmPopup.js';
import { Strings } from '../../strings.js';

export class SaveIssuesProceedConfirmation {
   static showSaveIssuesProceedConfirmation({
      title,
      message,
      onConfirm,
   } = {}) {
      ConfirmPopup.showItineraryConfirmPopup({
         title,
         message,
         confirmText: Strings.itinerary.confirmation.proceedAnyway,
         cancelText: Strings.itinerary.actions.cancel,
         onConfirm,
      });
   }
}
