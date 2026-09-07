import { VisitDateRules } from './visitDateRules.js';

const LOCAL_NOON_HOUR = 12;

export class VisitDateRuleHelpers {
   static createInvalidDate() {
      return new Date(Number.NaN);
   }

   static isValidDate(date) {
      return Number.isFinite(date?.getTime?.());
   }

   static createLocalNoonDate(year, monthIndex, day) {
      return new Date(year, monthIndex, day, LOCAL_NOON_HOUR, 0, 0, 0);
   }

   static matchesDateParts(date, {
      year,
      monthIndex,
      day,
   } = {}) {
      return date.getFullYear() === year
         && date.getMonth() === monthIndex
         && date.getDate() === day;
   }

   static createAllowedVisitDateRange(
      daysAhead = VisitDateRules.DEFAULT_DAYS_AHEAD,
      referenceToday = null
   ) {
      const today = VisitDateRules.normalizeDate(referenceToday) ?? VisitDateRules.getToday();
      const maxDate = new Date(today);

      maxDate.setDate(today.getDate() + daysAhead);

      return {
         today,
         maxDate,
      };
   }
}
