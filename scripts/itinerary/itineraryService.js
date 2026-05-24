import {
   acceptItineraryRequest,
   clearItineraryRequest,
   getItineraryRequest,
   getZooHoursRequest,
   setItineraryRequest,
} from '../api/itineraryApi.js';
import {
   createEmptyItineraryDraft,
   isItineraryEmptyDraft,
   normalizeItineraryDraft,
   toSetItineraryPayload,
} from './itineraryShape.js';
import { buildItineraryValidationState } from './itineraryValidation.js';
import {
   getDay,
   getMonth,
   getYear,
} from '../visitDates/visitDateRules.js';

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
      validation: buildItineraryValidationState(normalizedDraft),
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

   const month = getMonth(date);
   const day = getDay(date);
   const year = getYear(date);

   if (month == null || day == null || year == null) {
      return null;
   }

   const result = await getZooHoursRequest({ day, month, year });
   return result?.hours || null;
}

export async function saveItinerary(itinerary = {}) {
   const payload = toSetItineraryPayload(itinerary);
   const result = await setItineraryRequest(payload);

   const normalizedItinerary = normalizeItinerary(result?.itinerary);
   normalizedItinerary.saveIssues = result.issues;
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

export async function acceptItinerary() {
   const result = await acceptItineraryRequest();
   const acceptedItinerary = normalizeItinerary(result?.itinerary);

   dispatchItineraryUpdated(acceptedItinerary);

   return acceptedItinerary;
}

export async function hasActiveItinerary() {
   const itin = await getItinerary();
   return Boolean(itin.isActive) && !isItineraryEmpty(itin);
}
