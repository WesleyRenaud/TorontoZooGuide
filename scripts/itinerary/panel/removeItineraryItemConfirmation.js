import { showItineraryConfirmPopup } from './components/confirmPopup.js';
import { getItineraryPanelMountEl } from './components/popup.js';
import { TransportationScheduleItemKey } from '../selectors/transportationSelector/scheduleItemKey.js';
import { ScheduleItemKind } from '../../shared/enums/scheduleItemKind.js';
import { APP_STRINGS } from '../../strings.js';

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
   const strings = APP_STRINGS.itinerary.confirmation;

   if (isTransitModeTransportationRemove(itemType, key)) {
      return strings.removeTransitTransportationMessage;
   }

   return strings.removeItemMessage;
}

export function showRemoveItineraryItemConfirmation({
   itemType = null,
   key = null,
   onConfirm,
   onCancel,
} = {}) {
   const strings = APP_STRINGS.itinerary.confirmation;

   showItineraryConfirmPopup({
      title: strings.removeItemTitle,
      message: removeConfirmationMessage(itemType, key),
      confirmText: APP_STRINGS.itinerary.dayPlanner.remove,
      cancelText: APP_STRINGS.itinerary.actions.cancel,
      mountEl: getItineraryPanelMountEl() ?? document.body,
      onConfirm,
      onCancel,
   });
}
