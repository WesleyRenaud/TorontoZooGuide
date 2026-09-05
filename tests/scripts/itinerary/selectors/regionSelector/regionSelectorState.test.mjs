import assert from 'node:assert/strict';
import { afterEach, beforeEach, test } from 'node:test';

import { State } from '../../../../../scripts/itinerary/selectors/regionSelector/state.js';
import { StorageKeys } from '../../../../../scripts/itinerary/storageKeys.js';
import { DraftStorage } from '../../../../../scripts/itinerary/draftStorage.js';
import { createLocalStorageMock } from '../../../helpers/localStorageMock.mjs';
import { createFetchMock } from '../../../helpers/fetchMock.mjs';

beforeEach(() => {
   globalThis.localStorage = createLocalStorageMock();
});

afterEach(() => {
   delete globalThis.localStorage;
   delete globalThis.fetch;
});

test('Test_GetAnimalsByExhibit_TestGetAnimalsByExhibitReceivesMonthAndDayFromStoredVisit_ExpectOk', async () => {
   localStorage.setItem(StorageKeys.DATE_KEY, '2026-08-12');

   globalThis.fetch = createFetchMock({
      '/get-animals-by-exhibit': (_url, options) => {
         const body = JSON.parse(options.body);
         assert.equal(body.month, 'AUG');
         assert.equal(body.day, 12);
         assert.equal(body.forItinerary, true);
         assert.ok(Array.isArray(body.exhibitsToInclude));

         return { animals: [] };
      },
   });

   const state = State.createRegionSelectorState();
   state.setRegions([{ name: 'R1', exhibits: ['E1'] }]);
   assert.equal(state.toggleRegion('R1'), true);

   await state.buildUpdatedAnimalsFromSelection();
});

test('Test_GetAnimalsByExhibit_TestGetAnimalsByExhibitFallsBackToTodayWhenNoVisit_ExpectOk', async () => {
   globalThis.fetch = async (url, options) => {
      assert.equal(url, '/get-animals-by-exhibit');
      const body = JSON.parse(options.body);
      assert.equal(typeof body.month, 'string');
      assert.equal(typeof body.day, 'number');
      assert.ok(body.month.length >= 3);
      assert.ok(body.day >= 1 && body.day <= 31);

      return {
         ok: true,
         status: 200,
         statusText: 'OK',
         text: async () => '{"animals":[]}',
      };
   };

   const state = State.createRegionSelectorState();
   state.setRegions([{ name: 'R1', exhibits: ['E1'] }]);
   assert.equal(state.toggleRegion('R1'), true);

   await state.buildUpdatedAnimalsFromSelection();
});

test('Test_BuildUpdatedAnimalsFromSelection_TestBuildUpdatedAnimalsFromSelectionKeepsRemainingAnimalsAfterIncompleteExhibitDeselect_ExpectOk', async () => {
   localStorage.setItem(
      StorageKeys.ANIMALS_KEY,
      JSON.stringify([
         {
            species: 'African Lion',
            exhibit: 'Africa Savanna',
         },
         {
            species: 'African Penguin',
            exhibit: 'Africa Savanna',
         },
      ])
   );
   localStorage.setItem(
      StorageKeys.SELECTED_EXHIBITS_KEY,
      JSON.stringify(['Africa Savanna'])
   );

   globalThis.fetch = async () => ({
      ok: true,
      status: 200,
      statusText: 'OK',
      text: async () => JSON.stringify({
         animals: [
            {
               species: 'African Lion',
               exhibit: 'Africa Savanna',
            },
            {
               species: 'African Penguin',
               exhibit: 'Africa Savanna',
            },
            {
               species: 'Masai Giraffe',
               exhibit: 'Africa Savanna',
            },
         ],
      }),
   });

   DraftStorage.removeAnimalFromItineraryAnimalDraft(
      'animals',
      'African Penguin||Africa Savanna'
   );

   const state = State.createRegionSelectorState();
   state.setRegions([{ name: 'Africa', exhibits: ['Africa Savanna'] }]);
   await state.hydrateSelectionsFromStorage();

   assert.deepEqual(
      [...state.getSelectedExhibitNamesSet()],
      []
   );

   const animals = await state.buildUpdatedAnimalsFromSelection();
   const species = animals.map((animal) => animal.species).sort();

   assert.deepEqual(species, ['African Lion']);
});

