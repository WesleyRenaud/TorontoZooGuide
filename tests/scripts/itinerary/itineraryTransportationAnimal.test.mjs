import assert from 'node:assert/strict';
import test from 'node:test';

import { ItineraryTransportationAnimal } from '../../../scripts/itinerary/itineraryTransportationAnimal.js';


test('Test_IsAddedByTransportation_TestNull_ExpectFalse', () => {
   const animal = null;

   const isAdded = ItineraryTransportationAnimal.isAddedByTransportation(animal);

   assert.equal(isAdded, false);
});


test('Test_IsAddedByTransportation_TestMissingFlag_ExpectFalse', () => {
   const animal = {};

   const isAdded = ItineraryTransportationAnimal.isAddedByTransportation(animal);

   assert.equal(isAdded, false);
});


test('Test_IsAddedByTransportation_TestFalse_ExpectFalse', () => {
   const addedByTransportation = false;
   const animal = { added_by_transportation: addedByTransportation };

   const isAdded = ItineraryTransportationAnimal.isAddedByTransportation(animal);

   assert.equal(isAdded, addedByTransportation);
});


test('Test_IsAddedByTransportation_TestTrue_ExpectTrue', () => {
   const addedByTransportation = true;
   const animal = { added_by_transportation: addedByTransportation };

   const isAdded = ItineraryTransportationAnimal.isAddedByTransportation(animal);

   assert.equal(isAdded, addedByTransportation);
});
