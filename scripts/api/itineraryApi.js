import { ApiClient } from './apiClient.js';
import { ItineraryAdjustmentTypes } from '../itinerary/itineraryAdjustmentTypes.js';
import { ItineraryErrorTypes } from '../itinerary/itineraryErrorTypes.js';
import { ItineraryPathModel } from '../itinerary/itineraryPathModel.js';
import { ItineraryTransportationStationRoles } from '../itinerary/itineraryTransportationStationRoles.js';
import { GuardiansTalkScheduleItemKey } from '../itinerary/selectors/guardiansTalkSelector/scheduleItemKey.js';
import { WildEncounterScheduleItemKey } from '../itinerary/selectors/wildEncounterSelector/scheduleItemKey.js';
import { ScheduleItemKind } from '../shared/enums/scheduleItemKind.js';
import { ValueNormalizer } from './valueNormalizer.js';

const ITINERARY_COLLECTION_FIELDS = [
   ['animals', 'animals'],
   ['attractions', 'attractions'],
   ['guardiansTalks', 'guardians_talks'],
   ['wildEncounters', 'wild_encounters'],
   ['transportations', 'transportations'],
   ['transportationStations', 'transportation_stations'],
];

function mapScheduleItemKeyToWire(itemType, key) {
   const kind = ScheduleItemKind.scheduleItemKindFromItemType(itemType);

   if (
      kind === ScheduleItemKind.WILD_ENCOUNTER
      && key instanceof WildEncounterScheduleItemKey
   ) {
      return key.toWire();
   }

   if (
      kind === ScheduleItemKind.GUARDIANS_TALK
      && key instanceof GuardiansTalkScheduleItemKey
   ) {
      return key.toWire();
   }

   return ValueNormalizer.asTrimmedString(key);
}

function normalizeItineraryEvent(event) {
   const source = ValueNormalizer.asObject(event);

   return {
      event_type: ValueNormalizer.asTrimmedString(source.event_type),
      start_time: ValueNormalizer.asTrimmedString(source.start_time),
      end_time: ValueNormalizer.asTrimmedString(source.end_time),
   };
}

function normalizeItineraryEvents(events) {
   return ValueNormalizer.asArray(events)
      .map(normalizeItineraryEvent)
      .filter((event) => Boolean(event.event_type));
}

function normalizeItineraryTransportation(row) {
   const source = ValueNormalizer.asObject(row);

   return {
      ...source,
      name: ValueNormalizer.asTrimmedString(source.name),
      route: ValueNormalizer.asTrimmedString(source.route),
      route_marker_sequences: ValueNormalizer.asArray(source.route_marker_sequences).map(
         ValueNormalizer.asTrimmedStringList
      ),
      route_duration_minutes: ValueNormalizer.normalizeNumber(source.route_duration_minutes),
      added_as_attraction: ValueNormalizer.asBoolean(source.added_as_attraction),
      bulk_transit_evaluated: ValueNormalizer.asBoolean(source.bulk_transit_evaluated),
   };
}

function normalizeItineraryTransportations(transportations) {
   return ValueNormalizer.asArray(transportations).map(normalizeItineraryTransportation);
}

function normalizeCollectionFields(source = {}, fields) {
   return Object.fromEntries(
      fields.map(([targetKey, responseKey]) => [
         targetKey,
         ValueNormalizer.asArray(source[responseKey]),
      ])
   );
}

function normalizeItineraryCollections(source = {}) {
   return normalizeCollectionFields(source, ITINERARY_COLLECTION_FIELDS);
}

function normalizeItineraryModel(itinerary) {
   const source = ValueNormalizer.asObject(itinerary);
   const collections = normalizeItineraryCollections(source);

   return {
      date: ValueNormalizer.asTrimmedString(source.date),
      arrivalTime: ValueNormalizer.asTrimmedString(source.arrival_time),
      departureTime: ValueNormalizer.asTrimmedString(source.departure_time),
      selectedExhibits: ValueNormalizer.asTrimmedStringList(source.selected_exhibits),
      ...collections,
      transportations: normalizeItineraryTransportations(source.transportations),
      events: normalizeItineraryEvents(source.events),
   };
}

function normalizeNamedStringMap(values) {
   const source = ValueNormalizer.asObject(values);

   return Object.freeze(
      Object.fromEntries(
         Object.entries(source)
            .map(([key, value]) => [key, ValueNormalizer.asTrimmedString(value)])
            .filter(([, value]) => value)
      )
   );
}

function normalizeItineraryErrorTypes(errorTypes) {
   return normalizeNamedStringMap(errorTypes);
}

function normalizeItineraryAdjustmentTypes(adjustmentTypes) {
   return normalizeNamedStringMap(adjustmentTypes);
}

function normalizeVisitBoundaryEventTypes(config) {
   const source = ValueNormalizer.asObject(config.itinerary_visit_boundary_event_types);

   return {
      arrival: ValueNormalizer.asTrimmedString(source.arrival),
      departure: ValueNormalizer.asTrimmedString(source.departure),
   };
}

