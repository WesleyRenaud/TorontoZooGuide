import { showItineraryConfirmPopup } from './components/confirmPopup.js';
import { getItineraryPanelMountEl } from './components/popup.js';
import { APP_STRINGS } from '../../strings.js';

export class ScheduleItemNotOnItineraryConfirmation {
   static showScheduleItemNotOnItineraryConfirmation({
      onConfirm,
      onCancel,
   } = {}) {
      const strings = APP_STRINGS.itinerary.confirmation;

      showItineraryConfirmPopup({
         title: strings.scheduleItemNotOnItineraryTitle,
         message: strings.scheduleItemNotOnItineraryMessage,
         confirmText: strings.scheduleItemNotOnItineraryConfirm,
         doNotShowAgainLabel: strings.doNotShowAgain,
         cancelText: APP_STRINGS.itinerary.actions.cancel,
         mountEl: getItineraryPanelMountEl() ?? document.body,
         onConfirm,
         onCancel,
      });
   }
}
