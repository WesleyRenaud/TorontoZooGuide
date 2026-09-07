import { TimelineLayoutConstants } from '../../../shared/timelineLayoutConstants.js';

export class ScheduledPillOverlapHelpers {
   static minutesPerSlotFromHeightPx(heightPx) {
      return (heightPx / TimelineLayoutConstants.TIMELINE_SLOT_HEIGHT_PX) * TimelineLayoutConstants.TIMELINE_SLOT_MINUTES;
   }
}
