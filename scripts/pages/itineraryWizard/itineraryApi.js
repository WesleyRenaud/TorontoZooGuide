import { postJson } from '../../api/apiClient.js';

export function isItineraryEmpty(itin) {
   if (!itin || typeof itin !== 'object') return true;

   const animals = Array.isArray(itin.animals) ? itin.animals : [];
   const attractions = Array.isArray(itin.attractions) ? itin.attractions : [];
   const guardiansTalks = Array.isArray(itin.guardiansTalks)
      ? itin.guardiansTalks
      : Array.isArray(itin.guardians_talks)
         ? itin.guardians_talks
         : [];
   const wildEncounters = Array.isArray(itin.wildEncounters)
      ? itin.wildEncounters
      : Array.isArray(itin.wild_encounters)
         ? itin.wild_encounters
         : [];

   return !animals.length && !attractions.length && !guardiansTalks.length && !wildEncounters.length;
}

export function normalizeItinerary(itin) {
   if (!itin || typeof itin !== 'object') {
      return {
         isActive: false,
         date: '',
         animals: [],
         attractions: [],
         guardiansTalks: [],
         wildEncounters: [],
      };
   }

   return {
      isActive: !isItineraryEmpty(itin),
      date: itin.date || itin.date || '',
      animals: Array.isArray(itin.animals) ? itin.animals : [],
      attractions: Array.isArray(itin.attractions) ? itin.attractions : [],
      guardiansTalks: Array.isArray(itin.guardiansTalks)
         ? itin.guardiansTalks
         : Array.isArray(itin.guardians_talks)
            ? itin.guardians_talks
            : [],
      wildEncounters: Array.isArray(itin.wildEncounters)
         ? itin.wildEncounters
         : Array.isArray(itin.wild_encounters)
            ? itin.wild_encounters
            : [],
   };
}

export async function getItinerary() {
   const result = await postJson('/get-itinerary', {});
   return normalizeItinerary(result?.itinerary);
}

export async function saveItinerary({
   date = '',
   animals = [],
   attractions = [],
   guardiansTalks = [],
   wildEncounters = [],
   isActive = true,
} = {}) {
   const result = await postJson('/set-itinerary', {
      date: date,
      animals,
      attractions,
      guardiansTalks,
      wildEncounters,
      isActive,
   });

   const itinerary = normalizeItinerary(result?.itinerary);

   window.dispatchEvent(new CustomEvent('tzg:itineraryUpdated', {
      detail: { itinerary },
   }));

   return itinerary;
}

export async function clearItinerary() {
   const result = await postJson('/clear-itinerary', {});
   const emptyItinerary = normalizeItinerary(null);

   window.dispatchEvent(new CustomEvent('tzg:itineraryCleared'));
   window.dispatchEvent(new CustomEvent('tzg:itineraryUpdated', {
      detail: { itinerary: emptyItinerary },
   }));

   return result;
}

export async function hasActiveItinerary() {
   const itin = await getItinerary();
   return Boolean(itin.isActive) && !isItineraryEmpty(itin);
}