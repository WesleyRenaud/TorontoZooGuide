import assert from 'node:assert/strict';
import { afterEach, beforeEach, test } from 'node:test';

import { RegionSelectorStore } from '../../../../../scripts/itinerary/selectors/regionSelector/regionSelectorStore.js';
import { StorageKeys } from '../../../../../scripts/itinerary/storageKeys.js';
import { DraftStore } from '../../../../../scripts/itinerary/draftStore.js';
import { ScheduleItemKeySeparator } from '../../../../../scripts/itinerary/scheduleItemKeySeparator.js';
import { createLocalStorageMock } from '../../../helpers/localStorageMock.mjs';
import { createFetchMock } from '../../../helpers/fetchMock.mjs';

beforeEach(() => {
   globalThis.localStorage = createLocalStorageMock();
});

afterEach(() => {
   delete globalThis.localStorage;
   delete globalThis.fetch;
});


test('Test_GetAnimalsByExhibit_TestStoredVisit_ExpectMonthAndDay', async () => {
   const isoDate = '2026-08-12';
   const month = 'AUG';
   const day = 12;
   localStorage.setItem(StorageKeys.DATE_KEY, isoDate);
   globalThis.fetch = createFetchMock({
      '/get-animals-by-exhibit': (_url, options) => {
         const body = JSON.parse(options.body);
         assert.equal(body.month, month);
         assert.equal(body.day, day);
         assert.equal(body.forItinerary, true);
         assert.ok(Array.isArray(body.exhibitsToInclude));

         return { animals: [] };
      },
   });
   const regionName = 'R1';
   const exhibitName = 'E1';
   const state = RegionSelectorStore.createRegionSelectorState();
   state.setRegions([{ name: regionName, exhibits: [exhibitName] }]);

   const toggled = state.toggleRegion(regionName);
   await state.buildUpdatedAnimalsFromSelection();

   assert.equal(toggled, true);
});


test('Test_GetAnimalsByExhibit_TestNoVisit_ExpectTodayFallback', async () => {
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
   const regionName = 'R1';
   const exhibitName = 'E1';
   const state = RegionSelectorStore.createRegionSelectorState();
   state.setRegions([{ name: regionName, exhibits: [exhibitName] }]);

   const toggled = state.toggleRegion(regionName);
   await state.buildUpdatedAnimalsFromSelection();

   assert.equal(toggled, true);
});


test('Test_BuildUpdatedAnimalsFromSelection_TestIncompleteDeselect_ExpectRemainingAnimals', async () => {
   const lion = { species: 'African Lion', exhibit: 'Africa Savanna' };
   const penguin = { species: 'African Penguin', exhibit: 'Africa Savanna' };
   const giraffe = { species: 'Masai Giraffe', exhibit: 'Africa Savanna' };
   localStorage.setItem(StorageKeys.ANIMALS_KEY, JSON.stringify([lion, penguin]));
   localStorage.setItem(StorageKeys.SELECTED_EXHIBITS_KEY, JSON.stringify([lion.exhibit]));
   globalThis.fetch = async () => ({
      ok: true,
      status: 200,
      statusText: 'OK',
      text: async () => JSON.stringify({ animals: [lion, penguin, giraffe] }),
   });
   DraftStore.removeAnimalFromItineraryAnimalDraft(
      'animals',
      [penguin.species, penguin.exhibit].join(ScheduleItemKeySeparator.VALUE)
   );
   const state = RegionSelectorStore.createRegionSelectorState();
   state.setRegions([{ name: 'Africa', exhibits: [lion.exhibit] }]);
   await state.hydrateSelectionsFromStorage();

   const animals = await state.buildUpdatedAnimalsFromSelection();

   assert.deepEqual([...state.getSelectedExhibitNamesSet()], []);
   assert.deepEqual(animals.map((animal) => animal.species).sort(), [lion.species]);
});


