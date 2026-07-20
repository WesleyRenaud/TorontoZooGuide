import {
   createEmptyItineraryDraft,
   normalizeItineraryDraft,
} from './itineraryShape.js';
import {
   buildSelectedAnimalKey,
   buildSelectedAnimalKeyFromWire,
   getExhibitNamesFromAnimals,
   makeSelectedAnimal,
   normalizeSelectedAnimal,
} from './selectors/regionSelector/regionSelection.js';
import {
   addRemovedAnimalKey,
   clearRemovedAnimalKeys,
   loadSelectedNames,
   saveSelectedNames,
} from './selectors/regionSelector/regionStorage.js';
import { ScheduleItemKind } from '../shared/enums/scheduleItemKind.js';
import {
   ANIMALS_KEY,
   ATTRACTIONS_KEY,
   DATE_KEY,
   GUARDIANS_KEY,
   REMOVED_ANIMALS_KEY,
   SELECTED_EXHIBITS_KEY,
   SELECTED_REGIONS_KEY,
   WILD_KEY,
} from './storageKeys.js';

export {
   areItineraryDraftsEqual,
   cloneItineraryDraft,
   createEmptyItineraryDraft,
   isItineraryEmptyDraft,
   normalizeItineraryDraft,
} from './itineraryShape.js';

const DRAFT_ITEM_STORAGE_KEYS = Object.freeze({
   animals: ANIMALS_KEY,
   attractions: ATTRACTIONS_KEY,
   guardiansTalks: GUARDIANS_KEY,
   wildEncounters: WILD_KEY,
});

export const ITINERARY_DRAFT_KEYS = [
   DATE_KEY,
   ANIMALS_KEY,
   ATTRACTIONS_KEY,
   GUARDIANS_KEY,
   WILD_KEY,
];

export const ITINERARY_SELECTION_KEYS = [
   SELECTED_EXHIBITS_KEY,
   SELECTED_REGIONS_KEY,
   REMOVED_ANIMALS_KEY,
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
   return localStorage.getItem(DATE_KEY) || '';
}

export function setStoredItineraryDate(date) {
   if (!date) {
      localStorage.removeItem(DATE_KEY);
      return;
   }

   localStorage.setItem(DATE_KEY, date);
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
      .map(makeSelectedAnimal)
      .filter(Boolean);

   saveArray(ANIMALS_KEY, draftAnimals);
}

function pruneSelectedExhibitsWithoutAnimals(animals = []) {
   const presentExhibits = new Set(getExhibitNamesFromAnimals(animals));
   const nextSelectedExhibits = loadSelectedNames(SELECTED_EXHIBITS_KEY)
      .filter((exhibitName) => presentExhibits.has(exhibitName));

   saveSelectedNames(SELECTED_EXHIBITS_KEY, nextSelectedExhibits);
}

function syncSelectedExhibitsFromItinerary(itinerary = {}) {
   if (!Array.isArray(itinerary.selectedExhibits)) {
      return;
   }

   saveSelectedNames(SELECTED_EXHIBITS_KEY, itinerary.selectedExhibits);
}

export function syncItineraryAnimalDraftFromItinerary(itinerary = {}) {
   writeItineraryAnimalDraft(itinerary.animals ?? []);
   syncSelectedExhibitsFromItinerary(itinerary);
   clearRemovedAnimalKeys();
}

export function removeAnimalFromItineraryAnimalDraft(itemType, key) {
   if (itemType !== ScheduleItemKind.ANIMAL.itemType || !key) {
      return;
   }

   const removeKey = buildSelectedAnimalKeyFromWire(key);

   if (!removeKey) {
      return;
   }

   addRemovedAnimalKey(removeKey);

   const remainingAnimals = loadArray(ANIMALS_KEY)
      .map(normalizeSelectedAnimal)
      .filter((animal) => animal && buildSelectedAnimalKey(animal) !== removeKey);

   writeItineraryAnimalDraft(remainingAnimals);
   pruneSelectedExhibitsWithoutAnimals(remainingAnimals);
}
