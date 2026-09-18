import assert from 'node:assert/strict';
import test from 'node:test';

import { ItineraryTransportationAnimal } from '../../../scripts/itinerary/itineraryTransportationAnimal.js';

test('Test_IsAddedByTransportation_TestFlag_ExpectBoolean', () => {
   assert.equal(ItineraryTransportationAnimal.isAddedByTransportation(null), false);
   assert.equal(ItineraryTransportationAnimal.isAddedByTransportation({}), false);
   assert.equal(ItineraryTransportationAnimal.isAddedByTransportation({
      added_by_transportation: false,
   }), false);
   assert.equal(ItineraryTransportationAnimal.isAddedByTransportation({
      added_by_transportation: true,
   }), true);
});
