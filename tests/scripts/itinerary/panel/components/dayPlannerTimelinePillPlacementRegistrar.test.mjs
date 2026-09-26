import assert from 'node:assert/strict';
import test from 'node:test';

import { DayPlannerTimelineMetrics } from '../../../../../scripts/itinerary/panel/dayPlannerTimelineMetrics.js';
import { DayPlannerTimelinePillPlacementRegistrar } from '../../../../../scripts/itinerary/panel/components/dayPlannerTimelinePillPlacementRegistrar.js';
import { Position } from '../../../../../scripts/shared/enums/position.js';
import { TimelineLayoutConstants } from '../../../../../scripts/shared/timelineLayoutConstants.js';
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
   const horizontalOffsetIndex = Position.THIRD;

   DayPlannerTimelinePillPlacementRegistrar.applyHorizontalOffsetIndex(
      element,
      horizontalOffsetIndex
   );

   assert.equal(
      element.getAttribute('data-horizontal-offset-index'),
      String(horizontalOffsetIndex)
   );
   assert.equal(
      element.style['--itinerary-pill-horizontal-offset-index'],
      String(horizontalOffsetIndex)
   );
});


test('Test_MarkScheduledPillStrip_TestAttribute_ExpectTrue', () => {
   const pillStrip = createDomNode('div');

   DayPlannerTimelinePillPlacementRegistrar.markScheduledPillStrip(pillStrip);

   assert.equal(DayPlannerTimelinePillPlacementRegistrar.isScheduledPillStrip(pillStrip), true);
});


test('Test_IsScheduledPillStrip_TestUnmarked_ExpectFalse', () => {
   const pillStrip = createDomNode('div');

   const isScheduled = DayPlannerTimelinePillPlacementRegistrar.isScheduledPillStrip(pillStrip);

   assert.equal(isScheduled, false);
});


test('Test_RegisterTimelinePlacement_TestPush_ExpectStored', () => {
   const gridLine = {};
   const placement = {
      offsetFraction: 0.25,
      durationFraction: 0.5,
      horizontalOffsetIndex: Position.SECOND,
      anchorOffsetFraction: 0.1,
   };

   DayPlannerTimelinePillPlacementRegistrar.registerTimelinePlacement(gridLine, placement);

   assert.deepEqual(
      DayPlannerTimelinePillPlacementRegistrar.getTimelinePlacements(gridLine),
      [placement]
   );
});


test('Test_FindPointPillStrip_TestMatchesOffset_ExpectChild', () => {
   const offsetFraction = 0.25;
   const gridLine = createDomNode('div');
   const scheduled = createDomNode('div', 'itinerary-day-pill-strip');
   DayPlannerTimelinePillPlacementRegistrar.markScheduledPillStrip(scheduled);
   const other = createDomNode('div', 'itinerary-day-pill-strip');
   other.setAttribute('data-offset-fraction', '0.5');
   const match = createDomNode('div', 'itinerary-day-pill-strip');
   match.setAttribute('data-offset-fraction', String(offsetFraction));
   const ignored = createDomNode('div', 'other');
   gridLine.appendChild(scheduled);
   gridLine.appendChild(ignored);
   gridLine.appendChild(other);
   gridLine.appendChild(match);

   const found = DayPlannerTimelinePillPlacementRegistrar.findPointPillStrip(
      gridLine,
      offsetFraction
   );

   assert.equal(found, match);
});


test('Test_FindPointPillStrip_TestMissingOffset_ExpectNull', () => {
   const gridLine = createDomNode('div');
   const other = createDomNode('div', 'itinerary-day-pill-strip');
   other.setAttribute('data-offset-fraction', '0.5');
   gridLine.appendChild(other);

   const found = DayPlannerTimelinePillPlacementRegistrar.findPointPillStrip(gridLine, 0.75);

   assert.equal(found, null);
});


test('Test_ResolveStripPlacementBand_TestDuration_ExpectFraction', () => {
   const original = DayPlannerTimelineMetrics.getPointPillStripPlacementBand;
   const offsetFraction = 0.2;
   const durationMinutes = TimelineLayoutConstants.TIMELINE_SLOT_MINUTES * 2;
   const slotMinutes = TimelineLayoutConstants.TIMELINE_SLOT_MINUTES;

   DayPlannerTimelineMetrics.getPointPillStripPlacementBand = () => ({
      offsetFraction,
      durationFraction: 0,
   });

   try {
      const band = DayPlannerTimelinePillPlacementRegistrar.resolveStripPlacementBand(
         {},
         offsetFraction,
         durationMinutes,
         slotMinutes
      );

      assert.deepEqual(band, {
         offsetFraction,
         durationFraction: durationMinutes / slotMinutes,
      });
   } finally {
      DayPlannerTimelineMetrics.getPointPillStripPlacementBand = original;
   }
});


test('Test_ResolveStripPlacementBand_TestZeroSlot_ExpectDurationOverDefault', () => {
   const original = DayPlannerTimelineMetrics.getPointPillStripPlacementBand;
   const offsetFraction = 0.2;
   const durationMinutes = TimelineLayoutConstants.TIMELINE_SLOT_MINUTES * 2;
   const slotMinutes = 0;

   DayPlannerTimelineMetrics.getPointPillStripPlacementBand = () => ({
      offsetFraction,
      durationFraction: 0,
   });

   try {
      const band = DayPlannerTimelinePillPlacementRegistrar.resolveStripPlacementBand(
         {},
         offsetFraction,
         durationMinutes,
         slotMinutes
      );

      assert.deepEqual(band, {
         offsetFraction,
         durationFraction: durationMinutes / TimelineLayoutConstants.TIMELINE_SLOT_MINUTES,
      });
   } finally {
      DayPlannerTimelineMetrics.getPointPillStripPlacementBand = original;
   }
});


test('Test_ResolveStripPlacementBand_TestPoint_ExpectZeroDuration', () => {
   const original = DayPlannerTimelineMetrics.getPointPillStripPlacementBand;
   const offsetFraction = 0.2;
   const pointBand = {
      offsetFraction,
      durationFraction: 0,
   };

   DayPlannerTimelineMetrics.getPointPillStripPlacementBand = () => pointBand;

   try {
      const band = DayPlannerTimelinePillPlacementRegistrar.resolveStripPlacementBand(
         {},
         offsetFraction
      );

      assert.deepEqual(band, pointBand);
   } finally {
      DayPlannerTimelineMetrics.getPointPillStripPlacementBand = original;
   }
});
