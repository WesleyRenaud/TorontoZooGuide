import assert from 'node:assert/strict';
import { afterEach, beforeEach, test } from 'node:test';

import {
   ANIMALS_KEY,
   ATTRACTIONS_KEY,
   DATE_KEY,
   GUARDIANS_KEY,
   SELECTED_EXHIBITS_KEY,
   WILD_KEY,
} from '../../scripts/itinerary/storageKeys.js';
import {
   clearItineraryDraftStorage,
   isStoredItineraryStale,
   loadStoredItineraryDraft,
   safeParseJSON,
   writeStoredItineraryDraft,
} from '../../scripts/itinerary/draftStorage.js';

function createLocalStorageMock() {
   const values = new Map();

   return {
      getItem: (key) => values.get(key) ?? null,
      setItem: (key, value) => {
         values.set(key, String(value));
      },
      removeItem: (key) => {
         values.delete(key);
      },
   };
}

beforeEach(() => {
   globalThis.localStorage = createLocalStorageMock();
});

afterEach(() => {
   delete globalThis.localStorage;
});

function toLocalISODate(date) {
   const year = date.getFullYear();
   const month = String(date.getMonth() + 1).padStart(2, '0');
   const day = String(date.getDate()).padStart(2, '0');
   return `${year}-${month}-${day}`;
}

test('safeParseJSON returns a fallback for malformed stored values', () => {
   assert.deepEqual(safeParseJSON('{"name":"Zootique"}', {}), { name: 'Zootique' });
   assert.deepEqual(safeParseJSON('{bad json', []), []);
});

test('writes and loads the stored itinerary draft', () => {
   writeStoredItineraryDraft({
      date: '2026-06-15',
      animals: [{ species: 'African Lion' }],
      attractions: [{ name: 'Conservation Carousel' }],
      guardiansTalks: [{ name: 'Amur Tiger' }],
      wildEncounters: [{ name: 'African Rainforest' }],
   });

   assert.equal(localStorage.getItem(DATE_KEY), '2026-06-15');
   assert.deepEqual(JSON.parse(localStorage.getItem(ANIMALS_KEY)), [{ species: 'African Lion' }]);
   assert.deepEqual(loadStoredItineraryDraft(), {
      date: '2026-06-15',
      arrivalTime: '',
      departureTime: '',
      animals: [{ species: 'African Lion' }],
      attractions: [{ name: 'Conservation Carousel' }],
      guardiansTalks: [{ name: 'Amur Tiger' }],
      wildEncounters: [{ name: 'African Rainforest' }],
      events: [],
   });
});

test('clears draft storage while optionally preserving selection storage', () => {
   writeStoredItineraryDraft({
      date: '2026-06-15',
      animals: [{ species: 'African Lion' }],
   });
   localStorage.setItem(SELECTED_EXHIBITS_KEY, JSON.stringify(['Africa Savanna']));

   clearItineraryDraftStorage({ includeSelections: false });

   assert.equal(localStorage.getItem(DATE_KEY), null);
   assert.equal(localStorage.getItem(ANIMALS_KEY), null);
   assert.equal(localStorage.getItem(ATTRACTIONS_KEY), null);
   assert.equal(localStorage.getItem(GUARDIANS_KEY), null);
   assert.equal(localStorage.getItem(WILD_KEY), null);
   assert.equal(localStorage.getItem(SELECTED_EXHIBITS_KEY), '["Africa Savanna"]');
});

test('detects stale stored itinerary dates', () => {
   const today = new Date();
   const yesterday = new Date(today);
   yesterday.setDate(today.getDate() - 1);

   writeStoredItineraryDraft({ date: toLocalISODate(yesterday) });
   assert.equal(isStoredItineraryStale(), true);

   writeStoredItineraryDraft({ date: toLocalISODate(today) });
   assert.equal(isStoredItineraryStale(), false);
});
