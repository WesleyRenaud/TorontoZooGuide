import {
   computePointPillStripPlacementBand,
   computePointPillVerticalSpanFraction,
   parseStripTopOffsetFromProbeTop,
   readCssLengthPx,
   resolveTimelineElement,
} from './dayPlannerTimelinePlacement.js';

const timelineSlotHeightByTimeline = new WeakMap();
const pointPillHeightByTimeline = new WeakMap();
const pointPillStripTopOffsetByTimeline = new WeakMap();

export function getTimelineSlotHeightPx(gridLine) {
   const timeline = resolveTimelineElement(gridLine);

   if (!timeline) {
      return null;
   }

   const cachedHeight = timelineSlotHeightByTimeline.get(timeline);

   if (cachedHeight) {
      return cachedHeight;
   }

   let slotHeight = null;

   if (typeof getComputedStyle === 'function') {
      slotHeight = readCssLengthPx(
         getComputedStyle(timeline),
         '--itinerary-half-hour-slot-height'
      );
   }

   if (!slotHeight && gridLine.offsetHeight > 0) {
      slotHeight = gridLine.offsetHeight;
   }

   if (slotHeight) {
      timelineSlotHeightByTimeline.set(timeline, slotHeight);
   }

   return slotHeight;
}

export function measurePointPillStripTopOffsetPx(gridLine) {
   const timeline = resolveTimelineElement(gridLine);

   if (!timeline) {
      return null;
   }

   const cachedOffset = pointPillStripTopOffsetByTimeline.get(timeline);

   if (cachedOffset) {
      return cachedOffset;
   }

   if (typeof getComputedStyle === 'function') {
      const fromCssVariable = readCssLengthPx(
         getComputedStyle(timeline),
         '--itinerary-pill-strip-top-offset'
      );

      if (fromCssVariable) {
         pointPillStripTopOffsetByTimeline.set(timeline, fromCssVariable);
         return fromCssVariable;
      }
   }

   if (typeof document === 'undefined') {
      return null;
   }

   const probeStrip = document.createElement('div');
   probeStrip.className = 'itinerary-day-pill-strip';
   probeStrip.style.visibility = 'hidden';
   probeStrip.style.position = 'absolute';
   probeStrip.style.pointerEvents = 'none';
   gridLine.appendChild(probeStrip);

   const topPx = Number.parseFloat(getComputedStyle(probeStrip).top);
   gridLine.removeChild(probeStrip);

   const stripTopOffset = parseStripTopOffsetFromProbeTop(topPx);

   if (stripTopOffset) {
      pointPillStripTopOffsetByTimeline.set(timeline, stripTopOffset);
   }

   return stripTopOffset;
}

export function measurePointPillHeightPx(gridLine) {
   const timeline = resolveTimelineElement(gridLine);

   if (!timeline || typeof document === 'undefined') {
      return null;
   }

   const cachedHeight = pointPillHeightByTimeline.get(timeline);

   if (cachedHeight) {
      return cachedHeight;
   }

   const probePill = document.createElement('span');
   probePill.className = 'itinerary-day-open-pill';
   probePill.textContent = 'Arrival';

   const probeStrip = document.createElement('div');
   probeStrip.className = 'itinerary-day-pill-strip';
   probeStrip.style.visibility = 'hidden';
   probeStrip.style.position = 'absolute';
   probeStrip.style.pointerEvents = 'none';
   probeStrip.appendChild(probePill);
   gridLine.appendChild(probeStrip);

   const pillHeight = probePill.offsetHeight
      || probePill.getBoundingClientRect?.().height
      || 0;

   gridLine.removeChild(probeStrip);

   if (pillHeight > 0) {
      pointPillHeightByTimeline.set(timeline, pillHeight);
      return pillHeight;
   }

   return null;
}

export function getPointPillVerticalSpanFraction(gridLine) {
   const slotHeight = getTimelineSlotHeightPx(gridLine);

   if (!slotHeight) {
      return null;
   }

   const measuredPillHeight = measurePointPillHeightPx(gridLine);

   if (measuredPillHeight) {
      return computePointPillVerticalSpanFraction(slotHeight, measuredPillHeight);
   }

   const existingPill = gridLine.querySelector?.('.itinerary-day-open-pill');

   if (existingPill?.offsetHeight > 0) {
      return computePointPillVerticalSpanFraction(slotHeight, existingPill.offsetHeight);
   }

   return null;
}

export function getPointPillStripPlacementBand(gridLine, offsetFraction = 0) {
   return computePointPillStripPlacementBand({
      slotHeight: getTimelineSlotHeightPx(gridLine),
      pillHeight: measurePointPillHeightPx(gridLine),
      stripTopOffset: measurePointPillStripTopOffsetPx(gridLine),
      offsetFraction,
   });
}
