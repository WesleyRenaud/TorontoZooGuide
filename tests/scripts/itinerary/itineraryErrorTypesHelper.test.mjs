import assert from 'node:assert/strict';
import test from 'node:test';

import { ItineraryErrorTypes } from '../../../scripts/itinerary/itineraryErrorTypes.js';
import { ItineraryErrorTypesHelper } from '../../../scripts/itinerary/itineraryErrorTypesHelper.js';

test('Test_NormalizeItineraryErrorType_TestExplicitType_ExpectTrimmed', () => {
   ItineraryErrorTypes.updateItineraryErrorTypesFromConfig({
      errorTypes: { SUCCESS: 'success', SAVE_FAILED: 'save_failed' },
      suppressedErrorTypes: [],
   });

   assert.equal(
      ItineraryErrorTypesHelper.normalizeItineraryErrorType('  save_failed  ', true),
      'save_failed'
   );
});

test('Test_NormalizeItineraryErrorType_TestLegacySuccessFlag_ExpectMapped', () => {
   ItineraryErrorTypes.updateItineraryErrorTypesFromConfig({
      errorTypes: { SUCCESS: 'success', SAVE_FAILED: 'save_failed' },
      suppressedErrorTypes: [],
   });

   assert.equal(
      ItineraryErrorTypesHelper.normalizeItineraryErrorType('', false),
      'save_failed'
   );
   assert.equal(
      ItineraryErrorTypesHelper.normalizeItineraryErrorType('', true),
      'success'
   );
});
