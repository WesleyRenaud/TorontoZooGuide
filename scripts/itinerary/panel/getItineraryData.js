import {
   ITIN_KEY,
   safeParseJSON,
   clearStaleItineraryStorage
} from './storage.js';

export function getItineraryData() {
   clearStaleItineraryStorage();

   const raw = localStorage.getItem(ITIN_KEY);
   if (!raw) return null;

   const itin = safeParseJSON(raw, null);
   if (!itin) return null;

   return {
      itin,
      animals: Array.isArray(itin.animals) ? itin.animals : [],
      attractions: Array.isArray(itin.attractions) ? itin.attractions : [],
      guardiansTalks: Array.isArray(itin.guardiansTalks) ? itin.guardiansTalks : [],
      wildEncounters: Array.isArray(itin.wildEncounters) ? itin.wildEncounters : [],
   };
}