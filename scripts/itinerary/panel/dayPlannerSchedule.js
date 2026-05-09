import { formatClockTime } from './format.js';

export function parseClockTimeMinutes(timeValue) {
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

export function formatMinutesAsClockTime(totalMinutes) {
   const hours = Math.floor(totalMinutes / 60);
   const minutes = totalMinutes % 60;

   return formatClockTime(
      `${String(hours).padStart(2, '0')}:${String(minutes).padStart(2, '0')}`
   );
}

export function buildHalfHourSlotStarts(openMinutes, closeMinutes) {
   if (
      !Number.isFinite(openMinutes)
      || !Number.isFinite(closeMinutes)
      || closeMinutes <= openMinutes
   ) {
      return [];
   }

   const slotStarts = [];
   const firstHalfHour = Math.ceil(openMinutes / 30) * 30;

   slotStarts.push(openMinutes);

   for (let slotStart = firstHalfHour; slotStart < closeMinutes; slotStart += 30) {
      if (slotStart === openMinutes) {
         continue;
      }

      slotStarts.push(slotStart);
   }

   return slotStarts;
}
