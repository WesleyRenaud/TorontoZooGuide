import assert from 'node:assert/strict';
import test from 'node:test';

import { ItineraryApiNormalizer } from '../../../scripts/api/itineraryApiNormalizer.js';
import { ItineraryErrorTypes } from '../../../scripts/itinerary/itineraryErrorTypes.js';
import { ItineraryPathModel } from '../../../scripts/itinerary/itineraryPathModel.js';
import { GuardiansTalkScheduleItemKey } from '../../../scripts/itinerary/selectors/guardiansTalkSelector/guardiansTalkScheduleItemKey.js';
import { WildEncounterScheduleItemKey } from '../../../scripts/itinerary/selectors/wildEncounterSelector/wildEncounterScheduleItemKey.js';
import { ItineraryAdjustmentType } from '../../../scripts/shared/enums/itineraryAdjustmentType.js';
import { ItineraryErrorType } from '../../../scripts/shared/enums/itineraryErrorType.js';
import { ScheduleItemKind } from '../../../scripts/shared/enums/scheduleItemKind.js';
import { Position } from '../../../scripts/shared/enums/position.js';


test('Test_NormalizeItineraryEvent_TestFields_ExpectTrimmed', () => {
   const eventType = 'arrival';
   const startTime = '09:00';
   const endTime = '09:15';
   const event = {
      event_type: `  ${eventType}  `,
      start_time: `  ${startTime}  `,
      end_time: `  ${endTime}  `,
   };

   const normalized = ItineraryApiNormalizer.normalizeItineraryEvent(event);

   assert.deepEqual(normalized, {
      event_type: eventType,
      start_time: startTime,
      end_time: endTime,
   });
});


test('Test_NormalizeItineraryEvents_TestBlankTypes_ExpectFiltered', () => {
   const eventType = 'arrival';
   const startTime = '09:00';
   const endTime = '09:15';
   const arrival = { event_type: eventType, start_time: startTime, end_time: endTime };
   const blank = { event_type: '', start_time: '10:00', end_time: '10:15' };

   const events = ItineraryApiNormalizer.normalizeItineraryEvents([arrival, blank]);

   assert.deepEqual(events, [arrival]);
});


test('Test_NormalizeItineraryTransportation_TestFlags_ExpectNormalized', () => {
   const name = 'Zoomobile';
   const route = 'Summer';
   const markerA = 'a';
   const markerB = 'b';
   const durationMinutes = '25';
   const addedAsAttraction = true;
   const bulkTransitEvaluated = false;
   const extra = 'keep';
   const row = {
      name: `  ${name}  `,
      route: `  ${route}  `,
      route_marker_sequences: [[`  ${markerA}  `, ''], [markerB]],
      route_duration_minutes: durationMinutes,
      added_as_attraction: addedAsAttraction,
      bulk_transit_evaluated: bulkTransitEvaluated,
      extra,
   };

   const transportation = ItineraryApiNormalizer.normalizeItineraryTransportation(row);

   assert.deepEqual(transportation, {
      name,
      route,
      route_marker_sequences: [[markerA], [markerB]],
      route_duration_minutes: Number(durationMinutes),
      added_as_attraction: addedAsAttraction,
      bulk_transit_evaluated: bulkTransitEvaluated,
      extra,
   });
});


