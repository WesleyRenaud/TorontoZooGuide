import { ConfirmPopup } from './components/confirmPopup.js';
import { ItineraryPanelPopup } from './components/itineraryPanelPopup.js';
import { Strings } from '../../strings.js';

export class ScheduleItemNotOnItineraryConfirmation {
   static showScheduleItemNotOnItineraryConfirmation({
      onConfirm,
      onCancel,
   } = {}) {
      ConfirmPopup.showItineraryConfirmPopup({
         title: Strings.itinerary.confirmation.scheduleItemNotOnItineraryTitle,
         message: Strings.itinerary.confirmation.scheduleItemNotOnItineraryMessage,
         confirmText: Strings.itinerary.confirmation.scheduleItemNotOnItineraryConfirm,
         doNotShowAgainLabel: Strings.itinerary.confirmation.doNotShowAgain,
         cancelText: Strings.itinerary.actions.cancel,
         mountEl: ItineraryPanelPopup.getItineraryPanelMountEl() ?? document.body,
         onConfirm,
         onCancel,
      });
   }
}
