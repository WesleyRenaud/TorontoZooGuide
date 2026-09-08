import { ItineraryPanelFragment } from '../../itinerary/panel/components/itineraryPanelFragment.js';
import { OpeningScheduleChecker } from './openingScheduleChecker.js';
import { OpeningScheduleOverlapDialogBuilder } from './openingScheduleOverlapDialogBuilder.js';

export class OpeningScheduleOverlapFragment {
   static ROOT_SELECTOR = '.console-overlap-dialog-root';

   static showOpeningScheduleOverlapDialog() {
      document.querySelector(OpeningScheduleOverlapFragment.ROOT_SELECTOR)?.__tzgPopupCleanup?.();

      return new Promise((resolve) => {
         const { root, overlay, buttons } = OpeningScheduleOverlapDialogBuilder.createDialogLayout();
         const { close, dismiss } = ItineraryPanelFragment.mountDismissablePopup({
            mountEl: document.body,
            root,
            overlay,
            initialFocusEl: buttons.cancel,
            onDismiss: () => resolve(null),
         });

         buttons.cancel.addEventListener('click', dismiss);

         buttons.replace.addEventListener('click', () => {
            close();
            resolve(OpeningScheduleChecker.OPENING_SCHEDULE_OVERLAP_RESOLUTION.REPLACE);
         });

         buttons.trim.addEventListener('click', () => {
            close();
            resolve(OpeningScheduleChecker.OPENING_SCHEDULE_OVERLAP_RESOLUTION.TRIM);
         });
      });
   }
}
