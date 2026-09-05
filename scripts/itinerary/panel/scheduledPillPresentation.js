import { Constants } from '../../shared/constants.js';

export class ScheduledPillPresentation {
   static isExtendedScheduledPill(durationMinutes) {
      return Number.isFinite(durationMinutes)
         && durationMinutes >= Constants.EXTENDED_SCHEDULED_PILL_MINUTES;
   }
}
