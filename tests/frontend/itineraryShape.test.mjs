import assert from 'node:assert/strict';
import test from 'node:test';

import {
   areItineraryDraftsEqual,
   cloneItineraryDraft,
   createEmptyItineraryDraft,
   isItineraryEmptyDraft,
   normalizeItineraryDraft,
} from '../../scripts/itinerary/itineraryShape.js';

test('creates and normalizes itinerary draft shape', () => {
   assert.deepEqual(createEmptyItineraryDraft(), {
      date: '',
      animals: [],
      attractions: [],
      guardiansTalks: [],
      wildEncounters: [],
   });

   assert.deepEqual(normalizeItineraryDraft({
      date: '2026-06-15',
      animals: [{ species: 'African Lion' }],
      attractions: 'Conservation Carousel',
      guardiansTalks: [{ name: 'Amur Tiger' }],
      wildEncounters: null,
   }), {
      date: '2026-06-15',
      animals: [{ species: 'African Lion' }],
      attractions: [],
      guardiansTalks: [{ name: 'Amur Tiger' }],
      wildEncounters: [],
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
         animals: [{ species: 'African Lion', likelihood: 90 }],
      },
      {
         date: '2026-06-15',
         animals: [{ species: 'African Lion', likelihood: 90 }],
      }
   ), true);

   assert.equal(areItineraryDraftsEqual(
      { animals: [{ species: 'African Lion' }] },
      { animals: [{ species: 'Amur Tiger' }] }
   ), false);
});

test('treats a draft with only a date as empty', () => {
   assert.equal(isItineraryEmptyDraft({ date: '2026-06-15' }), true);
   assert.equal(isItineraryEmptyDraft({
      date: '2026-06-15',
      wildEncounters: [{ name: 'African Rainforest' }],
   }), false);
});
