import { parseClockTimeMinutes } from './panel/dayPlannerSchedule.js';

export function sortScheduledOccurrencesByStartTime(
   rows = [],
   getTimeOfDay = (row) => row?.start_time ?? ''
) {
   if (!Array.isArray(rows)) {
      return [];
   }

   return rows.slice().sort((left, right) => {
      const leftMinutes = parseClockTimeMinutes(getTimeOfDay(left));
      const rightMinutes = parseClockTimeMinutes(getTimeOfDay(right));

      return (
         (leftMinutes ?? Number.MAX_SAFE_INTEGER)
         - (rightMinutes ?? Number.MAX_SAFE_INTEGER)
      );
   });
}
