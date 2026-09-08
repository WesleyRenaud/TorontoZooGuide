import assert from 'node:assert/strict';
import test from 'node:test';

import { RemovedItemsPopupHelper } from '../../../../../scripts/itinerary/panel/components/removedItemsPopupHelper.js';

test('Test_ToggleKeptItem_TestAddAndRemove_ExpectMapUpdated', () => {
   const kept = new Map();
   RemovedItemsPopupHelper.toggleKeptItem(
      kept,
      { name: 'Carousel' },
      (item) => item.name,
      (item) => ({ ...item, kept: true })
   );
   assert.deepEqual(kept.get('Carousel'), { name: 'Carousel', kept: true });

   RemovedItemsPopupHelper.toggleKeptItem(
      kept,
      { name: 'Carousel' },
      (item) => item.name,
      (item) => item
   );
   assert.equal(kept.has('Carousel'), false);
});

test('Test_ToggleKeptItem_TestMissingKey_ExpectNoChange', () => {
   const kept = new Map();
   RemovedItemsPopupHelper.toggleKeptItem(
      kept,
      { name: '' },
      () => '',
      (item) => item
   );
   assert.equal(kept.size, 0);
});
