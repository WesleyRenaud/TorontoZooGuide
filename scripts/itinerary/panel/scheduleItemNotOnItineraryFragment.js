import { ConfirmFragment } from './components/confirmFragment.js';
import { ItineraryPanelFragment } from './components/itineraryPanelFragment.js';
import { Strings } from '../../strings.js';

export class ScheduleItemNotOnItineraryFragment {
   static showScheduleItemNotOnItineraryConfirmation({
      onConfirm,
      onCancel,
   } = {}) {
      ConfirmFragment.showItineraryConfirmPopup({
         title: Strings.itinerary.confirmation.scheduleItemNotOnItineraryTitle,
         message: Strings.itinerary.confirmation.scheduleItemNotOnItineraryMessage,
         confirmText: Strings.itinerary.confirmation.scheduleItemNotOnItineraryConfirm,
         doNotShowAgainLabel: Strings.itinerary.confirmation.doNotShowAgain,
         cancelText: Strings.itinerary.actions.cancel,
         mountEl: ItineraryPanelFragment.getItineraryPanelMountEl() ?? document.body,
         onConfirm,
         onCancel,
      });
   }
}
