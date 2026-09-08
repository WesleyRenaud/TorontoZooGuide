import assert from 'node:assert/strict';
import { test } from 'node:test';

import { TimelineLayoutConstants } from '../../../../scripts/shared/timelineLayoutConstants.js';
import { DayPlannerTimelinePlacer } from '../../../../scripts/itinerary/panel/dayPlannerTimelinePlacer.js';
import { DayPlannerTimelineMetrics } from '../../../../scripts/itinerary/panel/dayPlannerTimelineMetrics.js';
import { createDomNode } from '../../helpers/domNodeMock.mjs';
import { installDomTestHooks } from '../../helpers/domTestSetup.mjs';

function _makeTimelineGridLine() {
   const timeline = createDomNode('div', 'itinerary-day-timeline');
   const gridLine = createDomNode('div', 'itinerary-day-grid-line');

   timeline.appendChild(gridLine);

   return { timeline, gridLine };
}

installDomTestHooks();

test('Test_ReadCssLengthPx_TestParsesPositiveCSSLengthsAndRejectsInvalidValues_ExpectOk', () => {
   const style = {
      getPropertyValue(property) {
         if (property === '--valid') {
            return ' 730px ';
         }

         if (property === '--zero') {
            return '0px';
         }

         if (property === '--invalid') {
            return 'auto';
         }

         return '';
      },
   };

   assert.equal(DayPlannerTimelinePlacer.readCssLengthPx(style, '--valid'), 730);
   assert.equal(DayPlannerTimelinePlacer.readCssLengthPx(style, '--zero'), null);
   assert.equal(DayPlannerTimelinePlacer.readCssLengthPx(style, '--invalid'), null);
   assert.equal(DayPlannerTimelinePlacer.readCssLengthPx(style, '--missing'), null);
   assert.equal(DayPlannerTimelinePlacer.readCssLengthPx(null, '--valid'), null);
});

test('Test_ResolveTimelineElement_TestWalksParentNodesWhenClosestIsUnavailable_ExpectOk', () => {
   const timeline = createDomNode('div', 'itinerary-day-timeline');
   const row = createDomNode('div', 'itinerary-day-row');
   const gridLine = createDomNode('div', 'itinerary-day-grid-line');

   timeline.appendChild(row);
   row.appendChild(gridLine);

   assert.equal(DayPlannerTimelinePlacer.resolveTimelineElement(gridLine), timeline);
   assert.equal(DayPlannerTimelinePlacer.resolveTimelineElement(null), null);
});

test('Test_ParseStripTopOffsetFromProbeTop_TestConvertsNegativeProbeTopsToOffsets_ExpectOk', () => {
   assert.equal(DayPlannerTimelinePlacer.parseStripTopOffsetFromProbeTop(-80), 80);
   assert.equal(DayPlannerTimelinePlacer.parseStripTopOffsetFromProbeTop(0), null);
   assert.equal(DayPlannerTimelinePlacer.parseStripTopOffsetFromProbeTop(Number.NaN), null);
});

test('Test_ComputePointPillStripPlacementBand_TestConvertsSlotOffsetsIntoFractions_ExpectOk', () => {
   const atAnchor = DayPlannerTimelinePlacer.computePointPillStripPlacementBand({
      slotHeight: TimelineLayoutConstants.TIMELINE_SLOT_HEIGHT_PX,
      pillHeight: TimelineLayoutConstants.TIMELINE_POINT_PILL_HEIGHT_PX,
      stripTopOffset: TimelineLayoutConstants.TIMELINE_PILL_STRIP_TOP_OFFSET_PX,
      offsetFraction: 0,
   });

   assert.equal(
      atAnchor.offsetFraction,
      -TimelineLayoutConstants.TIMELINE_PILL_STRIP_TOP_OFFSET_PX / TimelineLayoutConstants.TIMELINE_SLOT_HEIGHT_PX
   );
   assert.equal(
      atAnchor.durationFraction,
      TimelineLayoutConstants.TIMELINE_POINT_PILL_HEIGHT_PX / TimelineLayoutConstants.TIMELINE_SLOT_HEIGHT_PX
   );

   const midway = DayPlannerTimelinePlacer.computePointPillStripPlacementBand({
      slotHeight: TimelineLayoutConstants.TIMELINE_SLOT_HEIGHT_PX,
      pillHeight: TimelineLayoutConstants.TIMELINE_POINT_PILL_HEIGHT_PX,
      stripTopOffset: TimelineLayoutConstants.TIMELINE_PILL_STRIP_TOP_OFFSET_PX,
      offsetFraction: 0.5,
   });

   assert.equal(
      midway.offsetFraction,
      (0.5 * TimelineLayoutConstants.TIMELINE_SLOT_HEIGHT_PX - TimelineLayoutConstants.TIMELINE_PILL_STRIP_TOP_OFFSET_PX)
         / TimelineLayoutConstants.TIMELINE_SLOT_HEIGHT_PX
   );
});

