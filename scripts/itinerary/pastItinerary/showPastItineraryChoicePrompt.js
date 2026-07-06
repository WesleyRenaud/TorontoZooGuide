import { showItineraryConfirmPopup } from '../panel/components/confirmPopup.js';
import { APP_STRINGS } from '../../strings.js';

export function showPastItineraryChoicePrompt({
   mountEl,
   onClear,
   onRecover,
   deps = {},
} = {}) {
   if (!mountEl) {
      return;
   }

   const { showConfirmPopup = showItineraryConfirmPopup } = deps;

   showConfirmPopup({
      mountEl,
      title: APP_STRINGS.itinerary.stale.title,
      message: APP_STRINGS.itinerary.stale.message,
      cancelText: APP_STRINGS.itinerary.actions.clear,
      confirmText: APP_STRINGS.itinerary.stale.recover,
      onCancel: () => {
         onClear?.();
      },
      onConfirm: () => {
         onRecover?.();
      },
   });
}
