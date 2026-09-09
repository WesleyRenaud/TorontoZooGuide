import assert from 'node:assert/strict';
import test from 'node:test';

import { ItineraryErrorTypesHelper } from '../../../scripts/itinerary/itineraryErrorTypesHelper.js';

test('Test_NormalizeItineraryErrorType_TestExplicitType_ExpectTrimmed', () => {
   assert.equal(
      ItineraryErrorTypesHelper.normalizeItineraryErrorType('  saveFailed  ', true),
      'saveFailed'
   );
});

test('Test_NormalizeItineraryErrorType_TestLegacySuccessFlag_ExpectMapped', () => {
   assert.equal(
      ItineraryErrorTypesHelper.normalizeItineraryErrorType('', false),
      'saveFailed'
   );
   assert.equal(
      ItineraryErrorTypesHelper.normalizeItineraryErrorType('', true),
      'success'
   );
});
