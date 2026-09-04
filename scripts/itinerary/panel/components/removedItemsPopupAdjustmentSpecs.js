import { formatClockTime } from '../format.js';
import { getItineraryAdjustmentTypes } from '../../itineraryAdjustmentTypes.js';
import { APP_STRINGS } from '../../../strings.js';

export class RemovedItemsPopupAdjustmentSpecs {
   static buildAdjustmentRowSpec(
      adjustment = {},
      {
         adjustmentTypes = getItineraryAdjustmentTypes(),
         strings = APP_STRINGS,
         formatTime = formatClockTime,
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
