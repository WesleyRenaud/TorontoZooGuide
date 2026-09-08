import { DayPlannerSchedule } from '../../../itinerary/panel/dayPlannerSchedule.js';

export class AttractionHoursScheduleHelpers {
   static timePairIsOrdered(startTime, endTime) {
      const startMinutes = DayPlannerSchedule.parseClockTimeMinutes(startTime);
      const endMinutes = DayPlannerSchedule.parseClockTimeMinutes(endTime);

      return (
         startMinutes != null
         && endMinutes != null
         && startMinutes < endMinutes
      );
   }
}
