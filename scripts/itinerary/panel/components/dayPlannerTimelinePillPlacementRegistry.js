import { DayPlannerTimelineMetrics } from '../dayPlannerTimelineMetrics.js';
import { TimelineLayoutConstants } from '../../../shared/timelineLayoutConstants.js';

const timelinePlacementsByGridLine = new WeakMap();

export class DayPlannerTimelinePillPlacementRegistry {
   static getTimelinePlacements(gridLine) {
      let placements = timelinePlacementsByGridLine.get(gridLine);

      if (!placements) {
         placements = [];
         timelinePlacementsByGridLine.set(gridLine, placements);
      }

      return placements;
   }

   static applyHorizontalOffsetIndex(element, horizontalOffsetIndex) {
      element.setAttribute('data-horizontal-offset-index', String(horizontalOffsetIndex));
      element.style.setProperty(
         '--itinerary-pill-horizontal-offset-index',
         String(horizontalOffsetIndex)
      );
   }

   static markScheduledPillStrip(pillStrip) {
      pillStrip.setAttribute('data-scheduled-column', 'true');
   }

   static registerTimelinePlacement(
      gridLine,
      {
         offsetFraction,
         durationFraction,
         horizontalOffsetIndex,
         anchorOffsetFraction,
      }
   ) {
      DayPlannerTimelinePillPlacementRegistry.getTimelinePlacements(gridLine).push({
         offsetFraction,
         durationFraction,
         horizontalOffsetIndex,
         anchorOffsetFraction,
      });
   }

   static isScheduledPillStrip(strip) {
      return (
         strip.getAttribute?.('data-scheduled-column')
         ?? strip.attributes?.['data-scheduled-column']
      ) === 'true';
   }

   static findPointPillStrip(gridLine, offsetFraction = 0) {
      const offsetKey = String(offsetFraction);

      for (const child of gridLine.children) {
         if (child.className !== 'itinerary-day-pill-strip' || DayPlannerTimelinePillPlacementRegistry.isScheduledPillStrip(child)) {
            continue;
         }

         const childOffset = child.getAttribute?.('data-offset-fraction')
            ?? child.attributes?.['data-offset-fraction']
            ?? '0';

         if (childOffset === offsetKey) {
            return child;
         }
      }

      return null;
   }

   static resolveStripPlacementBand(
      gridLine,
      offsetFraction = 0,
      durationMinutes = null,
      slotSpanMinutes = TimelineLayoutConstants.TIMELINE_SLOT_MINUTES
   ) {
      const pointBand = DayPlannerTimelineMetrics.getPointPillStripPlacementBand(gridLine, offsetFraction);

      if (Number.isFinite(durationMinutes) && durationMinutes > 0) {
         const slotSpan = Number.isFinite(slotSpanMinutes) && slotSpanMinutes > 0
            ? slotSpanMinutes
            : TimelineLayoutConstants.TIMELINE_SLOT_MINUTES;

         return {
            offsetFraction: pointBand.offsetFraction,
            durationFraction: durationMinutes / slotSpan,
         };
      }

      return pointBand;
   }
}
