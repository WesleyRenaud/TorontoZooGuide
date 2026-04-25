import {
   DATE_KEY,
   ANIMALS_KEY,
   ATTRACTIONS_KEY,
   GUARDIANS_KEY,
   WILD_KEY,
   SELECTED_EXHIBITS_KEY,
   SELECTED_REGIONS_KEY,
} from './storageKeys.js';
import {
   createEmptyItineraryDraft,
   normalizeItineraryDraft,
} from './itineraryShape.js';

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
