import { Format } from './panel/format.js';

export class ScheduledOccurrenceTimeRange {
   static buildScheduledOccurrenceTimeRange(item = {}) {
      const startTime = Format.formatClockTime(item.start_time);

      if (!startTime) {
         return '';
      }

      const endTime = Format.formatClockTime(item.end_time);

      return endTime
         ? `${startTime} - ${endTime}`
         : startTime;
   }
}