test('Test_HydrateSelectionsFromStorage_TestMissingCatalogAnimals_ExpectDeselected', async () => {
   const lion = { species: 'African Lion', exhibit: 'Africa Savanna' };
   const cattle = { species: 'Watusi Cattle', exhibit: 'Africa Savanna' };
   localStorage.setItem(StorageKeys.ANIMALS_KEY, JSON.stringify([lion]));
   localStorage.setItem(StorageKeys.SELECTED_EXHIBITS_KEY, JSON.stringify([lion.exhibit]));
   globalThis.fetch = async () => ({
      ok: true,
      status: 200,
      statusText: 'OK',
      text: async () => JSON.stringify({ animals: [lion, cattle] }),
   });
   DraftStore.removeAnimalFromItineraryAnimalDraft(
      'animals',
      [cattle.species, cattle.exhibit].join(ScheduleItemKeySeparator.VALUE)
   );
   const state = RegionSelectorStore.createRegionSelectorState();
   state.setRegions([{ name: 'Africa', exhibits: [lion.exhibit] }]);

   await state.hydrateSelectionsFromStorage();

   assert.deepEqual([...state.getSelectedExhibitNamesSet()], []);
   assert.deepEqual(JSON.parse(localStorage.getItem(StorageKeys.SELECTED_EXHIBITS_KEY)), []);
});


test('Test_HydrateSelectionsFromStorage_TestCatalogGrew_ExpectKept', async () => {
   const lion = { species: 'African Lion', exhibit: 'Africa Savanna' };
   const cattle = { species: 'Watusi Cattle', exhibit: 'Africa Savanna' };
   localStorage.setItem(StorageKeys.DATE_KEY, '2026-10-17');
   localStorage.setItem(StorageKeys.ANIMALS_KEY, JSON.stringify([lion]));
   localStorage.setItem(StorageKeys.SELECTED_EXHIBITS_KEY, JSON.stringify([lion.exhibit]));
   globalThis.fetch = async () => ({
      ok: true,
      status: 200,
      statusText: 'OK',
      text: async () => JSON.stringify({ animals: [lion, cattle] }),
   });
   const state = RegionSelectorStore.createRegionSelectorState();
   state.setRegions([{ name: 'Africa', exhibits: [lion.exhibit] }]);

   await state.hydrateSelectionsFromStorage();

   assert.deepEqual([...state.getSelectedExhibitNamesSet()], [lion.exhibit]);
   assert.equal(state.selectedExhibitsNeedCatalogRebuild(), true);

   const animals = await state.buildUpdatedAnimalsFromSelection();

   assert.equal(state.selectedExhibitsNeedCatalogRebuild(), false);
   assert.deepEqual(
      JSON.parse(localStorage.getItem(StorageKeys.SELECTED_EXHIBITS_KEY)),
      [lion.exhibit]
   );
   assert.deepEqual(
      animals.map((animal) => animal.species).sort(),
      [lion.species, cattle.species].sort()
   );
});


test('Test_ToggleExhibit_TestReselect_ExpectRemovedAnimalsRestored', async () => {
   const lion = { species: 'African Lion', exhibit: 'Africa Savanna' };
   const penguin = { species: 'African Penguin', exhibit: 'Africa Savanna' };
   localStorage.setItem(StorageKeys.ANIMALS_KEY, JSON.stringify([lion]));
   localStorage.setItem(StorageKeys.SELECTED_EXHIBITS_KEY, JSON.stringify([lion.exhibit]));
   globalThis.fetch = async () => ({
      ok: true,
      status: 200,
      statusText: 'OK',
      text: async () => JSON.stringify({ animals: [lion, penguin] }),
   });
   DraftStore.removeAnimalFromItineraryAnimalDraft(
      'animals',
      [penguin.species, penguin.exhibit].join(ScheduleItemKeySeparator.VALUE)
   );
   const state = RegionSelectorStore.createRegionSelectorState();
   state.setRegions([{ name: 'Africa', exhibits: [lion.exhibit] }]);
   await state.hydrateSelectionsFromStorage();

   assert.deepEqual([...state.getSelectedExhibitNamesSet()], []);

   const toggled = state.toggleExhibit('Africa', lion.exhibit);
   const animals = await state.buildUpdatedAnimalsFromSelection();

   assert.equal(toggled, true);
   assert.deepEqual(
      animals.map((animal) => animal.species).sort(),
      [lion.species, penguin.species].sort()
   );
});


