import assert from 'node:assert/strict';
import test from 'node:test';

import { ItineraryShape } from '../../../scripts/itinerary/itineraryShape.js';

test('Test_CreateAndNormalizeItineraryDraft_TestMixedInput_ExpectNormalizedShape', () => {
   assert.deepEqual(ItineraryShape.createEmptyItineraryDraft(), {
      date: '',
      arrivalTime: '',
      departureTime: '',
      animals: [],
      attractions: [],
      guardiansTalks: [],
      wildEncounters: [],
      transportations: [],
      transportationStations: [],
      events: [],
   });

   assert.deepEqual(ItineraryShape.normalizeItineraryDraft({
      date: '2026-06-15',
      arrivalTime: '09:30',
      departureTime: '17:00',
      animals: [{ species: 'African Lion' }],
      attractions: 'Conservation Carousel',
      guardiansTalks: [{ name: 'Amur Tiger' }],
      wildEncounters: null,
   }), {
      date: '2026-06-15',
      arrivalTime: '09:30',
      departureTime: '17:00',
      animals: [{ species: 'African Lion' }],
      attractions: [],
      guardiansTalks: [{ name: 'Amur Tiger' }],
      wildEncounters: [],
      transportations: [],
      transportationStations: [],
      events: [],
   });

   assert.deepEqual(ItineraryShape.normalizeItineraryDraft({
      events: [{ event_type: 'lunch', start_time: '12:00', end_time: '12:40' }],
   }), {
      date: '',
      arrivalTime: '',
      departureTime: '',
      animals: [],
      attractions: [],
      guardiansTalks: [],
      wildEncounters: [],
      transportations: [],
      transportationStations: [],
      events: [{ event_type: 'lunch', start_time: '12:00', end_time: '12:40' }],
   });
});

test('Test_CloneItineraryDraft_TestArrayFields_ExpectIndependentCopy', () => {
   const draft = {
      date: '2026-06-15',
      animals: [{ species: 'African Lion' }],
      attractions: [{ name: 'Conservation Carousel' }],
      guardiansTalks: [],
      wildEncounters: [{ name: 'African Rainforest' }],
   };

   const clone = ItineraryShape.cloneItineraryDraft(draft);
   clone.animals.push({ species: 'Amur Tiger' });

   assert.notEqual(clone.animals, draft.animals);
   assert.deepEqual(draft.animals, [{ species: 'African Lion' }]);
});

test('Test_AreItineraryDraftsEqual_TestNormalizedDrafts_ExpectDeepEquality', () => {
   assert.equal(ItineraryShape.areItineraryDraftsEqual(
      {
         date: '2026-06-15',
         animals: [{ species: 'African Lion', exhibit: 'Africa Savanna', likelihood: 90 }],
      },
      {
         date: '2026-06-15',
         animals: [{ species: 'African Lion', exhibit: 'Africa Savanna', likelihood: 90 }],
      }
   ), true);

   assert.equal(ItineraryShape.areItineraryDraftsEqual(
      { animals: [{ species: 'African Lion', exhibit: 'Africa Savanna' }] },
      { animals: [{ species: 'Amur Tiger', exhibit: 'Eurasia' }] }
   ), false);
});

test('Test_AreItineraryDraftsSemanticallyEqual_TestMetadataAndOrder_ExpectEqual', () => {
   assert.equal(ItineraryShape.areItineraryDraftsSemanticallyEqual(
      {
         date: '2026-06-15',
         animals: [
            { species: 'African Lion', exhibit: 'Africa Savanna', likelihood: 90, imageSrc: '/a.png' },
         ],
      },
      {
         date: '2026-06-15',
         animals: [
            { species: 'African Lion', exhibit: 'Africa Savanna', likelihood: 5 },
         ],
      }
   ), true);

   assert.equal(ItineraryShape.areItineraryDraftsSemanticallyEqual(
      {
         date: '2026-06-15',
         animals: [
            { species: 'Amur Tiger', exhibit: 'Eurasia' },
            { species: 'African Lion', exhibit: 'Africa Savanna' },
         ],
      },
      {
         date: '2026-06-15',
         animals: [
            { species: 'African Lion', exhibit: 'Africa Savanna' },
            { species: 'Amur Tiger', exhibit: 'Eurasia' },
         ],
      }
   ), true);

   assert.equal(ItineraryShape.areItineraryDraftsSemanticallyEqual(
      { date: '2026-06-15', animals: [{ species: 'African Lion', exhibit: 'Africa Savanna' }] },
      { date: '2026-06-16', animals: [{ species: 'African Lion', exhibit: 'Africa Savanna' }] }
   ), false);
});

