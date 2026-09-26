import assert from 'node:assert/strict';
import { afterEach, beforeEach, test } from 'node:test';

import { StorageKeys } from '../../../scripts/itinerary/storageKeys.js';
import { DraftStore } from '../../../scripts/itinerary/draftStore.js';
import { ScheduleItemKeySeparator } from '../../../scripts/itinerary/scheduleItemKeySeparator.js';
import { Position } from '../../../scripts/shared/enums/position.js';
import { createLocalStorageMock } from '../helpers/localStorageMock.mjs';

function _toLocalISODate(date) {
   const year = date.getFullYear();
   const month = String(date.getMonth() + 1).padStart(2, '0');
   const day = String(date.getDate()).padStart(2, '0');
   return `${year}-${month}-${day}`;
}

beforeEach(() => {
   globalThis.localStorage = createLocalStorageMock();
});

afterEach(() => {
   delete globalThis.localStorage;
});


test('Test_SafeParseJSON_TestValidJson_ExpectParsed', () => {
   const name = 'Zootique';
   const raw = JSON.stringify({ name });

   const parsed = DraftStore.safeParseJSON(raw, {});

   assert.equal(parsed.name, name);
});


test('Test_SafeParseJSON_TestMalformed_ExpectFallback', () => {
   const fallback = [];

   const parsed = DraftStore.safeParseJSON('{bad json', fallback);

   assert.equal(parsed, fallback);
});


test('Test_WriteAndLoadStoredItineraryDraft_TestRoundTrip_ExpectPersisted', () => {
   const date = '2026-06-15';
   const animals = [{ species: 'African Lion' }];
   const attractions = [{ name: 'Conservation Carousel' }];
   const guardiansTalks = [{ name: 'Amur Tiger' }];
   const wildEncounters = [{ name: 'African Rainforest' }];
   const draft = {
      date,
      animals,
      attractions,
      guardiansTalks,
      wildEncounters,
   };

   DraftStore.writeStoredItineraryDraft(draft);
   const loaded = DraftStore.loadStoredItineraryDraft();

   assert.equal(localStorage.getItem(StorageKeys.DATE_KEY), date);
   assert.deepEqual(JSON.parse(localStorage.getItem(StorageKeys.ANIMALS_KEY)), animals);
   assert.equal(loaded.date, date);
   assert.deepEqual(loaded.animals, animals);
   assert.deepEqual(loaded.attractions, attractions);
   assert.deepEqual(loaded.guardiansTalks, guardiansTalks);
   assert.deepEqual(loaded.wildEncounters, wildEncounters);
});


test('Test_ClearItineraryDraftStorage_TestOptionalSelections_ExpectCleared', () => {
   const date = '2026-06-15';
   const africaSavanna = 'Africa Savanna';
   DraftStore.writeStoredItineraryDraft({
      date,
      animals: [{ species: 'African Lion' }],
   });
   localStorage.setItem(StorageKeys.SELECTED_EXHIBITS_KEY, JSON.stringify([africaSavanna]));

   DraftStore.clearItineraryDraftStorage({ includeSelections: false });

   assert.equal(localStorage.getItem(StorageKeys.DATE_KEY), null);
   assert.equal(localStorage.getItem(StorageKeys.ANIMALS_KEY), null);
   assert.equal(localStorage.getItem(StorageKeys.ATTRACTIONS_KEY), null);
   assert.equal(localStorage.getItem(StorageKeys.GUARDIANS_KEY), null);
   assert.equal(localStorage.getItem(StorageKeys.WILD_KEY), null);
   assert.equal(localStorage.getItem(StorageKeys.TRANSPORTATIONS_KEY), null);
   assert.equal(localStorage.getItem(StorageKeys.SELECTED_EXHIBITS_KEY), JSON.stringify([africaSavanna]));
});


test('Test_IsStoredItineraryStale_TestPastDate_ExpectDetected', () => {
   const today = new Date();
   const yesterday = new Date(today);
   yesterday.setDate(today.getDate() - 1);
   DraftStore.writeStoredItineraryDraft({ date: _toLocalISODate(yesterday) });

   const isStale = DraftStore.isStoredItineraryStale();

   assert.equal(isStale, true);
});


