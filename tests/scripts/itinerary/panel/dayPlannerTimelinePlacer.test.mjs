import assert from 'node:assert/strict';
import test from 'node:test';

import { DayPlannerTimelinePlacer } from '../../../../scripts/itinerary/panel/dayPlannerTimelinePlacer.js';
import { createDomNode } from '../../helpers/domNodeMock.mjs';
import { installDomTestHooks } from '../../helpers/domTestSetup.mjs';

installDomTestHooks();


test('Test_ReadCssLengthPx_TestPixelValue_ExpectParsed', () => {
   const rawValue = ' 42px ';
   const property = '--ok';
   const style = {
      getPropertyValue(name) {
         return name === property ? rawValue : '';
      },
   };

   const length = DayPlannerTimelinePlacer.readCssLengthPx(style, property);

   assert.equal(length, Number.parseFloat(rawValue));
});


test('Test_ReadCssLengthPx_TestZero_ExpectNull', () => {
   const property = '--zero';
   const style = {
      getPropertyValue(name) {
         return name === property ? '0' : '';
      },
   };

   const length = DayPlannerTimelinePlacer.readCssLengthPx(style, property);

   assert.equal(length, null);
});


test('Test_ReadCssLengthPx_TestNonNumeric_ExpectNull', () => {
   const property = '--bad';
   const style = {
      getPropertyValue(name) {
         return name === property ? 'auto' : '';
      },
   };

   const length = DayPlannerTimelinePlacer.readCssLengthPx(style, property);

   assert.equal(length, null);
});


test('Test_ReadCssLengthPx_TestMissing_ExpectNull', () => {
   const property = '--missing';
   const style = {
      getPropertyValue() {
         return '';
      },
   };

   const length = DayPlannerTimelinePlacer.readCssLengthPx(style, property);

   assert.equal(length, null);
});


test('Test_ReadCssLengthPx_TestNullStyle_ExpectNull', () => {
   const style = null;
   const property = '--ok';

   const length = DayPlannerTimelinePlacer.readCssLengthPx(style, property);

   assert.equal(length, null);
});


test('Test_ResolveTimelineElement_TestClosest_ExpectTimeline', () => {
   const timeline = createDomNode('div', 'itinerary-day-timeline');
   const gridLine = createDomNode('div', 'itinerary-day-grid-line');
   timeline.appendChild(gridLine);

   const resolved = DayPlannerTimelinePlacer.resolveTimelineElement(gridLine);

   assert.equal(resolved, timeline);
});


test('Test_ResolveTimelineElement_TestNull_ExpectNull', () => {
   const gridLine = null;

   const resolved = DayPlannerTimelinePlacer.resolveTimelineElement(gridLine);

   assert.equal(resolved, null);
});


test('Test_ResolveTimelineElement_TestWalkParents_ExpectTimeline', () => {
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

   const resolved = DayPlannerTimelinePlacer.resolveTimelineElement(child);

   assert.equal(resolved, nestedTimeline);
});


test('Test_ResolveTimelineElement_TestOrphan_ExpectNull', () => {
   const orphan = {
      parentElement: { classList: { contains: () => false }, parentElement: null, parent: null },
      parent: null,
   };

   const resolved = DayPlannerTimelinePlacer.resolveTimelineElement(orphan);

   assert.equal(resolved, null);
});


test('Test_ParseStripTopOffsetFromProbeTop_TestNegative_ExpectAbsolute', () => {
   const topPx = -12;

   const offset = DayPlannerTimelinePlacer.parseStripTopOffsetFromProbeTop(topPx);

   assert.equal(offset, Math.abs(topPx));
});


test('Test_ParseStripTopOffsetFromProbeTop_TestZero_ExpectNull', () => {
   const topPx = 0;

   const offset = DayPlannerTimelinePlacer.parseStripTopOffsetFromProbeTop(topPx);

   assert.equal(offset, null);
});


test('Test_ParseStripTopOffsetFromProbeTop_TestNaN_ExpectNull', () => {
   const topPx = Number.NaN;

   const offset = DayPlannerTimelinePlacer.parseStripTopOffsetFromProbeTop(topPx);

   assert.equal(offset, null);
});


test('Test_ComputePointPillVerticalSpanFraction_TestHeights_ExpectFraction', () => {
   const slotHeight = 20;
   const pillHeight = 5;

   const fraction = DayPlannerTimelinePlacer.computePointPillVerticalSpanFraction(slotHeight, pillHeight);

   assert.equal(fraction, pillHeight / slotHeight);
});


test('Test_ComputePointPillVerticalSpanFraction_TestZeroSlot_ExpectNull', () => {
   const slotHeight = 0;
   const pillHeight = 5;

   const fraction = DayPlannerTimelinePlacer.computePointPillVerticalSpanFraction(slotHeight, pillHeight);

   assert.equal(fraction, null);
});


test('Test_ComputePointPillStripPlacementBand_TestMeasured_ExpectBand', () => {
   const slotHeight = 100;
   const pillHeight = 20;
   const stripTopOffset = 10;
   const offsetFraction = 0.5;

   const band = DayPlannerTimelinePlacer.computePointPillStripPlacementBand({
      slotHeight,
      pillHeight,
      stripTopOffset,
      offsetFraction,
   });

   assert.deepEqual(band, {
      offsetFraction: ((offsetFraction * slotHeight) - stripTopOffset) / slotHeight,
      durationFraction: pillHeight / slotHeight,
   });
});


test('Test_ComputePointPillStripPlacementBand_TestMissingSlot_ExpectFallback', () => {
   const offsetFraction = 0.25;

   const band = DayPlannerTimelinePlacer.computePointPillStripPlacementBand({
      slotHeight: null,
      pillHeight: 20,
      stripTopOffset: 10,
      offsetFraction,
   });

   assert.deepEqual(band, {
      offsetFraction,
      durationFraction: 0,
   });
});
