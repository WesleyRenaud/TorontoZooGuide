import { DayPlannerTimelinePillPlacementRegistrar } from './dayPlannerTimelinePillPlacementRegistrar.js';
import { ItineraryPanelHelper } from '../itineraryPanelHelper.js';
import { TimelineLayoutConstants } from '../../../shared/timelineLayoutConstants.js';

export class DayPlannerTimelinePillPlacer {
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
      const existingStrip = DayPlannerTimelinePillPlacementRegistrar.findPointPillStrip(gridLine, offsetFraction);

      if (existingStrip) {
         return existingStrip;
      }

      const placementBand = DayPlannerTimelinePillPlacementRegistrar.resolveStripPlacementBand(gridLine, offsetFraction);
      const pillStrip = ItineraryPanelHelper.el('div', 'itinerary-day-pill-strip');

      if (offsetFraction > 0) {
         pillStrip.setAttribute('data-offset-fraction', String(offsetFraction));
         pillStrip.style.setProperty(
            '--itinerary-pill-offset-fraction',
            String(offsetFraction)
         );
      }

      DayPlannerTimelinePillPlacementRegistrar.applyHorizontalOffsetIndex(pillStrip, 0);
      DayPlannerTimelinePillPlacementRegistrar.registerTimelinePlacement(gridLine, {
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
      const placementBand = DayPlannerTimelinePillPlacementRegistrar.resolveStripPlacementBand(
         gridLine,
         offsetFraction,
         durationMinutes,
         slotSpanMinutes
      );
      const pillStrip = ItineraryPanelHelper.el('div', 'itinerary-day-pill-strip');

      if (offsetFraction > 0) {
         pillStrip.setAttribute('data-offset-fraction', String(offsetFraction));
         pillStrip.style.setProperty(
            '--itinerary-pill-offset-fraction',
            String(offsetFraction)
         );
      }

      DayPlannerTimelinePillPlacementRegistrar.markScheduledPillStrip(pillStrip);
      DayPlannerTimelinePillPlacementRegistrar.registerTimelinePlacement(gridLine, {
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
      return DayPlannerTimelinePillPlacer.computeTimelineHorizontalOffsetIndex(
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
      return DayPlannerTimelinePillPlacer.computeTimelineHorizontalOffsetIndex(...args);
   }
}
