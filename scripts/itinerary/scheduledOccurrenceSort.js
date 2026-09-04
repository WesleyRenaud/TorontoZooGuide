import { DayPlannerSchedule } from './panel/dayPlannerSchedule.js';

export class ScheduledOccurrenceSort {
   static sortScheduledOccurrencesByStartTime(
      rows = [],
      getTimeOfDay = (row) => row?.start_time ?? ''
   ) {
      if (!Array.isArray(rows)) {
         return [];
      }

      return rows.slice().sort((left, right) => {
         const leftMinutes = DayPlannerSchedule.parseClockTimeMinutes(getTimeOfDay(left));
         const rightMinutes = DayPlannerSchedule.parseClockTimeMinutes(getTimeOfDay(right));

         return (
            (leftMinutes ?? Number.MAX_SAFE_INTEGER)
            - (rightMinutes ?? Number.MAX_SAFE_INTEGER)
         );
      });
   }
}