test('Test_HydrateSelectionsFromStorage_TestHydrateSelectionsFromStorageDeselectsExhibitsMissingCatalogAnimals_ExpectOk', async () => {
   localStorage.setItem(
      StorageKeys.ANIMALS_KEY,
      JSON.stringify([
         { species: 'African Lion', exhibit: 'Africa Savanna' },
      ])
   );
   localStorage.setItem(
      StorageKeys.SELECTED_EXHIBITS_KEY,
      JSON.stringify(['Africa Savanna'])
   );

   globalThis.fetch = async () => ({
      ok: true,
      status: 200,
      statusText: 'OK',
      text: async () => JSON.stringify({
         animals: [
            { species: 'African Lion', exhibit: 'Africa Savanna' },
            { species: 'Watusi Cattle', exhibit: 'Africa Savanna' },
         ],
      }),
   });

   DraftStorage.removeAnimalFromItineraryAnimalDraft(
      'animals',
      'Watusi Cattle||Africa Savanna'
   );

   const state = State.createRegionSelectorState();
   state.setRegions([{ name: 'Africa', exhibits: ['Africa Savanna'] }]);
   await state.hydrateSelectionsFromStorage();

   assert.deepEqual([...state.getSelectedExhibitNamesSet()], []);
   assert.deepEqual(
      JSON.parse(localStorage.getItem(StorageKeys.SELECTED_EXHIBITS_KEY)),
      []
   );
});

test('Test_HydrateSelectionsFromStorage_TestHydrateSelectionsFromStorageKeepsExhibitsWhenCatalogGrowsForA_ExpectOk', async () => {
   localStorage.setItem(StorageKeys.DATE_KEY, '2026-10-17');
   localStorage.setItem(
      StorageKeys.ANIMALS_KEY,
      JSON.stringify([
         { species: 'African Lion', exhibit: 'Africa Savanna' },
      ])
   );
   localStorage.setItem(
      StorageKeys.SELECTED_EXHIBITS_KEY,
      JSON.stringify(['Africa Savanna'])
   );

   globalThis.fetch = async () => ({
      ok: true,
      status: 200,
      statusText: 'OK',
      text: async () => JSON.stringify({
         animals: [
            { species: 'African Lion', exhibit: 'Africa Savanna' },
            { species: 'Watusi Cattle', exhibit: 'Africa Savanna' },
         ],
      }),
   });

   const state = State.createRegionSelectorState();
   state.setRegions([{ name: 'Africa', exhibits: ['Africa Savanna'] }]);
   await state.hydrateSelectionsFromStorage();

   assert.deepEqual(
      [...state.getSelectedExhibitNamesSet()],
      ['Africa Savanna']
   );
   assert.equal(state.selectedExhibitsNeedCatalogRebuild(), true);
   assert.deepEqual(
      JSON.parse(localStorage.getItem(StorageKeys.SELECTED_EXHIBITS_KEY)),
      ['Africa Savanna']
   );

   const animals = await state.buildUpdatedAnimalsFromSelection();

   assert.deepEqual(
      animals.map((animal) => animal.species).sort(),
      ['African Lion', 'Watusi Cattle']
   );
   assert.equal(state.selectedExhibitsNeedCatalogRebuild(), false);
});

