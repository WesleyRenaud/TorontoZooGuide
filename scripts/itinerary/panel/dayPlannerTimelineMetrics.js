import { DayPlannerTimelinePlacement } from './dayPlannerTimelinePlacement.js';

const timelineSlotHeightByTimeline = new WeakMap();
const pointPillHeightByTimeline = new WeakMap();
const pointPillStripTopOffsetByTimeline = new WeakMap();

export class DayPlannerTimelineMetrics {
   static getTimelineSlotHeightPx(gridLine) {
      const timeline = DayPlannerTimelinePlacement.resolveTimelineElement(gridLine);

      if (!timeline) {
         return null;
      }

      const cachedHeight = timelineSlotHeightByTimeline.get(timeline);

      if (cachedHeight) {
         return cachedHeight;
      }

      let slotHeight = null;

      if (typeof getComputedStyle === 'function') {
         slotHeight = DayPlannerTimelinePlacement.readCssLengthPx(
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


   static measurePointPillStripTopOffsetPx(gridLine) {
      const timeline = DayPlannerTimelinePlacement.resolveTimelineElement(gridLine);

      if (!timeline) {
         return null;
      }

      const cachedOffset = pointPillStripTopOffsetByTimeline.get(timeline);

      if (cachedOffset) {
         return cachedOffset;
      }

      if (typeof getComputedStyle === 'function') {
         const fromCssVariable = DayPlannerTimelinePlacement.readCssLengthPx(
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

      const stripTopOffset = DayPlannerTimelinePlacement.parseStripTopOffsetFromProbeTop(topPx);

      if (stripTopOffset) {
         pointPillStripTopOffsetByTimeline.set(timeline, stripTopOffset);
      }

      return stripTopOffset;
   }


   static measurePointPillHeightPx(gridLine) {
      const timeline = DayPlannerTimelinePlacement.resolveTimelineElement(gridLine);

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


   static getPointPillVerticalSpanFraction(gridLine) {
      const slotHeight = DayPlannerTimelineMetrics.getTimelineSlotHeightPx(gridLine);

      if (!slotHeight) {
         return null;
      }

      const measuredPillHeight = DayPlannerTimelineMetrics.measurePointPillHeightPx(gridLine);

      if (measuredPillHeight) {
         return DayPlannerTimelinePlacement.computePointPillVerticalSpanFraction(slotHeight, measuredPillHeight);
      }

      const existingPill = gridLine.querySelector?.('.itinerary-day-open-pill');

      if (existingPill?.offsetHeight > 0) {
         return DayPlannerTimelinePlacement.computePointPillVerticalSpanFraction(slotHeight, existingPill.offsetHeight);
      }

      return null;
   }


   static getPointPillStripPlacementBand(gridLine, offsetFraction = 0) {
      return DayPlannerTimelinePlacement.computePointPillStripPlacementBand({
         slotHeight: DayPlannerTimelineMetrics.getTimelineSlotHeightPx(gridLine),
         pillHeight: DayPlannerTimelineMetrics.measurePointPillHeightPx(gridLine),
         stripTopOffset: DayPlannerTimelineMetrics.measurePointPillStripTopOffsetPx(gridLine),
         offsetFraction,
      });
   }

}
