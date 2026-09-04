import { DayPlannerTimelineMetrics } from '../dayPlannerTimelineMetrics.js';
import { el } from '../dom.js';
import { TIMELINE_SLOT_MINUTES } from '../../../shared/constants.js';

const timelinePlacementsByGridLine = new WeakMap();

function getTimelinePlacements(gridLine) {
   let placements = timelinePlacementsByGridLine.get(gridLine);

   if (!placements) {
      placements = [];
      timelinePlacementsByGridLine.set(gridLine, placements);
   }

   return placements;
}

function applyHorizontalOffsetIndex(element, horizontalOffsetIndex) {
   element.setAttribute('data-horizontal-offset-index', String(horizontalOffsetIndex));
   element.style.setProperty(
      '--itinerary-pill-horizontal-offset-index',
      String(horizontalOffsetIndex)
   );
}

function markScheduledPillStrip(pillStrip) {
   pillStrip.setAttribute('data-scheduled-column', 'true');
}

function registerTimelinePlacement(
   gridLine,
   {
      offsetFraction,
      durationFraction,
      horizontalOffsetIndex,
      anchorOffsetFraction,
   }
) {
   getTimelinePlacements(gridLine).push({
      offsetFraction,
      durationFraction,
      horizontalOffsetIndex,
      anchorOffsetFraction,
   });
}

function isScheduledPillStrip(strip) {
   return (
      strip.getAttribute?.('data-scheduled-column')
      ?? strip.attributes?.['data-scheduled-column']
   ) === 'true';
}

function findPointPillStrip(gridLine, offsetFraction = 0) {
   const offsetKey = String(offsetFraction);

   for (const child of gridLine.children) {
      if (child.className !== 'itinerary-day-pill-strip' || isScheduledPillStrip(child)) {
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

function resolveStripPlacementBand(
   gridLine,
   offsetFraction = 0,
   durationMinutes = null,
   slotSpanMinutes = TIMELINE_SLOT_MINUTES
) {
   const pointBand = DayPlannerTimelineMetrics.getPointPillStripPlacementBand(gridLine, offsetFraction);

   if (Number.isFinite(durationMinutes) && durationMinutes > 0) {
      const slotSpan = Number.isFinite(slotSpanMinutes) && slotSpanMinutes > 0
         ? slotSpanMinutes
         : TIMELINE_SLOT_MINUTES;

      return {
         offsetFraction: pointBand.offsetFraction,
         durationFraction: durationMinutes / slotSpan,
      };
   }

   return pointBand;
}

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
      const existingStrip = findPointPillStrip(gridLine, offsetFraction);

      if (existingStrip) {
         return existingStrip;
      }

      const placementBand = resolveStripPlacementBand(gridLine, offsetFraction);
      const pillStrip = el('div', 'itinerary-day-pill-strip');

      if (offsetFraction > 0) {
         pillStrip.setAttribute('data-offset-fraction', String(offsetFraction));
         pillStrip.style.setProperty(
            '--itinerary-pill-offset-fraction',
            String(offsetFraction)
         );
      }

      applyHorizontalOffsetIndex(pillStrip, 0);
      registerTimelinePlacement(gridLine, {
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
      slotSpanMinutes = TIMELINE_SLOT_MINUTES
   ) {
      const placementBand = resolveStripPlacementBand(
         gridLine,
         offsetFraction,
         durationMinutes,
         slotSpanMinutes
      );
      const pillStrip = el('div', 'itinerary-day-pill-strip');

      if (offsetFraction > 0) {
         pillStrip.setAttribute('data-offset-fraction', String(offsetFraction));
         pillStrip.style.setProperty(
            '--itinerary-pill-offset-fraction',
            String(offsetFraction)
         );
      }

      markScheduledPillStrip(pillStrip);
      registerTimelinePlacement(gridLine, {
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
