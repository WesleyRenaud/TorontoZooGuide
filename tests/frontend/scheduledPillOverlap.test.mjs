import assert from 'node:assert/strict';
import { test } from 'node:test';

import { makeScheduledItem } from './helpers/scheduledPillTestSetup.mjs';
import {
   computeFirstFreeHorizontalOffsetIndex,
   doScheduledTimeRangesOverlap,
   formatScheduledPillGroupLabel,
   getScheduledItemEndMinutes,
   getScheduledItemTimeRange,
   getScheduledPillMinDisplayMinutes,
   getScheduledPillVisualBand,
   MAX_TIMELINE_PILL_COLUMNS,
   scheduledPillsOverlapInDefaultPosition,
} from '../../scripts/itinerary/panel/components/scheduledPillOverlap.js';

test('getScheduledItemEndMinutes uses parsed endMinutes from schedule times', () => {
   assert.equal(
      getScheduledItemEndMinutes({
         startMinutes: 600,
         maximumDuration: 8,
         endMinutes: 615,
      }),
      615
   );
   assert.ok(Number.isNaN(getScheduledItemEndMinutes({
      startMinutes: 600,
      maximumDuration: 8,
   })));
});

test('getScheduledItemTimeRange returns start and end minutes', () => {
   assert.deepEqual(
      getScheduledItemTimeRange({
         startMinutes: 570,
         endMinutes: 600,
      }),
      {
         startMinutes: 570,
         endMinutes: 600,
      }
   );
});

test('getScheduledPillVisualBand expands short visits to the minimum display span', () => {
   const band = getScheduledPillVisualBand(
      makeScheduledItem('Babirusa', 570, 2, 570)
   );

   assert.equal(band.endMinutes - band.startMinutes, getScheduledPillMinDisplayMinutes());
});

test('getScheduledPillVisualBand spans clustered summary items', () => {
   const band = getScheduledPillVisualBand({
      summaryItems: [
         makeScheduledItem('Babirusa', 570, 2, 570),
         makeScheduledItem('Cheetah', 575, 2, 570),
      ],
   });

   assert.ok(band.startMinutes < 570);
   assert.ok(band.endMinutes > 572);
});

test('doScheduledTimeRangesOverlap uses strict bounds for touching windows', () => {
   assert.equal(
      doScheduledTimeRangesOverlap(
         { startMinutes: 570, endMinutes: 600 },
         { startMinutes: 590, endMinutes: 620 }
      ),
      true
   );
   assert.equal(
      doScheduledTimeRangesOverlap(
         { startMinutes: 570, endMinutes: 600 },
         { startMinutes: 600, endMinutes: 630 }
      ),
      false
   );
});

test('scheduledPillsOverlapInDefaultPosition detects overlap within a slot', () => {
   assert.equal(
      scheduledPillsOverlapInDefaultPosition(
         makeScheduledItem('Babirusa', 570, 30),
         makeScheduledItem('Cheetah', 575, 30)
      ),
      true
   );
});

test('scheduledPillsOverlapInDefaultPosition ignores back-to-back slot boundaries', () => {
   assert.equal(
      scheduledPillsOverlapInDefaultPosition(
         makeScheduledItem('Babirusa', 570, 30, 570),
         makeScheduledItem('Greater One-Horned Rhinoceros', 600, 30, 600)
      ),
      false
   );
});

test('computeFirstFreeHorizontalOffsetIndex reuses open columns', () => {
   const placedItems = [
      { ...makeScheduledItem('Babirusa', 570, 30), horizontalOffsetIndex: 0 },
      { ...makeScheduledItem('Red Panda', 630, 30), horizontalOffsetIndex: 2 },
   ];

   assert.equal(
      computeFirstFreeHorizontalOffsetIndex(
         placedItems,
         makeScheduledItem('Cheetah', 575, 30)
      ),
      1
   );
});

test('computeFirstFreeHorizontalOffsetIndex returns past maxColumn when all columns are blocked', () => {
   const candidate = makeScheduledItem('Cheetah', 575, 30);
   const placedItems = [
      { ...makeScheduledItem('Babirusa', 570, 30), horizontalOffsetIndex: 0 },
      { ...makeScheduledItem('Red Panda', 576, 30), horizontalOffsetIndex: 1 },
   ];

   assert.equal(
      computeFirstFreeHorizontalOffsetIndex(placedItems, candidate),
      MAX_TIMELINE_PILL_COLUMNS
   );
});

test('formatScheduledPillGroupLabel matches map-style counted labels', () => {
   assert.equal(
      formatScheduledPillGroupLabel([{ label: 'African Lion' }]),
      'African Lion'
   );
   assert.equal(
      formatScheduledPillGroupLabel([
         { label: 'African Lion' },
         { label: 'Cheetah' },
      ]),
      'African Lion + 1'
   );
});