test('Test_IsItineraryEmptyDraft_TestDateOnly_ExpectNonEmpty', () => {
   assert.equal(ItineraryShape.isItineraryEmptyDraft({ date: '2026-06-15' }), false);
   assert.equal(ItineraryShape.isItineraryEmptyDraft({
      date: '2026-06-15',
      arrivalTime: '09:30',
   }), false);
   assert.equal(ItineraryShape.isItineraryEmptyDraft({
      date: '2026-06-15',
      wildEncounters: [{ name: 'African Rainforest' }],
   }), false);
   assert.equal(ItineraryShape.isItineraryEmptyDraft({
      date: '2026-06-15',
      events: [{ event_type: 'lunch', start_time: '12:00', end_time: '12:40' }],
   }), false);
   assert.equal(ItineraryShape.isItineraryEmptyDraft({
      transportations: [{ name: 'Zoomobile', added_as_attraction: true }],
   }), false);
});

test('Test_IsItineraryCompletelyUnset_TestDateOnlyVsUnset_ExpectDistinguished', () => {
   assert.equal(ItineraryShape.isItineraryEmptyDraft({ date: '2026-06-15' }), false);
   assert.equal(ItineraryShape.hasSavedItineraryContent({ date: '2026-06-15' }), true);
   assert.equal(ItineraryShape.isItineraryCompletelyUnset({ date: '2026-06-15' }), false);
   assert.equal(ItineraryShape.isItineraryCompletelyUnset(null), true);
   assert.equal(ItineraryShape.isItineraryCompletelyUnset({}), true);
   assert.equal(ItineraryShape.isItineraryEmptyDraft({
      date: '2026-06-15',
      animals: [{ species: 'Tiger', exhibit: 'Savanna' }],
   }), false);
});

test('Test_ToSetItineraryPayload_TestCanonicalShapes_ExpectSaveApiShape', () => {
   assert.deepEqual(ItineraryShape.toSetItineraryPayload({
      date: '2026-06-15',
      animals: [
         { species: 'African Lion', exhibit: 'Africa Savanna', likelihood: 90 },
         { species: '  ', exhibit: 'Africa Savanna' },
         {
            species: ' Masai Giraffe ',
            exhibit: 'Africa Savanna',
            enclosure_name: ' Giraffe House ',
         },
      ],
      attractions: [{ name: 'Conservation Carousel' }, 'Greenhouse'],
      guardiansTalks: [{ name: 'African Lion', type: 'guardiansTalk' }],
      wildEncounters: [{ name: 'African Rainforest', start_time: '14:00' }],
   }), {
      date: '2026-06-15',
      arrivalTime: '',
      departureTime: '',
      animals: [
         { species: 'African Lion', exhibit: 'Africa Savanna' },
         {
            species: 'Masai Giraffe',
            exhibit: 'Africa Savanna',
            enclosure_name: 'Giraffe House',
         },
      ],
      attractions: ['Conservation Carousel', 'Greenhouse'],
      transportations: [],
      guardiansTalks: [{
         name: 'African Lion',
         start_time: null,
         end_time: null,
      }],
      wildEncounters: ['African Rainforest||14:00'],
   });
});

