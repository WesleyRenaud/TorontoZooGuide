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

function normalizeItineraryModel(itinerary) {
   const source = asObject(itinerary);

   return {
      date: asTrimmedString(source.date),
      ...normalizeItineraryCollections(source),
   };
}

function normalizeItineraryConfig(config) {
   const source = asObject(config);

   return {
      animalVisibilityChangeThreshold: source.animal_visibility_change_threshold,
   };
}

function normalizeItineraryResponse(response) {
   const source = asObject(response);

   return {
      success: source.success !== false,
      error: asNullableString(source.error),
      issues: asArray(source.issues),
      itinerary: normalizeItineraryModel(source.itinerary),
      itineraryConfig: normalizeItineraryConfig(source.itinerary_config),
   };
}

function normalizeZooHours(hours) {
   const source = asObject(hours);

   return {
      date: asTrimmedString(source.date),
      earlyAdmissionTime: asTrimmedString(source.earlyAdmissionTime),
      openTime: asTrimmedString(source.openTime),
      lastAdmissionTime: asTrimmedString(source.lastAdmissionTime),
      closeTime: asTrimmedString(source.closeTime),
   };
}

function normalizeZooHoursResponse(response) {
   const source = asObject(response);

   return {
      hours: normalizeZooHours(source.hours),
   };
}

function normalizeItineraryDateResponse(response) {
   const source = asObject(response);

   return {
      date: asNullableString(source.date),
   };
}

export async function getItineraryDateRequest() {
   const response = await postJson('/get-itinerary-date', {});
   return normalizeItineraryDateResponse(response);
}

export async function getItineraryRequest(temp) {
   const response = await postJson('/get-itinerary', { temp });
   return normalizeItineraryResponse(response);
}

export async function getZooHoursRequest({ day, month, year }) {
   const response = await postJson('/get-zoo-hours', { day, month, year });
   return normalizeZooHoursResponse(response);
}

export async function setItineraryRequest(payload) {
   const response = await postJson('/set-itinerary', payload);
   return normalizeItineraryResponse(response);
}

export async function acceptItineraryRequest(temp) {
   const response = await postJson('/accept-itinerary', { temp });
   return normalizeItineraryResponse(response);
}

export function clearItineraryRequest() {
   return postJson('/clear-itinerary', {});
}
