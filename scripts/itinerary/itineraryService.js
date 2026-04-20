import {
   clearItineraryRequest,
   getItineraryRequest,
   setItineraryRequest,
} from '../../api/itineraryApi.js';

function emptyItinerary() {
   return {
      isActive: false,
      date: '',
      animals: [],
      attractions: [],
      guardiansTalks: [],
      wildEncounters: [],
   };
}

function asArray(value) {
   return Array.isArray(value) ? value : [];
}

export function isItineraryEmpty(itin) {
   if (!itin || typeof itin !== 'object') return true;

   const animals = asArray(itin.animals);
   const attractions = asArray(itin.attractions);
   const guardiansTalks = asArray(itin.guardiansTalks);
   const wildEncounters = asArray(itin.wildEncounters);

   return !animals.length && !attractions.length && !guardiansTalks.length && !wildEncounters.length;
}

export function normalizeItinerary(itin) {
   if (!itin || typeof itin !== 'object') {
      return emptyItinerary();
   }

   const normalized = {
      date: typeof itin.date === 'string' ? itin.date : '',
      animals: asArray(itin.animals),
      attractions: asArray(itin.attractions),
      guardiansTalks: asArray(itin.guardiansTalks),
      wildEncounters: asArray(itin.wildEncounters),
   };

   return {
      ...normalized,
      isActive: !isItineraryEmpty(normalized),
   };
}

export async function getItinerary() {
   const result = await getItineraryRequest();
   return normalizeItinerary(result.itinerary);
}

export async function saveItinerary({
   date = '',
   animals = [],
   attractions = [],
   guardiansTalks = [],
   wildEncounters = [],
   isActive = true,
} = {}) {
   const result = await setItineraryRequest({
      date,
      animals,
      attractions,
      guardiansTalks,
      wildEncounters,
      isActive,
   });

   const itinerary = normalizeItinerary(result.itinerary);

   window.dispatchEvent(new CustomEvent('tzg:itineraryUpdated', {
      detail: { itinerary },
   }));

   return itinerary;
}

export async function clearItinerary() {
   const result = await clearItineraryRequest();
   const clearedItinerary = emptyItinerary();

   window.dispatchEvent(new CustomEvent('tzg:itineraryCleared'));
   window.dispatchEvent(new CustomEvent('tzg:itineraryUpdated', {
      detail: { itinerary: clearedItinerary },
   }));

   return result;
}

export async function hasActiveItinerary() {
   const itin = await getItinerary();
   return Boolean(itin.isActive) && !isItineraryEmpty(itin);
}
