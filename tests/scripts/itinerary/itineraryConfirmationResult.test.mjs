import assert from 'node:assert/strict';
import test from 'node:test';

import { ItineraryConfirmationResult } from '../../../scripts/itinerary/itineraryConfirmationResult.js';

test('Test_CreateItineraryConfirmationCancelledResult_TestPayload_ExpectCancelled', () => {
   assert.deepEqual(
      ItineraryConfirmationResult.createItineraryConfirmationCancelledResult({ draft: true }),
      { draft: true, cancelled: true }
   );
});

test('Test_IsItineraryConfirmationCancelled_TestResult_ExpectBoolean', () => {
   assert.equal(ItineraryConfirmationResult.isItineraryConfirmationCancelled({ cancelled: true }), true);
   assert.equal(ItineraryConfirmationResult.isItineraryConfirmationCancelled({}), false);
});
