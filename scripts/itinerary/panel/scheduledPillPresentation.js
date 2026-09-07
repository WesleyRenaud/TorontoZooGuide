import { TimelineLayoutConstants } from '../../shared/timelineLayoutConstants.js';

export class ScheduledPillPresentation {
   static isExtendedScheduledPill(durationMinutes) {
      return Number.isFinite(durationMinutes)
         && durationMinutes >= TimelineLayoutConstants.EXTENDED_SCHEDULED_PILL_MINUTES;
   }
}
