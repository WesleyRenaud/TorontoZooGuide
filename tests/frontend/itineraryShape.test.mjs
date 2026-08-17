import assert from 'node:assert/strict';
import test from 'node:test';

import {
   areItineraryDraftsEqual,
   areItineraryDraftsSemanticallyEqual,
   cloneItineraryDraft,
   createEmptyItineraryDraft,
   hasSavedItineraryContent,
   isItineraryCompletelyUnset,
   isItineraryEmptyDraft,
   normalizeItineraryDraft,
   toSetItineraryPayload,
} from '../../scripts/itinerary/itineraryShape.js';

test('creates and normalizes itinerary draft shape', () => {
   assert.deepEqual(createEmptyItineraryDraft(), {
      date: '',
      arrivalTime: '',
      departureTime: '',
      animals: [],
      attractions: [],
      guardiansTalks: [],
      wildEncounters: [],
      transportations: [],
      events: [],
   });

   assert.deepEqual(normalizeItineraryDraft({
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
      events: [],
   });

   assert.deepEqual(normalizeItineraryDraft({
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
      events: [{ event_type: 'lunch', start_time: '12:00', end_time: '12:40' }],
   });
});

test('clones draft arrays without mutating the original draft', () => {
   const draft = {
      date: '2026-06-15',
      animals: [{ species: 'African Lion' }],
      attractions: [{ name: 'Conservation Carousel' }],
      guardiansTalks: [],
      wildEncounters: [{ name: 'African Rainforest' }],
   };

   const clone = cloneItineraryDraft(draft);
   clone.animals.push({ species: 'Amur Tiger' });

   assert.notEqual(clone.animals, draft.animals);
   assert.deepEqual(draft.animals, [{ species: 'African Lion' }]);
});

test('compares normalized itinerary drafts deeply', () => {
   assert.equal(areItineraryDraftsEqual(
      {
         date: '2026-06-15',
         animals: [{ species: 'African Lion', exhibit: 'Africa Savanna', likelihood: 90 }],
      },
      {
         date: '2026-06-15',
         animals: [{ species: 'African Lion', exhibit: 'Africa Savanna', likelihood: 90 }],
      }
   ), true);

   assert.equal(areItineraryDraftsEqual(
      { animals: [{ species: 'African Lion', exhibit: 'Africa Savanna' }] },
      { animals: [{ species: 'Amur Tiger', exhibit: 'Eurasia' }] }
   ), false);
});

test('semantic draft equality ignores animal metadata and list order', () => {
   assert.equal(areItineraryDraftsSemanticallyEqual(
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

   assert.equal(areItineraryDraftsSemanticallyEqual(
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

   assert.equal(areItineraryDraftsSemanticallyEqual(
      { date: '2026-06-15', animals: [{ species: 'African Lion', exhibit: 'Africa Savanna' }] },
      { date: '2026-06-16', animals: [{ species: 'African Lion', exhibit: 'Africa Savanna' }] }
   ), false);
});

test('treats a draft with only a date as non-empty', () => {
   assert.equal(isItineraryEmptyDraft({ date: '2026-06-15' }), false);
   assert.equal(isItineraryEmptyDraft({
      date: '2026-06-15',
      arrivalTime: '09:30',
   }), false);
   assert.equal(isItineraryEmptyDraft({
      date: '2026-06-15',
      wildEncounters: [{ name: 'African Rainforest' }],
   }), false);
   assert.equal(isItineraryEmptyDraft({
      date: '2026-06-15',
      events: [{ event_type: 'lunch', start_time: '12:00', end_time: '12:40' }],
   }), false);
});

test('distinguishes date-only drafts from completely unset itineraries', () => {
   assert.equal(isItineraryEmptyDraft({ date: '2026-06-15' }), false);
   assert.equal(hasSavedItineraryContent({ date: '2026-06-15' }), true);
   assert.equal(isItineraryCompletelyUnset({ date: '2026-06-15' }), false);
   assert.equal(isItineraryCompletelyUnset(null), true);
   assert.equal(isItineraryCompletelyUnset({}), true);
   assert.equal(isItineraryEmptyDraft({
      date: '2026-06-15',
      animals: [{ species: 'Tiger', exhibit: 'Savanna' }],
   }), false);
});

test('toSetItineraryPayload sends canonical shapes for the save API', () => {
   assert.deepEqual(toSetItineraryPayload({
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

test('toSetItineraryPayload moves also-transportation attractions into transportations', () => {
   assert.deepEqual(toSetItineraryPayload({
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

test('toSetItineraryPayload serializes wild encounters as wire strings', () => {
   assert.deepEqual(toSetItineraryPayload({
      date: '2026-06-15',
      wildEncounters: [{
         name: 'Kangaroo',
         start_time: '13:00',
         end_time: '13:45',
      }],
   }).wildEncounters, ['Kangaroo||13:00||13:45']);
});

test('toSetItineraryPayload keeps schedule times when provided', () => {
   assert.deepEqual(toSetItineraryPayload({
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
