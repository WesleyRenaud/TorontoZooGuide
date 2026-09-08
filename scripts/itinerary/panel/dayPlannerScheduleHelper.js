import { ValueNormalizer } from '../../api/valueNormalizer.js';
import { DayPlannerScheduleController } from './dayPlannerScheduleController.js';

export class DayPlannerScheduleHelper {
   static isTimeWithinBounds(timeValue, bounds) {
      if (!bounds) {
         return true;
      }

      const normalizedTimeValue = ValueNormalizer.asTrimmedString(timeValue);

      if (!normalizedTimeValue) {
         return true;
      }

      const timeMinutes = DayPlannerScheduleController.parseClockTimeMinutes(normalizedTimeValue);

      if (!Number.isFinite(timeMinutes)) {
         return false;
      }

      return (
         timeMinutes >= bounds.minMinutes
         && timeMinutes <= bounds.maxMinutes
      );
   }
}
