import assert from 'node:assert/strict';
import { afterEach, beforeEach, test } from 'node:test';

import { createRegionSelectorState } from '../../scripts/itinerary/selectors/regionSelector/state.js';
import { StorageKeys } from '../../scripts/itinerary/storageKeys.js';
import { DraftStorage } from '../../scripts/itinerary/draftStorage.js';
import { createLocalStorageMock } from './helpers/localStorageMock.mjs';
import { createFetchMock } from './helpers/fetchMock.mjs';

beforeEach(() => {
   globalThis.localStorage = createLocalStorageMock();
});

afterEach(() => {
   delete globalThis.localStorage;
   delete globalThis.fetch;
});

test('getAnimalsByExhibit receives month and day from stored visit date', async () => {
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

   const state = createRegionSelectorState();
   state.setRegions([{ name: 'R1', exhibits: ['E1'] }]);
   assert.equal(state.toggleRegion('R1'), true);

   await state.buildUpdatedAnimalsFromSelection();
});

test('getAnimalsByExhibit falls back to today when no visit date is stored', async () => {
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

   const state = createRegionSelectorState();
   state.setRegions([{ name: 'R1', exhibits: ['E1'] }]);
   assert.equal(state.toggleRegion('R1'), true);

   await state.buildUpdatedAnimalsFromSelection();
});

test('buildUpdatedAnimalsFromSelection keeps remaining animals after incomplete exhibit deselect', async () => {
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

   const state = createRegionSelectorState();
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

test('hydrateSelectionsFromStorage deselects exhibits missing catalog animals', async () => {
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

   const state = createRegionSelectorState();
   state.setRegions([{ name: 'Africa', exhibits: ['Africa Savanna'] }]);
   await state.hydrateSelectionsFromStorage();

   assert.deepEqual([...state.getSelectedExhibitNamesSet()], []);
   assert.deepEqual(
      JSON.parse(localStorage.getItem(StorageKeys.SELECTED_EXHIBITS_KEY)),
      []
   );
});

test('hydrateSelectionsFromStorage keeps exhibits when catalog grows for a new date', async () => {
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

   const state = createRegionSelectorState();
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

test('re-selecting an exhibit re-hydrates previously removed animals', async () => {
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

   const state = createRegionSelectorState();
   state.setRegions([{ name: 'Africa', exhibits: ['Africa Savanna'] }]);
   await state.hydrateSelectionsFromStorage();

   assert.deepEqual([...state.getSelectedExhibitNamesSet()], []);
   assert.equal(state.toggleExhibit('Africa', 'Africa Savanna'), true);

   const animals = await state.buildUpdatedAnimalsFromSelection();
   const species = animals.map((animal) => animal.species).sort();

   assert.deepEqual(species, ['African Lion', 'African Penguin']);
});

test('deselecting a bulk exhibit removes its animals from the draft', async () => {
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

   const state = createRegionSelectorState();
   state.setRegions([{ name: 'Africa', exhibits: ['Africa Savanna'] }]);
   await state.hydrateSelectionsFromStorage();
   assert.equal(state.toggleExhibit('Africa', 'Africa Savanna'), true);

   const animals = await state.buildUpdatedAnimalsFromSelection();

   assert.deepEqual(animals, []);
   assert.deepEqual(JSON.parse(localStorage.getItem(StorageKeys.ANIMALS_KEY)), []);
});

test('deselecting a bulk exhibit keeps manually added animals from other exhibits', async () => {
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

   const state = createRegionSelectorState();
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
