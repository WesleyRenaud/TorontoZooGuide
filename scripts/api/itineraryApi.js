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
   ['guardiansTalks', 'guardians_talks'],
   ['wildEncounters', 'wild_encounters'],
];

const VALIDATION_COLLECTION_FIELDS = [
   ['animals', 'animals'],
   ['attractions', 'attractions'],
   ['guardiansTalks', 'guardiansTalks'],
   ['wildEncounters', 'wildEncounters'],
];

function normalizeCollectionFields(source = {}, fields) {
   return Object.fromEntries(
      fields.map(([targetKey, responseKey]) => [
         targetKey,
         asArray(source[responseKey]),
      ])
   );
}

function normalizeItineraryCollections(source = {}) {
   return normalizeCollectionFields(source, ITINERARY_COLLECTION_FIELDS);
}

function normalizeValidationCollections(source = {}) {
   return normalizeCollectionFields(source, VALIDATION_COLLECTION_FIELDS);
}

function normalizeItineraryModel(itinerary) {
   const source = asObject(itinerary);

   return {
      date: asTrimmedString(source.date),
      ...normalizeItineraryCollections(source),
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

function normalizeZooHours(hours) {
   const source = asObject(hours);

   return {
      date: asTrimmedString(source.date),
      openTime: asTrimmedString(source.openTime),
      closeTime: asTrimmedString(source.closeTime),
      lastAdmissionTime: asTrimmedString(source.lastAdmissionTime),
   };
}

function normalizeZooHoursResponse(response) {
   const source = asObject(response);

   return {
      hours: normalizeZooHours(source.hours),
   };
}

function normalizeValidationBucket(bucket) {
   return normalizeValidationCollections(asObject(bucket));
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

export async function getZooHoursRequest(date) {
   const response = await postJson('/get-zoo-hours', { date });
   return normalizeZooHoursResponse(response);
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
