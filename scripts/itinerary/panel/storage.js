export const ITIN_KEY = 'tzg.itinerary';
export const DATE_KEY = 'tzg.itineraryDateISO';

export const ANIMALS_KEY = 'tzg.itineraryAnimals';
export const ATTRACTIONS_KEY = 'tzg.itineraryAttractions';
export const GUARDIANS_KEY = 'tzg.itineraryGuardiansTalks';
export const WILD_KEY = 'tzg.itineraryWildEncounters';

export function safeParseJSON(raw, fallback) {
   try {
      return JSON.parse(raw);
   } catch {
      return fallback;
   }
}

export function getStoredItineraryDateISO() {
   return localStorage.getItem(DATE_KEY) || '';
}

export function normalizeDateToLocalMidnight(dateValue) {
   if(!dateValue) return null;

   const date = new Date(dateValue);

   if(Number.isNaN(date.getTime())) {
      return null;
   }

   date.setHours(0, 0, 0, 0);
   return date;
}

export function isStoredItineraryStale() {
   const storedDateISO = getStoredItineraryDateISO();

   if(!storedDateISO) {
      return false;
   }

   const storedDate = normalizeDateToLocalMidnight(storedDateISO);

   if(!storedDate) {
      return false;
   }

   const today = new Date();
   today.setHours(0, 0, 0, 0);

   return storedDate < today;
}

export function clearStaleItineraryStorage() {
   if(isStoredItineraryStale()) {
      clearItineraryStorage();
      return true;
   }

   return false;
}

export function clearItineraryStorage() {
   localStorage.removeItem(ITIN_KEY);
   localStorage.removeItem(DATE_KEY);

   localStorage.removeItem(ANIMALS_KEY);
   localStorage.removeItem(ATTRACTIONS_KEY);
   localStorage.removeItem(GUARDIANS_KEY);
   localStorage.removeItem(WILD_KEY);

   window.dispatchEvent(new CustomEvent('tzg:itineraryUpdated'));
}