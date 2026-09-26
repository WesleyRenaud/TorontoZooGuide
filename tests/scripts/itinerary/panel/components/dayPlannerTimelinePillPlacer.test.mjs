import assert from 'node:assert/strict';
import { test } from 'node:test';

import { DayPlannerTimelinePillPlacer } from '../../../../../scripts/itinerary/panel/components/dayPlannerTimelinePillPlacer.js';
import { Position } from '../../../../../scripts/shared/enums/position.js';
import { TimelineLayoutConstants } from '../../../../../scripts/shared/timelineLayoutConstants.js';
import { createDomNode } from '../../../helpers/domNodeMock.mjs';
import { installDomTestHooks } from '../../../helpers/domTestSetup.mjs';

function _makeTimelineGridLine() {
   const timeline = createDomNode('div', 'itinerary-day-timeline');
   const gridLine = createDomNode('div', 'itinerary-day-grid-line');

   timeline.appendChild(gridLine);

   return { timeline, gridLine };
}

installDomTestHooks();


test('Test_ComputeTimelineHorizontalOffsetIndex_TestEmptyPlacements_ExpectFirst', () => {
   const offsetFraction = 0.5;
   const durationFraction = 0.5;

   const index = DayPlannerTimelinePillPlacer.computeTimelineHorizontalOffsetIndex(
      [],
      offsetFraction,
      durationFraction
   );

   assert.equal(index, Position.FIRST);
});


test('Test_ComputeTimelineHorizontalOffsetIndex_TestOneOverlap_ExpectSecond', () => {
   const offsetFraction = 0.5;
   const durationFraction = 0.5;
   const placements = [
      {
         offsetFraction: 0.25,
         durationFraction,
         horizontalOffsetIndex: Position.FIRST,
      },
   ];

   const index = DayPlannerTimelinePillPlacer.computeTimelineHorizontalOffsetIndex(
      placements,
      offsetFraction,
      durationFraction
   );

   assert.equal(index, Position.SECOND);
});


test('Test_ComputeTimelineHorizontalOffsetIndex_TestTwoOverlaps_ExpectThird', () => {
   const offsetFraction = 0.5;
   const durationFraction = 0.5;
   const placements = [
      {
         offsetFraction: 0.25,
         durationFraction,
         horizontalOffsetIndex: Position.FIRST,
      },
      {
         offsetFraction,
         durationFraction,
         horizontalOffsetIndex: Position.SECOND,
      },
   ];

   const index = DayPlannerTimelinePillPlacer.computeTimelineHorizontalOffsetIndex(
      placements,
      offsetFraction,
      durationFraction
   );

   assert.equal(index, Position.THIRD);
});


test('Test_ComputeStripHorizontalOffsetIndex_TestMappedOffsets_ExpectThird', () => {
   const offsetFraction = 0.5;
   const durationFraction = 0.5;
   const placements = [
      { offsetFraction: 0, horizontalOffsetIndex: Position.FIRST },
      { offsetFraction: 0.25, horizontalOffsetIndex: Position.SECOND },
   ];

   const index = DayPlannerTimelinePillPlacer.computeStripHorizontalOffsetIndex(
      placements,
      offsetFraction,
      durationFraction
   );

   assert.equal(index, Position.THIRD);
});


test('Test_GetOrCreatePointPillStrip_TestSameOffset_ExpectReused', () => {
   const { gridLine } = _makeTimelineGridLine();
   const offsetFraction = 0.25;

   const firstStrip = DayPlannerTimelinePillPlacer.getOrCreatePointPillStrip(
      gridLine,
      offsetFraction
   );
   const secondStrip = DayPlannerTimelinePillPlacer.getOrCreatePointPillStrip(
      gridLine,
      offsetFraction
   );

   assert.equal(firstStrip, secondStrip);
   assert.equal(gridLine.querySelectorAll('.itinerary-day-pill-strip').length, 1);
   assert.equal(firstStrip.getAttribute('data-offset-fraction'), String(offsetFraction));
});


test('Test_CreateScheduledPillStrip_TestPointAndScheduled_ExpectSeparateStrips', () => {
   const { gridLine } = _makeTimelineGridLine();
   const offsetFraction = 0;
   const durationMinutes = TimelineLayoutConstants.TIMELINE_SLOT_MINUTES;

   DayPlannerTimelinePillPlacer.getOrCreatePointPillStrip(gridLine, offsetFraction);
   const scheduledStrip = DayPlannerTimelinePillPlacer.createScheduledPillStrip(
      gridLine,
      offsetFraction,
      durationMinutes
   );

   assert.equal(scheduledStrip.getAttribute('data-scheduled-column'), 'true');
   assert.equal(gridLine.querySelectorAll('.itinerary-day-pill-strip').length, 2);
});


test('Test_CreateScheduledPillStrip_TestOffset_ExpectFractionAttribute', () => {
   const { gridLine } = _makeTimelineGridLine();
   const offsetFraction = 0.4;
   const durationMinutes = 20;

   const offsetStrip = DayPlannerTimelinePillPlacer.createScheduledPillStrip(
      gridLine,
      offsetFraction,
      durationMinutes
   );

   assert.equal(offsetStrip.getAttribute('data-offset-fraction'), String(offsetFraction));
});


test('Test_ComputeSpanHorizontalOffsetIndex_TestDeprecatedAlias_ExpectDelegates', () => {
   const offsetFraction = 0.5;
   const durationFraction = 0.5;

   const spanIndex = DayPlannerTimelinePillPlacer.computeSpanHorizontalOffsetIndex(
      [],
      offsetFraction,
      durationFraction
   );
   const timelineIndex = DayPlannerTimelinePillPlacer.computeTimelineHorizontalOffsetIndex(
      [],
      offsetFraction,
      durationFraction
   );

   assert.equal(spanIndex, timelineIndex);
});
