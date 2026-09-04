import {
   createEmptyItineraryDraft,
   normalizeItineraryDraft,
} from './itineraryShape.js';
import { RegionSelection } from './selectors/regionSelector/regionSelection.js';
import { RegionStorage } from './selectors/regionSelector/regionStorage.js';
import { ScheduleItemKind } from '../shared/enums/scheduleItemKind.js';
import { StorageKeys } from './storageKeys.js';

export {
   areItineraryDraftsEqual,
   cloneItineraryDraft,
   createEmptyItineraryDraft,
   isItineraryEmptyDraft,
   normalizeItineraryDraft,
} from './itineraryShape.js';

const DRAFT_ITEM_STORAGE_KEYS = Object.freeze({
   animals: StorageKeys.ANIMALS_KEY,
   attractions: StorageKeys.ATTRACTIONS_KEY,
   guardiansTalks: StorageKeys.GUARDIANS_KEY,
   wildEncounters: StorageKeys.WILD_KEY,
   transportations: StorageKeys.TRANSPORTATIONS_KEY,
});

export const ITINERARY_DRAFT_KEYS = [
   StorageKeys.DATE_KEY,
   StorageKeys.ANIMALS_KEY,
   StorageKeys.ATTRACTIONS_KEY,
   StorageKeys.GUARDIANS_KEY,
   StorageKeys.WILD_KEY,
   StorageKeys.TRANSPORTATIONS_KEY,
];

export const ITINERARY_SELECTION_KEYS = [
   StorageKeys.SELECTED_EXHIBITS_KEY,
   StorageKeys.SELECTED_REGIONS_KEY,
   StorageKeys.REMOVED_ANIMALS_KEY,
];

export const ITINERARY_STORAGE_KEYS = [
   ...ITINERARY_DRAFT_KEYS,
   ...ITINERARY_SELECTION_KEYS,
];

export function safeParseJSON(raw, fallback) {
   try {
      return JSON.parse(raw);
   } catch {
      return fallback;
   }
}

export function loadArray(key) {
   const parsed = safeParseJSON(localStorage.getItem(key), []);
   return Array.isArray(parsed) ? parsed : [];
}

export function saveArray(key, items = []) {
   localStorage.setItem(key, JSON.stringify(items));
}

export function getStoredItineraryDate() {
   return localStorage.getItem(StorageKeys.DATE_KEY) || '';
}

export function setStoredItineraryDate(date) {
   if (!date) {
      localStorage.removeItem(StorageKeys.DATE_KEY);
      return;
   }

   localStorage.setItem(StorageKeys.DATE_KEY, date);
}

function loadStoredDraftItems() {
   return Object.fromEntries(
      Object.entries(DRAFT_ITEM_STORAGE_KEYS).map(([draftKey, storageKey]) => (
         [draftKey, loadArray(storageKey)]
      ))
   );
}

export function loadStoredItineraryDraft() {
   return normalizeItineraryDraft({
      date: getStoredItineraryDate(),
      ...loadStoredDraftItems(),
   });
}

export function writeStoredItineraryDraft(draft = createEmptyItineraryDraft()) {
   const normalizedDraft = normalizeItineraryDraft(draft);

   setStoredItineraryDate(normalizedDraft.date);

   Object.entries(DRAFT_ITEM_STORAGE_KEYS).forEach(([draftKey, storageKey]) => {
      saveArray(storageKey, normalizedDraft[draftKey]);
   });
}

export function normalizeDateToLocalMidnight(dateValue) {
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

export function isStoredItineraryStale() {
   const storedDate = getStoredItineraryDate();

   if (!storedDate) return false;

   const normalizedStoredDate = normalizeDateToLocalMidnight(storedDate);
   if (!normalizedStoredDate) return false;

   const today = new Date();
   today.setHours(0, 0, 0, 0);

   return normalizedStoredDate < today;
}

export function clearItineraryDraftStorage({ includeSelections = true } = {}) {
   const keys = includeSelections
      ? ITINERARY_STORAGE_KEYS
      : ITINERARY_DRAFT_KEYS;

   keys.forEach((key) => {
      localStorage.removeItem(key);
   });
}

export function clearItinerarySelectionStorage() {
   ITINERARY_SELECTION_KEYS.forEach((key) => {
      localStorage.removeItem(key);
   });
}

function writeItineraryAnimalDraft(animals = []) {
   const draftAnimals = animals
      .map(RegionSelection.makeSelectedAnimal)
      .filter(Boolean);

   saveArray(StorageKeys.ANIMALS_KEY, draftAnimals);
}

function pruneSelectedExhibitsWithoutAnimals(animals = []) {
   const presentExhibits = new Set(RegionSelection.getExhibitNamesFromAnimals(animals));
   const nextSelectedExhibits = RegionStorage.loadSelectedNames(StorageKeys.SELECTED_EXHIBITS_KEY)
      .filter((exhibitName) => presentExhibits.has(exhibitName));

   RegionStorage.saveSelectedNames(StorageKeys.SELECTED_EXHIBITS_KEY, nextSelectedExhibits);
}

function syncSelectedExhibitsFromItinerary(itinerary = {}) {
   if (!Array.isArray(itinerary.selectedExhibits)) {
      return;
   }

   RegionStorage.saveSelectedNames(StorageKeys.SELECTED_EXHIBITS_KEY, itinerary.selectedExhibits);
}

export function syncItineraryAnimalDraftFromItinerary(itinerary = {}) {
   writeItineraryAnimalDraft(itinerary.animals ?? []);
   syncSelectedExhibitsFromItinerary(itinerary);
   RegionStorage.clearRemovedAnimalKeys();
}

export function removeAnimalFromItineraryAnimalDraft(itemType, key) {
   if (itemType !== ScheduleItemKind.ANIMAL.itemType || !key) {
      return;
   }

   const removeKey = RegionSelection.buildSelectedAnimalKeyFromWire(key);

   if (!removeKey) {
      return;
   }

   RegionStorage.addRemovedAnimalKey(removeKey);

   const remainingAnimals = loadArray(StorageKeys.ANIMALS_KEY)
      .map(RegionSelection.normalizeSelectedAnimal)
      .filter((animal) => animal && RegionSelection.buildSelectedAnimalKey(animal) !== removeKey);

   writeItineraryAnimalDraft(remainingAnimals);
   pruneSelectedExhibitsWithoutAnimals(remainingAnimals);
}