test('Test_Re_TestReSelectingAnExhibitReHydratesPreviouslyRemoved_ExpectOk', async () => {
   localStorage.setItem(
      StorageKeys.ANIMALS_KEY,
      JSON.stringify([
         { species: 'African Lion', exhibit: 'Africa Savanna' },
      ])
   );
   localStorage.setItem(
      StorageKeys.SELECTED_EXHIBITS_KEY,
      JSON.stringify(['Africa Savanna'])
   );

   globalThis.fetch = async () => ({
      ok: true,
      status: 200,
      statusText: 'OK',
      text: async () => JSON.stringify({
         animals: [
            { species: 'African Lion', exhibit: 'Africa Savanna' },
            { species: 'African Penguin', exhibit: 'Africa Savanna' },
         ],
      }),
   });

   DraftStorage.removeAnimalFromItineraryAnimalDraft(
      'animals',
      'African Penguin||Africa Savanna'
   );

   const state = State.createRegionSelectorState();
   state.setRegions([{ name: 'Africa', exhibits: ['Africa Savanna'] }]);
   await state.hydrateSelectionsFromStorage();

   assert.deepEqual([...state.getSelectedExhibitNamesSet()], []);
   assert.equal(state.toggleExhibit('Africa', 'Africa Savanna'), true);

   const animals = await state.buildUpdatedAnimalsFromSelection();
   const species = animals.map((animal) => animal.species).sort();

   assert.deepEqual(species, ['African Lion', 'African Penguin']);
});

test('Test_Deselecting_TestDeselectingABulkExhibitRemovesItsAnimalsFrom_ExpectOk', async () => {
   localStorage.setItem(
      StorageKeys.ANIMALS_KEY,
      JSON.stringify([
         { species: 'African Lion', exhibit: 'Africa Savanna' },
         { species: 'African Penguin', exhibit: 'Africa Savanna' },
      ])
   );
   localStorage.setItem(
      StorageKeys.SELECTED_EXHIBITS_KEY,
      JSON.stringify(['Africa Savanna'])
   );

   globalThis.fetch = async () => ({
      ok: true,
      status: 200,
      statusText: 'OK',
      text: async () => JSON.stringify({ animals: [] }),
   });

   const state = State.createRegionSelectorState();
   state.setRegions([{ name: 'Africa', exhibits: ['Africa Savanna'] }]);
   await state.hydrateSelectionsFromStorage();
   assert.equal(state.toggleExhibit('Africa', 'Africa Savanna'), true);

   const animals = await state.buildUpdatedAnimalsFromSelection();

   assert.deepEqual(animals, []);
   assert.deepEqual(JSON.parse(localStorage.getItem(StorageKeys.ANIMALS_KEY)), []);
});

test('Test_Deselecting_TestDeselectingABulkExhibitKeepsManuallyAddedAnimals_ExpectOk', async () => {
   localStorage.setItem(
      StorageKeys.ANIMALS_KEY,
      JSON.stringify([
         { species: 'African Lion', exhibit: 'Africa Savanna' },
         { species: 'Red Panda', exhibit: 'Indo-Malaya' },
      ])
   );
   localStorage.setItem(
      StorageKeys.SELECTED_EXHIBITS_KEY,
      JSON.stringify(['Africa Savanna'])
   );

   globalThis.fetch = async () => ({
      ok: true,
      status: 200,
      statusText: 'OK',
      text: async () => JSON.stringify({
         animals: [
            { species: 'African Lion', exhibit: 'Africa Savanna' },
         ],
      }),
   });

   const state = State.createRegionSelectorState();
   state.setRegions([
      { name: 'Africa', exhibits: ['Africa Savanna'] },
      { name: 'Indo-Malaya', exhibits: ['Indo-Malaya'] },
   ]);
   await state.hydrateSelectionsFromStorage();
   assert.equal(state.toggleExhibit('Africa', 'Africa Savanna'), true);

   const animals = await state.buildUpdatedAnimalsFromSelection();
   const species = animals.map((animal) => animal.species);

   assert.deepEqual(species, ['Red Panda']);
});
