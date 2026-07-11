import assert from 'node:assert/strict';
import { afterEach, beforeEach, test } from 'node:test';

import { createRegionSelectorState } from '../../scripts/itinerary/selectors/regionSelector/state.js';
import { ANIMALS_KEY, DATE_KEY, SELECTED_EXHIBITS_KEY } from '../../scripts/itinerary/storageKeys.js';
import { removeAnimalFromItineraryAnimalDraft } from '../../scripts/itinerary/draftStorage.js';
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
   localStorage.setItem(DATE_KEY, '2026-08-12');

   globalThis.fetch = createFetchMock({
      '/get-animals-by-exhibit': (_url, options) => {
         const body = JSON.parse(options.body);
         assert.equal(body.month, 'AUG');
         assert.equal(body.day, 12);
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

test('buildUpdatedAnimalsFromSelection keeps removed animals out of exhibit refresh', async () => {
   localStorage.setItem(
      ANIMALS_KEY,
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
      SELECTED_EXHIBITS_KEY,
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

   removeAnimalFromItineraryAnimalDraft(
      'animals',
      'African Penguin||Africa Savanna'
   );

   const state = createRegionSelectorState();
   state.setRegions([{ name: 'Africa', exhibits: ['Africa Savanna'] }]);
   state.hydrateSelectionsFromStorage();

   const animals = await state.buildUpdatedAnimalsFromSelection();
   const species = animals.map((animal) => animal.species).sort();

   assert.deepEqual(species, ['African Lion', 'Masai Giraffe']);
});

test('re-selecting an exhibit re-hydrates previously removed animals', async () => {
   localStorage.setItem(
      ANIMALS_KEY,
      JSON.stringify([
         { species: 'African Lion', exhibit: 'Africa Savanna' },
      ])
   );
   localStorage.setItem(
      SELECTED_EXHIBITS_KEY,
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

   removeAnimalFromItineraryAnimalDraft(
      'animals',
      'African Penguin||Africa Savanna'
   );

   const state = createRegionSelectorState();
   state.setRegions([{ name: 'Africa', exhibits: ['Africa Savanna'] }]);
   state.hydrateSelectionsFromStorage();

   assert.equal(state.toggleExhibit('Africa', 'Africa Savanna'), true);
   assert.equal(state.toggleExhibit('Africa', 'Africa Savanna'), true);

   const animals = await state.buildUpdatedAnimalsFromSelection();
   const species = animals.map((animal) => animal.species).sort();

   assert.deepEqual(species, ['African Lion', 'African Penguin']);
});

test('deselecting a bulk exhibit removes its animals from the draft', async () => {
   localStorage.setItem(
      ANIMALS_KEY,
      JSON.stringify([
         { species: 'African Lion', exhibit: 'Africa Savanna' },
         { species: 'African Penguin', exhibit: 'Africa Savanna' },
      ])
   );
   localStorage.setItem(
      SELECTED_EXHIBITS_KEY,
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
   state.hydrateSelectionsFromStorage();
   assert.equal(state.toggleExhibit('Africa', 'Africa Savanna'), true);

   const animals = await state.buildUpdatedAnimalsFromSelection();

   assert.deepEqual(animals, []);
   assert.deepEqual(JSON.parse(localStorage.getItem(ANIMALS_KEY)), []);
});

test('deselecting a bulk exhibit keeps manually added animals from other exhibits', async () => {
   localStorage.setItem(
      ANIMALS_KEY,
      JSON.stringify([
         { species: 'African Lion', exhibit: 'Africa Savanna' },
         { species: 'Red Panda', exhibit: 'Indo-Malaya' },
      ])
   );
   localStorage.setItem(
      SELECTED_EXHIBITS_KEY,
      JSON.stringify(['Africa Savanna'])
   );

   globalThis.fetch = async () => ({
      ok: true,
      status: 200,
      statusText: 'OK',
      text: async () => JSON.stringify({ animals: [] }),
   });

   const state = createRegionSelectorState();
   state.setRegions([
      { name: 'Africa', exhibits: ['Africa Savanna'] },
      { name: 'Indo-Malaya', exhibits: ['Indo-Malaya'] },
   ]);
   state.hydrateSelectionsFromStorage();
   assert.equal(state.toggleExhibit('Africa', 'Africa Savanna'), true);

   const animals = await state.buildUpdatedAnimalsFromSelection();
   const species = animals.map((animal) => animal.species);

   assert.deepEqual(species, ['Red Panda']);
});
