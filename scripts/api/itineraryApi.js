import { postJson } from './apiClient.js';
import {
   asArray,
   asNullableString,
   asObject,
   asTrimmedString,
} from './normalizeValues.js';

const ITINERARY_COLLECTION_FIELDS = [
   ['animals', 'animals'],
   ['attractions', 'attractions'],
   ['guardiansTalks', 'guardiansTalks'],
   ['wildEncounters', 'wildEncounters'],
];

function readCollectionField(source, camelKey, snakeKey = camelKey) {
   return asArray(source[camelKey] ?? source[snakeKey]);
}

function normalizeItineraryCollections(source = {}) {
   return Object.fromEntries(
      ITINERARY_COLLECTION_FIELDS.map(([camelKey, snakeKey]) => [
         camelKey,
         readCollectionField(source, camelKey, snakeKey),
      ])
   );
}

function normalizeItineraryModel(itinerary) {
   const source = asObject(itinerary);

   return {
      date: asTrimmedString(source.date),
      ...normalizeItineraryCollections({
         ...source,
         guardiansTalks: source.guardiansTalks ?? source.guardians_talks,
         wildEncounters: source.wildEncounters ?? source.wild_encounters,
      }),
   };
}

function normalizeItineraryResponse(response) {
   const source = asObject(response);

   return {
      success: source.success !== false,
      error: asNullableString(source.error),
      itinerary: normalizeItineraryModel(source.itinerary),
   };
}

function normalizeValidationBucket(bucket) {
   return normalizeItineraryCollections(asObject(bucket));
}

function normalizeValidatedItineraryResponse(response) {
   const source = asObject(response);

   return {
      success: source.success !== false,
      error: asNullableString(source.error),
      previous: normalizeValidationBucket(source.previous),
      validated: normalizeValidationBucket(source.validated),
      removed: normalizeValidationBucket(source.removed),
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
