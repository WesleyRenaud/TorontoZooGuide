import assert from 'node:assert/strict';
import test from 'node:test';

import { RemovedItems } from '../../../../../scripts/itinerary/wizard/diff/removedItems.js';

test('Test_FindRemovedItemsByField_TestMissingFromValidated_ExpectRemoved', () => {
   assert.deepEqual(
      RemovedItems.findRemovedItemsByField(
         [{ name: 'Carousel' }, { name: 'Zoomobile' }, { name: '' }],
         [{ name: 'Carousel' }],
         'name'
      ),
      [{ name: 'Zoomobile' }]
   );
});

test('Test_MergeRemovedItems_TestBackendOnly_ExpectBackend', () => {
   const backend = [{ name: 'Talk', removalReason: 'unavailable' }];
   assert.deepEqual(
      RemovedItems.mergeRemovedItems(backend, [], [{ name: 'Talk' }], 'name'),
      backend
   );
});

test('Test_MergeRemovedItems_TestInferredOnly_ExpectInferred', () => {
   assert.deepEqual(
      RemovedItems.mergeRemovedItems(
         null,
         [{ name: 'Giraffe' }],
         [],
         'name'
      ),
      [{ name: 'Giraffe' }]
   );
});

test('Test_MergeRemovedItems_TestBoth_ExpectDedupedUnion', () => {
   assert.deepEqual(
      RemovedItems.mergeRemovedItems(
         [{ name: 'Talk', removalReason: 'closed' }],
         [{ name: 'Talk' }, { name: 'Encounter' }],
         [],
         'name'
      ),
      [
         { name: 'Talk', removalReason: 'closed' },
         { name: 'Encounter' },
      ]
   );
});
