import { ValueNormalizer } from '../api/valueNormalizer.js';
import { ZooClockTimeHelper } from '../shared/zooClockTimeHelper.js';
import { Strings } from '../strings.js';
import { VisitDateRuleHelper } from './visitDateRuleHelper.js';

export class VisitDateValidator {
   static MS_PER_DAY = 86400000;

   static DEFAULT_DAYS_AHEAD = 360;

   static parseLocalDate(dateStr) {
      const parts = String(dateStr).split('-');

      if (parts.length !== 3) {
         return VisitDateRuleHelper.createInvalidDate();
      }

      const [year, month, day] = parts.map(Number);
      const monthIndex = month - 1;

      if (
         !Number.isInteger(year)
         || !Number.isInteger(month)
         || !Number.isInteger(day)
      ) {
         return VisitDateRuleHelper.createInvalidDate();
      }

      const parsed = VisitDateRuleHelper.createLocalNoonDate(year, monthIndex, day);

      if (!VisitDateRuleHelper.isValidDate(parsed)) {
         return VisitDateRuleHelper.createInvalidDate();
      }

      if (!VisitDateRuleHelper.matchesDateParts(parsed, { year, monthIndex, day })) {
         return VisitDateRuleHelper.createInvalidDate();
      }

      return parsed;
   }

   static isWithinNextNDays(dateStr, n, referenceToday = null) {
      const target = VisitDateValidator.normalizeDate(VisitDateValidator.parseLocalDate(dateStr));

      if (!target) {
         return false;
      }

      const today = VisitDateValidator.normalizeDate(referenceToday) ?? VisitDateValidator.getToday();
      const diffDays = (target - today) / VisitDateValidator.MS_PER_DAY;
      return diffDays >= 0 && diffDays <= n;
   }

   static getMonth(dateStr) {
      const date = VisitDateValidator.parseLocalDate(dateStr);

      if (!VisitDateRuleHelper.isValidDate(date)) {
         return null;
      }

      return date.toLocaleString('en-US', { month: 'short' }).toUpperCase();
   }

   static getDay(dateStr) {
      const date = VisitDateValidator.parseLocalDate(dateStr);
      return VisitDateRuleHelper.isValidDate(date) ? date.getDate() : null;
   }

   static getYear(dateStr) {
      const date = VisitDateValidator.parseLocalDate(dateStr);
      return VisitDateRuleHelper.isValidDate(date) ? date.getFullYear() : null;
   }

   static isoDateToMonFirstDow(iso) {
      const date = iso ? VisitDateValidator.parseLocalDate(iso) : VisitDateValidator.getToday();

      if (!VisitDateRuleHelper.isValidDate(date)) {
         return 1;
      }

      const jsDay = date.getDay();
      return jsDay === 0 ? 7 : jsDay;
   }

   static toISODate(d) {
      const y = d.getFullYear();
      const m = String(d.getMonth() + 1).padStart(2, '0');
      const day = String(d.getDate()).padStart(2, '0');
      return `${y}-${m}-${day}`;
   }

   static getToday() {
      const today = new Date();

      return VisitDateRuleHelper.createLocalNoonDate(
         today.getFullYear(),
         today.getMonth(),
         today.getDate()
      );
   }

   static resolveOptionalStartDate(startDate) {
      return startDate || VisitDateValidator.toISODate(VisitDateValidator.getToday());
   }

   static formatLocalDateLong(value) {
      const date = value instanceof Date
         ? value
         : VisitDateValidator.parseLocalDate(value);

      if (!VisitDateRuleHelper.isValidDate(date)) {
         return '';
      }

      return date.toLocaleDateString(undefined, {
         month: 'long',
         day: 'numeric',
         year: 'numeric',
      });
   }

   static formatLocalDateRange(startValue, endValue) {
      const startDate = VisitDateValidator.formatLocalDateLong(startValue);
      const endDate = VisitDateValidator.formatLocalDateLong(endValue);

      if (!startDate) {
         return '';
      }

      if (!endDate) {
         return startDate;
      }

      return Strings.format.timeRange(startDate, endDate);
   }

   static getMaxDate(daysAhead = VisitDateValidator.DEFAULT_DAYS_AHEAD, referenceToday = null) {
      return VisitDateRuleHelper.createAllowedVisitDateRange(daysAhead, referenceToday).maxDate;
   }

