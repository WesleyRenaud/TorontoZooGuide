import { ItineraryAdjustmentTypes } from '../itinerary/itineraryAdjustmentTypes.js';
import { ItineraryErrorTypes } from '../itinerary/itineraryErrorTypes.js';
import { ItineraryPathModel } from '../itinerary/itineraryPathModel.js';
import { ItineraryTransportationStationRoles } from '../itinerary/itineraryTransportationStationRoles.js';
import { GuardiansTalkScheduleItemKey } from '../itinerary/selectors/guardiansTalkSelector/guardiansTalkScheduleItemKey.js';
import { WildEncounterScheduleItemKey } from '../itinerary/selectors/wildEncounterSelector/wildEncounterScheduleItemKey.js';
import { ScheduleItemKind } from '../shared/enums/scheduleItemKind.js';
import { ValueNormalizer } from './valueNormalizer.js';

export class ItineraryApiNormalizer {
   static ITINERARY_COLLECTION_FIELDS = [
      ['animals', ScheduleItemKind.ANIMAL.itemType],
      ['attractions', ScheduleItemKind.ATTRACTION.itemType],
      ['guardiansTalks', ScheduleItemKind.GUARDIANS_TALK.itemType],
      ['wildEncounters', ScheduleItemKind.WILD_ENCOUNTER.itemType],
      ['transportations', ScheduleItemKind.TRANSPORTATION.itemType],
      ['transportationStations', 'transportation_stations'],
   ];

