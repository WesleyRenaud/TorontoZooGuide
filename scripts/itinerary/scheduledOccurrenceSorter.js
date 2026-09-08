import { DayPlannerScheduleController } from './panel/dayPlannerScheduleController.js';

export class ScheduledOccurrenceSorter {
   static sortScheduledOccurrencesByStartTime(
      rows = [],
      getTimeOfDay = (row) => row?.start_time ?? ''
   ) {
      if (!Array.isArray(rows)) {
         return [];
      }

      return rows.slice().sort((left, right) => {
         const leftMinutes = DayPlannerScheduleController.parseClockTimeMinutes(getTimeOfDay(left));
         const rightMinutes = DayPlannerScheduleController.parseClockTimeMinutes(getTimeOfDay(right));

         return (
            (leftMinutes ?? Number.MAX_SAFE_INTEGER)
            - (rightMinutes ?? Number.MAX_SAFE_INTEGER)
         );
      });
   }
}
