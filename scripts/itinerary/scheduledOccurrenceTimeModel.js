import { ItineraryItemFormatter } from './panel/itineraryItemFormatter.js';
import { Strings } from '../strings.js';

export class ScheduledOccurrenceTimeModel {
   static buildScheduledOccurrenceTimeRange(item = {}) {
      const startTime = ItineraryItemFormatter.formatClockTime(item.start_time);

      if (!startTime) {
         return '';
      }

      const endTime = ItineraryItemFormatter.formatClockTime(item.end_time);

      return endTime
         ? Strings.format.timeRange(startTime, endTime)
         : startTime;
   }
}
