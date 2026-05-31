import { getPointPillStripPlacementBand } from '../dayPlannerTimelineMetrics.js';
import { el } from '../dom.js';
import { TIMELINE_SLOT_MINUTES } from '../../../shared/constants.js';

const timelinePlacementsByGridLine = new WeakMap();

function makeTimelinePill(label) {
   return el('span', 'itinerary-day-open-pill', label);
}

function makeScheduledPill(label, durationMinutes) {
   const durationFraction = durationMinutes / TIMELINE_SLOT_MINUTES;
   const pill = el('span', 'itinerary-day-scheduled-pill', label);

   pill.style.setProperty(
      '--itinerary-scheduled-pill-duration-fraction',
      String(durationFraction)
   );
   pill.setAttribute('data-duration-fraction', String(durationFraction));

   return pill;
}

function getTimelinePlacements(gridLine) {
   let placements = timelinePlacementsByGridLine.get(gridLine);

   if (!placements) {
      placements = [];
      timelinePlacementsByGridLine.set(gridLine, placements);
   }

   return placements;
}

export function computeTimelineHorizontalOffsetIndex(
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

function applyHorizontalOffsetIndex(element, horizontalOffsetIndex) {
   if (horizontalOffsetIndex <= 0) {
      return;
   }

   element.setAttribute('data-horizontal-offset-index', String(horizontalOffsetIndex));
   element.style.setProperty(
      '--itinerary-pill-horizontal-offset-index',
      String(horizontalOffsetIndex)
   );
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

function findPlacementForOffset(gridLine, offsetFraction) {
   const offsetKey = String(offsetFraction);

   return getTimelinePlacements(gridLine).find(
      (placement) => String(placement.anchorOffsetFraction) === offsetKey
   ) ?? null;
}

function findPillStrip(gridLine, offsetFraction = 0) {
   const offsetKey = String(offsetFraction);

   for (const child of gridLine.children) {
      if (child.className !== 'itinerary-day-pill-strip') {
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

function getOrCreatePillStrip(gridLine, offsetFraction = 0) {
   const existingStrip = findPillStrip(gridLine, offsetFraction);

   if (existingStrip) {
      return existingStrip;
   }

   const placementBand = getPointPillStripPlacementBand(gridLine, offsetFraction);
   const placements = getTimelinePlacements(gridLine);
   const horizontalOffsetIndex = computeTimelineHorizontalOffsetIndex(
      placements,
      placementBand.offsetFraction,
      placementBand.durationFraction
   );
   const pillStrip = el('div', 'itinerary-day-pill-strip');

   if (offsetFraction > 0) {
      pillStrip.setAttribute('data-offset-fraction', String(offsetFraction));
      pillStrip.style.setProperty(
         '--itinerary-pill-offset-fraction',
         String(offsetFraction)
      );
   }

   applyHorizontalOffsetIndex(pillStrip, horizontalOffsetIndex);
   registerTimelinePlacement(gridLine, {
      ...placementBand,
      anchorOffsetFraction: offsetFraction,
      horizontalOffsetIndex,
   });
   gridLine.appendChild(pillStrip);

   return pillStrip;
}

function expandPlacementForScheduledPill(
   gridLine,
   offsetFraction,
   durationMinutes
) {
   const existingPlacement = findPlacementForOffset(gridLine, offsetFraction);

   if (!existingPlacement) {
      return;
   }

   const durationFraction = durationMinutes / TIMELINE_SLOT_MINUTES;

   existingPlacement.durationFraction = Math.max(
      existingPlacement.durationFraction,
      durationFraction
   );
}

function findFirstScheduledPillInStrip(strip) {
   for (const child of strip.children) {
      if (child.className === 'itinerary-day-scheduled-pill') {
         return child;
      }
   }

   return null;
}

function insertPointPillInStrip(strip, pill) {
   const firstScheduledPill = findFirstScheduledPillInStrip(strip);

   if (firstScheduledPill) {
      strip.insertBefore(pill, firstScheduledPill);
      return;
   }

   strip.appendChild(pill);
}

export function appendTimelinePill(gridLine, label, offsetFraction = 0) {
   if (!label) {
      return;
   }

   insertPointPillInStrip(
      getOrCreatePillStrip(gridLine, offsetFraction),
      makeTimelinePill(label)
   );
}

export function appendScheduledDurationPill(
   gridLine,
   {
      label,
      offsetFraction = 0,
      durationMinutes,
   }
) {
   if (!label || !Number.isFinite(durationMinutes) || durationMinutes <= 0) {
      return;
   }

   const strip = getOrCreatePillStrip(gridLine, offsetFraction);

   expandPlacementForScheduledPill(gridLine, offsetFraction, durationMinutes);
   strip.appendChild(makeScheduledPill(label, durationMinutes));
}

export function appendItineraryTimeMarkers(gridLine, markersByAnchorSlot, slotStart) {
   (markersByAnchorSlot.get(slotStart) ?? []).forEach((marker) => {
      appendTimelinePill(gridLine, marker.label, marker.offsetFraction);
   });
}

export function computeStripHorizontalOffsetIndex(
   placedStrips,
   offsetFraction,
   pointPillVerticalSpanFraction
) {
   return computeTimelineHorizontalOffsetIndex(
      placedStrips.map((strip) => ({
         offsetFraction: strip.offsetFraction,
         durationFraction: pointPillVerticalSpanFraction,
         horizontalOffsetIndex: strip.horizontalOffsetIndex,
      })),
      offsetFraction,
      pointPillVerticalSpanFraction
   );
}

export const computeSpanHorizontalOffsetIndex = computeTimelineHorizontalOffsetIndex;
