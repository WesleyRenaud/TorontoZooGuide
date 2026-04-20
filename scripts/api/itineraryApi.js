import { postJson } from './apiClient.js';
import {
   asArray,
   asObject,
} from './normalizeValues.js';

function normalizeItineraryModel(itinerary) {
   const source = asObject(itinerary);

   return {
      date: typeof source.date === 'string' ? source.date : '',
      animals: asArray(source.animals),
      attractions: asArray(source.attractions),
      guardiansTalks: asArray(source.guardians_talks),
      wildEncounters: asArray(source.wild_encounters),
   };
}

function normalizeItineraryResponse(response) {
   const source = asObject(response);

   return {
      success: source.success !== false,
      error: source.error ?? null,
      itinerary: normalizeItineraryModel(source.itinerary),
   };
}

function normalizeValidatedItineraryResponse(response) {
   const source = asObject(response);

   return {
      success: source.success !== false,
      error: source.error ?? null,
      previous: {
         animals: asArray(source.previous?.animals),
         attractions: asArray(source.previous?.attractions),
         guardiansTalks: asArray(source.previous?.guardiansTalks),
         wildEncounters: asArray(source.previous?.wildEncounters),
      },
      validated: {
         animals: asArray(source.validated?.animals),
         attractions: asArray(source.validated?.attractions),
         guardiansTalks: asArray(source.validated?.guardiansTalks),
         wildEncounters: asArray(source.validated?.wildEncounters),
      },
      removed: {
         animals: asArray(source.removed?.animals),
         attractions: asArray(source.removed?.attractions),
         guardiansTalks: asArray(source.removed?.guardiansTalks),
         wildEncounters: asArray(source.removed?.wildEncounters),
      },
   };
}

export async function getItineraryRequest() {
   const response = await postJson('/get-itinerary', {});
   return normalizeItineraryResponse(response);
}

export async function setItineraryRequest(payload) {
   const response = await postJson('/set-itinerary', payload);
   return normalizeItineraryResponse(response);
}

export function clearItineraryRequest() {
   return postJson('/clear-itinerary', {});
}

export async function validateItineraryDraftRequest(payload) {
   const response = await postJson('/validate-itinerary', payload);
   return normalizeValidatedItineraryResponse(response);
}