   static normalizeDate(d) {
      if (!VisitDateRuleHelper.isValidDate(d)) {
         return null;
      }

      return VisitDateRuleHelper.createLocalNoonDate(
         d.getFullYear(),
         d.getMonth(),
         d.getDate()
      );
   }

   static isBeforeToday(d, referenceToday = null) {
      const candidate = VisitDateValidator.normalizeDate(d);

      if (!candidate) {
         return false;
      }

      const today = VisitDateValidator.normalizeDate(referenceToday) ?? VisitDateValidator.getToday();

      return candidate < today;
   }

   static isAfterMaxDate(
      d,
      daysAhead = VisitDateValidator.DEFAULT_DAYS_AHEAD,
      referenceToday = null
   ) {
      const candidate = VisitDateValidator.normalizeDate(d);

      if (!candidate) {
         return false;
      }

      return candidate > VisitDateValidator.getMaxDate(daysAhead, referenceToday);
   }

   /**
    * Parses "HH:MM" (24h) or "H:MM AM/PM" zoo-style clock strings to minutes from midnight.
    */
   static parseZooClockTimeMinutes(timeValue) {
      return ZooClockTimeHelper.parseMinutes(timeValue);
   }

   /**
    * Formats a zoo clock string as 12-hour display (matches backend format_display_time_value).
    */
   static formatZooDisplayClockTime(timeValue) {
      return ZooClockTimeHelper.formatDisplay(timeValue);
   }

   /**
    * Normalizes a zoo clock string to canonical 12-hour display (matches backend normalize_schedule_time).
    */
   static normalizeScheduleTime(timeValue) {
      return ZooClockTimeHelper.normalizeScheduleTime(timeValue);
   }

   /**
    * @deprecated Use normalizeScheduleTime.
    */
   static normalizeItineraryScheduleTime(timeValue) {
      return VisitDateValidator.normalizeScheduleTime(timeValue);
   }

   /**
    * True when local wall-clock time is at or after the zoo's close time for the current calendar day.
    */
   static isLocalTimeAtOrPastZooClose(closeTimeStr, now = new Date()) {
      const closeMinutes = VisitDateValidator.parseZooClockTimeMinutes(closeTimeStr);

      if (closeMinutes == null) {
         return false;
      }

      const nowMinutes = (now.getHours() * 60) + now.getMinutes();

      return nowMinutes >= closeMinutes;
   }

   static addLocalCalendarDays(localNoonDate, deltaDays) {
      const base = VisitDateValidator.normalizeDate(localNoonDate);

      if (!base) {
         return VisitDateValidator.getToday();
      }

      const d = new Date(base);

      d.setDate(d.getDate() + deltaDays);

      return VisitDateValidator.normalizeDate(d);
   }

   /**
    * True when a visit date is before the earliest selectable floor passed to the map
    * date picker and visit-date clamping (minDate / clampToAllowedVisitDate).
    */
   static isVisitDateBeforeEarliestFloor(dateValue, earliestNoon) {
      const trimmedDateValue = ValueNormalizer.asTrimmedString(dateValue);

      if (typeof dateValue === 'string' && !trimmedDateValue) {
         return false;
      }

      const visitDate = VisitDateValidator.normalizeDate(
         typeof dateValue === 'string'
            ? VisitDateValidator.parseLocalDate(trimmedDateValue)
            : dateValue
      );
      const floor = VisitDateValidator.normalizeDate(earliestNoon);

      if (!visitDate || !floor) {
         return false;
      }

      return visitDate < floor;
   }

   static clampToAllowedVisitDate(
      d,
      daysAhead = VisitDateValidator.DEFAULT_DAYS_AHEAD,
      earliestNoon = null,
      referenceToday = null
   ) {
      const calendarToday = VisitDateValidator.normalizeDate(referenceToday)
         ?? VisitDateValidator.getToday();
      const maxDate = VisitDateValidator.addLocalCalendarDays(calendarToday, daysAhead);
      const floor = VisitDateValidator.normalizeDate(earliestNoon) ?? calendarToday;
      const normalized = VisitDateValidator.normalizeDate(d);

      if (!normalized) {
         return floor;
      }

      if (VisitDateValidator.isVisitDateBeforeEarliestFloor(normalized, floor)) {
         return floor;
      }

      if (normalized > maxDate) {
         return maxDate;
      }

      return normalized;
   }
}
