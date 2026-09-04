import assert from 'node:assert/strict';
import { test } from 'node:test';

import { makeScheduledItem } from '../../../helpers/scheduledPillTestSetup.mjs';
import {
   MAX_TIMELINE_PILL_COLUMNS,
   ScheduledPillOverlap,
} from '../../../../../scripts/itinerary/panel/components/scheduledPillOverlap.js';

test('Test_GetScheduledItemEndMinutes_TestUsesParsedEndMinutesFromScheduleTimes_ExpectOk', () => {
   assert.equal(
      ScheduledPillOverlap.getScheduledItemEndMinutes({
         startMinutes: 600,
         maximumDuration: 8,
         endMinutes: 615,
      }),
      615
   );
   assert.ok(Number.isNaN(ScheduledPillOverlap.getScheduledItemEndMinutes({
      startMinutes: 600,
      maximumDuration: 8,
   })));
});

test('Test_GetScheduledItemTimeRange_TestReturnsStartAndEndMinutes_ExpectOk', () => {
   assert.deepEqual(
      ScheduledPillOverlap.getScheduledItemTimeRange({
         startMinutes: 570,
         endMinutes: 600,
      }),
      {
         startMinutes: 570,
         endMinutes: 600,
      }
   );
});

test('Test_GetScheduledPillVisualBand_TestExpandsShortVisitsToTheMinimumDisplaySpan_ExpectOk', () => {
   const band = ScheduledPillOverlap.getScheduledPillVisualBand(
      makeScheduledItem('Babirusa', 570, 2, 570)
   );

   assert.equal(band.endMinutes - band.startMinutes, ScheduledPillOverlap.getScheduledPillMinDisplayMinutes());
});

test('Test_GetScheduledPillVisualBand_TestSpansClusteredSummaryItems_ExpectOk', () => {
   const band = ScheduledPillOverlap.getScheduledPillVisualBand({
      summaryItems: [
         makeScheduledItem('Babirusa', 570, 2, 570),
         makeScheduledItem('Cheetah', 575, 2, 570),
      ],
   });

   assert.ok(band.startMinutes < 570);
   assert.ok(band.endMinutes > 572);
});

test('Test_DoScheduledTimeRangesOverlap_TestUsesStrictBoundsForTouchingWindows_ExpectOk', () => {
   assert.equal(
      ScheduledPillOverlap.doScheduledTimeRangesOverlap(
         { startMinutes: 570, endMinutes: 600 },
         { startMinutes: 590, endMinutes: 620 }
      ),
      true
   );
   assert.equal(
      ScheduledPillOverlap.doScheduledTimeRangesOverlap(
         { startMinutes: 570, endMinutes: 600 },
         { startMinutes: 600, endMinutes: 630 }
      ),
      false
   );
});

test('Test_ScheduledPillsOverlapInDefaultPosition_TestDetectsOverlapWithinASlot_ExpectOk', () => {
   assert.equal(
      ScheduledPillOverlap.scheduledPillsOverlapInDefaultPosition(
         makeScheduledItem('Babirusa', 570, 30),
         makeScheduledItem('Cheetah', 575, 30)
      ),
      true
   );
});

test('Test_ScheduledPillsOverlapInDefaultPosition_TestIgnoresBackToBackSlotBoundaries_ExpectOk', () => {
   assert.equal(
      ScheduledPillOverlap.scheduledPillsOverlapInDefaultPosition(
         makeScheduledItem('Babirusa', 570, 30, 570),
         makeScheduledItem('Greater One-Horned Rhinoceros', 600, 30, 600)
      ),
      false
   );
});

test('Test_ComputeFirstFreeHorizontalOffsetIndex_TestReusesOpenColumns_ExpectOk', () => {
   const placedItems = [
      { ...makeScheduledItem('Babirusa', 570, 30), horizontalOffsetIndex: 0 },
      { ...makeScheduledItem('Red Panda', 630, 30), horizontalOffsetIndex: 2 },
   ];

   assert.equal(
      ScheduledPillOverlap.computeFirstFreeHorizontalOffsetIndex(
         placedItems,
         makeScheduledItem('Cheetah', 575, 30)
      ),
      1
   );
});

test('Test_ComputeFirstFreeHorizontalOffsetIndex_TestReturnsPastMaxColumnWhenAllColumnsAreBlocked_ExpectOk', () => {
   const candidate = makeScheduledItem('Cheetah', 575, 30);
   const placedItems = [
      { ...makeScheduledItem('Babirusa', 570, 30), horizontalOffsetIndex: 0 },
      { ...makeScheduledItem('Red Panda', 576, 30), horizontalOffsetIndex: 1 },
   ];

   assert.equal(
      ScheduledPillOverlap.computeFirstFreeHorizontalOffsetIndex(placedItems, candidate),
      MAX_TIMELINE_PILL_COLUMNS
   );
});

test('Test_FormatScheduledPillGroupLabel_TestFormatsAnimalViewingSpotLabels_ExpectOk', () => {
   assert.equal(
      ScheduledPillOverlap.formatScheduledPillGroupLabel([
         { label: 'Marabou Stork • Savanna Overlook' },
      ]),
      'Marabou Stork • Savanna Overlook'
   );
   assert.equal(
      ScheduledPillOverlap.formatScheduledPillGroupLabel([
         { label: 'Marabou Stork • Savanna Overlook' },
         { label: 'Southern Ground Hornbill • Savanna Overlook' },
      ]),
      'Marabou Stork • Savanna Overlook + 1'
   );
});

test('Test_FormatScheduledPillGroupLabel_TestMatchesMapStyleCountedLabels_ExpectOk', () => {
   assert.equal(
      ScheduledPillOverlap.formatScheduledPillGroupLabel([{ label: 'African Lion' }]),
      'African Lion'
   );
   assert.equal(
      ScheduledPillOverlap.formatScheduledPillGroupLabel([
         { label: 'African Lion' },
         { label: 'Cheetah' },
      ]),
      'African Lion + 1'
   );
});

test('Test_FormatScheduledPillGroupLabel_TestPrefersTheLongestVisitDuration_ExpectOk', () => {
   assert.equal(
      ScheduledPillOverlap.formatScheduledPillGroupLabel([
         { label: 'Lake Malawi Cichlid', maximumDuration: 2 },
         { label: 'Masai Giraffe', maximumDuration: 30 },
      ]),
      'Masai Giraffe + 1'
   );
});

test('Test_SortScheduledItemsForGroupDisplay_TestOrdersGroupedAnimalsByMaxDuration_ExpectOk', () => {
   assert.deepEqual(
      ScheduledPillOverlap.sortScheduledItemsForGroupDisplay([
         { label: 'Lake Malawi Cichlid', maximumDuration: 2 },
         { label: 'Masai Giraffe', maximumDuration: 30 },
         { label: 'Red Panda', maximumDuration: 8 },
      ]).map((item) => item.label),
      [
         'Masai Giraffe',
         'Red Panda',
         'Lake Malawi Cichlid',
      ]
   );
});
