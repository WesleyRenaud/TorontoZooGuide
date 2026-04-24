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

function createAllowedVisitDateRange(daysAhead = DEFAULT_DAYS_AHEAD) {
   const today = getToday();
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

export function isWithinNextNDays(dateStr, n) {
   const target = normalizeDate(parseLocalDate(dateStr));

   if (!target) {
      return false;
   }

   const diffDays = (target - getToday()) / MS_PER_DAY;
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

export function getMaxDate(daysAhead = DEFAULT_DAYS_AHEAD) {
   return createAllowedVisitDateRange(daysAhead).maxDate;
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

export function isBeforeToday(d) {
   const candidate = normalizeDate(d);

   if (!candidate) {
      return false;
   }

   return candidate < getToday();
}

export function isAfterMaxDate(d, daysAhead = DEFAULT_DAYS_AHEAD) {
   const candidate = normalizeDate(d);

   if (!candidate) {
      return false;
   }

   return candidate > getMaxDate(daysAhead);
}

export function clampToAllowedVisitDate(d, daysAhead = DEFAULT_DAYS_AHEAD) {
   const { today, maxDate } = createAllowedVisitDateRange(daysAhead);
   const normalized = normalizeDate(d);

   if (!normalized) {
      return today;
   }

   if (normalized < today) {
      return today;
   }

   if (normalized > maxDate) {
      return maxDate;
   }

   return normalized;
}
