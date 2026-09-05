import { ConfirmPopup } from './components/confirmPopup.js';
import { Popup } from './components/popup.js';
import { APP_STRINGS } from '../../strings.js';

export class ScheduleItemNotOnItineraryConfirmation {
   static showScheduleItemNotOnItineraryConfirmation({
      onConfirm,
      onCancel,
   } = {}) {
      const strings = APP_STRINGS.itinerary.confirmation;

      ConfirmPopup.showItineraryConfirmPopup({
         title: strings.scheduleItemNotOnItineraryTitle,
         message: strings.scheduleItemNotOnItineraryMessage,
         confirmText: strings.scheduleItemNotOnItineraryConfirm,
         doNotShowAgainLabel: strings.doNotShowAgain,
         cancelText: APP_STRINGS.itinerary.actions.cancel,
         mountEl: Popup.getItineraryPanelMountEl() ?? document.body,
         onConfirm,
         onCancel,
      });
   }
}
