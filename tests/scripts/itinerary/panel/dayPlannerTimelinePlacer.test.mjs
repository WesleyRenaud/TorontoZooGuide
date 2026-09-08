import assert from 'node:assert/strict';
import test from 'node:test';

import { DayPlannerTimelinePlacer } from '../../../../scripts/itinerary/panel/dayPlannerTimelinePlacer.js';
import { createDomNode } from '../../helpers/domNodeMock.mjs';
import { installDomTestHooks } from '../../helpers/domTestSetup.mjs';

installDomTestHooks();

test('Test_ReadCssLengthPx_TestValidAndInvalid_ExpectParsedOrNull', () => {
   const style = {
      getPropertyValue(property) {
         if (property === '--ok') return ' 42px ';
         if (property === '--zero') return '0';
         if (property === '--bad') return 'auto';
         return '';
      },
   };

   assert.equal(DayPlannerTimelinePlacer.readCssLengthPx(style, '--ok'), 42);
   assert.equal(DayPlannerTimelinePlacer.readCssLengthPx(style, '--zero'), null);
   assert.equal(DayPlannerTimelinePlacer.readCssLengthPx(style, '--bad'), null);
   assert.equal(DayPlannerTimelinePlacer.readCssLengthPx(style, '--missing'), null);
   assert.equal(DayPlannerTimelinePlacer.readCssLengthPx(null, '--ok'), null);
});

test('Test_ResolveTimelineElement_TestClosestAndWalk_ExpectTimeline', () => {
   const timeline = createDomNode('div', 'itinerary-day-timeline');
   const gridLine = createDomNode('div', 'itinerary-day-grid-line');
   timeline.appendChild(gridLine);

   assert.equal(DayPlannerTimelinePlacer.resolveTimelineElement(gridLine), timeline);
   assert.equal(DayPlannerTimelinePlacer.resolveTimelineElement(null), null);

   const nestedTimeline = createDomNode('div', 'itinerary-day-timeline');
   const row = createDomNode('div', 'row');
   const child = {
      parentElement: row,
      parent: row,
   };
   row.parentElement = nestedTimeline;
   row.parent = nestedTimeline;
   nestedTimeline.parentElement = null;
   nestedTimeline.classList = { contains: (name) => name === 'itinerary-day-timeline' };
   row.classList = { contains: () => false };

   assert.equal(DayPlannerTimelinePlacer.resolveTimelineElement(child), nestedTimeline);

   const orphan = {
      parentElement: { classList: { contains: () => false }, parentElement: null, parent: null },
      parent: null,
   };
   assert.equal(DayPlannerTimelinePlacer.resolveTimelineElement(orphan), null);
});

test('Test_ParseStripTopOffsetFromProbeTop_TestValues_ExpectOffsetOrNull', () => {
   assert.equal(DayPlannerTimelinePlacer.parseStripTopOffsetFromProbeTop(-12), 12);
   assert.equal(DayPlannerTimelinePlacer.parseStripTopOffsetFromProbeTop(0), null);
   assert.equal(DayPlannerTimelinePlacer.parseStripTopOffsetFromProbeTop(Number.NaN), null);
});

test('Test_ComputePointPillVerticalSpanFraction_TestInputs_ExpectFractionOrNull', () => {
   assert.equal(DayPlannerTimelinePlacer.computePointPillVerticalSpanFraction(20, 5), 0.25);
   assert.equal(DayPlannerTimelinePlacer.computePointPillVerticalSpanFraction(0, 5), null);
});

test('Test_ComputePointPillStripPlacementBand_TestMeasuredAndFallback_ExpectBand', () => {
   assert.deepEqual(
      DayPlannerTimelinePlacer.computePointPillStripPlacementBand({
         slotHeight: 100,
         pillHeight: 20,
         stripTopOffset: 10,
         offsetFraction: 0.5,
      }),
      {
         offsetFraction: 0.4,
         durationFraction: 0.2,
      }
   );

   assert.deepEqual(
      DayPlannerTimelinePlacer.computePointPillStripPlacementBand({
         slotHeight: null,
         pillHeight: 20,
         stripTopOffset: 10,
         offsetFraction: 0.25,
      }),
      {
         offsetFraction: 0.25,
         durationFraction: 0,
      }
   );
});
