import assert from 'node:assert/strict';
import test from 'node:test';

import { RemovedItemsPopupHelper } from '../../../../../scripts/itinerary/panel/components/removedItemsPopupHelper.js';


test('Test_ToggleKeptItem_TestAdd_ExpectMapUpdated', () => {
   const attractionName = 'Conservation Carousel';
   const attraction = { name: attractionName };
   const kept = new Map();

   RemovedItemsPopupHelper.toggleKeptItem(
      kept,
      attraction,
      (item) => item.name,
      (item) => ({ ...item, kept: true })
   );

   assert.deepEqual(kept.get(attractionName), { name: attractionName, kept: true });
});


test('Test_ToggleKeptItem_TestRemove_ExpectMapCleared', () => {
   const attractionName = 'Conservation Carousel';
   const attraction = { name: attractionName };
   const kept = new Map([[attractionName, { name: attractionName, kept: true }]]);

   RemovedItemsPopupHelper.toggleKeptItem(
      kept,
      attraction,
      (item) => item.name,
      (item) => item
   );

   assert.equal(kept.has(attractionName), false);
});


test('Test_ToggleKeptItem_TestMissingKey_ExpectNoChange', () => {
   const kept = new Map();
   const attraction = { name: '' };

   RemovedItemsPopupHelper.toggleKeptItem(
      kept,
      attraction,
      () => '',
      (item) => item
   );

   assert.equal(kept.size, 0);
});
