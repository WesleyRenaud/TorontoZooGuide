import assert from 'node:assert/strict';
import { afterEach, beforeEach, test } from 'node:test';

import {
   computeStripHorizontalOffsetIndex,
   computeTimelineHorizontalOffsetIndex,
   createScheduledPillStrip,
   getOrCreatePointPillStrip,
} from '../../scripts/itinerary/panel/components/dayPlannerTimelinePillPlacement.js';
import { createDomNode } from './helpers/domNodeMock.mjs';
import { installDocument, installTestWindow, teardownDocument } from './helpers/domMock.mjs';

function makeTimelineGridLine() {
   const timeline = createDomNode('div', 'itinerary-day-timeline');
   const gridLine = createDomNode('div', 'itinerary-day-grid-line');

   timeline.appendChild(gridLine);

   return { timeline, gridLine };
}

test('computeTimelineHorizontalOffsetIndex shifts later overlapping placements', () => {
   assert.equal(computeTimelineHorizontalOffsetIndex([], 0.5, 0.5), 0);
   assert.equal(computeTimelineHorizontalOffsetIndex([
      {
         offsetFraction: 0.25,
         durationFraction: 0.5,
         horizontalOffsetIndex: 0,
      },
   ], 0.5, 0.5), 1);
   assert.equal(computeTimelineHorizontalOffsetIndex([
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

test('computeStripHorizontalOffsetIndex maps strip offsets into placement indexes', () => {
   assert.equal(
      computeStripHorizontalOffsetIndex(
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
   beforeEach(() => {
      installTestWindow();
      installDocument();
   });

   afterEach(() => {
      teardownDocument();
      delete globalThis.window;
   });

   test('getOrCreatePointPillStrip reuses strips at the same offset', () => {
      const { gridLine } = makeTimelineGridLine();
      const firstStrip = getOrCreatePointPillStrip(gridLine, 0.25);
      const secondStrip = getOrCreatePointPillStrip(gridLine, 0.25);

      assert.equal(firstStrip, secondStrip);
      assert.equal(gridLine.querySelectorAll('.itinerary-day-pill-strip').length, 1);
      assert.equal(firstStrip.getAttribute('data-offset-fraction'), '0.25');
   });

   test('createScheduledPillStrip marks scheduled strips separately from point strips', () => {
      const { gridLine } = makeTimelineGridLine();

      getOrCreatePointPillStrip(gridLine, 0);
      const scheduledStrip = createScheduledPillStrip(gridLine, 0, 30);

      assert.equal(scheduledStrip.getAttribute('data-scheduled-column'), 'true');
      assert.equal(gridLine.querySelectorAll('.itinerary-day-pill-strip').length, 2);
   });
});
