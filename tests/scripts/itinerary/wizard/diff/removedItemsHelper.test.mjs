import assert from 'node:assert/strict';
import test from 'node:test';

import { RemovedItemsHelper } from '../../../../../scripts/itinerary/wizard/diff/removedItemsHelper.js';


test('Test_BuildValidatedItemKeySet_TestItems_ExpectUniqueKeys', () => {
   const carousel = 'Carousel';
   const zoomobile = 'Zoomobile';
   const field = 'name';
   const items = [
      { [field]: carousel },
      { [field]: `  ${carousel}  ` },
      { [field]: '' },
      { [field]: zoomobile },
   ];

   const keys = [...RemovedItemsHelper.buildValidatedItemKeySet(items, field)].sort();

   assert.deepEqual(keys, [carousel.toLowerCase(), zoomobile.toLowerCase()]);
});
