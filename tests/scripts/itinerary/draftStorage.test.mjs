import assert from 'node:assert/strict';
import { afterEach, beforeEach, test } from 'node:test';

import { StorageKeys } from '../../../scripts/itinerary/storageKeys.js';
import { DraftStorage } from '../../../scripts/itinerary/draftStorage.js';
import { createLocalStorageMock } from '../helpers/localStorageMock.mjs';

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

test('Test_SafeParseJSON_TestMalformed_ExpectFallback', () => {
   assert.deepEqual(DraftStorage.safeParseJSON('{"name":"Zootique"}', {}), { name: 'Zootique' });
   assert.deepEqual(DraftStorage.safeParseJSON('{bad json', []), []);
});

test('Test_WriteAndLoadStoredItineraryDraft_TestRoundTrip_ExpectPersisted', () => {
   DraftStorage.writeStoredItineraryDraft({
      date: '2026-06-15',
      animals: [{ species: 'African Lion' }],
      attractions: [{ name: 'Conservation Carousel' }],
      guardiansTalks: [{ name: 'Amur Tiger' }],
      wildEncounters: [{ name: 'African Rainforest' }],
   });

   assert.equal(localStorage.getItem(StorageKeys.DATE_KEY), '2026-06-15');
   assert.deepEqual(JSON.parse(localStorage.getItem(StorageKeys.ANIMALS_KEY)), [{ species: 'African Lion' }]);
   assert.deepEqual(DraftStorage.loadStoredItineraryDraft(), {
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

test('Test_ClearItineraryDraftStorage_TestOptionalSelections_ExpectCleared', () => {
   DraftStorage.writeStoredItineraryDraft({
      date: '2026-06-15',
      animals: [{ species: 'African Lion' }],
   });
   localStorage.setItem(StorageKeys.SELECTED_EXHIBITS_KEY, JSON.stringify(['Africa Savanna']));

   DraftStorage.clearItineraryDraftStorage({ includeSelections: false });

   assert.equal(localStorage.getItem(StorageKeys.DATE_KEY), null);
   assert.equal(localStorage.getItem(StorageKeys.ANIMALS_KEY), null);
   assert.equal(localStorage.getItem(StorageKeys.ATTRACTIONS_KEY), null);
   assert.equal(localStorage.getItem(StorageKeys.GUARDIANS_KEY), null);
   assert.equal(localStorage.getItem(StorageKeys.WILD_KEY), null);
   assert.equal(localStorage.getItem(StorageKeys.TRANSPORTATIONS_KEY), null);
   assert.equal(localStorage.getItem(StorageKeys.SELECTED_EXHIBITS_KEY), '["Africa Savanna"]');
});

test('Test_IsStoredItineraryStale_TestPastDate_ExpectDetected', () => {
   const today = new Date();
   const yesterday = new Date(today);
   yesterday.setDate(today.getDate() - 1);

   DraftStorage.writeStoredItineraryDraft({ date: toLocalISODate(yesterday) });
   assert.equal(DraftStorage.isStoredItineraryStale(), true);

   DraftStorage.writeStoredItineraryDraft({ date: toLocalISODate(today) });
   assert.equal(DraftStorage.isStoredItineraryStale(), false);
});

test('Test_SyncItineraryAnimalDraftFromItinerary_TestAnimalsOnly_ExpectNoInventedExhibits', () => {
   DraftStorage.syncItineraryAnimalDraftFromItinerary({
      animals: [
         { species: 'African Lion', exhibit: 'Africa Savanna' },
         { species: 'Amur Tiger', exhibit: 'Eurasia Wilds' },
      ],
   });

   const storedAnimals = JSON.parse(localStorage.getItem(StorageKeys.ANIMALS_KEY));

   assert.equal(storedAnimals.length, 2);
   assert.equal(localStorage.getItem(StorageKeys.SELECTED_EXHIBITS_KEY), null);
});

test('Test_SyncItineraryAnimalDraftFromItinerary_TestExistingExhibits_ExpectPreserved', () => {
   localStorage.setItem(
      StorageKeys.SELECTED_EXHIBITS_KEY,
      JSON.stringify(['Africa Savanna'])
   );

   DraftStorage.syncItineraryAnimalDraftFromItinerary({
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

test('Test_RemoveAnimalFromItineraryAnimalDraft_TestRemainingAnimals_ExpectExhibitKept', () => {
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

   DraftStorage.removeAnimalFromItineraryAnimalDraft(
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

test('Test_RemoveAnimalFromItineraryAnimalDraft_TestLastAnimal_ExpectExhibitDropped', () => {
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

   DraftStorage.removeAnimalFromItineraryAnimalDraft(
      'animals',
      'African Penguin||Africa Savanna'
   );

   assert.deepEqual(JSON.parse(localStorage.getItem(StorageKeys.ANIMALS_KEY)), []);
   assert.deepEqual(JSON.parse(localStorage.getItem(StorageKeys.SELECTED_EXHIBITS_KEY)), []);
});

test('Test_RemoveAnimalFromItineraryAnimalDraft_TestNonAnimal_ExpectIgnored', () => {
   localStorage.setItem(
      StorageKeys.ANIMALS_KEY,
      JSON.stringify([{ species: 'African Lion', exhibit: 'Africa Savanna' }])
   );

   DraftStorage.removeAnimalFromItineraryAnimalDraft('events', 'Lunch||');
   DraftStorage.removeAnimalFromItineraryAnimalDraft('animals', '');

   assert.equal(JSON.parse(localStorage.getItem(StorageKeys.ANIMALS_KEY)).length, 1);
});

test('Test_SyncItineraryAnimalDraftFromItinerary_TestRemovedKeys_ExpectCleared', () => {
   localStorage.setItem(
      StorageKeys.REMOVED_ANIMALS_KEY,
      JSON.stringify(['african penguin||africa savanna'])
   );

   DraftStorage.syncItineraryAnimalDraftFromItinerary({
      animals: [{ species: 'African Lion', exhibit: 'Africa Savanna' }],
   });

   assert.deepEqual(JSON.parse(localStorage.getItem(StorageKeys.REMOVED_ANIMALS_KEY)), []);
});
