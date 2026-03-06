// scripts/itinerary/panel/storage.js
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

export function clearItineraryStorage() {
   localStorage.removeItem(ITIN_KEY);
   localStorage.removeItem(DATE_KEY);

   // Clear step storage too (so rebuild is clean)
   localStorage.removeItem(ANIMALS_KEY);
   localStorage.removeItem(ATTRACTIONS_KEY);
   localStorage.removeItem(GUARDIANS_KEY);
   localStorage.removeItem(WILD_KEY);

   window.dispatchEvent(new CustomEvent('tzg:itineraryUpdated'));
}