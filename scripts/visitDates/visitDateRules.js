export const DEFAULT_DAYS_AHEAD = 360;

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
   daysAhead = DEFAULT_DAYS_AHEAD,
   referenceToday = null
) {
   const today = normalizeDate(referenceToday) ?? getToday();
   const maxDate = new Date(today);

   maxDate.setDate(today.getDate() + daysAhead);

   return {
      today,
      maxDate,
   };
}

export function parseLocalDate(dateStr) {
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

export function isWithinNextNDays(dateStr, n, referenceToday = null) {
   const target = normalizeDate(parseLocalDate(dateStr));

   if (!target) {
      return false;
   }

   const today = normalizeDate(referenceToday) ?? getToday();
   const diffDays = (target - today) / MS_PER_DAY;
   return diffDays >= 0 && diffDays <= n;
}

export function getMonth(dateStr) {
   const date = parseLocalDate(dateStr);

   if (!isValidDate(date)) {
      return null;
   }

   return date.toLocaleString('en-US', { month: 'short' }).toUpperCase();
}

export function getDay(dateStr) {
   const date = parseLocalDate(dateStr);
   return isValidDate(date) ? date.getDate() : null;
}

export function getYear(dateStr) {
   const date = parseLocalDate(dateStr);
   return isValidDate(date) ? date.getFullYear() : null;
}

export function isoDateToMonFirstDow(iso) {
   const date = iso ? parseLocalDate(iso) : getToday();

   if (!isValidDate(date)) {
      return 1;
   }

   const jsDay = date.getDay();
   return jsDay === 0 ? 7 : jsDay;
}

export function toISODate(d) {
   const y = d.getFullYear();
   const m = String(d.getMonth() + 1).padStart(2, '0');
   const day = String(d.getDate()).padStart(2, '0');
   return `${y}-${m}-${day}`;
}

export function getToday() {
   const today = new Date();

   return createLocalNoonDate(
      today.getFullYear(),
      today.getMonth(),
      today.getDate()
   );
}

export function getMaxDate(daysAhead = DEFAULT_DAYS_AHEAD, referenceToday = null) {
   return createAllowedVisitDateRange(daysAhead, referenceToday).maxDate;
}

export function normalizeDate(d) {
   if (!isValidDate(d)) {
      return null;
   }

   return createLocalNoonDate(
      d.getFullYear(),
      d.getMonth(),
      d.getDate()
   );
}

export function isBeforeToday(d, referenceToday = null) {
   const candidate = normalizeDate(d);

   if (!candidate) {
      return false;
   }

   const today = normalizeDate(referenceToday) ?? getToday();

   return candidate < today;
}

export function isAfterMaxDate(
   d,
   daysAhead = DEFAULT_DAYS_AHEAD,
   referenceToday = null
) {
   const candidate = normalizeDate(d);

   if (!candidate) {
      return false;
   }

   return candidate > getMaxDate(daysAhead, referenceToday);
}

/**
 * Parses "HH:MM" (24h) or "H:MM AM/PM" zoo-style clock strings to minutes from midnight.
 */
export function parseZooClockTimeMinutes(timeValue) {
   if (typeof timeValue !== 'string') {
      return null;
   }

   const normalizedTimeValue = timeValue.trim();
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
export function formatZooDisplayClockTime(timeValue) {
   const minutes = parseZooClockTimeMinutes(timeValue);

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
export function normalizeScheduleTime(timeValue) {
   return formatZooDisplayClockTime(timeValue);
}

/**
 * @deprecated Use normalizeScheduleTime.
 */
export function normalizeItineraryScheduleTime(timeValue) {
   return normalizeScheduleTime(timeValue);
}

/**
 * True when local wall-clock time is at or after the zoo's close time for the current calendar day.
 */
export function isLocalTimeAtOrPastZooClose(closeTimeStr, now = new Date()) {
   const closeMinutes = parseZooClockTimeMinutes(closeTimeStr);

   if (closeMinutes == null) {
      return false;
   }

   const nowMinutes = (now.getHours() * 60) + now.getMinutes();

   return nowMinutes >= closeMinutes;
}

export function addLocalCalendarDays(localNoonDate, deltaDays) {
   const base = normalizeDate(localNoonDate);

   if (!base) {
      return getToday();
   }

   const d = new Date(base);

   d.setDate(d.getDate() + deltaDays);

   return normalizeDate(d);
}

export function clampToAllowedVisitDate(
   d,
   daysAhead = DEFAULT_DAYS_AHEAD,
   earliestNoon = null,
   referenceToday = null
) {
   const calendarToday = normalizeDate(referenceToday) ?? getToday();
   const maxDate = addLocalCalendarDays(calendarToday, daysAhead);
   const floor = normalizeDate(earliestNoon) ?? calendarToday;
   const normalized = normalizeDate(d);

   if (!normalized) {
      return floor;
   }

   if (normalized < floor) {
      return floor;
   }

   if (normalized > maxDate) {
      return maxDate;
   }

   return normalized;
}
