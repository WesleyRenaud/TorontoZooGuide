import assert from 'node:assert/strict';
import { afterEach, beforeEach, test } from 'node:test';

import { DraftStorageHelper } from '../../../scripts/itinerary/draftStorageHelper.js';
import { DraftStore } from '../../../scripts/itinerary/draftStore.js';
import { RegionStorageStore } from '../../../scripts/itinerary/selectors/regionSelector/regionStorageStore.js';
import { RegionStore } from '../../../scripts/itinerary/selectors/regionSelector/regionStore.js';
import { StorageKeys } from '../../../scripts/itinerary/storageKeys.js';
import { createLocalStorageMock } from '../helpers/localStorageMock.mjs';

beforeEach(() => {
   globalThis.localStorage = createLocalStorageMock();
});

afterEach(() => {
   delete globalThis.localStorage;
});

test('Test_LoadStoredDraftItems_TestPersistedArrays_ExpectDraftMap', () => {
   DraftStore.saveArray(StorageKeys.ANIMALS_KEY, [{ species: 'African Lion' }]);
   DraftStore.saveArray(StorageKeys.ATTRACTIONS_KEY, [{ name: 'Carousel' }]);

   const draftItems = DraftStorageHelper.loadStoredDraftItems();
   assert.deepEqual(draftItems.animals, [{ species: 'African Lion' }]);
   assert.deepEqual(draftItems.attractions, [{ name: 'Carousel' }]);
   assert.deepEqual(draftItems.guardiansTalks, []);
   assert.deepEqual(draftItems.wildEncounters, []);
   assert.deepEqual(draftItems.transportations, []);
});

test('Test_WriteItineraryAnimalDraft_TestAnimals_ExpectNormalizedSaved', () => {
   const originalMake = RegionStore.makeSelectedAnimal;
   RegionStore.makeSelectedAnimal = (animal) => (
      animal?.species
         ? { species: animal.species, id: animal.species }
         : null
   );

   try {
      DraftStorageHelper.writeItineraryAnimalDraft([
         { species: 'African Lion' },
         { name: 'skip' },
      ]);
      assert.deepEqual(DraftStore.loadArray(StorageKeys.ANIMALS_KEY), [
         { species: 'African Lion', id: 'African Lion' },
      ]);
   } finally {
      RegionStore.makeSelectedAnimal = originalMake;
   }
});

test('Test_PruneSelectedExhibitsWithoutAnimals_TestMissing_ExpectFiltered', () => {
   RegionStorageStore.saveSelectedNames(StorageKeys.SELECTED_EXHIBITS_KEY, [
      'African Rainforest',
      'Malayan Woods',
   ]);

   const originalExhibits = RegionStore.getExhibitNamesFromAnimals;
   RegionStore.getExhibitNamesFromAnimals = () => ['African Rainforest'];

   try {
      DraftStorageHelper.pruneSelectedExhibitsWithoutAnimals([{ species: 'African Lion' }]);
      assert.deepEqual(
         RegionStorageStore.loadSelectedNames(StorageKeys.SELECTED_EXHIBITS_KEY),
         ['African Rainforest']
      );
   } finally {
      RegionStore.getExhibitNamesFromAnimals = originalExhibits;
   }
});

test('Test_SyncSelectedExhibitsFromItinerary_TestArray_ExpectSaved', () => {
   DraftStorageHelper.syncSelectedExhibitsFromItinerary({
      selectedExhibits: ['Canadian Domain'],
   });
   assert.deepEqual(
      RegionStorageStore.loadSelectedNames(StorageKeys.SELECTED_EXHIBITS_KEY),
      ['Canadian Domain']
   );

   DraftStorageHelper.syncSelectedExhibitsFromItinerary({});
   assert.deepEqual(
      RegionStorageStore.loadSelectedNames(StorageKeys.SELECTED_EXHIBITS_KEY),
      ['Canadian Domain']
   );
});
