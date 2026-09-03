import assert from 'node:assert/strict';
import { test } from 'node:test';

import {
   TIMELINE_PILL_STRIP_TOP_OFFSET_PX,
   TIMELINE_POINT_PILL_HEIGHT_PX,
   TIMELINE_SLOT_HEIGHT_PX,
} from '../../scripts/shared/constants.js';
import {
   computePointPillStripPlacementBand,
   computePointPillVerticalSpanFraction,
   parseStripTopOffsetFromProbeTop,
   readCssLengthPx,
   resolveTimelineElement,
} from '../../scripts/itinerary/panel/dayPlannerTimelinePlacement.js';
import {
   getPointPillStripPlacementBand,
   getPointPillVerticalSpanFraction,
   getTimelineSlotHeightPx,
   measurePointPillHeightPx,
   measurePointPillStripTopOffsetPx,
} from '../../scripts/itinerary/panel/dayPlannerTimelineMetrics.js';
import { createDomNode } from './helpers/domNodeMock.mjs';
import { installDomTestHooks } from './helpers/domTestSetup.mjs';

function makeTimelineGridLine() {
   const timeline = createDomNode('div', 'itinerary-day-timeline');
   const gridLine = createDomNode('div', 'itinerary-day-grid-line');

   timeline.appendChild(gridLine);

   return { timeline, gridLine };
}

test('readCssLengthPx parses positive CSS lengths and rejects invalid values', () => {
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

   assert.equal(readCssLengthPx(style, '--valid'), 730);
   assert.equal(readCssLengthPx(style, '--zero'), null);
   assert.equal(readCssLengthPx(style, '--invalid'), null);
   assert.equal(readCssLengthPx(style, '--missing'), null);
   assert.equal(readCssLengthPx(null, '--valid'), null);
});

test('resolveTimelineElement walks parent nodes when closest is unavailable', () => {
   const timeline = createDomNode('div', 'itinerary-day-timeline');
   const row = createDomNode('div', 'itinerary-day-row');
   const gridLine = createDomNode('div', 'itinerary-day-grid-line');

   timeline.appendChild(row);
   row.appendChild(gridLine);

   assert.equal(resolveTimelineElement(gridLine), timeline);
   assert.equal(resolveTimelineElement(null), null);
});

test('parseStripTopOffsetFromProbeTop converts negative probe tops to offsets', () => {
   assert.equal(parseStripTopOffsetFromProbeTop(-80), 80);
   assert.equal(parseStripTopOffsetFromProbeTop(0), null);
   assert.equal(parseStripTopOffsetFromProbeTop(Number.NaN), null);
});

test('computePointPillStripPlacementBand converts slot offsets into fractions', () => {
   const atAnchor = computePointPillStripPlacementBand({
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

   const midway = computePointPillStripPlacementBand({
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

test('computePointPillStripPlacementBand falls back when measurements are missing', () => {
   assert.deepEqual(
      computePointPillStripPlacementBand({
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

test('computePointPillVerticalSpanFraction returns pill height relative to slot height', () => {
   assert.equal(
      computePointPillVerticalSpanFraction(
         TIMELINE_SLOT_HEIGHT_PX,
         TIMELINE_POINT_PILL_HEIGHT_PX
      ),
      TIMELINE_POINT_PILL_HEIGHT_PX / TIMELINE_SLOT_HEIGHT_PX
   );
   assert.equal(computePointPillVerticalSpanFraction(0, 10), null);
});

test.describe('day planner timeline measurements', () => {
   installDomTestHooks();

   test('getTimelineSlotHeightPx reads the timeline slot height from CSS variables', () => {
      const { gridLine } = makeTimelineGridLine();

      assert.equal(getTimelineSlotHeightPx(gridLine), TIMELINE_SLOT_HEIGHT_PX);
   });

   test('measurePointPillHeightPx and strip offset use timeline CSS variables', () => {
      const { gridLine } = makeTimelineGridLine();

      assert.equal(measurePointPillHeightPx(gridLine), TIMELINE_POINT_PILL_HEIGHT_PX);
      assert.equal(
         measurePointPillStripTopOffsetPx(gridLine),
         TIMELINE_PILL_STRIP_TOP_OFFSET_PX
      );
   });

   test('getPointPillVerticalSpanFraction uses measured pill and slot heights', () => {
      const { gridLine } = makeTimelineGridLine();

      assert.equal(
         getPointPillVerticalSpanFraction(gridLine),
         TIMELINE_POINT_PILL_HEIGHT_PX / TIMELINE_SLOT_HEIGHT_PX
      );
   });

   test('getPointPillStripPlacementBand matches computed placement fractions', () => {
      const { gridLine } = makeTimelineGridLine();

      assert.deepEqual(
         getPointPillStripPlacementBand(gridLine, 0),
         computePointPillStripPlacementBand({
            slotHeight: TIMELINE_SLOT_HEIGHT_PX,
            pillHeight: TIMELINE_POINT_PILL_HEIGHT_PX,
            stripTopOffset: TIMELINE_PILL_STRIP_TOP_OFFSET_PX,
            offsetFraction: 0,
         })
      );
   });

   test('getPointPillVerticalSpanFraction falls back to an existing open pill height', () => {
      const { gridLine } = makeTimelineGridLine();
      const pill = createDomNode('span', 'itinerary-day-open-pill');

      gridLine.appendChild(pill);

      assert.equal(
         getPointPillVerticalSpanFraction(gridLine),
         TIMELINE_POINT_PILL_HEIGHT_PX / TIMELINE_SLOT_HEIGHT_PX
      );
   });
});
