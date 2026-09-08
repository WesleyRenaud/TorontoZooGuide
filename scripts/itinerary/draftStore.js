import { DraftStorageHelper } from './draftStorageHelper.js';
import { ItineraryShape } from './itineraryShape.js';
import { RegionStorageStore } from './selectors/regionSelector/regionStorageStore.js';
import { RegionStore } from './selectors/regionSelector/regionStore.js';
import { ScheduleItemKind } from '../shared/enums/scheduleItemKind.js';
import { StorageKeys } from './storageKeys.js';

export class DraftStore {
   static ITINERARY_DRAFT_KEYS = [
      StorageKeys.DATE_KEY,
      StorageKeys.ANIMALS_KEY,
      StorageKeys.ATTRACTIONS_KEY,
      StorageKeys.GUARDIANS_KEY,
      StorageKeys.WILD_KEY,
      StorageKeys.TRANSPORTATIONS_KEY,
   ];

   static ITINERARY_SELECTION_KEYS = [
      StorageKeys.SELECTED_EXHIBITS_KEY,
      StorageKeys.SELECTED_REGIONS_KEY,
      StorageKeys.REMOVED_ANIMALS_KEY,
   ];

   static ITINERARY_STORAGE_KEYS = [
      ...DraftStore.ITINERARY_DRAFT_KEYS,
      ...DraftStore.ITINERARY_SELECTION_KEYS,
   ];

   static safeParseJSON(raw, fallback) {
      try {
         return JSON.parse(raw);
      } catch {
         return fallback;
      }
   }

   static loadArray(key) {
      const parsed = DraftStore.safeParseJSON(localStorage.getItem(key), []);
      return Array.isArray(parsed) ? parsed : [];
   }

   static saveArray(key, items = []) {
      localStorage.setItem(key, JSON.stringify(items));
   }

   static getStoredItineraryDate() {
      return localStorage.getItem(StorageKeys.DATE_KEY) || '';
   }

   static setStoredItineraryDate(date) {
      if (!date) {
         localStorage.removeItem(StorageKeys.DATE_KEY);
         return;
      }

      localStorage.setItem(StorageKeys.DATE_KEY, date);
   }

   static loadStoredItineraryDraft() {
      return ItineraryShape.normalizeItineraryDraft({
         date: DraftStore.getStoredItineraryDate(),
         ...DraftStorageHelper.loadStoredDraftItems(),
      });
   }

   static writeStoredItineraryDraft(draft = ItineraryShape.createEmptyItineraryDraft()) {
      const normalizedDraft = ItineraryShape.normalizeItineraryDraft(draft);

      DraftStore.setStoredItineraryDate(normalizedDraft.date);

      Object.entries(DraftStorageHelper.DRAFT_ITEM_STORAGE_KEYS).forEach(([draftKey, storageKey]) => {
         DraftStore.saveArray(storageKey, normalizedDraft[draftKey]);
      });
   }

   static normalizeDateToLocalMidnight(dateValue) {
      if (!dateValue) return null;

      const isoDateParts = typeof dateValue === 'string'
         ? dateValue.match(/^(\d{4})-(\d{2})-(\d{2})$/)
         : null;
      const date = isoDateParts
         ? new Date(
            Number(isoDateParts[1]),
            Number(isoDateParts[2]) - 1,
            Number(isoDateParts[3])
         )
         : new Date(dateValue);

      if (Number.isNaN(date.getTime())) {
         return null;
      }

      date.setHours(0, 0, 0, 0);
      return date;
   }

   static isStoredItineraryStale() {
      const storedDate = DraftStore.getStoredItineraryDate();

      if (!storedDate) return false;

      const normalizedStoredDate = DraftStore.normalizeDateToLocalMidnight(storedDate);
      if (!normalizedStoredDate) return false;

      const today = new Date();
      today.setHours(0, 0, 0, 0);

      return normalizedStoredDate < today;
   }

   static clearItineraryDraftStorage({ includeSelections = true } = {}) {
      const keys = includeSelections
         ? DraftStore.ITINERARY_STORAGE_KEYS
         : DraftStore.ITINERARY_DRAFT_KEYS;

      keys.forEach((key) => {
         localStorage.removeItem(key);
      });
   }

   static clearItinerarySelectionStorage() {
      DraftStore.ITINERARY_SELECTION_KEYS.forEach((key) => {
         localStorage.removeItem(key);
      });
   }

   static syncItineraryAnimalDraftFromItinerary(itinerary = {}) {
      DraftStorageHelper.writeItineraryAnimalDraft(itinerary.animals ?? []);
      DraftStorageHelper.syncSelectedExhibitsFromItinerary(itinerary);
      RegionStorageStore.clearRemovedAnimalKeys();
   }

   static removeAnimalFromItineraryAnimalDraft(itemType, key) {
      if (itemType !== ScheduleItemKind.ANIMAL.itemType || !key) {
         return;
      }

      const removeKey = RegionStore.buildSelectedAnimalKeyFromWire(key);

      if (!removeKey) {
         return;
      }

      RegionStorageStore.addRemovedAnimalKey(removeKey);

      const remainingAnimals = DraftStore.loadArray(StorageKeys.ANIMALS_KEY)
         .map(RegionStore.normalizeSelectedAnimal)
         .filter((animal) => animal && RegionStore.buildSelectedAnimalKey(animal) !== removeKey);

      DraftStorageHelper.writeItineraryAnimalDraft(remainingAnimals);
      DraftStorageHelper.pruneSelectedExhibitsWithoutAnimals(remainingAnimals);
   }
}
