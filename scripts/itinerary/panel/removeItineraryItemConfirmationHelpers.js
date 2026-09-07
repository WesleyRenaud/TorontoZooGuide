import { TransportationScheduleItemKey } from '../selectors/transportationSelector/transportationScheduleItemKey.js';
import { ScheduleItemKind } from '../../shared/enums/scheduleItemKind.js';
import { Strings } from '../../strings.js';

export class RemoveItineraryItemConfirmationHelpers {
   static isTransitModeTransportationRemove(itemType, key) {
      if (itemType !== ScheduleItemKind.TRANSPORTATION.itemType) {
         return false;
      }

      const transportationKey = TransportationScheduleItemKey.fromWire(key);

      return (
         transportationKey != null
         && transportationKey.addedAsAttraction === false
      );
   }

   static removeConfirmationMessage(itemType, key) {
      if (RemoveItineraryItemConfirmationHelpers.isTransitModeTransportationRemove(itemType, key)) {
         return Strings.itinerary.confirmation.removeTransitTransportationMessage;
      }

      return Strings.itinerary.confirmation.removeItemMessage;
   }
}
