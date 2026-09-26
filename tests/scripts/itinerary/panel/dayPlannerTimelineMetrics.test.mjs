import assert from 'node:assert/strict';
import { test } from 'node:test';

import { DayPlannerTimelineMetrics } from '../../../../scripts/itinerary/panel/dayPlannerTimelineMetrics.js';
import { DayPlannerTimelinePlacer } from '../../../../scripts/itinerary/panel/dayPlannerTimelinePlacer.js';
import { TimelineLayoutConstants } from '../../../../scripts/shared/timelineLayoutConstants.js';
import { createDomNode } from '../../helpers/domNodeMock.mjs';
import { installDomTestHooks } from '../../helpers/domTestSetup.mjs';

function _makeTimelineGridLine() {
   const timeline = createDomNode('div', 'itinerary-day-timeline');
   const gridLine = createDomNode('div', 'itinerary-day-grid-line');

   timeline.appendChild(gridLine);

   return { timeline, gridLine };
}

installDomTestHooks();


test('Test_ReadCssLengthPx_TestPositiveLength_ExpectParsed', () => {
   const lengthPx = 730;
   const property = '--valid';
   const style = {
      getPropertyValue(name) {
         return name === property ? ` ${lengthPx}px ` : '';
      },
   };

   const parsed = DayPlannerTimelinePlacer.readCssLengthPx(style, property);

   assert.equal(parsed, lengthPx);
});


test('Test_ReadCssLengthPx_TestZeroLength_ExpectNull', () => {
   const property = '--zero';
   const style = {
      getPropertyValue(name) {
         return name === property ? '0px' : '';
      },
   };

   const parsed = DayPlannerTimelinePlacer.readCssLengthPx(style, property);

   assert.equal(parsed, null);
});


test('Test_ReadCssLengthPx_TestInvalidLength_ExpectNull', () => {
   const property = '--invalid';
   const style = {
      getPropertyValue(name) {
         return name === property ? 'auto' : '';
      },
   };

   const parsed = DayPlannerTimelinePlacer.readCssLengthPx(style, property);

   assert.equal(parsed, null);
});


test('Test_ReadCssLengthPx_TestMissingProperty_ExpectNull', () => {
   const style = {
      getPropertyValue() {
         return '';
      },
   };

   const parsed = DayPlannerTimelinePlacer.readCssLengthPx(style, '--missing');

   assert.equal(parsed, null);
});


test('Test_ReadCssLengthPx_TestNullStyle_ExpectNull', () => {
   const parsed = DayPlannerTimelinePlacer.readCssLengthPx(null, '--valid');

   assert.equal(parsed, null);
});


test('Test_ResolveTimelineElement_TestWalksParents_ExpectTimeline', () => {
   const timeline = createDomNode('div', 'itinerary-day-timeline');
   const row = createDomNode('div', 'itinerary-day-row');
   const gridLine = createDomNode('div', 'itinerary-day-grid-line');
   timeline.appendChild(row);
   row.appendChild(gridLine);

   const resolved = DayPlannerTimelinePlacer.resolveTimelineElement(gridLine);

   assert.equal(resolved, timeline);
});


test('Test_ResolveTimelineElement_TestNull_ExpectNull', () => {
   const resolved = DayPlannerTimelinePlacer.resolveTimelineElement(null);

   assert.equal(resolved, null);
});


test('Test_ParseStripTopOffsetFromProbeTop_TestNegativeProbe_ExpectOffset', () => {
   const probeTop = -80;

   const offset = DayPlannerTimelinePlacer.parseStripTopOffsetFromProbeTop(probeTop);

   assert.equal(offset, Math.abs(probeTop));
});


test('Test_ParseStripTopOffsetFromProbeTop_TestZero_ExpectNull', () => {
   const offset = DayPlannerTimelinePlacer.parseStripTopOffsetFromProbeTop(0);

   assert.equal(offset, null);
});


test('Test_ParseStripTopOffsetFromProbeTop_TestNaN_ExpectNull', () => {
   const offset = DayPlannerTimelinePlacer.parseStripTopOffsetFromProbeTop(Number.NaN);

   assert.equal(offset, null);
});


test('Test_ComputePointPillStripPlacementBand_TestAnchor_ExpectFractions', () => {
   const offsetFraction = 0;

   const atAnchor = DayPlannerTimelinePlacer.computePointPillStripPlacementBand({
      slotHeight: TimelineLayoutConstants.TIMELINE_SLOT_HEIGHT_PX,
      pillHeight: TimelineLayoutConstants.TIMELINE_POINT_PILL_HEIGHT_PX,
      stripTopOffset: TimelineLayoutConstants.TIMELINE_PILL_STRIP_TOP_OFFSET_PX,
      offsetFraction,
   });

   assert.equal(
      atAnchor.offsetFraction,
      -TimelineLayoutConstants.TIMELINE_PILL_STRIP_TOP_OFFSET_PX / TimelineLayoutConstants.TIMELINE_SLOT_HEIGHT_PX
   );
   assert.equal(
      atAnchor.durationFraction,
      TimelineLayoutConstants.TIMELINE_POINT_PILL_HEIGHT_PX / TimelineLayoutConstants.TIMELINE_SLOT_HEIGHT_PX
   );
});