test('Test_IsStoredItineraryStale_TestToday_ExpectFalse', () => {
   const today = new Date();
   DraftStore.writeStoredItineraryDraft({ date: _toLocalISODate(today) });

   const isStale = DraftStore.isStoredItineraryStale();

   assert.equal(isStale, false);
});


test('Test_SyncItineraryAnimalDraftFromItinerary_TestAnimalsOnly_ExpectNoInventedExhibits', () => {
   const animals = [
      { species: 'African Lion', exhibit: 'Africa Savanna' },
      { species: 'Amur Tiger', exhibit: 'Eurasia Wilds' },
   ];

   DraftStore.syncItineraryAnimalDraftFromItinerary({ animals });

   const storedAnimals = JSON.parse(localStorage.getItem(StorageKeys.ANIMALS_KEY));
   assert.equal(storedAnimals.length, animals.length);
   assert.equal(localStorage.getItem(StorageKeys.SELECTED_EXHIBITS_KEY), null);
});


test('Test_SyncItineraryAnimalDraftFromItinerary_TestExistingExhibits_ExpectPreserved', () => {
   const africaSavanna = 'Africa Savanna';
   localStorage.setItem(
      StorageKeys.SELECTED_EXHIBITS_KEY,
      JSON.stringify([africaSavanna])
   );

   DraftStore.syncItineraryAnimalDraftFromItinerary({
      animals: [
         { species: 'African Lion', exhibit: africaSavanna },
         { species: 'Cheetah', exhibit: africaSavanna },
      ],
   });

   const selectedExhibits = JSON.parse(localStorage.getItem(StorageKeys.SELECTED_EXHIBITS_KEY));
   assert.deepEqual(selectedExhibits, [africaSavanna]);
});


test('Test_RemoveAnimalFromItineraryAnimalDraft_TestRemainingAnimals_ExpectExhibitKept', () => {
   const africaSavanna = 'Africa Savanna';
   const africanLion = { species: 'African Lion', exhibit: africaSavanna };
   const watusiCattle = { species: 'Watusi Cattle', exhibit: africaSavanna };
   localStorage.setItem(
      StorageKeys.ANIMALS_KEY,
      JSON.stringify([africanLion, watusiCattle])
   );
   localStorage.setItem(
      StorageKeys.SELECTED_EXHIBITS_KEY,
      JSON.stringify([africaSavanna])
   );

   DraftStore.removeAnimalFromItineraryAnimalDraft(
      'animals',
      [watusiCattle.species, africaSavanna].join(ScheduleItemKeySeparator.VALUE)
   );

   const storedAnimals = JSON.parse(localStorage.getItem(StorageKeys.ANIMALS_KEY)).map((animal) => ({
      species: animal.species,
      exhibit: animal.exhibit,
   }));
   const selectedExhibits = JSON.parse(localStorage.getItem(StorageKeys.SELECTED_EXHIBITS_KEY));
   assert.deepEqual(storedAnimals, [africanLion]);
   assert.deepEqual(selectedExhibits, [africaSavanna]);
});


test('Test_RemoveAnimalFromItineraryAnimalDraft_TestLastAnimal_ExpectExhibitDropped', () => {
   const africaSavanna = 'Africa Savanna';
   const africanPenguin = { species: 'African Penguin', exhibit: africaSavanna };
   localStorage.setItem(
      StorageKeys.ANIMALS_KEY,
      JSON.stringify([africanPenguin])
   );
   localStorage.setItem(
      StorageKeys.SELECTED_EXHIBITS_KEY,
      JSON.stringify([africaSavanna])
   );

   DraftStore.removeAnimalFromItineraryAnimalDraft(
      'animals',
      [africanPenguin.species, africaSavanna].join(ScheduleItemKeySeparator.VALUE)
   );

   const storedAnimals = JSON.parse(localStorage.getItem(StorageKeys.ANIMALS_KEY));
   const selectedExhibits = JSON.parse(localStorage.getItem(StorageKeys.SELECTED_EXHIBITS_KEY));
   assert.deepEqual(storedAnimals, []);
   assert.deepEqual(selectedExhibits, []);
});


