import { formatClockTime } from './format.js';

export function parseClockTimeMinutes(timeValue) {
   if (typeof timeValue !== 'string') {
      return null;
   }

   const timeParts = timeValue.trim().match(/^(\d{1,2}):(\d{2})$/);

   if (!timeParts) {
      return null;
   }

   const hours = Number(timeParts[1]);
   const minutes = Number(timeParts[2]);

   if (hours < 0 || hours > 23 || minutes < 0 || minutes > 59) {
      return null;
   }

   return (hours * 60) + minutes;
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
