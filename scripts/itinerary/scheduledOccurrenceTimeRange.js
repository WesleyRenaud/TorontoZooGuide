import { ItineraryItemFormatter } from './panel/itineraryItemFormatter.js';

export class ScheduledOccurrenceTimeRange {
   static buildScheduledOccurrenceTimeRange(item = {}) {
      const startTime = ItineraryItemFormatter.formatClockTime(item.start_time);

      if (!startTime) {
         return '';
      }

      const endTime = ItineraryItemFormatter.formatClockTime(item.end_time);

      return endTime
         ? `${startTime} - ${endTime}`
         : startTime;
   }
}
