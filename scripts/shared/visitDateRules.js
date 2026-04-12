export const DEFAULT_DAYS_AHEAD = 360;

export function toISODate(d) {
   const y = d.getFullYear();
   const m = String(d.getMonth() + 1).padStart(2, '0');
   const day = String(d.getDate()).padStart(2, '0');
   return `${y}-${m}-${day}`;
}

export function getToday() {
   const today = new Date();

   return new Date(
      today.getFullYear(),
      today.getMonth(),
      today.getDate(),
      12, 0, 0, 0
   );
}

export function getMaxDate(daysAhead = DEFAULT_DAYS_AHEAD) {
   const today = getToday();
   const max = new Date(today);
   max.setDate(today.getDate() + daysAhead);
   return max;
}

export function normalizeDate(d) {
   if (!d || !Number.isFinite(d.getTime())) return null;

   return new Date(
      d.getFullYear(),
      d.getMonth(),
      d.getDate(),
      12, 0, 0, 0
   );
}

export function isBeforeToday(d) {
   const candidate = normalizeDate(d);
   if (!candidate) return false;
   return candidate < getToday();
}

export function isAfterMaxDate(d, daysAhead = DEFAULT_DAYS_AHEAD) {
   const candidate = normalizeDate(d);
   if (!candidate) return false;
   return candidate > getMaxDate(daysAhead);
}

export function clampToAllowedVisitDate(d, daysAhead = DEFAULT_DAYS_AHEAD) {
   const today = getToday();
   const maxDate = getMaxDate(daysAhead);
   const normalized = normalizeDate(d);

   if (!normalized) return today;
   if (normalized < today) return today;
   if (normalized > maxDate) return maxDate;

   return normalized;
}