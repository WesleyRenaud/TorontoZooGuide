import { postJson } from './apiClient.js';
import {
   normalizeItineraryAdjustmentType,
   updateItineraryAdjustmentTypesFromConfig,
} from '../itinerary/itineraryAdjustmentTypes.js';
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

function normalizeItineraryAdjustmentTypes(adjustmentTypes) {
   const source = asObject(adjustmentTypes);

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

function normalizeItineraryStatuses(statuses) {
   return asArray(statuses)
      .map((entry) => {
         const source = asObject(entry);

         return {
            status: asTrimmedString(source.status),
            isSuppressable: Boolean(source.is_suppressable),
            isSuppressed: Boolean(source.is_suppressed),
         };
      })
      .filter((entry) => Boolean(entry.status));
}

function normalizeItineraryConfig(config) {
   const source = asObject(config);
   const normalizedStatuses = normalizeItineraryStatuses(source.itinerary_statuses);
   const normalizedConfig = {
      animalVisibilityChangeThreshold: source.animal_visibility_change_threshold,
      eventTypes: asArray(source.itinerary_event_types)
         .map(asTrimmedString)
         .filter(Boolean),
      visitBoundaryEventTypes: normalizeVisitBoundaryEventTypes(source),
      errorTypes: normalizeItineraryErrorTypes(source.itinerary_error_types),
      adjustmentTypes: normalizeItineraryAdjustmentTypes(
         source.itinerary_adjustment_types
      ),
      statuses: normalizedStatuses,
      suppressedErrorTypes: asArray(source.suppressed_error_types)
         .map(asTrimmedString)
         .filter(Boolean),
   };

   if (
      normalizedConfig.suppressedErrorTypes.length === 0
      && normalizedStatuses.length > 0
   ) {
      normalizedConfig.suppressedErrorTypes = normalizedStatuses
         .filter((entry) => entry.isSuppressable && entry.isSuppressed)
         .map((entry) => entry.status);
   }

   updateItineraryErrorTypesFromConfig(normalizedConfig);
   updateItineraryAdjustmentTypesFromConfig(normalizedConfig);

   return normalizedConfig;
}

function normalizeItineraryReason(reason) {
   const source = asObject(reason);
   const code = asTrimmedString(source.code);

   return {
      code,
      type: code,
      items: asArray(source.items),
   };
}

function normalizeItineraryAdjustment(adjustment) {
   const source = asObject(adjustment);

   return {
      type: normalizeItineraryAdjustmentType(source.type),
      field: asTrimmedString(source.field),
      previousValue: asTrimmedString(source.previous_value ?? source.previousValue),
      value: asTrimmedString(source.value),
      reason: asTrimmedString(source.reason),
   };
}

function normalizeItineraryResult(source = {}, { includeItinerary = true } = {}) {
   const response = asObject(source);

   if (response.itinerary_config !== undefined) {
      normalizeItineraryConfig(response.itinerary_config);
   }

   const status = normalizeItineraryErrorTypeFromResponse(response);
   const reasons = asArray(response.reasons).map(
      normalizeItineraryReason
   );
   const adjustments = asArray(response.adjustments).map(
      normalizeItineraryAdjustment
   );
   const suppressedWarnings = asArray(response.suppressed_warnings)
      .map(asTrimmedString)
      .filter(Boolean);
   const result = {
      status,
      reasons,
      adjustments,
      errorType: status,
      issues: reasons,
      suppressedWarnings,
   };

   if (includeItinerary && response.itinerary !== undefined) {
      result.itinerary = normalizeItineraryModel(response.itinerary);
   }

   if (response.itinerary_config !== undefined) {
      result.itineraryConfig = normalizeItineraryConfig(response.itinerary_config);
   }

   return result;
}

function normalizeItineraryResponse(response) {
   return normalizeItineraryResult(response, { includeItinerary: true });
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
   return normalizeItineraryResult(response, { includeItinerary: true });
}

export async function scheduleItineraryItemRequest(
   request,
   {
      confirmingScheduleItemNotOnItinerary = false,
      confirmingGuardiansTalkUnschedule = false,
      confirmingWildEncounterUnschedule = false,
   } = {}
) {
   const response = await postJson('/schedule-itinerary-item', {
      ...request,
      confirmingScheduleItemNotOnItinerary,
      confirmingGuardiansTalkUnschedule,
      confirmingWildEncounterUnschedule,
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
   return normalizeItineraryResult(response, { includeItinerary: false });
}

export async function setItineraryArrivalTimeRequest(
   arrivalTime,
   {
      confirmingShortVisit = false,
      confirmingEarlyAdmission = false,
   } = {}
) {
   const response = await postJson('/set-itinerary-arrival-time', {
      arrivalTime: asTrimmedString(arrivalTime),
      confirmingShortVisit,
      confirmingEarlyAdmission,
   });

   return normalizeItineraryTimeSetResponse(response);
}

export async function setItineraryDepartureTimeRequest(
   departureTime,
   { confirmingShortVisit = false } = {}
) {
   const response = await postJson('/set-itinerary-departure-time', {
      departureTime: asTrimmedString(departureTime),
      confirmingShortVisit,
   });

   return normalizeItineraryTimeSetResponse(response);
}

export async function suppressItineraryWarningRequest(warningType) {
   const response = await postJson('/suppress-itinerary-warning', {
      warningType: asTrimmedString(warningType),
   });

   return normalizeItineraryResult(response, { includeItinerary: false });
}

export async function bulkScheduleAnimalsRequest(temp) {
   const response = await postJson('/bulk-schedule-animals', { temp });
   return normalizeItineraryResponse(response);
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
