import { ValueNormalizer } from '../api/valueNormalizer.js';

const LOCAL_NOON_HOUR = 12;
const MS_PER_DAY = 86400000;

function createInvalidDate() {
   return new Date(Number.NaN);
}

function isValidDate(date) {
   return Number.isFinite(date?.getTime?.());
}

function createLocalNoonDate(year, monthIndex, day) {
   return new Date(year, monthIndex, day, LOCAL_NOON_HOUR, 0, 0, 0);
}

function matchesDateParts(date, {
   year,
   monthIndex,
   day,
} = {}) {
   return date.getFullYear() === year
      && date.getMonth() === monthIndex
      && date.getDate() === day;
}

function createAllowedVisitDateRange(
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

export class VisitDateRules {
   static DEFAULT_DAYS_AHEAD = 360;

   static parseLocalDate(dateStr) {
      const parts = String(dateStr).split('-');

      if (parts.length !== 3) {
         return createInvalidDate();
      }

      const [year, month, day] = parts.map(Number);
      const monthIndex = month - 1;

      if (
         !Number.isInteger(year)
         || !Number.isInteger(month)
         || !Number.isInteger(day)
      ) {
         return createInvalidDate();
      }

      const parsed = createLocalNoonDate(year, monthIndex, day);

      if (!isValidDate(parsed)) {
         return createInvalidDate();
      }

      if (!matchesDateParts(parsed, { year, monthIndex, day })) {
         return createInvalidDate();
      }

      return parsed;
   }

   static isWithinNextNDays(dateStr, n, referenceToday = null) {
      const target = VisitDateRules.normalizeDate(VisitDateRules.parseLocalDate(dateStr));

      if (!target) {
         return false;
      }

      const today = VisitDateRules.normalizeDate(referenceToday) ?? VisitDateRules.getToday();
      const diffDays = (target - today) / MS_PER_DAY;
      return diffDays >= 0 && diffDays <= n;
   }

   static getMonth(dateStr) {
      const date = VisitDateRules.parseLocalDate(dateStr);

      if (!isValidDate(date)) {
         return null;
      }

      return date.toLocaleString('en-US', { month: 'short' }).toUpperCase();
   }

   static getDay(dateStr) {
      const date = VisitDateRules.parseLocalDate(dateStr);
      return isValidDate(date) ? date.getDate() : null;
   }

   static getYear(dateStr) {
      const date = VisitDateRules.parseLocalDate(dateStr);
      return isValidDate(date) ? date.getFullYear() : null;
   }

   static isoDateToMonFirstDow(iso) {
      const date = iso ? VisitDateRules.parseLocalDate(iso) : VisitDateRules.getToday();

      if (!isValidDate(date)) {
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

      return createLocalNoonDate(
         today.getFullYear(),
         today.getMonth(),
         today.getDate()
      );
   }

   static resolveOptionalStartDate(startDate) {
      return startDate || VisitDateRules.toISODate(VisitDateRules.getToday());
   }

   static formatLocalDateLong(value) {
      const date = value instanceof Date
         ? value
         : VisitDateRules.parseLocalDate(value);

      if (!isValidDate(date)) {
         return '';
      }

      return date.toLocaleDateString(undefined, {
         month: 'long',
         day: 'numeric',
         year: 'numeric',
      });
   }

   static formatLocalDateRange(startValue, endValue) {
      const startDate = VisitDateRules.formatLocalDateLong(startValue);
      const endDate = VisitDateRules.formatLocalDateLong(endValue);

      if (!startDate) {
         return '';
      }

      if (!endDate) {
         return startDate;
      }

      return `${startDate} - ${endDate}`;
   }

   static getMaxDate(daysAhead = VisitDateRules.DEFAULT_DAYS_AHEAD, referenceToday = null) {
      return createAllowedVisitDateRange(daysAhead, referenceToday).maxDate;
   }

   static normalizeDate(d) {
      if (!isValidDate(d)) {
         return null;
      }

      return createLocalNoonDate(
         d.getFullYear(),
         d.getMonth(),
         d.getDate()
      );
   }

   static isBeforeToday(d, referenceToday = null) {
      const candidate = VisitDateRules.normalizeDate(d);

      if (!candidate) {
         return false;
      }

      const today = VisitDateRules.normalizeDate(referenceToday) ?? VisitDateRules.getToday();

      return candidate < today;
   }

   static isAfterMaxDate(
      d,
      daysAhead = VisitDateRules.DEFAULT_DAYS_AHEAD,
      referenceToday = null
   ) {
      const candidate = VisitDateRules.normalizeDate(d);

      if (!candidate) {
         return false;
      }

      return candidate > VisitDateRules.getMaxDate(daysAhead, referenceToday);
   }

   /**
    * Parses "HH:MM" (24h) or "H:MM AM/PM" zoo-style clock strings to minutes from midnight.
    */
   static parseZooClockTimeMinutes(timeValue) {
      const normalizedTimeValue = ValueNormalizer.asTrimmedString(timeValue);

      if (!normalizedTimeValue) {
         return null;
      }

      const timeParts = normalizedTimeValue.match(/^(\d{1,2}):(\d{2})$/);

      if (timeParts) {
         const hours = Number(timeParts[1]);
         const minutes = Number(timeParts[2]);

         if (hours < 0 || hours > 23 || minutes < 0 || minutes > 59) {
            return null;
         }

         return (hours * 60) + minutes;
      }

      const displayTimeParts = normalizedTimeValue.match(/^(\d{1,2}):(\d{2})\s*(AM|PM)$/i);

      if (!displayTimeParts) {
         return null;
      }

      const displayHours = Number(displayTimeParts[1]);
      const displayMinutes = Number(displayTimeParts[2]);
      const period = displayTimeParts[3].toUpperCase();

      if (
         displayHours < 1
         || displayHours > 12
         || displayMinutes < 0
         || displayMinutes > 59
      ) {
         return null;
      }

      const hours = (displayHours % 12) + (period === 'PM' ? 12 : 0);

      return (hours * 60) + displayMinutes;
   }

   /**
    * Formats a zoo clock string as 12-hour display (matches backend format_display_time_value).
    */
   static formatZooDisplayClockTime(timeValue) {
      const minutes = VisitDateRules.parseZooClockTimeMinutes(timeValue);

      if (minutes == null) {
         return null;
      }

      const hours24 = Math.floor(minutes / 60);
      const mins = minutes % 60;
      const period = hours24 >= 12 ? 'PM' : 'AM';
      const hours12 = hours24 % 12 || 12;

      return `${hours12}:${String(mins).padStart(2, '0')} ${period}`;
   }

   /**
    * Normalizes a zoo clock string to canonical 12-hour display (matches backend normalize_schedule_time).
    */
   static normalizeScheduleTime(timeValue) {
      return VisitDateRules.formatZooDisplayClockTime(timeValue);
   }

   /**
    * @deprecated Use normalizeScheduleTime.
    */
   static normalizeItineraryScheduleTime(timeValue) {
      return VisitDateRules.normalizeScheduleTime(timeValue);
   }

   /**
    * True when local wall-clock time is at or after the zoo's close time for the current calendar day.
    */
   static isLocalTimeAtOrPastZooClose(closeTimeStr, now = new Date()) {
      const closeMinutes = VisitDateRules.parseZooClockTimeMinutes(closeTimeStr);

      if (closeMinutes == null) {
         return false;
      }

      const nowMinutes = (now.getHours() * 60) + now.getMinutes();

      return nowMinutes >= closeMinutes;
   }

   static addLocalCalendarDays(localNoonDate, deltaDays) {
      const base = VisitDateRules.normalizeDate(localNoonDate);

      if (!base) {
         return VisitDateRules.getToday();
      }

      const d = new Date(base);

      d.setDate(d.getDate() + deltaDays);

      return VisitDateRules.normalizeDate(d);
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

      const visitDate = VisitDateRules.normalizeDate(
         typeof dateValue === 'string'
            ? VisitDateRules.parseLocalDate(trimmedDateValue)
            : dateValue
      );
      const floor = VisitDateRules.normalizeDate(earliestNoon);

      if (!visitDate || !floor) {
         return false;
      }

      return visitDate < floor;
   }

   static clampToAllowedVisitDate(
      d,
      daysAhead = VisitDateRules.DEFAULT_DAYS_AHEAD,
      earliestNoon = null,
      referenceToday = null
   ) {
      const calendarToday = VisitDateRules.normalizeDate(referenceToday)
         ?? VisitDateRules.getToday();
      const maxDate = VisitDateRules.addLocalCalendarDays(calendarToday, daysAhead);
      const floor = VisitDateRules.normalizeDate(earliestNoon) ?? calendarToday;
      const normalized = VisitDateRules.normalizeDate(d);

      if (!normalized) {
         return floor;
      }

      if (VisitDateRules.isVisitDateBeforeEarliestFloor(normalized, floor)) {
         return floor;
      }

      if (normalized > maxDate) {
         return maxDate;
      }

      return normalized;
   }
}