test('Test_RemoveAnimalFromItineraryAnimalDraft_TestNonAnimalKind_ExpectIgnored', () => {
   const animals = [{ species: 'African Lion', exhibit: 'Africa Savanna' }];
   localStorage.setItem(StorageKeys.ANIMALS_KEY, JSON.stringify(animals));

   DraftStore.removeAnimalFromItineraryAnimalDraft(
      'events',
      `Lunch${ScheduleItemKeySeparator.VALUE}`
   );

   const storedAnimals = JSON.parse(localStorage.getItem(StorageKeys.ANIMALS_KEY));
   assert.equal(storedAnimals.length, animals.length);
});


test('Test_RemoveAnimalFromItineraryAnimalDraft_TestEmptyKey_ExpectIgnored', () => {
   const animals = [{ species: 'African Lion', exhibit: 'Africa Savanna' }];
   localStorage.setItem(StorageKeys.ANIMALS_KEY, JSON.stringify(animals));

   DraftStore.removeAnimalFromItineraryAnimalDraft('animals', '');

   const storedAnimals = JSON.parse(localStorage.getItem(StorageKeys.ANIMALS_KEY));
   assert.equal(storedAnimals.length, animals.length);
});


test('Test_SyncItineraryAnimalDraftFromItinerary_TestRemovedKeys_ExpectCleared', () => {
   const penguin = { species: 'African Penguin', exhibit: 'Africa Savanna' };
   localStorage.setItem(
      StorageKeys.REMOVED_ANIMALS_KEY,
      JSON.stringify([
         [penguin.species.toLowerCase(), penguin.exhibit.toLowerCase()]
            .join(ScheduleItemKeySeparator.VALUE),
      ])
   );

   DraftStore.syncItineraryAnimalDraftFromItinerary({
      animals: [{ species: 'African Lion', exhibit: 'Africa Savanna' }],
   });

   const removedAnimals = JSON.parse(localStorage.getItem(StorageKeys.REMOVED_ANIMALS_KEY));
   assert.deepEqual(removedAnimals, []);
});


test('Test_SetStoredItineraryDate_TestDate_ExpectPersisted', () => {
   const date = '2026-06-15';

   DraftStore.setStoredItineraryDate(date);

   assert.equal(localStorage.getItem(StorageKeys.DATE_KEY), date);
});


test('Test_SetStoredItineraryDate_TestEmpty_ExpectRemoved', () => {
   const date = '2026-06-15';
   DraftStore.setStoredItineraryDate(date);

   DraftStore.setStoredItineraryDate('');

   assert.equal(localStorage.getItem(StorageKeys.DATE_KEY), null);
});


test('Test_NormalizeDateToLocalMidnight_TestInvalid_ExpectNull', () => {
   const dateValue = 'not-a-date';

   const normalized = DraftStore.normalizeDateToLocalMidnight(dateValue);

   assert.equal(normalized, null);
});


test('Test_ClearItinerarySelectionStorage_TestKeys_ExpectCleared', () => {
   const africa = 'Africa';
   const date = '2026-06-15';
   localStorage.setItem(StorageKeys.SELECTED_EXHIBITS_KEY, JSON.stringify([africa]));
   localStorage.setItem(StorageKeys.SELECTED_REGIONS_KEY, JSON.stringify([africa]));
   localStorage.setItem(StorageKeys.REMOVED_ANIMALS_KEY, JSON.stringify(['lion']));
   localStorage.setItem(StorageKeys.DATE_KEY, date);

   DraftStore.clearItinerarySelectionStorage();

   assert.equal(localStorage.getItem(StorageKeys.SELECTED_EXHIBITS_KEY), null);
   assert.equal(localStorage.getItem(StorageKeys.SELECTED_REGIONS_KEY), null);
   assert.equal(localStorage.getItem(StorageKeys.REMOVED_ANIMALS_KEY), null);
   assert.equal(localStorage.getItem(StorageKeys.DATE_KEY), date);
});


test('Test_RemoveAnimalFromItineraryAnimalDraft_TestUnparseableKey_ExpectIgnored', () => {
   const animals = [{ species: 'African Lion', exhibit: 'Africa Savanna' }];
   localStorage.setItem(StorageKeys.ANIMALS_KEY, JSON.stringify(animals));

   DraftStore.removeAnimalFromItineraryAnimalDraft(
      'animals',
      `${ScheduleItemKeySeparator.VALUE}${animals[Position.FIRST].exhibit}`
   );

   const storedAnimals = JSON.parse(localStorage.getItem(StorageKeys.ANIMALS_KEY));
   assert.equal(storedAnimals.length, animals.length);
});
