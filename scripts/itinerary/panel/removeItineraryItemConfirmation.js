import { ConfirmPopup } from './components/confirmPopup.js';
import { Popup } from './components/popup.js';
import { TransportationScheduleItemKey } from '../selectors/transportationSelector/transportationScheduleItemKey.js';
import { ScheduleItemKind } from '../../shared/enums/scheduleItemKind.js';
import { Strings } from '../../strings.js';

function isTransitModeTransportationRemove(itemType, key) {
   if (itemType !== ScheduleItemKind.TRANSPORTATION.itemType) {
      return false;
   }

   const transportationKey = TransportationScheduleItemKey.fromWire(key);

   return (
      transportationKey != null
      && transportationKey.addedAsAttraction === false
   );
}

function removeConfirmationMessage(itemType, key) {
   if (isTransitModeTransportationRemove(itemType, key)) {
      return Strings.itinerary.confirmation.removeTransitTransportationMessage;
   }

   return Strings.itinerary.confirmation.removeItemMessage;
}

export class RemoveItineraryItemConfirmation {
   static showRemoveItineraryItemConfirmation({
      itemType = null,
      key = null,
      onConfirm,
      onCancel,
   } = {}) {
      ConfirmPopup.showItineraryConfirmPopup({
         title: Strings.itinerary.confirmation.removeItemTitle,
         message: removeConfirmationMessage(itemType, key),
         confirmText: Strings.itinerary.dayPlanner.remove,
         cancelText: Strings.itinerary.actions.cancel,
         mountEl: Popup.getItineraryPanelMountEl() ?? document.body,
         onConfirm,
         onCancel,
      });
   }
}
