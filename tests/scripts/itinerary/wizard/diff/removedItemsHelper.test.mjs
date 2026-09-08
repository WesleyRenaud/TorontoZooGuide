import assert from 'node:assert/strict';
import test from 'node:test';

import { RemovedItemsHelper } from '../../../../../scripts/itinerary/wizard/diff/removedItemsHelper.js';

test('Test_BuildValidatedItemKeySet_TestItems_ExpectUniqueKeys', () => {
   assert.deepEqual(
      [...RemovedItemsHelper.buildValidatedItemKeySet(
         [
            { name: 'Carousel' },
            { name: '  Carousel  ' },
            { name: '' },
            { name: 'Zoomobile' },
         ],
         'name'
      )].sort(),
      ['carousel', 'zoomobile']
   );
});
