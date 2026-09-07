import { ScheduledTimelinePillBuilder } from './scheduledTimelinePillBuilder.js';
import { TimelineLayoutConstants } from '../../../shared/timelineLayoutConstants.js';

export class ScheduledTimelinePill {
   static makeScheduledPill(
      label,
      durationMinutes,
      {
      startTime,
      endTime,
      groupItems = [],
      menuItems = [],
      menuAriaLabel = '',
      onLabelClick = null,
      item = null,
      slotSpanMinutes = TimelineLayoutConstants.TIMELINE_SLOT_MINUTES,
      displayDurationMinutes = durationMinutes,
      } = {}
   ) {
      if (!label || !Number.isFinite(durationMinutes) || durationMinutes <= 0) {
         return null;
      }

      let pill;

      if (groupItems.length > 1) {
         pill = ScheduledTimelinePillBuilder.buildGroupedScheduledPill(groupItems, durationMinutes, {
            menuAriaLabel,
         });
      }
      else if (menuItems.length > 0) {
         pill = ScheduledTimelinePillBuilder.buildScheduledPillWithMenu(label, durationMinutes, {
            startTime,
            endTime,
            menuItems,
            menuAriaLabel,
            onLabelClick,
            item,
         });
      }
      else {
         pill = ScheduledTimelinePillBuilder.buildScheduledPillWithoutMenu(label, durationMinutes, {
            startTime,
            endTime,
            onLabelClick,
            item,
         });
      }

      ScheduledTimelinePillBuilder.applyScheduledPillDuration(pill, displayDurationMinutes, slotSpanMinutes);
      ScheduledTimelinePillBuilder.applyScheduledPillRegionColors(pill, item);

      return pill;
   }
}