test('Test_NormalizeItineraryModel_TestCollections_ExpectNormalized', () => {
   const date = '2026-09-08';
   const arrivalTime = '09:00';
   const departureTime = '17:00';
   const exhibit = 'African Savanna';
   const species = 'Lion';
   const attraction = 'Carousel';
   const transportationName = 'Zoomobile';
   const eventType = 'arrival';
   const startTime = '09:00';
   const endTime = '09:15';
   const itinerary = {
      date: `  ${date}  `,
      arrival_time: `  ${arrivalTime}  `,
      departure_time: `  ${departureTime}  `,
      selected_exhibits: [`  ${exhibit}  `, ''],
      animals: [{ species }],
      attractions: [attraction],
      guardians_talks: [],
      wild_encounters: [],
      transportations: [{ name: transportationName, added_as_attraction: false }],
      transportation_stations: [],
      events: [{ event_type: eventType, start_time: startTime, end_time: endTime }],
   };

   const model = ItineraryApiNormalizer.normalizeItineraryModel(itinerary);

   assert.equal(model.date, date);
   assert.deepEqual(model.selectedExhibits, [exhibit]);
   assert.equal(model.transportations[Position.FIRST].name, transportationName);
   assert.equal(model.events[Position.FIRST].event_type, eventType);
});


test('Test_NormalizeZooHoursResponse_TestHours_ExpectNormalized', () => {
   const date = '2026-09-08';
   const earlyAdmissionTime = '09:00';
   const openTime = '10:00';
   const lastAdmissionTime = '16:00';
   const closeTime = '17:00';
   const response = {
      hours: {
         date: `  ${date}  `,
         earlyAdmissionTime: `  ${earlyAdmissionTime}  `,
         openTime,
         lastAdmissionTime,
         closeTime,
      },
   };

   const normalized = ItineraryApiNormalizer.normalizeZooHoursResponse(response);

   assert.deepEqual(normalized, {
      hours: {
         date,
         earlyAdmissionTime,
         openTime,
         lastAdmissionTime,
         closeTime,
      },
   });
});


test('Test_NormalizeItineraryDateResponse_TestBlank_ExpectNull', () => {
   const response = { date: '  ' };

   const normalized = ItineraryApiNormalizer.normalizeItineraryDateResponse(response);

   assert.deepEqual(normalized, { date: null });
});


test('Test_MapScheduleItemKeyToWire_TestString_ExpectTrimmed', () => {
   const itemType = 'animal';
   const species = 'African Lion';
   const key = `  ${species}  `;

   const wire = ItineraryApiNormalizer.mapScheduleItemKeyToWire(itemType, key);

   assert.equal(wire, species);
});


test('Test_MapScheduleItemKeyToWire_TestWildEncounterKey_ExpectWire', () => {
   const name = 'Red Panda';
   const startTime = '13:00';
   const key = new WildEncounterScheduleItemKey(name, startTime);

   const wire = ItineraryApiNormalizer.mapScheduleItemKeyToWire(
      ScheduleItemKind.WILD_ENCOUNTER.itemType,
      key
   );

   assert.deepEqual(wire, key.toWire());
});


test('Test_NormalizeItineraryStatuses_TestRows_ExpectNormalized', () => {
   const status = 'warning';
   const isSuppressable = true;
   const isSuppressed = false;
   const rows = [
      { status: `  ${status}  `, is_suppressable: isSuppressable, is_suppressed: isSuppressed },
      { status: '', is_suppressable: true, is_suppressed: true },
   ];

   const statuses = ItineraryApiNormalizer.normalizeItineraryStatuses(rows);

   assert.deepEqual(statuses, [{ status, isSuppressable, isSuppressed }]);
});


test('Test_NormalizeItineraryReason_TestCode_ExpectTypeAlias', () => {
   const code = 'conflict';
   const items = ['a'];
   const reason = {
      code: `  ${code}  `,
      items,
   };

   const normalized = ItineraryApiNormalizer.normalizeItineraryReason(reason);

   assert.deepEqual(normalized, { code, type: code, items });
});


