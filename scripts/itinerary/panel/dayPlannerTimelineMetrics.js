import { DayPlannerTimelinePlacer } from './dayPlannerTimelinePlacer.js';

export class DayPlannerTimelineMetrics {
   static timelineSlotHeightByTimeline = new WeakMap();

   static pointPillHeightByTimeline = new WeakMap();

   static pointPillStripTopOffsetByTimeline = new WeakMap();

   static getTimelineSlotHeightPx(gridLine) {
      const timeline = DayPlannerTimelinePlacer.resolveTimelineElement(gridLine);

      if (!timeline) {
         return null;
      }

      const cachedHeight = DayPlannerTimelineMetrics.timelineSlotHeightByTimeline.get(timeline);

      if (cachedHeight) {
         return cachedHeight;
      }

      let slotHeight = null;

      if (typeof getComputedStyle === 'function') {
         slotHeight = DayPlannerTimelinePlacer.readCssLengthPx(
            getComputedStyle(timeline),
            '--itinerary-half-hour-slot-height'
         );
      }

      if (!slotHeight && gridLine.offsetHeight > 0) {
         slotHeight = gridLine.offsetHeight;
      }

      if (slotHeight) {
         DayPlannerTimelineMetrics.timelineSlotHeightByTimeline.set(timeline, slotHeight);
      }

      return slotHeight;
   }


   static measurePointPillStripTopOffsetPx(gridLine) {
      const timeline = DayPlannerTimelinePlacer.resolveTimelineElement(gridLine);

      if (!timeline) {
         return null;
      }

      const cachedOffset = DayPlannerTimelineMetrics.pointPillStripTopOffsetByTimeline.get(timeline);

      if (cachedOffset) {
         return cachedOffset;
      }

      if (typeof getComputedStyle === 'function') {
         const fromCssVariable = DayPlannerTimelinePlacer.readCssLengthPx(
            getComputedStyle(timeline),
            '--itinerary-pill-strip-top-offset'
         );

         if (fromCssVariable) {
            DayPlannerTimelineMetrics.pointPillStripTopOffsetByTimeline.set(timeline, fromCssVariable);
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

      const stripTopOffset = DayPlannerTimelinePlacer.parseStripTopOffsetFromProbeTop(topPx);

      if (stripTopOffset) {
         DayPlannerTimelineMetrics.pointPillStripTopOffsetByTimeline.set(timeline, stripTopOffset);
      }

      return stripTopOffset;
   }


   static measurePointPillHeightPx(gridLine) {
      const timeline = DayPlannerTimelinePlacer.resolveTimelineElement(gridLine);

      if (!timeline || typeof document === 'undefined') {
         return null;
      }

      const cachedHeight = DayPlannerTimelineMetrics.pointPillHeightByTimeline.get(timeline);

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
         DayPlannerTimelineMetrics.pointPillHeightByTimeline.set(timeline, pillHeight);
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
         return DayPlannerTimelinePlacer.computePointPillVerticalSpanFraction(slotHeight, measuredPillHeight);
      }

      const existingPill = gridLine.querySelector?.('.itinerary-day-open-pill');

      if (existingPill?.offsetHeight > 0) {
         return DayPlannerTimelinePlacer.computePointPillVerticalSpanFraction(slotHeight, existingPill.offsetHeight);
      }

      return null;
   }


   static getPointPillStripPlacementBand(gridLine, offsetFraction = 0) {
      return DayPlannerTimelinePlacer.computePointPillStripPlacementBand({
         slotHeight: DayPlannerTimelineMetrics.getTimelineSlotHeightPx(gridLine),
         pillHeight: DayPlannerTimelineMetrics.measurePointPillHeightPx(gridLine),
         stripTopOffset: DayPlannerTimelineMetrics.measurePointPillStripTopOffsetPx(gridLine),
         offsetFraction,
      });
   }

}
