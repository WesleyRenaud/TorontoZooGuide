import { DraftStore } from './draftStore.js';
import { RegionStorageStore } from './selectors/regionSelector/regionStorageStore.js';
import { RegionStore } from './selectors/regionSelector/regionStore.js';
import { StorageKeys } from './storageKeys.js';

export class DraftStorageHelper {
   static DRAFT_ITEM_STORAGE_KEYS = Object.freeze({
      animals: StorageKeys.ANIMALS_KEY,
      attractions: StorageKeys.ATTRACTIONS_KEY,
      guardiansTalks: StorageKeys.GUARDIANS_KEY,
      wildEncounters: StorageKeys.WILD_KEY,
      transportations: StorageKeys.TRANSPORTATIONS_KEY,
   });

   static loadStoredDraftItems() {
      return Object.fromEntries(
         Object.entries(DraftStorageHelper.DRAFT_ITEM_STORAGE_KEYS).map(([draftKey, storageKey]) => (
            [draftKey, DraftStore.loadArray(storageKey)]
         ))
      );
   }

   static writeItineraryAnimalDraft(animals = []) {
      const draftAnimals = animals
         .map(RegionStore.makeSelectedAnimal)
         .filter(Boolean);

      DraftStore.saveArray(StorageKeys.ANIMALS_KEY, draftAnimals);
   }

   static pruneSelectedExhibitsWithoutAnimals(animals = []) {
      const presentExhibits = new Set(RegionStore.getExhibitNamesFromAnimals(animals));
      const nextSelectedExhibits = RegionStorageStore.loadSelectedNames(StorageKeys.SELECTED_EXHIBITS_KEY)
         .filter((exhibitName) => presentExhibits.has(exhibitName));

      RegionStorageStore.saveSelectedNames(StorageKeys.SELECTED_EXHIBITS_KEY, nextSelectedExhibits);
   }

   static syncSelectedExhibitsFromItinerary(itinerary = {}) {
      if (!Array.isArray(itinerary.selectedExhibits)) {
         return;
      }

      RegionStorageStore.saveSelectedNames(StorageKeys.SELECTED_EXHIBITS_KEY, itinerary.selectedExhibits);
   }
}
