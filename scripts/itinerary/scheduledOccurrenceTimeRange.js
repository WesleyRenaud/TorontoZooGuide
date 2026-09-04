import { formatClockTime } from './panel/format.js';

export class ScheduledOccurrenceTimeRange {
   static buildScheduledOccurrenceTimeRange(item = {}) {
      const startTime = formatClockTime(item.start_time);

      if (!startTime) {
         return '';
      }

      const endTime = formatClockTime(item.end_time);

      return endTime
         ? `${startTime} - ${endTime}`
         : startTime;
   }
}
