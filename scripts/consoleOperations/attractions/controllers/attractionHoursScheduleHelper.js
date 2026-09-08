import { DayPlannerScheduleController } from '../../../itinerary/panel/dayPlannerScheduleController.js';

export class AttractionHoursScheduleHelper {
   static timePairIsOrdered(startTime, endTime) {
      const startMinutes = DayPlannerScheduleController.parseClockTimeMinutes(startTime);
      const endMinutes = DayPlannerScheduleController.parseClockTimeMinutes(endTime);

      return (
         startMinutes != null
         && endMinutes != null
         && startMinutes < endMinutes
      );
   }
}
