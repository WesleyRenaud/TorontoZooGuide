import { ConfirmFragment } from '../panel/components/confirmFragment.js';
import { Strings } from '../../strings.js';

export class SaveIssuesProceedFragment {
   static showSaveIssuesProceedConfirmation({
      title,
      message,
      onConfirm,
   } = {}) {
      ConfirmFragment.showItineraryConfirmPopup({
         title,
         message,
         confirmText: Strings.itinerary.confirmation.proceedAnyway,
         cancelText: Strings.itinerary.actions.cancel,
         onConfirm,
      });
   }
}
