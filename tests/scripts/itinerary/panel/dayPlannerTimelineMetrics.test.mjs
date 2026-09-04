import assert from 'node:assert/strict';
import { test } from 'node:test';

import {
   TIMELINE_PILL_STRIP_TOP_OFFSET_PX,
   TIMELINE_POINT_PILL_HEIGHT_PX,
   TIMELINE_SLOT_HEIGHT_PX,
} from '../../../../scripts/shared/constants.js';
import { DayPlannerTimelinePlacement } from '../../../../scripts/itinerary/panel/dayPlannerTimelinePlacement.js';
import { DayPlannerTimelineMetrics } from '../../../../scripts/itinerary/panel/dayPlannerTimelineMetrics.js';
import { createDomNode } from '../../helpers/domNodeMock.mjs';
import { installDomTestHooks } from '../../helpers/domTestSetup.mjs';

function makeTimelineGridLine() {
   const timeline = createDomNode('div', 'itinerary-day-timeline');
   const gridLine = createDomNode('div', 'itinerary-day-grid-line');

   timeline.appendChild(gridLine);

   return { timeline, gridLine };
}

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

   assert.equal(DayPlannerTimelinePlacement.readCssLengthPx(style, '--valid'), 730);
   assert.equal(DayPlannerTimelinePlacement.readCssLengthPx(style, '--zero'), null);
   assert.equal(DayPlannerTimelinePlacement.readCssLengthPx(style, '--invalid'), null);
   assert.equal(DayPlannerTimelinePlacement.readCssLengthPx(style, '--missing'), null);
   assert.equal(DayPlannerTimelinePlacement.readCssLengthPx(null, '--valid'), null);
});

test('Test_ResolveTimelineElement_TestWalksParentNodesWhenClosestIsUnavailable_ExpectOk', () => {
   const timeline = createDomNode('div', 'itinerary-day-timeline');
   const row = createDomNode('div', 'itinerary-day-row');
   const gridLine = createDomNode('div', 'itinerary-day-grid-line');

   timeline.appendChild(row);
   row.appendChild(gridLine);

   assert.equal(DayPlannerTimelinePlacement.resolveTimelineElement(gridLine), timeline);
   assert.equal(DayPlannerTimelinePlacement.resolveTimelineElement(null), null);
});

test('Test_ParseStripTopOffsetFromProbeTop_TestConvertsNegativeProbeTopsToOffsets_ExpectOk', () => {
   assert.equal(DayPlannerTimelinePlacement.parseStripTopOffsetFromProbeTop(-80), 80);
   assert.equal(DayPlannerTimelinePlacement.parseStripTopOffsetFromProbeTop(0), null);
   assert.equal(DayPlannerTimelinePlacement.parseStripTopOffsetFromProbeTop(Number.NaN), null);
});

test('Test_ComputePointPillStripPlacementBand_TestConvertsSlotOffsetsIntoFractions_ExpectOk', () => {
   const atAnchor = DayPlannerTimelinePlacement.computePointPillStripPlacementBand({
      slotHeight: TIMELINE_SLOT_HEIGHT_PX,
      pillHeight: TIMELINE_POINT_PILL_HEIGHT_PX,
      stripTopOffset: TIMELINE_PILL_STRIP_TOP_OFFSET_PX,
      offsetFraction: 0,
   });

   assert.equal(
      atAnchor.offsetFraction,
      -TIMELINE_PILL_STRIP_TOP_OFFSET_PX / TIMELINE_SLOT_HEIGHT_PX
   );
   assert.equal(
      atAnchor.durationFraction,
      TIMELINE_POINT_PILL_HEIGHT_PX / TIMELINE_SLOT_HEIGHT_PX
   );

   const midway = DayPlannerTimelinePlacement.computePointPillStripPlacementBand({
      slotHeight: TIMELINE_SLOT_HEIGHT_PX,
      pillHeight: TIMELINE_POINT_PILL_HEIGHT_PX,
      stripTopOffset: TIMELINE_PILL_STRIP_TOP_OFFSET_PX,
      offsetFraction: 0.5,
   });

   assert.equal(
      midway.offsetFraction,
      (0.5 * TIMELINE_SLOT_HEIGHT_PX - TIMELINE_PILL_STRIP_TOP_OFFSET_PX)
         / TIMELINE_SLOT_HEIGHT_PX
   );
});

