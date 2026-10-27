import { Strings } from '../strings.js';
import { VisitDateRuleHelper } from './visitDateRuleHelper.js';
import { VisitDateValidator } from './visitDateValidator.js';

export class VisitDateFormatter {
   static toDate(value) {
      if (value instanceof Date) {
         return VisitDateRuleHelper.isValidDate(value)
            ? value
            : VisitDateRuleHelper.createInvalidDate();
      }

      return VisitDateValidator.parseLocalDate(value);
   }

   static format(value, options, locale = undefined) {
      const date = VisitDateFormatter.toDate(value);

      if (!VisitDateRuleHelper.isValidDate(date)) {
         return '';
      }

      return date.toLocaleDateString(locale, options);
   }

   static formatLong(value, locale = undefined) {
      return VisitDateFormatter.format(value, {
         weekday: 'long',
         year: 'numeric',
         month: 'long',
         day: 'numeric',
      }, locale);
   }

   static formatMonthDayYear(value) {
      return VisitDateFormatter.format(value, {
         month: 'long',
         day: 'numeric',
         year: 'numeric',
      });
   }

   static formatRange(startValue, endValue) {
      const startDate = VisitDateFormatter.formatMonthDayYear(startValue);
      const endDate = VisitDateFormatter.formatMonthDayYear(endValue);

      if (!startDate) {
         return '';
      }

      if (!endDate) {
         return startDate;
      }

      return Strings.format.timeRange(startDate, endDate);
   }

   static formatShort(isoDate) {
      const date = VisitDateValidator.parseLocalDate(isoDate);

      if (!VisitDateRuleHelper.isValidDate(date)) {
         return '';
      }

      if (VisitDateValidator.toISODate(date) !== isoDate) {
         return '';
      }

      return date.toLocaleDateString('en-US', {
         weekday: 'short',
         month: 'short',
         day: 'numeric',
      });
   }
}
