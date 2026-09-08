import assert from 'node:assert/strict';
import test from 'node:test';

import { DayPlannerTimelineMetrics } from '../../../../../scripts/itinerary/panel/dayPlannerTimelineMetrics.js';
import { DayPlannerTimelinePillPlacementRegistrar } from '../../../../../scripts/itinerary/panel/components/dayPlannerTimelinePillPlacementRegistrar.js';
import { createDomNode } from '../../../helpers/domNodeMock.mjs';
import { installDomTestHooks } from '../../../helpers/domTestSetup.mjs';

installDomTestHooks();

test('Test_GetTimelinePlacements_TestNewGridLine_ExpectSharedArray', () => {
   const gridLine = {};
   const first = DayPlannerTimelinePillPlacementRegistrar.getTimelinePlacements(gridLine);
   const second = DayPlannerTimelinePillPlacementRegistrar.getTimelinePlacements(gridLine);

   assert.equal(first, second);
   assert.deepEqual(first, []);
});

test('Test_ApplyHorizontalOffsetIndex_TestElement_ExpectAttributeAndCssVar', () => {
   const element = createDomNode('div');
   DayPlannerTimelinePillPlacementRegistrar.applyHorizontalOffsetIndex(element, 2);

   assert.equal(element.getAttribute('data-horizontal-offset-index'), '2');
   assert.equal(element.style['--itinerary-pill-horizontal-offset-index'], '2');
});

test('Test_MarkAndDetectScheduledPillStrip_TestAttribute_ExpectTrue', () => {
   const pillStrip = createDomNode('div');
   DayPlannerTimelinePillPlacementRegistrar.markScheduledPillStrip(pillStrip);

   assert.equal(DayPlannerTimelinePillPlacementRegistrar.isScheduledPillStrip(pillStrip), true);
   assert.equal(
      DayPlannerTimelinePillPlacementRegistrar.isScheduledPillStrip(createDomNode('div')),
      false
   );
});

test('Test_RegisterTimelinePlacement_TestPush_ExpectStored', () => {
   const gridLine = {};
   DayPlannerTimelinePillPlacementRegistrar.registerTimelinePlacement(gridLine, {
      offsetFraction: 0.25,
      durationFraction: 0.5,
      horizontalOffsetIndex: 1,
      anchorOffsetFraction: 0.1,
   });

   assert.deepEqual(DayPlannerTimelinePillPlacementRegistrar.getTimelinePlacements(gridLine), [
      {
         offsetFraction: 0.25,
         durationFraction: 0.5,
         horizontalOffsetIndex: 1,
         anchorOffsetFraction: 0.1,
      },
   ]);
});

test('Test_FindPointPillStrip_TestMatchesOffset_ExpectChild', () => {
   const gridLine = createDomNode('div');
   const scheduled = createDomNode('div', 'itinerary-day-pill-strip');
   DayPlannerTimelinePillPlacementRegistrar.markScheduledPillStrip(scheduled);
   const other = createDomNode('div', 'itinerary-day-pill-strip');
   other.setAttribute('data-offset-fraction', '0.5');
   const match = createDomNode('div', 'itinerary-day-pill-strip');
   match.setAttribute('data-offset-fraction', '0.25');
   const ignored = createDomNode('div', 'other');

   gridLine.appendChild(scheduled);
   gridLine.appendChild(ignored);
   gridLine.appendChild(other);
   gridLine.appendChild(match);

   assert.equal(
      DayPlannerTimelinePillPlacementRegistrar.findPointPillStrip(gridLine, 0.25),
      match
   );
   assert.equal(DayPlannerTimelinePillPlacementRegistrar.findPointPillStrip(gridLine, 0.75), null);
});

test('Test_ResolveStripPlacementBand_TestDurationAndPoint_ExpectBands', () => {
   const original = DayPlannerTimelineMetrics.getPointPillStripPlacementBand;
   DayPlannerTimelineMetrics.getPointPillStripPlacementBand = () => ({
      offsetFraction: 0.2,
      durationFraction: 0,
   });

   try {
      assert.deepEqual(
         DayPlannerTimelinePillPlacementRegistrar.resolveStripPlacementBand({}, 0.2, 60, 30),
         { offsetFraction: 0.2, durationFraction: 2 }
      );
      assert.deepEqual(
         DayPlannerTimelinePillPlacementRegistrar.resolveStripPlacementBand({}, 0.2, 60, 0),
         { offsetFraction: 0.2, durationFraction: 2 }
      );
      assert.deepEqual(
         DayPlannerTimelinePillPlacementRegistrar.resolveStripPlacementBand({}, 0.2),
         { offsetFraction: 0.2, durationFraction: 0 }
      );
   } finally {
      DayPlannerTimelineMetrics.getPointPillStripPlacementBand = original;
   }
});
