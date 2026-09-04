import assert from 'node:assert/strict';
import { test } from 'node:test';

import { DayPlannerTimelinePillPlacement } from '../../../../../scripts/itinerary/panel/components/dayPlannerTimelinePillPlacement.js';
import { createDomNode } from '../../../helpers/domNodeMock.mjs';
import { installDomTestHooks } from '../../../helpers/domTestSetup.mjs';

function makeTimelineGridLine() {
   const timeline = createDomNode('div', 'itinerary-day-timeline');
   const gridLine = createDomNode('div', 'itinerary-day-grid-line');

   timeline.appendChild(gridLine);

   return { timeline, gridLine };
}

test('Test_ComputeTimelineHorizontalOffsetIndex_TestShiftsLaterOverlappingPlacements_ExpectOk', () => {
   assert.equal(DayPlannerTimelinePillPlacement.computeTimelineHorizontalOffsetIndex([], 0.5, 0.5), 0);
   assert.equal(DayPlannerTimelinePillPlacement.computeTimelineHorizontalOffsetIndex([
      {
         offsetFraction: 0.25,
         durationFraction: 0.5,
         horizontalOffsetIndex: 0,
      },
   ], 0.5, 0.5), 1);
   assert.equal(DayPlannerTimelinePillPlacement.computeTimelineHorizontalOffsetIndex([
      {
         offsetFraction: 0.25,
         durationFraction: 0.5,
         horizontalOffsetIndex: 0,
      },
      {
         offsetFraction: 0.5,
         durationFraction: 0.5,
         horizontalOffsetIndex: 1,
      },
   ], 0.5, 0.5), 2);
});

test('Test_ComputeStripHorizontalOffsetIndex_TestMapsStripOffsetsIntoPlacementIndexes_ExpectOk', () => {
   assert.equal(
      DayPlannerTimelinePillPlacement.computeStripHorizontalOffsetIndex(
         [
            { offsetFraction: 0, horizontalOffsetIndex: 0 },
            { offsetFraction: 0.25, horizontalOffsetIndex: 1 },
         ],
         0.5,
         0.5
      ),
      2
   );
});

test.describe('timeline pill strip placement', () => {
   installDomTestHooks();

   test('Test_GetOrCreatePointPillStrip_TestReusesStripsAtTheSameOffset_ExpectOk', () => {
      const { gridLine } = makeTimelineGridLine();
      const firstStrip = DayPlannerTimelinePillPlacement.getOrCreatePointPillStrip(gridLine, 0.25);
      const secondStrip = DayPlannerTimelinePillPlacement.getOrCreatePointPillStrip(gridLine, 0.25);

      assert.equal(firstStrip, secondStrip);
      assert.equal(gridLine.querySelectorAll('.itinerary-day-pill-strip').length, 1);
      assert.equal(firstStrip.getAttribute('data-offset-fraction'), '0.25');
   });

   test('Test_CreateScheduledPillStrip_TestMarksScheduledStripsSeparatelyFromPointStrips_ExpectOk', () => {
      const { gridLine } = makeTimelineGridLine();

      DayPlannerTimelinePillPlacement.getOrCreatePointPillStrip(gridLine, 0);
      const scheduledStrip = DayPlannerTimelinePillPlacement.createScheduledPillStrip(gridLine, 0, 30);

      assert.equal(scheduledStrip.getAttribute('data-scheduled-column'), 'true');
      assert.equal(gridLine.querySelectorAll('.itinerary-day-pill-strip').length, 2);
   });
});
