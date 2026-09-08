import { ItineraryPanelPopup } from '../../itinerary/panel/components/itineraryPanelPopup.js';
import { OpeningScheduleOverlap } from './openingScheduleOverlap.js';
import { OpeningScheduleOverlapDialogBuilder } from './openingScheduleOverlapDialogBuilder.js';

export class OpeningScheduleOverlapDialog {
   static ROOT_SELECTOR = '.console-overlap-dialog-root';

   static showOpeningScheduleOverlapDialog() {
      document.querySelector(OpeningScheduleOverlapDialog.ROOT_SELECTOR)?.__tzgPopupCleanup?.();

      return new Promise((resolve) => {
         const { root, overlay, buttons } = OpeningScheduleOverlapDialogBuilder.createDialogLayout();
         const { close, dismiss } = ItineraryPanelPopup.mountDismissablePopup({
            mountEl: document.body,
            root,
            overlay,
            initialFocusEl: buttons.cancel,
            onDismiss: () => resolve(null),
         });

         buttons.cancel.addEventListener('click', dismiss);

         buttons.replace.addEventListener('click', () => {
            close();
            resolve(OpeningScheduleOverlap.OPENING_SCHEDULE_OVERLAP_RESOLUTION.REPLACE);
         });

         buttons.trim.addEventListener('click', () => {
            close();
            resolve(OpeningScheduleOverlap.OPENING_SCHEDULE_OVERLAP_RESOLUTION.TRIM);
         });
      });
   }
}
