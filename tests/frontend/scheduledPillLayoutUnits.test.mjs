import assert from 'node:assert/strict';
import { test } from 'node:test';

import { makeScheduledItem } from './helpers/scheduledPillTestSetup.mjs';
import { getScheduledPillMinDisplayMinutes } from '../../scripts/itinerary/panel/components/scheduledPillOverlap.js';
import { clusterShortScheduledItemsForDisplay } from '../../scripts/itinerary/panel/components/scheduledPillLayoutUnits.js';

test('getScheduledPillMinDisplayMinutes matches the clustering threshold', () => {
   assert.ok(getScheduledPillMinDisplayMinutes() > 2.9);
   assert.ok(getScheduledPillMinDisplayMinutes() < 3.1);
});

test('clusterShortScheduledItemsForDisplay groups short visits until display span is filled', () => {
   const clusteredItems = clusterShortScheduledItemsForDisplay([
      makeScheduledItem('Babirusa', 570, 2, 570),
      makeScheduledItem('Cheetah', 572, 2, 570),
      makeScheduledItem('Red Panda', 582, 2, 570),
   ], 8);

   assert.equal(clusteredItems.length, 2);
   assert.equal(clusteredItems[0].label, 'Babirusa + 1');
   assert.equal(clusteredItems[1].label, 'Red Panda');
});

test('clusterShortScheduledItemsForDisplay pulls the next visit into an under-min pill', () => {
   const clusteredItems = clusterShortScheduledItemsForDisplay([
      makeScheduledItem('Babirusa', 570, 2, 570),
      makeScheduledItem('Cheetah', 572, 8, 570),
      makeScheduledItem('Greater One-Horned Rhinoceros', 580, 8, 570),
   ]);

   assert.equal(clusteredItems.length, 2);
   assert.equal(clusteredItems[0].label, 'Babirusa + 1');
   assert.equal(clusteredItems[1].label, 'Greater One-Horned Rhinoceros');
});

test('clusterShortScheduledItemsForDisplay keeps readable visits separate', () => {
   const clusteredItems = clusterShortScheduledItemsForDisplay([
      makeScheduledItem('Babirusa', 570, 30, 570),
      makeScheduledItem('Cheetah', 574, 30, 570),
      makeScheduledItem('Red Panda', 575, 30, 570),
   ]);

   assert.equal(clusteredItems.length, 3);
   assert.equal(clusteredItems[0].label, 'Babirusa');
   assert.equal(clusteredItems[1].label, 'Cheetah');
   assert.equal(clusteredItems[2].label, 'Red Panda');
});