test('Test_ComputePointPillStripPlacementBand_TestFallsBackWhenMeasurementsAreMissing_ExpectOk', () => {
   assert.deepEqual(
      DayPlannerTimelinePlacement.computePointPillStripPlacementBand({
         slotHeight: null,
         pillHeight: TIMELINE_POINT_PILL_HEIGHT_PX,
         stripTopOffset: TIMELINE_PILL_STRIP_TOP_OFFSET_PX,
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
      DayPlannerTimelinePlacement.computePointPillVerticalSpanFraction(
         TIMELINE_SLOT_HEIGHT_PX,
         TIMELINE_POINT_PILL_HEIGHT_PX
      ),
      TIMELINE_POINT_PILL_HEIGHT_PX / TIMELINE_SLOT_HEIGHT_PX
   );
   assert.equal(DayPlannerTimelinePlacement.computePointPillVerticalSpanFraction(0, 10), null);
});

test.describe('day planner timeline measurements', () => {
   installDomTestHooks();

   test('Test_GetTimelineSlotHeightPx_TestReadsTheTimelineSlotHeightFromCSSVariables_ExpectOk', () => {
      const { gridLine } = makeTimelineGridLine();

      assert.equal(DayPlannerTimelineMetrics.getTimelineSlotHeightPx(gridLine), TIMELINE_SLOT_HEIGHT_PX);
   });

   test('Test_MeasurePointPillHeightPx_TestAndStripOffsetUseTimelineCSSVariables_ExpectOk', () => {
      const { gridLine } = makeTimelineGridLine();

      assert.equal(DayPlannerTimelineMetrics.measurePointPillHeightPx(gridLine), TIMELINE_POINT_PILL_HEIGHT_PX);
      assert.equal(
         DayPlannerTimelineMetrics.measurePointPillStripTopOffsetPx(gridLine),
         TIMELINE_PILL_STRIP_TOP_OFFSET_PX
      );
   });

   test('Test_GetPointPillVerticalSpanFraction_TestUsesMeasuredPillAndSlotHeights_ExpectOk', () => {
      const { gridLine } = makeTimelineGridLine();

      assert.equal(
         DayPlannerTimelineMetrics.getPointPillVerticalSpanFraction(gridLine),
         TIMELINE_POINT_PILL_HEIGHT_PX / TIMELINE_SLOT_HEIGHT_PX
      );
   });

   test('Test_GetPointPillStripPlacementBand_TestMatchesComputedPlacementFractions_ExpectOk', () => {
      const { gridLine } = makeTimelineGridLine();

      assert.deepEqual(
         DayPlannerTimelineMetrics.getPointPillStripPlacementBand(gridLine, 0),
         DayPlannerTimelinePlacement.computePointPillStripPlacementBand({
            slotHeight: TIMELINE_SLOT_HEIGHT_PX,
            pillHeight: TIMELINE_POINT_PILL_HEIGHT_PX,
            stripTopOffset: TIMELINE_PILL_STRIP_TOP_OFFSET_PX,
            offsetFraction: 0,
         })
      );
   });

   test('Test_GetPointPillVerticalSpanFraction_TestFallsBackToAnExistingOpenPillHeight_ExpectOk', () => {
      const { gridLine } = makeTimelineGridLine();
      const pill = createDomNode('span', 'itinerary-day-open-pill');

      gridLine.appendChild(pill);

      assert.equal(
         DayPlannerTimelineMetrics.getPointPillVerticalSpanFraction(gridLine),
         TIMELINE_POINT_PILL_HEIGHT_PX / TIMELINE_SLOT_HEIGHT_PX
      );
   });
});
