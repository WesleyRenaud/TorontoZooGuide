import { ConfirmPopup } from '../panel/components/confirmPopup.js';
import { Strings } from '../../strings.js';

export class ShowPastItineraryChoicePrompt {
   static showPastItineraryChoicePrompt({
      mountEl,
      onClear,
      onRecover,
      deps = {},
   } = {}) {
      if (!mountEl) {
         return;
      }

      const { showConfirmPopup = ConfirmPopup.showItineraryConfirmPopup } = deps;

      showConfirmPopup({
         mountEl,
         title: Strings.itinerary.stale.title,
         message: Strings.itinerary.stale.message,
         cancelText: Strings.itinerary.actions.clear,
         confirmText: Strings.itinerary.stale.recover,
         onCancel: () => {
            onClear?.();
         },
         onConfirm: () => {
            onRecover?.();
         },
      });
   }
}
