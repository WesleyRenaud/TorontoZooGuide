import { Format } from '../format.js';
import { ItineraryAdjustmentTypes } from '../../itineraryAdjustmentTypes.js';
import { Strings } from '../../../strings.js';

export class RemovedItemsPopupAdjustmentSpecs {
   static buildAdjustmentRowSpec(
      adjustment = {},
      {
         adjustmentTypes = ItineraryAdjustmentTypes.getItineraryAdjustmentTypes(),
         strings = Strings,
         formatTime = Format.formatClockTime,
      } = {}
   ) {
      const oldTime = formatTime(adjustment.previousValue);
      const newTime = formatTime(adjustment.value);

      if (!oldTime || !newTime) {
         return null;
      }

      if (adjustment.type === adjustmentTypes?.ARRIVAL_TIME_ADJUSTED) {
         return {
            name: strings.itinerary.dayPlanner.arrivalLabel,
            alertLine: strings.itinerary.removedItems.arrivalAdjusted(oldTime, newTime),
         };
      }

      if (adjustment.type === adjustmentTypes?.DEPARTURE_TIME_ADJUSTED) {
         return {
            name: strings.labels.departure,
            alertLine: strings.itinerary.removedItems.departureAdjusted(oldTime, newTime),
         };
      }

      return null;
   }
}
