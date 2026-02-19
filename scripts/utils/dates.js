export function parseLocalDate(dateStr) {
   const [year, month, day] = String(dateStr).split('-').map(Number);
   return new Date(year, month - 1, day);
}

export function isWithinNextNDays(dateStr, n) {
   const today = new Date();
   today.setHours(0, 0, 0, 0);

   const target = parseLocalDate(dateStr);
   target.setHours(0, 0, 0, 0);

   const diffDays = (target - today) / 86400000;
   return diffDays >= 0 && diffDays <= n;
}

export function getMonth(dateStr) {
   const d = parseLocalDate(dateStr);
   return d.toLocaleString('en-US', { month: 'short' }).toUpperCase();
}

export function getDay(dateStr) {
   return parseLocalDate(dateStr).getDate();
}