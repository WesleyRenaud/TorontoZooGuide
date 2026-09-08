import { TimelineLayoutConstants } from '../../shared/timelineLayoutConstants.js';

export class ScheduledPillPresenter {
   static isExtendedScheduledPill(durationMinutes) {
      return Number.isFinite(durationMinutes)
         && durationMinutes >= TimelineLayoutConstants.EXTENDED_SCHEDULED_PILL_MINUTES;
   }
}