test('Test_NormalizeItineraryResult_TestStatusAndItinerary_ExpectResult', () => {
   const status = ItineraryErrorType.SUCCESS;
   const date = '2026-09-08';
   const arrivalTime = '09:00';
   const departureTime = '17:00';
   const warning = 'note';
   ItineraryErrorTypes.syncSuppressedItineraryErrorTypes({
      suppressedErrorTypes: [],
   });

   const result = ItineraryApiNormalizer.normalizeItineraryResult({
      status,
      reasons: [],
      adjustments: [],
      suppressed_warnings: [`  ${warning}  `],
      itinerary: {
         date,
         arrival_time: arrivalTime,
         departure_time: departureTime,
         selected_exhibits: [],
         animals: [],
         attractions: [],
         guardians_talks: [],
         wild_encounters: [],
         transportations: [],
         transportation_stations: [],
         events: [],
      },
   });

   assert.equal(result.status, status);
   assert.equal(result.itinerary.date, date);
   assert.deepEqual(result.suppressedWarnings, [warning]);
   assert.equal(result.itineraryPath, ItineraryPathModel.EMPTY_ITINERARY_PATH);
});


test('Test_MapScheduleItemKeyToWire_TestGuardiansTalkKey_ExpectWire', () => {
   const name = 'Amur Tiger';
   const startTime = '11:30';
   const endTime = '12:00';
   const key = new GuardiansTalkScheduleItemKey(name, startTime, endTime);

   const wire = ItineraryApiNormalizer.mapScheduleItemKeyToWire(
      ScheduleItemKind.GUARDIANS_TALK.itemType,
      key
   );

   assert.deepEqual(wire, key.toWire());
});


test('Test_NormalizeVisitBoundaryEventTypes_TestConfig_ExpectTrimmed', () => {
   const arrival = 'arrival';
   const departure = 'departure';
   const config = {
      itinerary_visit_boundary_event_types: {
         arrival: `  ${arrival}  `,
         departure: `  ${departure}  `,
      },
   };

   const eventTypes = ItineraryApiNormalizer.normalizeVisitBoundaryEventTypes(config);

   assert.deepEqual(eventTypes, { arrival, departure });
});


test('Test_NormalizeItineraryConfig_TestFullConfig_ExpectNormalizedAndSideEffects', () => {
   const visibilityThreshold = 0.5;
   const minLikelihood = 0.25;
   const arrival = 'arrival';
   const departure = 'departure';
   const warningStatus = 'warning';
   const errorStatus = 'error';
   const warningSuppressable = true;
   const warningSuppressed = true;
   const errorSuppressable = false;
   const errorSuppressed = true;
   const customError = 'custom';
   const configPayload = {
      animal_visibility_change_threshold: visibilityThreshold,
      itinerary_animal_min_likelihood: minLikelihood,
      itinerary_event_types: [`  ${arrival}  `, ''],
      itinerary_visit_boundary_event_types: {
         arrival,
         departure,
      },
      itinerary_statuses: [
         { status: warningStatus, is_suppressable: warningSuppressable, is_suppressed: warningSuppressed },
         { status: errorStatus, is_suppressable: errorSuppressable, is_suppressed: errorSuppressed },
      ],
      suppressed_error_types: [`  ${customError}  `],
   };

   const config = ItineraryApiNormalizer.normalizeItineraryConfig(configPayload);

   assert.equal(config.animalVisibilityChangeThreshold, visibilityThreshold);
   assert.equal(config.itineraryAnimalMinLikelihood, minLikelihood);
   assert.deepEqual(config.eventTypes, [arrival]);
   assert.deepEqual(config.visitBoundaryEventTypes, { arrival, departure });
   assert.equal(config.errorTypes, undefined);
   assert.equal(config.adjustmentTypes, undefined);
   assert.equal(config.transportationStationRoles, undefined);
   assert.deepEqual(config.statuses, [
      { status: warningStatus, isSuppressable: warningSuppressable, isSuppressed: warningSuppressed },
      { status: errorStatus, isSuppressable: errorSuppressable, isSuppressed: errorSuppressed },
   ]);
   assert.deepEqual(config.suppressedErrorTypes, [customError]);
   assert.deepEqual(ItineraryErrorTypes.suppressedItineraryErrorTypes, [customError]);
});


