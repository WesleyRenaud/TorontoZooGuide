import { ValueNormalizer } from '../../api/valueNormalizer.js';
import { DayPlannerSchedule } from './dayPlannerSchedule.js';

export class DayPlannerScheduleHelpers {
   static isTimeWithinBounds(timeValue, bounds) {
      if (!bounds) {
         return true;
      }

      const normalizedTimeValue = ValueNormalizer.asTrimmedString(timeValue);

      if (!normalizedTimeValue) {
         return true;
      }

      const timeMinutes = DayPlannerSchedule.parseClockTimeMinutes(normalizedTimeValue);

      if (!Number.isFinite(timeMinutes)) {
         return false;
      }

      return (
         timeMinutes >= bounds.minMinutes
         && timeMinutes <= bounds.maxMinutes
      );
   }
}