test('Test_ComputePointPillStripPlacementBand_TestMidway_ExpectOffsetFraction', () => {
   const offsetFraction = 0.5;

   const midway = DayPlannerTimelinePlacer.computePointPillStripPlacementBand({
      slotHeight: TimelineLayoutConstants.TIMELINE_SLOT_HEIGHT_PX,
      pillHeight: TimelineLayoutConstants.TIMELINE_POINT_PILL_HEIGHT_PX,
      stripTopOffset: TimelineLayoutConstants.TIMELINE_PILL_STRIP_TOP_OFFSET_PX,
      offsetFraction,
   });

   assert.equal(
      midway.offsetFraction,
      (
         offsetFraction * TimelineLayoutConstants.TIMELINE_SLOT_HEIGHT_PX
         - TimelineLayoutConstants.TIMELINE_PILL_STRIP_TOP_OFFSET_PX
      ) / TimelineLayoutConstants.TIMELINE_SLOT_HEIGHT_PX
   );
});


test('Test_ComputePointPillStripPlacementBand_TestMissingMeasurements_ExpectFallback', () => {
   const offsetFraction = 0.25;

   const band = DayPlannerTimelinePlacer.computePointPillStripPlacementBand({
      slotHeight: null,
      pillHeight: TimelineLayoutConstants.TIMELINE_POINT_PILL_HEIGHT_PX,
      stripTopOffset: TimelineLayoutConstants.TIMELINE_PILL_STRIP_TOP_OFFSET_PX,
      offsetFraction,
   });

   assert.deepEqual(band, {
      offsetFraction,
      durationFraction: 0,
   });
});


test('Test_ComputePointPillVerticalSpanFraction_TestMeasuredHeights_ExpectRatio', () => {
   const span = DayPlannerTimelinePlacer.computePointPillVerticalSpanFraction(
      TimelineLayoutConstants.TIMELINE_SLOT_HEIGHT_PX,
      TimelineLayoutConstants.TIMELINE_POINT_PILL_HEIGHT_PX
   );

   assert.equal(
      span,
      TimelineLayoutConstants.TIMELINE_POINT_PILL_HEIGHT_PX / TimelineLayoutConstants.TIMELINE_SLOT_HEIGHT_PX
   );
});


test('Test_ComputePointPillVerticalSpanFraction_TestZeroSlot_ExpectNull', () => {
   const pillHeight = 10;

   const span = DayPlannerTimelinePlacer.computePointPillVerticalSpanFraction(0, pillHeight);

   assert.equal(span, null);
});


test('Test_GetTimelineSlotHeightPx_TestCssVariable_ExpectSlotHeight', () => {
   const { gridLine } = _makeTimelineGridLine();

   const slotHeight = DayPlannerTimelineMetrics.getTimelineSlotHeightPx(gridLine);

   assert.equal(slotHeight, TimelineLayoutConstants.TIMELINE_SLOT_HEIGHT_PX);
});


test('Test_MeasurePointPillHeightPx_TestCssVariable_ExpectPillHeight', () => {
   const { gridLine } = _makeTimelineGridLine();

   const pillHeight = DayPlannerTimelineMetrics.measurePointPillHeightPx(gridLine);

   assert.equal(pillHeight, TimelineLayoutConstants.TIMELINE_POINT_PILL_HEIGHT_PX);
});


test('Test_MeasurePointPillStripTopOffsetPx_TestCssVariable_ExpectStripOffset', () => {
   const { gridLine } = _makeTimelineGridLine();

   const stripOffset = DayPlannerTimelineMetrics.measurePointPillStripTopOffsetPx(gridLine);

   assert.equal(stripOffset, TimelineLayoutConstants.TIMELINE_PILL_STRIP_TOP_OFFSET_PX);
});


test('Test_GetPointPillVerticalSpanFraction_TestMeasuredHeights_ExpectRatio', () => {
   const { gridLine } = _makeTimelineGridLine();

   const span = DayPlannerTimelineMetrics.getPointPillVerticalSpanFraction(gridLine);

   assert.equal(
      span,
      TimelineLayoutConstants.TIMELINE_POINT_PILL_HEIGHT_PX / TimelineLayoutConstants.TIMELINE_SLOT_HEIGHT_PX
   );
});