test('Test_ComputePointPillStripPlacementBand_TestFallsBackWhenMeasurementsAreMissing_ExpectOk', () => {
   assert.deepEqual(
      DayPlannerTimelinePlacer.computePointPillStripPlacementBand({
         slotHeight: null,
         pillHeight: TimelineLayoutConstants.TIMELINE_POINT_PILL_HEIGHT_PX,
         stripTopOffset: TimelineLayoutConstants.TIMELINE_PILL_STRIP_TOP_OFFSET_PX,
         offsetFraction: 0.25,
      }),
      {
         offsetFraction: 0.25,
         durationFraction: 0,
      }
   );
});

test('Test_ComputePointPillVerticalSpanFraction_TestReturnsPillHeightRelativeToSlotHeight_ExpectOk', () => {
   assert.equal(
      DayPlannerTimelinePlacer.computePointPillVerticalSpanFraction(
         TimelineLayoutConstants.TIMELINE_SLOT_HEIGHT_PX,
         TimelineLayoutConstants.TIMELINE_POINT_PILL_HEIGHT_PX
      ),
      TimelineLayoutConstants.TIMELINE_POINT_PILL_HEIGHT_PX / TimelineLayoutConstants.TIMELINE_SLOT_HEIGHT_PX
   );
   assert.equal(DayPlannerTimelinePlacer.computePointPillVerticalSpanFraction(0, 10), null);
});

test('Test_GetTimelineSlotHeightPx_TestReadsTheTimelineSlotHeightFromCSSVariables_ExpectOk', () => {
   const { gridLine } = _makeTimelineGridLine();

   assert.equal(DayPlannerTimelineMetrics.getTimelineSlotHeightPx(gridLine), TimelineLayoutConstants.TIMELINE_SLOT_HEIGHT_PX);
});

test('Test_MeasurePointPillHeightPx_TestAndStripOffsetUseTimelineCSSVariables_ExpectOk', () => {
   const { gridLine } = _makeTimelineGridLine();

   assert.equal(DayPlannerTimelineMetrics.measurePointPillHeightPx(gridLine), TimelineLayoutConstants.TIMELINE_POINT_PILL_HEIGHT_PX);
   assert.equal(
      DayPlannerTimelineMetrics.measurePointPillStripTopOffsetPx(gridLine),
      TimelineLayoutConstants.TIMELINE_PILL_STRIP_TOP_OFFSET_PX
   );
});

test('Test_GetPointPillVerticalSpanFraction_TestUsesMeasuredPillAndSlotHeights_ExpectOk', () => {
   const { gridLine } = _makeTimelineGridLine();

   assert.equal(
      DayPlannerTimelineMetrics.getPointPillVerticalSpanFraction(gridLine),
      TimelineLayoutConstants.TIMELINE_POINT_PILL_HEIGHT_PX / TimelineLayoutConstants.TIMELINE_SLOT_HEIGHT_PX
   );
});

test('Test_GetPointPillStripPlacementBand_TestMatchesComputedPlacementFractions_ExpectOk', () => {
   const { gridLine } = _makeTimelineGridLine();

   assert.deepEqual(
      DayPlannerTimelineMetrics.getPointPillStripPlacementBand(gridLine, 0),
      DayPlannerTimelinePlacer.computePointPillStripPlacementBand({
         slotHeight: TimelineLayoutConstants.TIMELINE_SLOT_HEIGHT_PX,
         pillHeight: TimelineLayoutConstants.TIMELINE_POINT_PILL_HEIGHT_PX,
         stripTopOffset: TimelineLayoutConstants.TIMELINE_PILL_STRIP_TOP_OFFSET_PX,
         offsetFraction: 0,
      })
   );
});

test('Test_GetPointPillVerticalSpanFraction_TestFallsBackToAnExistingOpenPillHeight_ExpectOk', () => {
   const { gridLine } = _makeTimelineGridLine();
   const pill = createDomNode('span', 'itinerary-day-open-pill');

   gridLine.appendChild(pill);

   assert.equal(
      DayPlannerTimelineMetrics.getPointPillVerticalSpanFraction(gridLine),
      TimelineLayoutConstants.TIMELINE_POINT_PILL_HEIGHT_PX / TimelineLayoutConstants.TIMELINE_SLOT_HEIGHT_PX
   );
});
