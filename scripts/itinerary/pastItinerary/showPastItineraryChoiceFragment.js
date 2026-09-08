import { ConfirmFragment } from '../panel/components/confirmFragment.js';
import { Strings } from '../../strings.js';

export class ShowPastItineraryChoiceFragment {
   static showPastItineraryChoicePrompt({
      mountEl,
      onClear,
      onRecover,
      deps = {},
   } = {}) {
      if (!mountEl) {
         return;
      }

      const { showConfirmPopup = ConfirmFragment.showItineraryConfirmPopup } = deps;

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