test('Test_GetPointPillStripPlacementBand_TestComputedFractions_ExpectMatch', () => {
   const { gridLine } = _makeTimelineGridLine();
   const offsetFraction = 0;

   const band = DayPlannerTimelineMetrics.getPointPillStripPlacementBand(gridLine, offsetFraction);

   assert.deepEqual(
      band,
      DayPlannerTimelinePlacer.computePointPillStripPlacementBand({
         slotHeight: TimelineLayoutConstants.TIMELINE_SLOT_HEIGHT_PX,
         pillHeight: TimelineLayoutConstants.TIMELINE_POINT_PILL_HEIGHT_PX,
         stripTopOffset: TimelineLayoutConstants.TIMELINE_PILL_STRIP_TOP_OFFSET_PX,
         offsetFraction,
      })
   );
});


test('Test_GetPointPillVerticalSpanFraction_TestExistingOpenPill_ExpectFallbackHeight', () => {
   const { timeline, gridLine } = _makeTimelineGridLine();
   const originalMeasure = DayPlannerTimelineMetrics.measurePointPillHeightPx;
   DayPlannerTimelineMetrics.pointPillHeightByTimeline.delete(timeline);
   DayPlannerTimelineMetrics.measurePointPillHeightPx = () => null;
   const pill = createDomNode('span', 'itinerary-day-open-pill');
   Object.defineProperty(pill, 'offsetHeight', {
      configurable: true,
      get: () => TimelineLayoutConstants.TIMELINE_POINT_PILL_HEIGHT_PX,
   });
   gridLine.appendChild(pill);

   try {
      const span = DayPlannerTimelineMetrics.getPointPillVerticalSpanFraction(gridLine);

      assert.equal(
         span,
         TimelineLayoutConstants.TIMELINE_POINT_PILL_HEIGHT_PX / TimelineLayoutConstants.TIMELINE_SLOT_HEIGHT_PX
      );
   } finally {
      DayPlannerTimelineMetrics.measurePointPillHeightPx = originalMeasure;
   }
});


test('Test_GetTimelineSlotHeightPx_TestNullTimeline_ExpectNull', () => {
   const slotHeight = DayPlannerTimelineMetrics.getTimelineSlotHeightPx(null);

   assert.equal(slotHeight, null);
});


test('Test_MeasurePointPillStripTopOffsetPx_TestNullTimeline_ExpectNull', () => {
   const stripOffset = DayPlannerTimelineMetrics.measurePointPillStripTopOffsetPx(null);

   assert.equal(stripOffset, null);
});


test('Test_MeasurePointPillHeightPx_TestNullTimeline_ExpectNull', () => {
   const pillHeight = DayPlannerTimelineMetrics.measurePointPillHeightPx(null);

   assert.equal(pillHeight, null);
});


test('Test_GetPointPillVerticalSpanFraction_TestNullTimeline_ExpectNull', () => {
   const span = DayPlannerTimelineMetrics.getPointPillVerticalSpanFraction(null);

   assert.equal(span, null);
});


test('Test_GetTimelineSlotHeightPx_TestCached_ExpectSameHeight', () => {
   const { gridLine } = _makeTimelineGridLine();

   const first = DayPlannerTimelineMetrics.getTimelineSlotHeightPx(gridLine);
   const second = DayPlannerTimelineMetrics.getTimelineSlotHeightPx(gridLine);

   assert.equal(first, TimelineLayoutConstants.TIMELINE_SLOT_HEIGHT_PX);
   assert.equal(second, TimelineLayoutConstants.TIMELINE_SLOT_HEIGHT_PX);
});


test('Test_MeasurePointPillStripTopOffsetPx_TestCached_ExpectSameOffset', () => {
   const { gridLine } = _makeTimelineGridLine();

   const first = DayPlannerTimelineMetrics.measurePointPillStripTopOffsetPx(gridLine);
   const second = DayPlannerTimelineMetrics.measurePointPillStripTopOffsetPx(gridLine);

   assert.equal(first, TimelineLayoutConstants.TIMELINE_PILL_STRIP_TOP_OFFSET_PX);
   assert.equal(second, TimelineLayoutConstants.TIMELINE_PILL_STRIP_TOP_OFFSET_PX);
});


test('Test_MeasurePointPillHeightPx_TestCached_ExpectSameHeight', () => {
   const { gridLine } = _makeTimelineGridLine();

   const first = DayPlannerTimelineMetrics.measurePointPillHeightPx(gridLine);
   const second = DayPlannerTimelineMetrics.measurePointPillHeightPx(gridLine);

   assert.equal(first, TimelineLayoutConstants.TIMELINE_POINT_PILL_HEIGHT_PX);
   assert.equal(second, TimelineLayoutConstants.TIMELINE_POINT_PILL_HEIGHT_PX);
});