   static mapScheduleItemKeyToWire(itemType, key) {
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

   static normalizeItineraryEvent(event) {
      const source = ValueNormalizer.asObject(event);

      return {
         event_type: ValueNormalizer.asTrimmedString(source.event_type),
         start_time: ValueNormalizer.asTrimmedString(source.start_time),
         end_time: ValueNormalizer.asTrimmedString(source.end_time),
      };
   }

   static normalizeItineraryEvents(events) {
      return ValueNormalizer.asArray(events)
         .map(ItineraryApiNormalizer.normalizeItineraryEvent)
         .filter((event) => Boolean(event.event_type));
   }

   static normalizeItineraryTransportation(row) {
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

   static normalizeItineraryTransportations(transportations) {
      return ValueNormalizer.asArray(transportations).map(ItineraryApiNormalizer.normalizeItineraryTransportation);
   }

   static normalizeCollectionFields(source = {}, fields) {
      return Object.fromEntries(
         fields.map(([targetKey, responseKey]) => [
            targetKey,
            ValueNormalizer.asArray(source[responseKey]),
         ])
      );
   }

   static normalizeItineraryCollections(source = {}) {
      return ItineraryApiNormalizer.normalizeCollectionFields(source, ItineraryApiNormalizer.ITINERARY_COLLECTION_FIELDS);
   }

   static normalizeItineraryModel(itinerary) {
      const source = ValueNormalizer.asObject(itinerary);
      const collections = ItineraryApiNormalizer.normalizeItineraryCollections(source);

      return {
         date: ValueNormalizer.asTrimmedString(source.date),
         arrivalTime: ValueNormalizer.asTrimmedString(source.arrival_time),
         departureTime: ValueNormalizer.asTrimmedString(source.departure_time),
         selectedExhibits: ValueNormalizer.asTrimmedStringList(source.selected_exhibits),
         ...collections,
         transportations: ItineraryApiNormalizer.normalizeItineraryTransportations(source.transportations),
         events: ItineraryApiNormalizer.normalizeItineraryEvents(source.events),
      };
   }

   static normalizeNamedStringMap(values) {
      const source = ValueNormalizer.asObject(values);

      return Object.freeze(
         Object.fromEntries(
            Object.entries(source)
               .map(([key, value]) => [key, ValueNormalizer.asTrimmedString(value)])
               .filter(([, value]) => value)
         )
      );
   }

   static normalizeItineraryErrorTypes(errorTypes) {
      return ItineraryApiNormalizer.normalizeNamedStringMap(errorTypes);
   }

   static normalizeItineraryAdjustmentTypes(adjustmentTypes) {
      return ItineraryApiNormalizer.normalizeNamedStringMap(adjustmentTypes);
   }

   static normalizeVisitBoundaryEventTypes(config) {
      const source = ValueNormalizer.asObject(config.itinerary_visit_boundary_event_types);

      return {
         arrival: ValueNormalizer.asTrimmedString(source.arrival),
         departure: ValueNormalizer.asTrimmedString(source.departure),
      };
   }

   static normalizeItineraryStatuses(statuses) {
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

   static normalizeItineraryConfig(config) {
      const source = ValueNormalizer.asObject(config);
      const normalizedStatuses = ItineraryApiNormalizer.normalizeItineraryStatuses(source.itinerary_statuses);
      const normalizedConfig = {
         animalVisibilityChangeThreshold: source.animal_visibility_change_threshold,
         itineraryAnimalMinLikelihood: source.itinerary_animal_min_likelihood,
         eventTypes: ValueNormalizer.asArray(source.itinerary_event_types)
            .map(ValueNormalizer.asTrimmedString)
            .filter(Boolean),
         visitBoundaryEventTypes: ItineraryApiNormalizer.normalizeVisitBoundaryEventTypes(source),
         errorTypes: ItineraryApiNormalizer.normalizeItineraryErrorTypes(source.itinerary_error_types),
         adjustmentTypes: ItineraryApiNormalizer.normalizeItineraryAdjustmentTypes(
            source.itinerary_adjustment_types
         ),
         transportationStationRoles: ItineraryApiNormalizer.normalizeNamedStringMap(
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

   static normalizeItineraryReason(reason) {
      const source = ValueNormalizer.asObject(reason);
      const code = ValueNormalizer.asTrimmedString(source.code);

      return {
         code,
         type: code,
         items: ValueNormalizer.asArray(source.items),
      };
   }

   static normalizeItineraryAdjustment(adjustment) {
      const source = ValueNormalizer.asObject(adjustment);

      return {
         type: ItineraryAdjustmentTypes.normalizeItineraryAdjustmentType(source.type),
         field: ValueNormalizer.asTrimmedString(source.field),
         previousValue: ValueNormalizer.asTrimmedString(source.previous_value ?? source.previousValue),
         value: ValueNormalizer.asTrimmedString(source.value),
         reason: ValueNormalizer.asTrimmedString(source.reason),
      };
   }

   static normalizeItineraryResult(source = {}, { includeItinerary = true } = {}) {
      const response = ValueNormalizer.asObject(source);

      if (response.itinerary_config !== undefined) {
         ItineraryApiNormalizer.normalizeItineraryConfig(response.itinerary_config);
      }

      const status = ItineraryErrorTypes.normalizeItineraryErrorTypeFromResponse(response);
      const reasons = ValueNormalizer.asArray(response.reasons).map(
         ItineraryApiNormalizer.normalizeItineraryReason
      );
      const adjustments = ValueNormalizer.asArray(response.adjustments).map(
         ItineraryApiNormalizer.normalizeItineraryAdjustment
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
         result.itinerary = ItineraryApiNormalizer.normalizeItineraryModel(response.itinerary);

         if (result.itineraryPath === undefined) {
            result.itineraryPath = ItineraryPathModel.EMPTY_ITINERARY_PATH;
         }
      }

      if (response.itinerary_config !== undefined) {
         result.itineraryConfig = ItineraryApiNormalizer.normalizeItineraryConfig(response.itinerary_config);
      }

      return result;
   }

   static normalizeItineraryResponse(response) {
      return ItineraryApiNormalizer.normalizeItineraryResult(response, { includeItinerary: true });
   }

   static normalizeZooHours(hours) {
      const source = ValueNormalizer.asObject(hours);

      return {
         date: ValueNormalizer.asTrimmedString(source.date),
         earlyAdmissionTime: ValueNormalizer.asTrimmedString(source.earlyAdmissionTime),
         openTime: ValueNormalizer.asTrimmedString(source.openTime),
         lastAdmissionTime: ValueNormalizer.asTrimmedString(source.lastAdmissionTime),
         closeTime: ValueNormalizer.asTrimmedString(source.closeTime),
      };
   }

   static normalizeZooHoursResponse(response) {
      const source = ValueNormalizer.asObject(response);

      return {
         hours: ItineraryApiNormalizer.normalizeZooHours(source.hours),
      };
   }

   static normalizeItineraryDateResponse(response) {
      const source = ValueNormalizer.asObject(response);

      return {
         date: ValueNormalizer.asNullableString(source.date),
      };
   }

   static normalizeScheduleItineraryItemResponse(response) {
      return ItineraryApiNormalizer.normalizeItineraryResult(response, { includeItinerary: true });
   }

   static normalizeItineraryTimeSetResponse(response) {
      return ItineraryApiNormalizer.normalizeItineraryResult(response, { includeItinerary: true });
   }
}
