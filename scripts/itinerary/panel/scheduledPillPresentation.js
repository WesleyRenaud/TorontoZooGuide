import { EXTENDED_SCHEDULED_PILL_MINUTES } from '../../shared/constants.js';

export function isExtendedScheduledPill(durationMinutes) {
   return Number.isFinite(durationMinutes)
      && durationMinutes >= EXTENDED_SCHEDULED_PILL_MINUTES;
}
