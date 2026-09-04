import assert from 'node:assert/strict';
import { afterEach, beforeEach, test } from 'node:test';

import { StorageKeys } from '../../scripts/itinerary/storageKeys.js';
import {
   clearItineraryDraftStorage,
   isStoredItineraryStale,
   loadStoredItineraryDraft,
   removeAnimalFromItineraryAnimalDraft,
   safeParseJSON,
   syncItineraryAnimalDraftFromItinerary,
   writeStoredItineraryDraft,
} from '../../scripts/itinerary/draftStorage.js';
import { createLocalStorageMock } from './helpers/localStorageMock.mjs';

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

   assert.equal(localStorage.getItem(StorageKeys.DATE_KEY), '2026-06-15');
   assert.deepEqual(JSON.parse(localStorage.getItem(StorageKeys.ANIMALS_KEY)), [{ species: 'African Lion' }]);
   assert.deepEqual(loadStoredItineraryDraft(), {
      date: '2026-06-15',
      arrivalTime: '',
      departureTime: '',
      animals: [{ species: 'African Lion' }],
      attractions: [{ name: 'Conservation Carousel' }],
      guardiansTalks: [{ name: 'Amur Tiger' }],
      wildEncounters: [{ name: 'African Rainforest' }],
      transportations: [],
      transportationStations: [],
      events: [],
   });
});

test('clears draft storage while optionally preserving selection storage', () => {
   writeStoredItineraryDraft({
      date: '2026-06-15',
      animals: [{ species: 'African Lion' }],
   });
   localStorage.setItem(StorageKeys.SELECTED_EXHIBITS_KEY, JSON.stringify(['Africa Savanna']));

   clearItineraryDraftStorage({ includeSelections: false });

   assert.equal(localStorage.getItem(StorageKeys.DATE_KEY), null);
   assert.equal(localStorage.getItem(StorageKeys.ANIMALS_KEY), null);
   assert.equal(localStorage.getItem(StorageKeys.ATTRACTIONS_KEY), null);
   assert.equal(localStorage.getItem(StorageKeys.GUARDIANS_KEY), null);
   assert.equal(localStorage.getItem(StorageKeys.WILD_KEY), null);
   assert.equal(localStorage.getItem(StorageKeys.TRANSPORTATIONS_KEY), null);
   assert.equal(localStorage.getItem(StorageKeys.SELECTED_EXHIBITS_KEY), '["Africa Savanna"]');
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

test('syncItineraryAnimalDraftFromItinerary mirrors animals without inventing exhibit selection', () => {
   syncItineraryAnimalDraftFromItinerary({
      animals: [
         { species: 'African Lion', exhibit: 'Africa Savanna' },
         { species: 'Amur Tiger', exhibit: 'Eurasia Wilds' },
      ],
   });

   const storedAnimals = JSON.parse(localStorage.getItem(StorageKeys.ANIMALS_KEY));

   assert.equal(storedAnimals.length, 2);
   assert.equal(localStorage.getItem(StorageKeys.SELECTED_EXHIBITS_KEY), null);
});

test('syncItineraryAnimalDraftFromItinerary preserves existing exhibit selection', () => {
   localStorage.setItem(
      StorageKeys.SELECTED_EXHIBITS_KEY,
      JSON.stringify(['Africa Savanna'])
   );

   syncItineraryAnimalDraftFromItinerary({
      animals: [
         { species: 'African Lion', exhibit: 'Africa Savanna' },
         { species: 'Cheetah', exhibit: 'Africa Savanna' },
      ],
   });

   assert.deepEqual(
      JSON.parse(localStorage.getItem(StorageKeys.SELECTED_EXHIBITS_KEY)),
      ['Africa Savanna']
   );
});

test('removeAnimalFromItineraryAnimalDraft keeps exhibit selection while animals remain', () => {
   localStorage.setItem(
      StorageKeys.ANIMALS_KEY,
      JSON.stringify([
         { species: 'African Lion', exhibit: 'Africa Savanna' },
         { species: 'Watusi Cattle', exhibit: 'Africa Savanna' },
      ])
   );
   localStorage.setItem(
      StorageKeys.SELECTED_EXHIBITS_KEY,
      JSON.stringify(['Africa Savanna'])
   );

   removeAnimalFromItineraryAnimalDraft(
      'animals',
      'Watusi Cattle||Africa Savanna'
   );

   assert.deepEqual(
      JSON.parse(localStorage.getItem(StorageKeys.ANIMALS_KEY)).map((animal) => ({
         species: animal.species,
         exhibit: animal.exhibit,
      })),
      [{ species: 'African Lion', exhibit: 'Africa Savanna' }]
   );
   // Incomplete coverage is evaluated when the region builder opens.
   assert.deepEqual(
      JSON.parse(localStorage.getItem(StorageKeys.SELECTED_EXHIBITS_KEY)),
      ['Africa Savanna']
   );
});

test('removeAnimalFromItineraryAnimalDraft drops animal and exhibit when empty', () => {
   localStorage.setItem(
      StorageKeys.ANIMALS_KEY,
      JSON.stringify([
         { species: 'African Penguin', exhibit: 'Africa Savanna' },
      ])
   );
   localStorage.setItem(
      StorageKeys.SELECTED_EXHIBITS_KEY,
      JSON.stringify(['Africa Savanna'])
   );

   removeAnimalFromItineraryAnimalDraft(
      'animals',
      'African Penguin||Africa Savanna'
   );

   assert.deepEqual(JSON.parse(localStorage.getItem(StorageKeys.ANIMALS_KEY)), []);
   assert.deepEqual(JSON.parse(localStorage.getItem(StorageKeys.SELECTED_EXHIBITS_KEY)), []);
});

test('removeAnimalFromItineraryAnimalDraft ignores non-animal item types', () => {
   localStorage.setItem(
      StorageKeys.ANIMALS_KEY,
      JSON.stringify([{ species: 'African Lion', exhibit: 'Africa Savanna' }])
   );

   removeAnimalFromItineraryAnimalDraft('events', 'Lunch||');
   removeAnimalFromItineraryAnimalDraft('animals', '');

   assert.equal(JSON.parse(localStorage.getItem(StorageKeys.ANIMALS_KEY)).length, 1);
});

test('syncItineraryAnimalDraftFromItinerary clears removed animal keys', () => {
   localStorage.setItem(
      StorageKeys.REMOVED_ANIMALS_KEY,
      JSON.stringify(['african penguin||africa savanna'])
   );

   syncItineraryAnimalDraftFromItinerary({
      animals: [{ species: 'African Lion', exhibit: 'Africa Savanna' }],
   });

   assert.deepEqual(JSON.parse(localStorage.getItem(StorageKeys.REMOVED_ANIMALS_KEY)), []);
});
