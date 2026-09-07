import { DayPlannerTimelinePillAppendHelpers } from './dayPlannerTimelinePillAppendHelpers.js';
import { DayPlannerTimelinePillPlacement } from './dayPlannerTimelinePillPlacement.js';
import { OpenTimelinePill } from './openTimelinePill.js';
import { ScheduledTimelinePill } from './scheduledTimelinePill.js';
import { TimelineLayoutConstants } from '../../../shared/timelineLayoutConstants.js';

export class DayPlannerTimelinePillAppend {
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
         ? OpenTimelinePill.makeBoundaryMarker(label, pillOptions)
         : OpenTimelinePill.makeOpenPill(label, pillOptions);

      if (!pill) {
         return;
      }

      const strip = DayPlannerTimelinePillPlacement.getOrCreatePointPillStrip(
         gridLine,
         offsetFraction
      );

      DayPlannerTimelinePillAppendHelpers.applyPointPillStripPlacement(strip, pillOptions.visitBoundaryPlacement);
      DayPlannerTimelinePillAppendHelpers.insertPointPillInStrip(strip, pill);
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
      const pill = ScheduledTimelinePill.makeScheduledPill(label, durationMinutes, {
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

      const strip = DayPlannerTimelinePillPlacement.createScheduledPillStrip(
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
         DayPlannerTimelinePillAppend.appendTimelinePill(
            gridLine,
            marker.label,
            marker.offsetFraction,
            DayPlannerTimelinePillAppendHelpers.resolveTimePillOptions(
               marker,
               timeHandlers,
               strings,
               visitBoundaryEventTypes
            )
         );
      });
   }
}
