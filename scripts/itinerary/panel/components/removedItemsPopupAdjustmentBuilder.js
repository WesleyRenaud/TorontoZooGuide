import { ItineraryItemFormatter } from '../itineraryItemFormatter.js';
import { ItineraryAdjustmentType } from '../../../shared/enums/itineraryAdjustmentType.js';
import { Strings } from '../../../strings.js';

export class RemovedItemsPopupAdjustmentBuilder {
   static buildAdjustmentRowSpec(
      adjustment = {},
      {
         strings = Strings,
         formatTime = ItineraryItemFormatter.formatClockTime,
      } = {}
   ) {
      const oldTime = formatTime(adjustment.previousValue);
      const newTime = formatTime(adjustment.value);

      if (!oldTime || !newTime) {
         return null;
      }

      if (adjustment.type === ItineraryAdjustmentType.ARRIVAL_TIME_ADJUSTED) {
         return {
            name: strings.itinerary.dayPlanner.arrivalLabel,
            alertLine: strings.itinerary.removedItems.arrivalAdjusted(oldTime, newTime),
         };
      }

      if (adjustment.type === ItineraryAdjustmentType.DEPARTURE_TIME_ADJUSTED) {
         return {
            name: strings.labels.departure,
            alertLine: strings.itinerary.removedItems.departureAdjusted(oldTime, newTime),
         };
      }

      return null;
   }
}
