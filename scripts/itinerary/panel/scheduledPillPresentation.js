import { formatClockTime } from './format.js';
import { EXTENDED_SCHEDULED_PILL_MINUTES } from '../../shared/constants.js';

export function isExtendedScheduledPill(durationMinutes) {
   return Number.isFinite(durationMinutes)
      && durationMinutes >= EXTENDED_SCHEDULED_PILL_MINUTES;
}

export function formatScheduledPillTimeRange(startTime, endTime) {
   const startLabel = formatClockTime(startTime);
   const endLabel = formatClockTime(endTime);

   if (!startLabel || !endLabel) {
      return '';
   }

   return `${startLabel} – ${endLabel}`;
}
