import { DraftStorage } from './draftStorage.js';
import { RegionSelection } from './selectors/regionSelector/regionSelection.js';
import { RegionStorage } from './selectors/regionSelector/regionStorage.js';
import { StorageKeys } from './storageKeys.js';

export class DraftStorageHelpers {
   static DRAFT_ITEM_STORAGE_KEYS = Object.freeze({
      animals: StorageKeys.ANIMALS_KEY,
      attractions: StorageKeys.ATTRACTIONS_KEY,
      guardiansTalks: StorageKeys.GUARDIANS_KEY,
      wildEncounters: StorageKeys.WILD_KEY,
      transportations: StorageKeys.TRANSPORTATIONS_KEY,
   });

   static loadStoredDraftItems() {
      return Object.fromEntries(
         Object.entries(DraftStorageHelpers.DRAFT_ITEM_STORAGE_KEYS).map(([draftKey, storageKey]) => (
            [draftKey, DraftStorage.loadArray(storageKey)]
         ))
      );
   }

   static writeItineraryAnimalDraft(animals = []) {
      const draftAnimals = animals
         .map(RegionSelection.makeSelectedAnimal)
         .filter(Boolean);

      DraftStorage.saveArray(StorageKeys.ANIMALS_KEY, draftAnimals);
   }

   static pruneSelectedExhibitsWithoutAnimals(animals = []) {
      const presentExhibits = new Set(RegionSelection.getExhibitNamesFromAnimals(animals));
      const nextSelectedExhibits = RegionStorage.loadSelectedNames(StorageKeys.SELECTED_EXHIBITS_KEY)
         .filter((exhibitName) => presentExhibits.has(exhibitName));

      RegionStorage.saveSelectedNames(StorageKeys.SELECTED_EXHIBITS_KEY, nextSelectedExhibits);
   }

   static syncSelectedExhibitsFromItinerary(itinerary = {}) {
      if (!Array.isArray(itinerary.selectedExhibits)) {
         return;
      }

      RegionStorage.saveSelectedNames(StorageKeys.SELECTED_EXHIBITS_KEY, itinerary.selectedExhibits);
   }
}
