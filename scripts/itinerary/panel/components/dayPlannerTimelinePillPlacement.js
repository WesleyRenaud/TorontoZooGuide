import { DayPlannerTimelinePillPlacementRegistry } from './dayPlannerTimelinePillPlacementRegistry.js';
import { ItineraryPanelDom } from '../itineraryPanelDom.js';
import { TimelineLayoutConstants } from '../../../shared/timelineLayoutConstants.js';

export class DayPlannerTimelinePillPlacement {
   static computeTimelineHorizontalOffsetIndex(
      placements = [],
      offsetFraction = 0,
      durationFraction = 0
   ) {
      const placementStart = offsetFraction;
      const placementEnd = offsetFraction + durationFraction;
      let maxIndex = -1;

      for (const placement of placements) {
         const placedEnd = placement.offsetFraction + placement.durationFraction;

         if (placementStart < placedEnd && placement.offsetFraction < placementEnd) {
            maxIndex = Math.max(maxIndex, placement.horizontalOffsetIndex);
         }
      }

      return maxIndex >= 0 ? maxIndex + 1 : 0;
   }

   static getOrCreatePointPillStrip(gridLine, offsetFraction = 0) {
      const existingStrip = DayPlannerTimelinePillPlacementRegistry.findPointPillStrip(gridLine, offsetFraction);

      if (existingStrip) {
         return existingStrip;
      }

      const placementBand = DayPlannerTimelinePillPlacementRegistry.resolveStripPlacementBand(gridLine, offsetFraction);
      const pillStrip = ItineraryPanelDom.el('div', 'itinerary-day-pill-strip');

      if (offsetFraction > 0) {
         pillStrip.setAttribute('data-offset-fraction', String(offsetFraction));
         pillStrip.style.setProperty(
            '--itinerary-pill-offset-fraction',
            String(offsetFraction)
         );
      }

      DayPlannerTimelinePillPlacementRegistry.applyHorizontalOffsetIndex(pillStrip, 0);
      DayPlannerTimelinePillPlacementRegistry.registerTimelinePlacement(gridLine, {
         ...placementBand,
         anchorOffsetFraction: offsetFraction,
         horizontalOffsetIndex: 0,
      });
      gridLine.appendChild(pillStrip);

      return pillStrip;
   }

   static createScheduledPillStrip(
      gridLine,
      offsetFraction = 0,
      durationMinutes = 0,
      slotSpanMinutes = TimelineLayoutConstants.TIMELINE_SLOT_MINUTES
   ) {
      const placementBand = DayPlannerTimelinePillPlacementRegistry.resolveStripPlacementBand(
         gridLine,
         offsetFraction,
         durationMinutes,
         slotSpanMinutes
      );
      const pillStrip = ItineraryPanelDom.el('div', 'itinerary-day-pill-strip');

      if (offsetFraction > 0) {
         pillStrip.setAttribute('data-offset-fraction', String(offsetFraction));
         pillStrip.style.setProperty(
            '--itinerary-pill-offset-fraction',
            String(offsetFraction)
         );
      }

      DayPlannerTimelinePillPlacementRegistry.markScheduledPillStrip(pillStrip);
      DayPlannerTimelinePillPlacementRegistry.registerTimelinePlacement(gridLine, {
         ...placementBand,
         anchorOffsetFraction: offsetFraction,
         horizontalOffsetIndex: 0,
      });
      gridLine.appendChild(pillStrip);

      return pillStrip;
   }

   static computeStripHorizontalOffsetIndex(
      placedStrips,
      offsetFraction,
      pointPillVerticalSpanFraction
   ) {
      return DayPlannerTimelinePillPlacement.computeTimelineHorizontalOffsetIndex(
         placedStrips.map((strip) => ({
            offsetFraction: strip.offsetFraction,
            durationFraction: pointPillVerticalSpanFraction,
            horizontalOffsetIndex: strip.horizontalOffsetIndex,
         })),
         offsetFraction,
         pointPillVerticalSpanFraction
      );
   }

   /** @deprecated */
   static computeSpanHorizontalOffsetIndex(...args) {
      return DayPlannerTimelinePillPlacement.computeTimelineHorizontalOffsetIndex(...args);
   }
}