test('Test_ToggleExhibit_TestDeselectBulk_ExpectAnimalsRemoved', async () => {
   const lion = { species: 'African Lion', exhibit: 'Africa Savanna' };
   const penguin = { species: 'African Penguin', exhibit: 'Africa Savanna' };
   localStorage.setItem(StorageKeys.ANIMALS_KEY, JSON.stringify([lion, penguin]));
   localStorage.setItem(StorageKeys.SELECTED_EXHIBITS_KEY, JSON.stringify([lion.exhibit]));
   globalThis.fetch = async () => ({
      ok: true,
      status: 200,
      statusText: 'OK',
      text: async () => JSON.stringify({ animals: [] }),
   });
   const state = RegionSelectorStore.createRegionSelectorState();
   state.setRegions([{ name: 'Africa', exhibits: [lion.exhibit] }]);
   await state.hydrateSelectionsFromStorage();

   const toggled = state.toggleExhibit('Africa', lion.exhibit);
   const animals = await state.buildUpdatedAnimalsFromSelection();

   assert.equal(toggled, true);
   assert.deepEqual(animals, []);
   assert.deepEqual(JSON.parse(localStorage.getItem(StorageKeys.ANIMALS_KEY)), []);
});


test('Test_ToggleExhibit_TestDeselectBulk_ExpectManualAnimalsKept', async () => {
   const lion = { species: 'African Lion', exhibit: 'Africa Savanna' };
   const panda = { species: 'Red Panda', exhibit: 'Indo-Malaya' };
   localStorage.setItem(StorageKeys.ANIMALS_KEY, JSON.stringify([lion, panda]));
   localStorage.setItem(StorageKeys.SELECTED_EXHIBITS_KEY, JSON.stringify([lion.exhibit]));
   globalThis.fetch = async () => ({
      ok: true,
      status: 200,
      statusText: 'OK',
      text: async () => JSON.stringify({ animals: [lion] }),
   });
   const state = RegionSelectorStore.createRegionSelectorState();
   state.setRegions([
      { name: 'Africa', exhibits: [lion.exhibit] },
      { name: panda.exhibit, exhibits: [panda.exhibit] },
   ]);
   await state.hydrateSelectionsFromStorage();

   const toggled = state.toggleExhibit('Africa', lion.exhibit);
   const animals = await state.buildUpdatedAnimalsFromSelection();

   assert.equal(toggled, true);
   assert.deepEqual(animals.map((animal) => animal.species), [panda.species]);
});


test('Test_CreateRegionSelectorState_TestGuardPaths_ExpectFallbacks', async () => {
   const lion = { species: 'African Lion', exhibit: 'Africa Savanna' };
   globalThis.fetch = async () => ({
      ok: true,
      status: 200,
      statusText: 'OK',
      text: async () => JSON.stringify({ animals: [lion] }),
   });
   const state = RegionSelectorStore.createRegionSelectorState();

   assert.deepEqual(state.getRegions(), []);
   assert.equal(state.toggleRegion('Missing'), false);

   const emptyName = 'Empty';
   const africa = 'Africa';
   const savanna = 'Africa Savanna';
   const tundra = 'Tundra';
   state.setRegions([
      { name: emptyName, exhibits: [] },
      { name: africa, exhibits: [savanna, tundra] },
   ]);
   assert.equal(state.toggleRegion(emptyName), false);
   assert.equal(state.toggleExhibit('Missing', savanna), false);
   assert.equal(state.toggleExhibit(africa, ''), false);

   await state.hydrateSelectionsFromStorage();
   assert.equal(state.toggleRegion(africa), true);
   assert.equal(state.toggleRegion(africa), true);

   const mystery = { species: 'Mystery Bird' };
   const panda = { species: 'Red Panda', exhibit: 'Indo-Malaya' };
   localStorage.setItem(StorageKeys.ANIMALS_KEY, JSON.stringify([mystery, panda, lion]));

   const preserved = await state.buildUpdatedAnimalsFromSelection();
   assert.deepEqual(
      preserved.map((animal) => animal.species).sort(),
      [mystery.species, panda.species].sort()
   );

   assert.equal(state.toggleExhibit(africa, savanna), true);
   localStorage.setItem(StorageKeys.ANIMALS_KEY, JSON.stringify([mystery, panda, lion]));

   const merged = await state.buildUpdatedAnimalsFromSelection();
   const species = merged.map((animal) => animal.species).sort();
   assert.ok(species.includes(mystery.species));
   assert.ok(species.includes(panda.species));
   assert.ok(species.includes(lion.species));
});
