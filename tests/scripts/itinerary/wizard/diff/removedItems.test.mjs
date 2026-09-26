import assert from 'node:assert/strict';
import test from 'node:test';

import { RemovedItems } from '../../../../../scripts/itinerary/wizard/diff/removedItems.js';


test('Test_FindRemovedItemsByField_TestMissingFromValidated_ExpectRemoved', () => {
   const carousel = { name: 'Conservation Carousel' };
   const zoomobile = { name: 'Zoomobile' };
   const blank = { name: '' };
   const field = 'name';
   const previousItems = [carousel, zoomobile, blank];
   const validatedItems = [carousel];

   const removed = RemovedItems.findRemovedItemsByField(
      previousItems,
      validatedItems,
      field
   );

   assert.deepEqual(removed, [zoomobile]);
});


test('Test_MergeRemovedItems_TestBackendOnly_ExpectBackend', () => {
   const backend = [{ name: 'Lion Talk', removalReason: 'unavailable' }];
   const inferred = [];
   const validated = [{ name: 'Lion Talk' }];
   const field = 'name';

   const merged = RemovedItems.mergeRemovedItems(backend, inferred, validated, field);

   assert.deepEqual(merged, backend);
});


test('Test_MergeRemovedItems_TestInferredOnly_ExpectInferred', () => {
   const inferred = [{ name: 'Masai Giraffe' }];
   const field = 'name';

   const merged = RemovedItems.mergeRemovedItems(null, inferred, [], field);

   assert.deepEqual(merged, inferred);
});


test('Test_MergeRemovedItems_TestBoth_ExpectDedupedUnion', () => {
   const talk = { name: 'Lion Talk', removalReason: 'closed' };
   const encounter = { name: 'Red Panda Encounter' };
   const inferredTalk = { name: talk.name };
   const field = 'name';

   const merged = RemovedItems.mergeRemovedItems(
      [talk],
      [inferredTalk, encounter],
      [],
      field
   );

   assert.deepEqual(merged, [talk, encounter]);
});
