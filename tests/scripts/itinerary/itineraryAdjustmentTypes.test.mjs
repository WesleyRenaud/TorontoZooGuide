import assert from 'node:assert/strict';
import test from 'node:test';

import { ItineraryAdjustmentTypes } from '../../../scripts/itinerary/itineraryAdjustmentTypes.js';

test('Test_UpdateAndGetItineraryAdjustmentTypes_TestConfig_ExpectFrozen', () => {
   ItineraryAdjustmentTypes.updateItineraryAdjustmentTypesFromConfig({
      adjustmentTypes: { EARLY: 'early_admission' },
   });

   assert.deepEqual(ItineraryAdjustmentTypes.getItineraryAdjustmentTypes(), {
      EARLY: 'early_admission',
   });
});

test('Test_NormalizeItineraryAdjustmentType_TestValues_ExpectMatchedOrPassthrough', () => {
   ItineraryAdjustmentTypes.updateItineraryAdjustmentTypesFromConfig({
      adjustmentTypes: { EARLY: 'early_admission' },
   });

   assert.equal(
      ItineraryAdjustmentTypes.normalizeItineraryAdjustmentType('early_admission'),
      'early_admission'
   );
   assert.equal(
      ItineraryAdjustmentTypes.normalizeItineraryAdjustmentType('custom'),
      'custom'
   );
   assert.equal(ItineraryAdjustmentTypes.normalizeItineraryAdjustmentType(''), '');

   ItineraryAdjustmentTypes.itineraryAdjustmentTypes = null;
   assert.equal(
      ItineraryAdjustmentTypes.normalizeItineraryAdjustmentType('early_admission'),
      'early_admission'
   );
});