test('Test_HydrateWizardDraftFromSavedItinerary_TestAddedAsAttraction_ExpectMovedToAttractions', () => {
   assert.deepEqual(ItineraryShape.hydrateWizardDraftFromSavedItinerary({
      date: '2026-08-17',
      attractions: [],
      transportations: [
         { name: 'Zoomobile', added_as_attraction: true },
         { name: 'Zoo Shuttle', added_as_attraction: false },
      ],
   }), {
      date: '2026-08-17',
      arrivalTime: '',
      departureTime: '',
      animals: [],
      attractions: [{ name: 'Zoomobile', addedAsAttraction: true }],
      guardiansTalks: [],
      wildEncounters: [],
      transportations: [{ name: 'Zoo Shuttle', added_as_attraction: false }],
      transportationStations: [],
      events: [],
   });
});

test('Test_ToSetItineraryPayload_TestSameNameRoles_ExpectBothKept', () => {
   assert.deepEqual(ItineraryShape.toSetItineraryPayload({
      date: '2026-08-17',
      attractions: [{ name: 'Zoomobile', addedAsAttraction: true }],
      transportations: [{ name: 'Zoomobile', addedAsAttraction: false }],
   }).transportations, [
      { name: 'Zoomobile', added_as_attraction: false },
      { name: 'Zoomobile', added_as_attraction: true },
   ]);
});

test('Test_ToSetItineraryPayload_TestSavedAddedAsAttraction_ExpectPreserved', () => {
   assert.deepEqual(ItineraryShape.toSetItineraryPayload({
      date: '2026-08-17',
      animals: [{ species: 'African Lion', exhibit: 'Africa Savanna' }],
      transportations: [{ name: 'Zoomobile', added_as_attraction: true }],
   }).transportations, [{
      name: 'Zoomobile',
      added_as_attraction: true,
   }]);
});

test('Test_ToSetItineraryPayload_TestAlsoTransportationAttractions_ExpectMoved', () => {
   assert.deepEqual(ItineraryShape.toSetItineraryPayload({
      date: '2026-06-15',
      attractions: [
         { name: 'Conservation Carousel' },
         { name: 'Zoomobile', addedAsAttraction: true },
      ],
      transportations: [
         { name: 'Zoo Shuttle', addedAsAttraction: false },
      ],
   }), {
      date: '2026-06-15',
      arrivalTime: '',
      departureTime: '',
      animals: [],
      attractions: ['Conservation Carousel'],
      transportations: [
         { name: 'Zoo Shuttle', added_as_attraction: false },
         { name: 'Zoomobile', added_as_attraction: true },
      ],
      guardiansTalks: [],
      wildEncounters: [],
   });
});

test('Test_ToSetItineraryPayload_TestWildEncounters_ExpectWireStrings', () => {
   assert.deepEqual(ItineraryShape.toSetItineraryPayload({
      date: '2026-06-15',
      wildEncounters: [{
         name: 'Kangaroo',
         start_time: '13:00',
         end_time: '13:45',
      }],
   }).wildEncounters, ['Kangaroo||13:00||13:45']);
});

test('Test_ToSetItineraryPayload_TestScheduleTimes_ExpectPreserved', () => {
   assert.deepEqual(ItineraryShape.toSetItineraryPayload({
      date: '2026-06-15',
      arrivalTime: '09:30',
      departureTime: '17:00',
      animals: [],
      attractions: [],
      guardiansTalks: [{
         name: 'African Lion',
         start_time: '13:45',
         end_time: '14:00',
      }],
      wildEncounters: [{
         name: 'Grizzly Bear',
         start_time: '13:00',
      }],
   }), {
      date: '2026-06-15',
      arrivalTime: '09:30',
      departureTime: '17:00',
      animals: [],
      attractions: [],
      transportations: [],
      guardiansTalks: [{
         name: 'African Lion',
         start_time: '13:45',
         end_time: '14:00',
      }],
      wildEncounters: ['Grizzly Bear||13:00'],
   });
});
