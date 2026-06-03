import { postJson } from './apiClient.js';
import {
   normalizeItineraryErrorTypeFromResponse,
   updateItineraryErrorTypesFromConfig,
} from '../itinerary/itineraryErrorTypes.js';
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

function normalizeItineraryEvent(event) {
   const source = asObject(event);

   return {
      event_type: asTrimmedString(source.event_type),
      start_time: asTrimmedString(source.start_time),
      end_time: asTrimmedString(source.end_time),
   };
}

function normalizeItineraryEvents(events) {
   return asArray(events)
      .map(normalizeItineraryEvent)
      .filter((event) => Boolean(event.event_type));
}

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
      arrivalTime: asTrimmedString(source.arrival_time),
      departureTime: asTrimmedString(source.departure_time),
      ...normalizeItineraryCollections(source),
      events: normalizeItineraryEvents(source.events),
   };
}

function normalizeItineraryErrorTypes(errorTypes) {
   const source = asObject(errorTypes);

   return Object.freeze(
      Object.fromEntries(
         Object.entries(source)
            .map(([key, value]) => [key, asTrimmedString(value)])
            .filter(([, value]) => value)
      )
   );
}

function normalizeVisitBoundaryEventTypes(config) {
   const source = asObject(config.itinerary_visit_boundary_event_types);

   return {
      arrival: asTrimmedString(source.arrival),
      departure: asTrimmedString(source.departure),
   };
}

function normalizeItineraryConfig(config) {
   const source = asObject(config);
   const normalizedConfig = {
      animalVisibilityChangeThreshold: source.animal_visibility_change_threshold,
      eventTypes: asArray(source.itinerary_event_types)
         .map(asTrimmedString)
         .filter(Boolean),
      visitBoundaryEventTypes: normalizeVisitBoundaryEventTypes(source),
      errorTypes: normalizeItineraryErrorTypes(source.itinerary_error_types),
      suppressedErrorTypes: asArray(source.suppressed_error_types)
         .map(asTrimmedString)
         .filter(Boolean),
   };

   updateItineraryErrorTypesFromConfig(normalizedConfig);

   return normalizedConfig;
}

function normalizeItineraryResponse(response) {
   const source = asObject(response);
   const itineraryConfig = normalizeItineraryConfig(source.itinerary_config);

   return {
      errorType: normalizeItineraryErrorTypeFromResponse(source),
      issues: asArray(source.issues),
      itinerary: normalizeItineraryModel(source.itinerary),
      itineraryConfig,
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

function normalizeScheduleItineraryItemResponse(response) {
   const source = asObject(response);

   return {
      errorType: normalizeItineraryErrorTypeFromResponse(source),
   };
}

export async function scheduleItineraryItemRequest(
   request,
   {
      confirmingScheduleItemNotOnItinerary = false,
      suppressScheduleItemNotOnItineraryWarning = false,
      confirmingGuardiansTalkUnschedule = false,
   } = {}
) {
   const response = await postJson('/schedule-itinerary-item', {
      ...request,
      confirmingScheduleItemNotOnItinerary,
      suppressScheduleItemNotOnItineraryWarning,
      confirmingGuardiansTalkUnschedule,
   });

   return normalizeScheduleItineraryItemResponse(response);
}

export async function unscheduleItineraryItemRequest({ itemType, key }) {
   const response = await postJson('/unschedule-itinerary-item', {
      itemType: asTrimmedString(itemType),
      key: asTrimmedString(key),
   });

   return normalizeScheduleItineraryItemResponse(response);
}

export async function removeItemFromItineraryRequest({ itemType, key }) {
   const response = await postJson('/remove-item-from-itinerary', {
      itemType: asTrimmedString(itemType),
      key: asTrimmedString(key),
   });

   return normalizeScheduleItineraryItemResponse(response);
}

function normalizeItineraryTimeSetResponse(response) {
   const source = asObject(response);
   const itineraryConfig = normalizeItineraryConfig(source.itinerary_config);

   return {
      errorType: normalizeItineraryErrorTypeFromResponse(source),
      itineraryConfig,
   };
}

export async function setItineraryArrivalTimeRequest(
   arrivalTime,
   { confirmingShortVisit = false, suppressShortVisitWarning = false } = {}
) {
   const response = await postJson('/set-itinerary-arrival-time', {
      arrivalTime: asTrimmedString(arrivalTime),
      confirmingShortVisit,
      suppressShortVisitWarning,
   });

   return normalizeItineraryTimeSetResponse(response);
}

export async function setItineraryDepartureTimeRequest(
   departureTime,
   { confirmingShortVisit = false, suppressShortVisitWarning = false } = {}
) {
   const response = await postJson('/set-itinerary-departure-time', {
      departureTime: asTrimmedString(departureTime),
      confirmingShortVisit,
      suppressShortVisitWarning,
   });

   return normalizeItineraryTimeSetResponse(response);
}

export async function acceptItineraryRequest(
   temp,
   { animalsToKeep = [], attractionsToKeep = [] } = {}
) {
   const response = await postJson('/accept-itinerary', {
      temp,
      animalsToKeep,
      attractionsToKeep,
   });
   return normalizeItineraryResponse(response);
}

export function clearItineraryRequest() {
   return postJson('/clear-itinerary', {});
}
