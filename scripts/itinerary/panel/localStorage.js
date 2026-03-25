export const DATE_KEY = 'tzg.itineraryDate';
export const ANIMALS_KEY = 'tzg.itineraryAnimals';
export const ATTRACTIONS_KEY = 'tzg.itineraryAttractions';
export const GUARDIANS_KEY = 'tzg.itineraryGuardiansTalks';
export const WILD_KEY = 'tzg.itineraryWildEncounters';
export const SELECTED_EXHIBITS_KEY = 'tzg.itinerarySelectedExhibits';
export const SELECTED_REGIONS_KEY = 'tzg.itinerarySelectedRegions';

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

export function saveArray(key, value) {
   const safeValue = Array.isArray(value) ? value : [];
   localStorage.setItem(key, JSON.stringify(safeValue));
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

export function normalizeDateToLocalMidnight(dateValue) {
   if (!dateValue) return null;

   const date = new Date(dateValue);

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

export function clearItineraryStorage({ emitEvent = true } = {}) {
   localStorage.removeItem(DATE_KEY);
   localStorage.removeItem(ANIMALS_KEY);
   localStorage.removeItem(ATTRACTIONS_KEY);
   localStorage.removeItem(GUARDIANS_KEY);
   localStorage.removeItem(WILD_KEY);
   localStorage.removeItem(SELECTED_EXHIBITS_KEY);
   localStorage.removeItem(SELECTED_REGIONS_KEY);

   if (emitEvent) {
      window.dispatchEvent(new CustomEvent('tzg:itineraryUpdated', {
         detail: {
            itinerary: {
               isActive: false,
               date: '',
               animals: [],
               attractions: [],
               guardiansTalks: [],
               wildEncounters: [],
            },
         },
      }));
   }
}

export function clearStaleItineraryStorage() {
   if (!isStoredItineraryStale()) {
      return false;
   }

   clearItineraryStorage();
   return true;
}