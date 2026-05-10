import {
   clearItineraryRequest,
   getItineraryRequest,
   getZooHoursRequest,
   setItineraryRequest,
} from '../api/itineraryApi.js';
import {
   createEmptyItineraryDraft,
   isItineraryEmptyDraft,
   normalizeItineraryDraft,
} from './itineraryShape.js';

function createEmptyItinerary() {
   return {
      ...createEmptyItineraryDraft(),
      isActive: false,
   };
}

function normalizeItineraryItems(items) {
   return Array.isArray(items) ? items : [];
}

function normalizeItinerarySource(itinerary) {
   const source = itinerary && typeof itinerary === 'object'
      ? itinerary
      : {};

   return {
      date: typeof source.date === 'string' ? source.date : '',
      animals: normalizeItineraryItems(source.animals),
      attractions: normalizeItineraryItems(source.attractions),
      guardiansTalks: normalizeItineraryItems(source.guardiansTalks),
      wildEncounters: normalizeItineraryItems(source.wildEncounters),
   };
}

function dispatchItineraryUpdated(itinerary) {
   window.dispatchEvent(new CustomEvent('tzg:itineraryUpdated', {
      detail: { itinerary },
   }));
}

export function isItineraryEmpty(itinerary) {
   return isItineraryEmptyDraft(
      normalizeItinerarySource(itinerary)
   );
}

export function normalizeItinerary(itinerary) {
   const normalizedDraft = normalizeItineraryDraft(
      normalizeItinerarySource(itinerary)
   );

   return {
      ...normalizedDraft,
      isActive: !isItineraryEmptyDraft(normalizedDraft),
   };
}

export async function getItinerary() {
   const result = await getItineraryRequest();
   return normalizeItinerary(result?.itinerary);
}

export async function getZooHours(date) {
   if (!date) {
      return null;
   }

   const result = await getZooHoursRequest(date);
   return result?.hours || null;
}

export async function saveItinerary(itinerary = {}) {
   const normalizedDraft = normalizeItineraryDraft(itinerary);
   const result = await setItineraryRequest({
      ...normalizedDraft,
   });

   const normalizedItinerary = normalizeItinerary(result?.itinerary);
   dispatchItineraryUpdated(normalizedItinerary);

   return normalizedItinerary;
}

export async function clearItinerary() {
   const result = await clearItineraryRequest();
   const clearedItinerary = createEmptyItinerary();

   window.dispatchEvent(new CustomEvent('tzg:itineraryCleared'));
   dispatchItineraryUpdated(clearedItinerary);

   return result;
}

export async function hasActiveItinerary() {
   const itin = await getItinerary();
   return Boolean(itin.isActive) && !isItineraryEmpty(itin);
}
