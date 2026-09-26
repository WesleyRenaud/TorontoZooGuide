import assert from 'node:assert/strict';
import test from 'node:test';

import { ItineraryDraftEqualityComparer } from '../../../scripts/itinerary/itineraryDraftEqualityComparer.js';


test('Test_AreDraftValuesEqual_TestSameNumber_ExpectTrue', () => {
   const value = 1;

   const equal = ItineraryDraftEqualityComparer.areDraftValuesEqual(value, value);

   assert.equal(equal, true);
});


test('Test_AreDraftValuesEqual_TestDifferentNumbers_ExpectFalse', () => {
   const left = 1;
   const right = 2;

   const equal = ItineraryDraftEqualityComparer.areDraftValuesEqual(left, right);

   assert.equal(equal, false);
});


test('Test_AreDraftValuesEqual_TestSameArray_ExpectTrue', () => {
   const value = ['African Lion'];

   const equal = ItineraryDraftEqualityComparer.areDraftValuesEqual(value, [...value]);

   assert.equal(equal, true);
});


test('Test_AreDraftValuesEqual_TestDifferentArray_ExpectFalse', () => {
   const left = ['African Lion'];
   const right = ['Amur Tiger'];

   const equal = ItineraryDraftEqualityComparer.areDraftValuesEqual(left, right);

   assert.equal(equal, false);
});


test('Test_AreDraftValuesEqual_TestDifferentArrayLength_ExpectFalse', () => {
   const left = ['African Lion'];
   const right = ['African Lion', 'Amur Tiger'];

   const equal = ItineraryDraftEqualityComparer.areDraftValuesEqual(left, right);

   assert.equal(equal, false);
});


test('Test_AreDraftValuesEqual_TestArrayAndString_ExpectFalse', () => {
   const value = 'African Lion';

   const equal = ItineraryDraftEqualityComparer.areDraftValuesEqual([value], value);

   assert.equal(equal, false);
});


test('Test_AreDraftValuesEqual_TestNullAndObject_ExpectFalse', () => {
   const left = null;
   const right = { a: 1 };

   const equal = ItineraryDraftEqualityComparer.areDraftValuesEqual(left, right);

   assert.equal(equal, false);
});


test('Test_AreDraftValuesEqual_TestObjectAndNull_ExpectFalse', () => {
   const left = { a: 1 };
   const right = null;

   const equal = ItineraryDraftEqualityComparer.areDraftValuesEqual(left, right);

   assert.equal(equal, false);
});


test('Test_AreDraftValuesEqual_TestNumberAndString_ExpectFalse', () => {
   const value = 1;

   const equal = ItineraryDraftEqualityComparer.areDraftValuesEqual(value, String(value));

   assert.equal(equal, false);
});


test('Test_AreObjectsEqual_TestNested_ExpectTrue', () => {
   const left = { a: 1, b: { c: 2 } };
   const right = { a: 1, b: { c: 2 } };

   const equal = ItineraryDraftEqualityComparer.areObjectsEqual(left, right);

   assert.equal(equal, true);
});


test('Test_AreObjectsEqual_TestDifferentKeys_ExpectFalse', () => {
   const left = { a: 1 };
   const right = { a: 1, b: 2 };

   const equal = ItineraryDraftEqualityComparer.areObjectsEqual(left, right);

   assert.equal(equal, false);
});


test('Test_SortStringsForComparison_TestUnsorted_ExpectSorted', () => {
   const tiger = 'Amur Tiger';
   const lion = 'African Lion';
   const values = [tiger, lion];

   const sorted = ItineraryDraftEqualityComparer.sortStringsForComparison(values);

   assert.deepEqual(sorted, [lion, tiger]);
});


test('Test_SortScheduledItemsForSaveComparison_TestUnsorted_ExpectSorted', () => {
   const zebra = { name: 'Grant\'s Zebra' };
   const lion = { name: 'African Lion' };
   const items = [zebra, lion];

   const sorted = ItineraryDraftEqualityComparer.sortScheduledItemsForSaveComparison(items);

   assert.deepEqual(sorted, [lion, zebra]);
});


