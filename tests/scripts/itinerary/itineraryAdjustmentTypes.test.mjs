import assert from 'node:assert/strict';
import test from 'node:test';

import { ItineraryAdjustmentTypes } from '../../../scripts/itinerary/itineraryAdjustmentTypes.js';

test('Test_GetItineraryAdjustmentTypes_TestSharedEnum_ExpectFrozen', () => {
   assert.deepEqual(ItineraryAdjustmentTypes.getItineraryAdjustmentTypes(), {
      ARRIVAL_TIME_ADJUSTED: 'arrivalTimeAdjusted',
      DEPARTURE_TIME_ADJUSTED: 'departureTimeAdjusted',
   });
   assert.equal(Object.isFrozen(ItineraryAdjustmentTypes.getItineraryAdjustmentTypes()), true);
});

test('Test_NormalizeItineraryAdjustmentType_TestValues_ExpectMatchedOrPassthrough', () => {
   assert.equal(
      ItineraryAdjustmentTypes.normalizeItineraryAdjustmentType('arrivalTimeAdjusted'),
      'arrivalTimeAdjusted'
   );
   assert.equal(
      ItineraryAdjustmentTypes.normalizeItineraryAdjustmentType('  departureTimeAdjusted  '),
      'departureTimeAdjusted'
   );
   assert.equal(
      ItineraryAdjustmentTypes.normalizeItineraryAdjustmentType('custom'),
      'custom'
   );
   assert.equal(ItineraryAdjustmentTypes.normalizeItineraryAdjustmentType(''), '');
});
