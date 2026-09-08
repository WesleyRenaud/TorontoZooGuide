import assert from 'node:assert/strict';
import test from 'node:test';

import { ItineraryDraftEqualityComparer } from '../../../scripts/itinerary/itineraryDraftEqualityComparer.js';

test('Test_AreDraftValuesEqual_TestPrimitivesAndArrays_ExpectComparison', () => {
   assert.equal(ItineraryDraftEqualityComparer.areDraftValuesEqual(1, 1), true);
   assert.equal(ItineraryDraftEqualityComparer.areDraftValuesEqual(1, 2), false);
   assert.equal(ItineraryDraftEqualityComparer.areDraftValuesEqual(['a'], ['a']), true);
   assert.equal(ItineraryDraftEqualityComparer.areDraftValuesEqual(['a'], ['b']), false);
   assert.equal(ItineraryDraftEqualityComparer.areDraftValuesEqual(['a'], 'a'), false);
});

test('Test_AreObjectsEqual_TestNested_ExpectDeepEquality', () => {
   assert.equal(
      ItineraryDraftEqualityComparer.areObjectsEqual(
         { a: 1, b: { c: 2 } },
         { a: 1, b: { c: 2 } }
      ),
      true
   );
   assert.equal(
      ItineraryDraftEqualityComparer.areObjectsEqual({ a: 1 }, { a: 1, b: 2 }),
      false
   );
});

test('Test_SortStringsForComparison_TestUnsorted_ExpectSorted', () => {
   assert.deepEqual(
      ItineraryDraftEqualityComparer.sortStringsForComparison(['Tiger', 'Lion']),
      ['Lion', 'Tiger']
   );
});

test('Test_AreItineraryDraftSaveItemSelectionsEqual_TestMatchingSaves_ExpectTrue', () => {
   const left = {
      arrivalTime: '09:00',
      departureTime: '17:00',
      animals: [{ species: 'African Lion', exhibit: 'African Savanna' }],
      attractions: ['Carousel'],
      transportations: [{ name: 'Zoomobile' }],
      guardiansTalks: [{ name: 'Lion Talk' }],
      wildEncounters: ['Red Panda'],
   };
   const right = {
      arrivalTime: '09:00',
      departureTime: '17:00',
      animals: [{ species: 'African Lion', exhibit: 'African Savanna' }],
      attractions: ['Carousel'],
      transportations: [{ name: 'Zoomobile' }],
      guardiansTalks: [{ name: 'Lion Talk' }],
      wildEncounters: ['Red Panda'],
   };

   assert.equal(
      ItineraryDraftEqualityComparer.areItineraryDraftSaveItemSelectionsEqual(left, right),
      true
   );
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

   assert.equal(
      ItineraryDraftEqualityComparer.areItineraryDraftSaveItemSelectionsEqual(
         base,
         { ...base, arrivalTime: '10:00' }
      ),
      false
   );
});