test('Test_SortTransportationsForSaveComparison_TestUnsorted_ExpectSorted', () => {
   const zoomobile = { name: 'Zoomobile' };
   const boat = { name: 'Boat' };
   const items = [zoomobile, boat];

   const sorted = ItineraryDraftEqualityComparer.sortTransportationsForSaveComparison(items);

   assert.deepEqual(sorted, [boat, zoomobile]);
});


test('Test_SortAnimalsForSaveComparison_TestUnsorted_ExpectSorted', () => {
   const exhibit = 'Africa Savanna';
   const zebra = { species: 'Grant\'s Zebra', exhibit };
   const lion = { species: 'African Lion', exhibit };
   const animals = [zebra, lion];

   const sorted = ItineraryDraftEqualityComparer.sortAnimalsForSaveComparison(animals);

   assert.deepEqual(sorted.map((animal) => animal.species), [lion.species, zebra.species]);
});


test('Test_AreItineraryDraftSaveItemSelectionsEqual_TestMatchingSaves_ExpectTrue', () => {
   const arrivalTime = '09:00';
   const departureTime = '17:00';
   const animal = { species: 'African Lion', exhibit: 'African Savanna' };
   const attraction = 'Conservation Carousel';
   const transportation = { name: 'Zoomobile' };
   const talk = { name: 'Lion Talk' };
   const wildEncounter = 'Red Panda';
   const left = {
      arrivalTime,
      departureTime,
      animals: [animal],
      attractions: [attraction],
      transportations: [transportation],
      guardiansTalks: [talk],
      wildEncounters: [wildEncounter],
   };
   const right = {
      arrivalTime,
      departureTime,
      animals: [animal],
      attractions: [attraction],
      transportations: [transportation],
      guardiansTalks: [talk],
      wildEncounters: [wildEncounter],
   };

   const equal = ItineraryDraftEqualityComparer.areItineraryDraftSaveItemSelectionsEqual(left, right);

   assert.equal(equal, true);
});


test('Test_AreItineraryDraftSaveItemSelectionsEqual_TestDifferentArrival_ExpectFalse', () => {
   const base = {
      arrivalTime: '09:00',
      departureTime: '17:00',
      animals: [],
      attractions: [],
      transportations: [],
      guardiansTalks: [],
      wildEncounters: [],
   };
   const changedArrival = '10:00';

   const equal = ItineraryDraftEqualityComparer.areItineraryDraftSaveItemSelectionsEqual(
      base,
      { ...base, arrivalTime: changedArrival }
   );

   assert.equal(equal, false);
});


test('Test_AreItineraryDraftSaveItemSelectionsEqual_TestDifferentDeparture_ExpectFalse', () => {
   const base = {
      arrivalTime: '09:00',
      departureTime: '17:00',
      animals: [],
      attractions: [],
      transportations: [],
      guardiansTalks: [],
      wildEncounters: [],
   };
   const changedDeparture = '18:00';

   const equal = ItineraryDraftEqualityComparer.areItineraryDraftSaveItemSelectionsEqual(
      base,
      { ...base, departureTime: changedDeparture }
   );

   assert.equal(equal, false);
});


test('Test_AreItineraryDraftSaveItemSelectionsEqual_TestDifferentAnimals_ExpectFalse', () => {
   const base = {
      arrivalTime: '09:00',
      departureTime: '17:00',
      animals: [],
      attractions: [],
      transportations: [],
      guardiansTalks: [],
      wildEncounters: [],
   };
   const animal = { species: 'African Lion', exhibit: 'Africa Savanna' };

   const equal = ItineraryDraftEqualityComparer.areItineraryDraftSaveItemSelectionsEqual(
      { ...base, animals: [animal] },
      base
   );

   assert.equal(equal, false);
});
