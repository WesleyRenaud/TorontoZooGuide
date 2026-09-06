import { ConfirmPopup } from './components/confirmPopup.js';
import { Popup } from './components/popup.js';
import { Strings } from '../../strings.js';

export class ScheduleItemNotOnItineraryConfirmation {
   static showScheduleItemNotOnItineraryConfirmation({
      onConfirm,
      onCancel,
   } = {}) {
      const strings = Strings.itinerary.confirmation;

      ConfirmPopup.showItineraryConfirmPopup({
         title: strings.scheduleItemNotOnItineraryTitle,
         message: strings.scheduleItemNotOnItineraryMessage,
         confirmText: strings.scheduleItemNotOnItineraryConfirm,
         doNotShowAgainLabel: strings.doNotShowAgain,
         cancelText: Strings.itinerary.actions.cancel,
         mountEl: Popup.getItineraryPanelMountEl() ?? document.body,
         onConfirm,
         onCancel,
      });
   }
}