test('Test_NormalizeItineraryConfig_TestStatusesWithoutExplicitSuppressed_ExpectDerived', () => {
   const warningStatus = 'warning';
   const errorStatus = 'error';

   const config = ItineraryApiNormalizer.normalizeItineraryConfig({
      itinerary_statuses: [
         { status: warningStatus, is_suppressable: true, is_suppressed: true },
         { status: errorStatus, is_suppressable: true, is_suppressed: false },
      ],
   });

   assert.deepEqual(config.suppressedErrorTypes, [warningStatus]);
});


test('Test_NormalizeItineraryAdjustment_TestRow_ExpectNormalized', () => {
   const type = ItineraryAdjustmentType.ARRIVAL_TIME_ADJUSTED;
   const field = 'animals';
   const previousValue = 'a';
   const value = 'b';
   const reason = 'conflict';
   const row = {
      type: `  ${type}  `,
      field: `  ${field}  `,
      previous_value: `  ${previousValue}  `,
      value: `  ${value}  `,
      reason: `  ${reason}  `,
   };

   const adjustment = ItineraryApiNormalizer.normalizeItineraryAdjustment(row);

   assert.deepEqual(adjustment, {
      type,
      field,
      previousValue,
      value,
      reason,
   });
});


test('Test_NormalizeItineraryResult_TestConfigPathAndAdjustments_ExpectNormalized', () => {
   const status = ItineraryErrorType.SUCCESS;
   const adjustmentType = ItineraryAdjustmentType.ARRIVAL_TIME_ADJUSTED;
   const field = 'animals';
   const value = 'lion';
   const itineraryPath = { stops: [], legs: [], points: [] };
   ItineraryErrorTypes.syncSuppressedItineraryErrorTypes({
      suppressedErrorTypes: [],
   });

   const result = ItineraryApiNormalizer.normalizeItineraryResult({
      status,
      reasons: [{ code: 'conflict', items: [] }],
      adjustments: [{ type: adjustmentType, field, value }],
      suppressed_warnings: [],
      itinerary_path: itineraryPath,
      itinerary_config: {
         itinerary_statuses: [],
      },
   }, { includeItinerary: false });

   assert.equal(result.status, status);
   assert.deepEqual(result.adjustments[Position.FIRST].type, adjustmentType);
   assert.deepEqual(result.itineraryPath, itineraryPath);
   assert.deepEqual(result.itineraryConfig.suppressedErrorTypes, []);
   assert.equal(result.itinerary, undefined);
});


test('Test_NormalizeItineraryResponse_TestPayload_ExpectResult', () => {
   const status = ItineraryErrorType.SUCCESS;
   ItineraryErrorTypes.syncSuppressedItineraryErrorTypes({
      suppressedErrorTypes: [],
   });

   const result = ItineraryApiNormalizer.normalizeItineraryResponse({
      status,
      reasons: [],
      adjustments: [],
      suppressed_warnings: [],
   });

   assert.equal(result.status, status);
   assert.equal(result.errorType, status);
});


test('Test_NormalizeScheduleItineraryItemResponse_TestPayload_ExpectResult', () => {
   const status = ItineraryErrorType.SUCCESS;
   ItineraryErrorTypes.syncSuppressedItineraryErrorTypes({
      suppressedErrorTypes: [],
   });

   const result = ItineraryApiNormalizer.normalizeScheduleItineraryItemResponse({
      status,
      reasons: [],
      adjustments: [],
      suppressed_warnings: [],
   });

   assert.equal(result.status, status);
});


test('Test_NormalizeItineraryTimeSetResponse_TestPayload_ExpectResult', () => {
   const status = ItineraryErrorType.SUCCESS;
   ItineraryErrorTypes.syncSuppressedItineraryErrorTypes({
      suppressedErrorTypes: [],
   });

   const result = ItineraryApiNormalizer.normalizeItineraryTimeSetResponse({
      status,
      reasons: [],
      adjustments: [],
      suppressed_warnings: [],
   });

   assert.equal(result.status, status);
});
