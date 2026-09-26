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
   const animal = { species: 'African Lion' };
   const attraction = { name: 'Conservation Carousel' };
   DraftStore.saveArray(StorageKeys.ANIMALS_KEY, [animal]);
   DraftStore.saveArray(StorageKeys.ATTRACTIONS_KEY, [attraction]);

   const draftItems = DraftStorageHelper.loadStoredDraftItems();

   assert.deepEqual(draftItems.animals, [animal]);
   assert.deepEqual(draftItems.attractions, [attraction]);
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
   const species = 'African Lion';

   try {
      DraftStorageHelper.writeItineraryAnimalDraft([
         { species },
         { name: 'skip' },
      ]);

      assert.deepEqual(DraftStore.loadArray(StorageKeys.ANIMALS_KEY), [
         { species, id: species },
      ]);
   } finally {
      RegionStore.makeSelectedAnimal = originalMake;
   }
});


test('Test_PruneSelectedExhibitsWithoutAnimals_TestMissing_ExpectFiltered', () => {
   const keptExhibit = 'African Rainforest';
   const droppedExhibit = 'Malayan Woods';
   RegionStorageStore.saveSelectedNames(StorageKeys.SELECTED_EXHIBITS_KEY, [
      keptExhibit,
      droppedExhibit,
   ]);
   const originalExhibits = RegionStore.getExhibitNamesFromAnimals;
   RegionStore.getExhibitNamesFromAnimals = () => [keptExhibit];
   const animals = [{ species: 'African Lion' }];

   try {
      DraftStorageHelper.pruneSelectedExhibitsWithoutAnimals(animals);

      assert.deepEqual(
         RegionStorageStore.loadSelectedNames(StorageKeys.SELECTED_EXHIBITS_KEY),
         [keptExhibit]
      );
   } finally {
      RegionStore.getExhibitNamesFromAnimals = originalExhibits;
   }
});


test('Test_SyncSelectedExhibitsFromItinerary_TestArray_ExpectSaved', () => {
   const exhibit = 'Canadian Domain';
   const itinerary = { selectedExhibits: [exhibit] };

   DraftStorageHelper.syncSelectedExhibitsFromItinerary(itinerary);

   assert.deepEqual(
      RegionStorageStore.loadSelectedNames(StorageKeys.SELECTED_EXHIBITS_KEY),
      [exhibit]
   );
});


test('Test_SyncSelectedExhibitsFromItinerary_TestMissing_ExpectUnchanged', () => {
   const exhibit = 'Canadian Domain';
   DraftStorageHelper.syncSelectedExhibitsFromItinerary({
      selectedExhibits: [exhibit],
   });

   DraftStorageHelper.syncSelectedExhibitsFromItinerary({});

   assert.deepEqual(
      RegionStorageStore.loadSelectedNames(StorageKeys.SELECTED_EXHIBITS_KEY),
      [exhibit]
   );
});