test('Test_GetTimelineSlotHeightPx_TestOffsetHeightFallback_ExpectMeasured', () => {
   const { timeline, gridLine } = _makeTimelineGridLine();
   const fallbackHeight = 55;
   const originalGetComputedStyle = globalThis.getComputedStyle;
   DayPlannerTimelineMetrics.timelineSlotHeightByTimeline.delete(timeline);
   DayPlannerTimelineMetrics.pointPillStripTopOffsetByTimeline.delete(timeline);
   DayPlannerTimelineMetrics.pointPillHeightByTimeline.delete(timeline);
   globalThis.getComputedStyle = () => ({
      top: '-40px',
      getPropertyValue() {
         return '';
      },
   });
   Object.defineProperty(gridLine, 'offsetHeight', {
      configurable: true,
      get: () => fallbackHeight,
   });

   try {
      const slotHeight = DayPlannerTimelineMetrics.getTimelineSlotHeightPx(gridLine);

      assert.equal(slotHeight, fallbackHeight);
   } finally {
      globalThis.getComputedStyle = originalGetComputedStyle;
   }
});


test('Test_MeasurePointPillStripTopOffsetPx_TestNegativeProbeTop_ExpectOffset', () => {
   const { timeline, gridLine } = _makeTimelineGridLine();
   const probeTop = -40;
   const originalGetComputedStyle = globalThis.getComputedStyle;
   DayPlannerTimelineMetrics.timelineSlotHeightByTimeline.delete(timeline);
   DayPlannerTimelineMetrics.pointPillStripTopOffsetByTimeline.delete(timeline);
   DayPlannerTimelineMetrics.pointPillHeightByTimeline.delete(timeline);
   globalThis.getComputedStyle = () => ({
      top: `${probeTop}px`,
      getPropertyValue() {
         return '';
      },
   });

   try {
      const stripOffset = DayPlannerTimelineMetrics.measurePointPillStripTopOffsetPx(gridLine);

      assert.equal(stripOffset, Math.abs(probeTop));
   } finally {
      globalThis.getComputedStyle = originalGetComputedStyle;
   }
});


test('Test_MeasurePointPillStripTopOffsetPx_TestMissingDocument_ExpectNull', () => {
   const { timeline, gridLine } = _makeTimelineGridLine();
   const originalDocument = globalThis.document;
   const originalGetComputedStyle = globalThis.getComputedStyle;
   DayPlannerTimelineMetrics.pointPillStripTopOffsetByTimeline.delete(timeline);
   globalThis.getComputedStyle = () => ({
      top: '-40px',
      getPropertyValue() {
         return '';
      },
   });

   try {
      delete globalThis.document;
      const stripOffset = DayPlannerTimelineMetrics.measurePointPillStripTopOffsetPx(gridLine);

      assert.equal(stripOffset, null);
   } finally {
      globalThis.document = originalDocument;
      globalThis.getComputedStyle = originalGetComputedStyle;
   }
});


test('Test_MeasurePointPillHeightPx_TestZeroProbe_ExpectNull', () => {
   const { timeline, gridLine } = _makeTimelineGridLine();
   const originalCreate = document.createElement;
   DayPlannerTimelineMetrics.pointPillHeightByTimeline.delete(timeline);
   document.createElement = (tagName) => {
      const node = originalCreate.call(document, tagName);
      Object.defineProperty(node, 'offsetHeight', {
         configurable: true,
         get: () => 0,
      });
      node.getBoundingClientRect = () => ({ height: 0 });
      return node;
   };

   try {
      const pillHeight = DayPlannerTimelineMetrics.measurePointPillHeightPx(gridLine);

      assert.equal(pillHeight, null);
   } finally {
      document.createElement = originalCreate;
   }
});


test('Test_GetPointPillVerticalSpanFraction_TestEmptyOpenPill_ExpectNull', () => {
   const { gridLine } = _makeTimelineGridLine();
   const originalMeasure = DayPlannerTimelineMetrics.measurePointPillHeightPx;
   DayPlannerTimelineMetrics.measurePointPillHeightPx = () => null;
   const emptyPill = createDomNode('span', 'itinerary-day-open-pill');
   Object.defineProperty(emptyPill, 'offsetHeight', {
      configurable: true,
      get: () => 0,
   });
   gridLine.appendChild(emptyPill);

   try {
      const span = DayPlannerTimelineMetrics.getPointPillVerticalSpanFraction(gridLine);

      assert.equal(span, null);
   } finally {
      DayPlannerTimelineMetrics.measurePointPillHeightPx = originalMeasure;
   }
});