function normalizeItineraryStatuses(statuses) {
   return ValueNormalizer.asArray(statuses)
      .map((entry) => {
         const source = ValueNormalizer.asObject(entry);

         return {
            status: ValueNormalizer.asTrimmedString(source.status),
            isSuppressable: Boolean(source.is_suppressable),
            isSuppressed: Boolean(source.is_suppressed),
         };
      })
      .filter((entry) => Boolean(entry.status));
}

function normalizeItineraryConfig(config) {
   const source = ValueNormalizer.asObject(config);
   const normalizedStatuses = normalizeItineraryStatuses(source.itinerary_statuses);
   const normalizedConfig = {
      animalVisibilityChangeThreshold: source.animal_visibility_change_threshold,
      itineraryAnimalMinLikelihood: source.itinerary_animal_min_likelihood,
      eventTypes: ValueNormalizer.asArray(source.itinerary_event_types)
         .map(ValueNormalizer.asTrimmedString)
         .filter(Boolean),
      visitBoundaryEventTypes: normalizeVisitBoundaryEventTypes(source),
      errorTypes: normalizeItineraryErrorTypes(source.itinerary_error_types),
      adjustmentTypes: normalizeItineraryAdjustmentTypes(
         source.itinerary_adjustment_types
      ),
      transportationStationRoles: normalizeNamedStringMap(
         source.itinerary_transportation_station_roles
      ),
      transportationStationOnboardingRoles: ValueNormalizer.asArray(
         source.itinerary_transportation_station_onboarding_roles
      )
         .map(ValueNormalizer.asTrimmedString)
         .filter(Boolean),
      transportationStationOffboardingRoles: ValueNormalizer.asArray(
         source.itinerary_transportation_station_offboarding_roles
      )
         .map(ValueNormalizer.asTrimmedString)
         .filter(Boolean),
      statuses: normalizedStatuses,
      suppressedErrorTypes: ValueNormalizer.asArray(source.suppressed_error_types)
         .map(ValueNormalizer.asTrimmedString)
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

   ItineraryErrorTypes.updateItineraryErrorTypesFromConfig(normalizedConfig);
   ItineraryAdjustmentTypes.updateItineraryAdjustmentTypesFromConfig(normalizedConfig);
   ItineraryTransportationStationRoles.updateItineraryTransportationStationRolesFromConfig(normalizedConfig);

   return normalizedConfig;
}

function normalizeItineraryReason(reason) {
   const source = ValueNormalizer.asObject(reason);
   const code = ValueNormalizer.asTrimmedString(source.code);

   return {
      code,
      type: code,
      items: ValueNormalizer.asArray(source.items),
   };
}

function normalizeItineraryAdjustment(adjustment) {
   const source = ValueNormalizer.asObject(adjustment);

   return {
      type: ItineraryAdjustmentTypes.normalizeItineraryAdjustmentType(source.type),
      field: ValueNormalizer.asTrimmedString(source.field),
      previousValue: ValueNormalizer.asTrimmedString(source.previous_value ?? source.previousValue),
      value: ValueNormalizer.asTrimmedString(source.value),
      reason: ValueNormalizer.asTrimmedString(source.reason),
   };
}

function normalizeItineraryResult(source = {}, { includeItinerary = true } = {}) {
   const response = ValueNormalizer.asObject(source);

   if (response.itinerary_config !== undefined) {
      normalizeItineraryConfig(response.itinerary_config);
   }

   const status = ItineraryErrorTypes.normalizeItineraryErrorTypeFromResponse(response);
   const reasons = ValueNormalizer.asArray(response.reasons).map(
      normalizeItineraryReason
   );
   const adjustments = ValueNormalizer.asArray(response.adjustments).map(
      normalizeItineraryAdjustment
   );
   const suppressedWarnings = ValueNormalizer.asArray(response.suppressed_warnings)
      .map(ValueNormalizer.asTrimmedString)
      .filter(Boolean);
   const result = {
      status,
      reasons,
      adjustments,
      errorType: status,
      issues: reasons,
      suppressedWarnings,
   };

   if (response.itinerary_path !== undefined) {
      result.itineraryPath = ItineraryPathModel.normalizeItineraryPath(response.itinerary_path);
   }

   if (includeItinerary && response.itinerary !== undefined) {
      result.itinerary = normalizeItineraryModel(response.itinerary);

      if (result.itineraryPath === undefined) {
         result.itineraryPath = ItineraryPathModel.EMPTY_ITINERARY_PATH;
      }
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
   const source = ValueNormalizer.asObject(hours);

   return {
      date: ValueNormalizer.asTrimmedString(source.date),
      earlyAdmissionTime: ValueNormalizer.asTrimmedString(source.earlyAdmissionTime),
      openTime: ValueNormalizer.asTrimmedString(source.openTime),
      lastAdmissionTime: ValueNormalizer.asTrimmedString(source.lastAdmissionTime),
      closeTime: ValueNormalizer.asTrimmedString(source.closeTime),
   };
}

function normalizeZooHoursResponse(response) {
   const source = ValueNormalizer.asObject(response);

   return {
      hours: normalizeZooHours(source.hours),
   };
}

function normalizeItineraryDateResponse(response) {
   const source = ValueNormalizer.asObject(response);

   return {
      date: ValueNormalizer.asNullableString(source.date),
   };
}

function normalizeScheduleItineraryItemResponse(response) {
   return normalizeItineraryResult(response, { includeItinerary: true });
}

function normalizeItineraryTimeSetResponse(response) {
   return normalizeItineraryResult(response, { includeItinerary: true });
}

export class ItineraryApi {
   static async getItineraryDateRequest() {
      const response = await ApiClient.postJson('/get-itinerary-date', {});
      return normalizeItineraryDateResponse(response);
   }

   static async getItineraryRequest(temp) {
      const response = await ApiClient.postJson('/get-itinerary', { temp });
      return normalizeItineraryResponse(response);
   }

   static async getZooHoursRequest({ day, month, year }) {
      const response = await ApiClient.postJson('/get-zoo-hours', { day, month, year });
      return normalizeZooHoursResponse(response);
   }

   static async setItineraryRequest(payload) {
      const response = await ApiClient.postJson('/set-itinerary', payload);
      return normalizeItineraryResponse(response);
   }

   static async scheduleItineraryItemRequest(
      request,
      {
         confirmingScheduleItemNotOnItinerary = false,
         confirmingAttractionOutsideOperatingHours = false,
         confirmingGuardiansTalkUnschedule = false,
         confirmingWildEncounterUnschedule = false,
         confirmingFixedTimeItemLongWait = false,
         confirmingGuardiansTalkWithoutAnimal = false,
      } = {}
   ) {
      const response = await ApiClient.postJson('/schedule-itinerary-item', {
         ...request,
         key: mapScheduleItemKeyToWire(request.itemType, request.key),
         confirmingScheduleItemNotOnItinerary,
         confirmingAttractionOutsideOperatingHours,
         confirmingGuardiansTalkUnschedule,
         confirmingWildEncounterUnschedule,
         confirmingFixedTimeItemLongWait,
         confirmingGuardiansTalkWithoutAnimal,
      });

      return normalizeScheduleItineraryItemResponse(response);
   }

   static async unscheduleItineraryItemRequest({ itemType, key }) {
      const response = await ApiClient.postJson('/unschedule-itinerary-item', {
         itemType: ValueNormalizer.asTrimmedString(itemType),
         key: mapScheduleItemKeyToWire(itemType, key),
      });

      return normalizeScheduleItineraryItemResponse(response);
   }

   static async removeItemFromItineraryRequest({ itemType, key }) {
      const response = await ApiClient.postJson('/remove-item-from-itinerary', {
         itemType: ValueNormalizer.asTrimmedString(itemType),
         key: mapScheduleItemKeyToWire(itemType, key),
      });

      return normalizeScheduleItineraryItemResponse(response);
   }

   static async setItineraryArrivalTimeRequest(
      arrivalTime,
      {
         confirmingShortVisit = false,
         confirmingEarlyAdmission = false,
      } = {}
   ) {
      const response = await ApiClient.postJson('/set-itinerary-arrival-time', {
         arrivalTime: ValueNormalizer.asTrimmedString(arrivalTime),
         confirmingShortVisit,
         confirmingEarlyAdmission,
      });

      return normalizeItineraryTimeSetResponse(response);
   }

   static async setItineraryDepartureTimeRequest(
      departureTime,
      { confirmingShortVisit = false } = {}
   ) {
      const response = await ApiClient.postJson('/set-itinerary-departure-time', {
         departureTime: ValueNormalizer.asTrimmedString(departureTime),
         confirmingShortVisit,
      });

      return normalizeItineraryTimeSetResponse(response);
   }

   static async suppressItineraryWarningRequest(warningType) {
      const response = await ApiClient.postJson('/suppress-itinerary-warning', {
         warningType: ValueNormalizer.asTrimmedString(warningType),
      });

      return normalizeItineraryResult(response, { includeItinerary: false });
   }

   static async bulkScheduleItineraryRequest(
      temp,
      { confirmingFixedTimeItemLongWait = false } = {}
   ) {
      const response = await ApiClient.postJson('/bulk-schedule-itinerary', {
         temp,
         confirmingFixedTimeItemLongWait,
      });
      return normalizeItineraryResponse(response);
   }

   static async unscheduleAllItineraryItemsRequest(temp) {
      const response = await ApiClient.postJson('/unschedule-all-itinerary-items', { temp });
      return normalizeItineraryResponse(response);
   }

   static async acceptItineraryRequest(
      temp,
      { animalsToKeep = [], attractionsToKeep = [] } = {}
   ) {
      const response = await ApiClient.postJson('/accept-itinerary', {
         temp,
         animalsToKeep,
         attractionsToKeep,
      });
      return normalizeItineraryResponse(response);
   }

   static clearItineraryRequest() {
      return ApiClient.postJson('/clear-itinerary', {});
   }
}
