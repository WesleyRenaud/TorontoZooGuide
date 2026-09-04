import assert from 'node:assert/strict';
import { test } from 'node:test';

import { makeScheduledItem } from '../../../helpers/scheduledPillTestSetup.mjs';
import { ScheduledPillOverlap } from '../../../../../scripts/itinerary/panel/components/scheduledPillOverlap.js';
import { ScheduledPillLayoutUnits } from '../../../../../scripts/itinerary/panel/components/scheduledPillLayoutUnits.js';

test('Test_GetScheduledPillMinDisplayMinutes_TestMatchesTheClusteringThreshold_ExpectOk', () => {
   assert.ok(ScheduledPillOverlap.getScheduledPillMinDisplayMinutes() > 2.9);
   assert.ok(ScheduledPillOverlap.getScheduledPillMinDisplayMinutes() < 3.1);
});

test('Test_ClusterShortScheduledItemsForDisplay_TestGroupsShortVisitsUntilDisplaySpanIsFilled_ExpectOk', () => {
   const clusteredItems = ScheduledPillLayoutUnits.clusterShortScheduledItemsForDisplay([
      makeScheduledItem('Babirusa', 570, 2, 570),
      makeScheduledItem('Cheetah', 572, 2, 570),
      makeScheduledItem('Red Panda', 582, 2, 570),
   ], 8);

   assert.equal(clusteredItems.length, 2);
   assert.equal(clusteredItems[0].label, 'Babirusa + 1');
   assert.equal(clusteredItems[1].label, 'Red Panda');
});

test('Test_ClusterShortScheduledItemsForDisplay_TestPullsTheNextVisitIntoAnUnderMinPill_ExpectOk', () => {
   const clusteredItems = ScheduledPillLayoutUnits.clusterShortScheduledItemsForDisplay([
      makeScheduledItem('Babirusa', 570, 2, 570),
      makeScheduledItem('Cheetah', 572, 8, 570),
      makeScheduledItem('Greater One-Horned Rhinoceros', 580, 8, 570),
   ]);

   assert.equal(clusteredItems.length, 2);
   assert.equal(clusteredItems[0].label, 'Cheetah + 1');
   assert.equal(clusteredItems[1].label, 'Greater One-Horned Rhinoceros');
});

test('Test_ClusterShortScheduledItemsForDisplay_TestKeepsReadableVisitsSeparate_ExpectOk', () => {
   const clusteredItems = ScheduledPillLayoutUnits.clusterShortScheduledItemsForDisplay([
      makeScheduledItem('Babirusa', 570, 30, 570),
      makeScheduledItem('Cheetah', 574, 30, 570),
      makeScheduledItem('Red Panda', 575, 30, 570),
   ]);

   assert.equal(clusteredItems.length, 3);
   assert.equal(clusteredItems[0].label, 'Babirusa');
   assert.equal(clusteredItems[1].label, 'Cheetah');
   assert.equal(clusteredItems[2].label, 'Red Panda');
});

test('Test_ClusterShortScheduledItemsForDisplay_TestOrdersGroupedAnimalsByMaxDuration_ExpectOk', () => {
   const clusteredItems = ScheduledPillLayoutUnits.clusterShortScheduledItemsForDisplay([
      makeScheduledItem('Lake Malawi Cichlid', 570, 2, 570),
      makeScheduledItem('Masai Giraffe', 572, 8, 570),
   ], 8);

   assert.equal(clusteredItems.length, 1);
   assert.equal(clusteredItems[0].label, 'Masai Giraffe + 1');
   assert.deepEqual(
      clusteredItems[0].clusterItems.map((item) => item.label),
      [
         'Masai Giraffe',
         'Lake Malawi Cichlid',
      ]
   );
});
