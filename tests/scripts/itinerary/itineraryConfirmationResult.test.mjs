import assert from 'node:assert/strict';
import test from 'node:test';

import { ItineraryConfirmationResult } from '../../../scripts/itinerary/itineraryConfirmationResult.js';


test('Test_CreateItineraryConfirmationCancelledResult_TestPayload_ExpectCancelled', () => {
   const draft = true;
   const payload = { draft };

   const result = ItineraryConfirmationResult.createItineraryConfirmationCancelledResult(payload);

   assert.deepEqual(result, { ...payload, cancelled: true });
});


test('Test_IsItineraryConfirmationCancelled_TestCancelled_ExpectTrue', () => {
   const cancelled = true;
   const result = { cancelled };

   const isCancelled = ItineraryConfirmationResult.isItineraryConfirmationCancelled(result);

   assert.equal(isCancelled, cancelled);
});


test('Test_IsItineraryConfirmationCancelled_TestMissing_ExpectFalse', () => {
   const result = {};

   const isCancelled = ItineraryConfirmationResult.isItineraryConfirmationCancelled(result);

   assert.equal(isCancelled, false);
});
