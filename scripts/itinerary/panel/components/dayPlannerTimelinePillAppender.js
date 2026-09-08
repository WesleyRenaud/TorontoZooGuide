import { DayPlannerTimelinePillAppendHelper } from './dayPlannerTimelinePillAppendHelper.js';
import { DayPlannerTimelinePillPlacer } from './dayPlannerTimelinePillPlacer.js';
import { OpenTimelineView } from './openTimelineView.js';
import { ScheduledTimelineView } from './scheduledTimelineView.js';
import { TimelineLayoutConstants } from '../../../shared/timelineLayoutConstants.js';

export class DayPlannerTimelinePillAppender {
   static appendTimelinePill(
      gridLine,
      label,
      offsetFraction = 0,
      pillOptions = {}
   ) {
      if (!label) {
         return;
      }

      const pill = pillOptions.visitBoundaryPlacement
         ? OpenTimelineView.makeBoundaryMarker(label, pillOptions)
         : OpenTimelineView.makeOpenPill(label, pillOptions);

      if (!pill) {
         return;
      }

      const strip = DayPlannerTimelinePillPlacer.getOrCreatePointPillStrip(
         gridLine,
         offsetFraction
      );

      DayPlannerTimelinePillAppendHelper.applyPointPillStripPlacement(strip, pillOptions.visitBoundaryPlacement);
      DayPlannerTimelinePillAppendHelper.insertPointPillInStrip(strip, pill);
   }

   static appendScheduledDurationPill(
      gridLine,
      {
         label,
         offsetFraction = 0,
         durationMinutes,
         displayDurationMinutes = durationMinutes,
         slotSpanMinutes = TimelineLayoutConstants.TIMELINE_SLOT_MINUTES,
         startTime,
         endTime,
         groupItems = [],
         menuItems = [],
         menuAriaLabel = '',
         onLabelClick = null,
         item = null,
      }
   ) {
      const pill = ScheduledTimelineView.makeScheduledPill(label, durationMinutes, {
         startTime,
         endTime,
         groupItems,
         menuItems,
         menuAriaLabel,
         onLabelClick,
         item,
         slotSpanMinutes,
         displayDurationMinutes,
      });

      if (!pill) {
         return;
      }

      const strip = DayPlannerTimelinePillPlacer.createScheduledPillStrip(
         gridLine,
         offsetFraction,
         displayDurationMinutes,
         slotSpanMinutes
      );

      strip.appendChild(pill);
   }

   static appendItineraryTimeMarkers(
      gridLine,
      markersByAnchorSlot,
      slotStart,
      timeHandlers = {},
      strings = {},
      visitBoundaryEventTypes = {}
   ) {
      (markersByAnchorSlot.get(slotStart) ?? []).forEach((marker) => {
         DayPlannerTimelinePillAppender.appendTimelinePill(
            gridLine,
            marker.label,
            marker.offsetFraction,
            DayPlannerTimelinePillAppendHelper.resolveTimePillOptions(
               marker,
               timeHandlers,
               strings,
               visitBoundaryEventTypes
            )
         );
      });
   }
}
