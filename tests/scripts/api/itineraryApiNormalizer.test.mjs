import assert from 'node:assert/strict';
import test from 'node:test';

import { ItineraryApiNormalizer } from '../../../scripts/api/itineraryApiNormalizer.js';
import { ItineraryErrorTypes } from '../../../scripts/itinerary/itineraryErrorTypes.js';
import { ItineraryPathModel } from '../../../scripts/itinerary/itineraryPathModel.js';
import { GuardiansTalkScheduleItemKey } from '../../../scripts/itinerary/selectors/guardiansTalkSelector/guardiansTalkScheduleItemKey.js';
import { WildEncounterScheduleItemKey } from '../../../scripts/itinerary/selectors/wildEncounterSelector/wildEncounterScheduleItemKey.js';
import { ScheduleItemKind } from '../../../scripts/shared/enums/scheduleItemKind.js';

test('Test_NormalizeItineraryEvent_TestFields_ExpectTrimmed', () => {
   assert.deepEqual(
      ItineraryApiNormalizer.normalizeItineraryEvent({
         event_type: '  arrival  ',
         start_time: '  09:00  ',
         end_time: '  09:15  ',
      }),
      {
         event_type: 'arrival',
         start_time: '09:00',
         end_time: '09:15',
      }
   );
});

test('Test_NormalizeItineraryEvents_TestBlankTypes_ExpectFiltered', () => {
   assert.deepEqual(
      ItineraryApiNormalizer.normalizeItineraryEvents([
         { event_type: 'arrival', start_time: '09:00', end_time: '09:15' },
         { event_type: '', start_time: '10:00', end_time: '10:15' },
      ]),
      [{ event_type: 'arrival', start_time: '09:00', end_time: '09:15' }]
   );
});

test('Test_NormalizeItineraryTransportation_TestFlags_ExpectNormalized', () => {
   assert.deepEqual(
      ItineraryApiNormalizer.normalizeItineraryTransportation({
         name: '  Zoomobile  ',
         route: '  Summer  ',
         route_marker_sequences: [['  a  ', ''], ['b']],
         route_duration_minutes: '25',
         added_as_attraction: true,
         bulk_transit_evaluated: false,
         extra: 'keep',
      }),
      {
         name: 'Zoomobile',
         route: 'Summer',
         route_marker_sequences: [['a'], ['b']],
         route_duration_minutes: 25,
         added_as_attraction: true,
         bulk_transit_evaluated: false,
         extra: 'keep',
      }
   );
});

test('Test_NormalizeItineraryModel_TestCollections_ExpectNormalized', () => {
   const model = ItineraryApiNormalizer.normalizeItineraryModel({
      date: '  2026-09-08  ',
      arrival_time: '  09:00  ',
      departure_time: '  17:00  ',
      selected_exhibits: ['  African Savanna  ', ''],
      animals: [{ species: 'Lion' }],
      attractions: ['Carousel'],
      guardians_talks: [],
      wild_encounters: [],
      transportations: [{ name: 'Zoomobile', added_as_attraction: false }],
      transportation_stations: [],
      events: [{ event_type: 'arrival', start_time: '09:00', end_time: '09:15' }],
   });

   assert.equal(model.date, '2026-09-08');
   assert.deepEqual(model.selectedExhibits, ['African Savanna']);
   assert.equal(model.transportations[0].name, 'Zoomobile');
   assert.equal(model.events[0].event_type, 'arrival');
});

test('Test_NormalizeZooHoursResponse_TestHours_ExpectNormalized', () => {
   assert.deepEqual(
      ItineraryApiNormalizer.normalizeZooHoursResponse({
         hours: {
            date: '  2026-09-08  ',
            earlyAdmissionTime: '  09:00  ',
            openTime: '10:00',
            lastAdmissionTime: '16:00',
            closeTime: '17:00',
         },
      }),
      {
         hours: {
            date: '2026-09-08',
            earlyAdmissionTime: '09:00',
            openTime: '10:00',
            lastAdmissionTime: '16:00',
            closeTime: '17:00',
         },
      }
   );
});

test('Test_NormalizeItineraryDateResponse_TestBlank_ExpectNull', () => {
   assert.deepEqual(
      ItineraryApiNormalizer.normalizeItineraryDateResponse({ date: '  ' }),
      { date: null }
   );
});

test('Test_MapScheduleItemKeyToWire_TestStringAndWildEncounterKey_ExpectWire', () => {
   assert.equal(
      ItineraryApiNormalizer.mapScheduleItemKeyToWire('animal', '  African Lion  '),
      'African Lion'
   );

   const key = new WildEncounterScheduleItemKey('Red Panda', '13:00');
   assert.deepEqual(
      ItineraryApiNormalizer.mapScheduleItemKeyToWire(
         ScheduleItemKind.WILD_ENCOUNTER.itemType,
         key
      ),
      key.toWire()
   );
});

test('Test_NormalizeItineraryStatuses_TestRows_ExpectNormalized', () => {
   assert.deepEqual(
      ItineraryApiNormalizer.normalizeItineraryStatuses([
         { status: '  warning  ', is_suppressable: true, is_suppressed: false },
         { status: '', is_suppressable: true, is_suppressed: true },
      ]),
      [{ status: 'warning', isSuppressable: true, isSuppressed: false }]
   );
});

test('Test_NormalizeItineraryReason_TestCode_ExpectTypeAlias', () => {
   assert.deepEqual(
      ItineraryApiNormalizer.normalizeItineraryReason({
         code: '  conflict  ',
         items: ['a'],
      }),
      { code: 'conflict', type: 'conflict', items: ['a'] }
   );
});

test('Test_NormalizeItineraryResult_TestStatusAndItinerary_ExpectResult', () => {
   ItineraryErrorTypes.syncSuppressedItineraryErrorTypes({
      suppressedErrorTypes: [],
   });

   const result = ItineraryApiNormalizer.normalizeItineraryResult({
      status: 'success',
      reasons: [],
      adjustments: [],
      suppressed_warnings: ['  note  '],
      itinerary: {
         date: '2026-09-08',
         arrival_time: '09:00',
         departure_time: '17:00',
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

   assert.equal(result.status, 'success');
   assert.equal(result.itinerary.date, '2026-09-08');
   assert.deepEqual(result.suppressedWarnings, ['note']);
   assert.equal(result.itineraryPath, ItineraryPathModel.EMPTY_ITINERARY_PATH);
});

test('Test_MapScheduleItemKeyToWire_TestGuardiansTalkKey_ExpectWire', () => {
   const key = new GuardiansTalkScheduleItemKey('Amur Tiger', '11:30', '12:00');

   assert.deepEqual(
      ItineraryApiNormalizer.mapScheduleItemKeyToWire(
         ScheduleItemKind.GUARDIANS_TALK.itemType,
         key
      ),
      key.toWire()
   );
});

test('Test_NormalizeVisitBoundaryEventTypes_TestConfig_ExpectTrimmed', () => {
   assert.deepEqual(
      ItineraryApiNormalizer.normalizeVisitBoundaryEventTypes({
         itinerary_visit_boundary_event_types: {
            arrival: '  arrival  ',
            departure: '  departure  ',
         },
      }),
      { arrival: 'arrival', departure: 'departure' }
   );
});

test('Test_NormalizeItineraryConfig_TestFullConfig_ExpectNormalizedAndSideEffects', () => {
   const config = ItineraryApiNormalizer.normalizeItineraryConfig({
      animal_visibility_change_threshold: 0.5,
      itinerary_animal_min_likelihood: 0.25,
      itinerary_event_types: ['  arrival  ', ''],
      itinerary_visit_boundary_event_types: {
         arrival: 'arrival',
         departure: 'departure',
      },
      itinerary_statuses: [
         { status: 'warning', is_suppressable: true, is_suppressed: true },
         { status: 'error', is_suppressable: false, is_suppressed: true },
      ],
      suppressed_error_types: ['  custom  '],
   });

   assert.equal(config.animalVisibilityChangeThreshold, 0.5);
   assert.equal(config.itineraryAnimalMinLikelihood, 0.25);
   assert.deepEqual(config.eventTypes, ['arrival']);
   assert.deepEqual(config.visitBoundaryEventTypes, { arrival: 'arrival', departure: 'departure' });
   assert.equal(config.errorTypes, undefined);
   assert.equal(config.adjustmentTypes, undefined);
   assert.equal(config.transportationStationRoles, undefined);
   assert.deepEqual(config.statuses, [
      { status: 'warning', isSuppressable: true, isSuppressed: true },
      { status: 'error', isSuppressable: false, isSuppressed: true },
   ]);
   assert.deepEqual(config.suppressedErrorTypes, ['custom']);
   assert.deepEqual(ItineraryErrorTypes.suppressedItineraryErrorTypes, ['custom']);
});

test('Test_NormalizeItineraryConfig_TestStatusesWithoutExplicitSuppressed_ExpectDerived', () => {
   const config = ItineraryApiNormalizer.normalizeItineraryConfig({
      itinerary_statuses: [
         { status: 'warning', is_suppressable: true, is_suppressed: true },
         { status: 'error', is_suppressable: true, is_suppressed: false },
      ],
   });

   assert.deepEqual(config.suppressedErrorTypes, ['warning']);
});

test('Test_NormalizeItineraryAdjustment_TestRow_ExpectNormalized', () => {
   assert.deepEqual(
      ItineraryApiNormalizer.normalizeItineraryAdjustment({
         type: '  arrivalTimeAdjusted  ',
         field: '  animals  ',
         previous_value: '  a  ',
         value: '  b  ',
         reason: '  conflict  ',
      }),
      {
         type: 'arrivalTimeAdjusted',
         field: 'animals',
         previousValue: 'a',
         value: 'b',
         reason: 'conflict',
      }
   );
});

test('Test_NormalizeItineraryResult_TestConfigPathAndAdjustments_ExpectNormalized', () => {
   ItineraryErrorTypes.syncSuppressedItineraryErrorTypes({
      suppressedErrorTypes: [],
   });

   const result = ItineraryApiNormalizer.normalizeItineraryResult({
      status: 'success',
      reasons: [{ code: 'conflict', items: [] }],
      adjustments: [{ type: 'arrivalTimeAdjusted', field: 'animals', value: 'lion' }],
      suppressed_warnings: [],
      itinerary_path: { stops: [], legs: [], points: [] },
      itinerary_config: {
         itinerary_statuses: [],
      },
   }, { includeItinerary: false });

   assert.equal(result.status, 'success');
   assert.deepEqual(result.adjustments[0].type, 'arrivalTimeAdjusted');
   assert.deepEqual(result.itineraryPath, { stops: [], legs: [], points: [] });
   assert.deepEqual(result.itineraryConfig.suppressedErrorTypes, []);
   assert.equal(result.itinerary, undefined);
});

test('Test_NormalizeItineraryResponse_TestPayload_ExpectResult', () => {
   ItineraryErrorTypes.syncSuppressedItineraryErrorTypes({
      suppressedErrorTypes: [],
   });

   const result = ItineraryApiNormalizer.normalizeItineraryResponse({
      status: 'success',
      reasons: [],
      adjustments: [],
      suppressed_warnings: [],
   });

   assert.equal(result.status, 'success');
   assert.equal(result.errorType, 'success');
});

test('Test_NormalizeScheduleItineraryItemResponse_TestPayload_ExpectResult', () => {
   ItineraryErrorTypes.syncSuppressedItineraryErrorTypes({
      suppressedErrorTypes: [],
   });

   const result = ItineraryApiNormalizer.normalizeScheduleItineraryItemResponse({
      status: 'success',
      reasons: [],
      adjustments: [],
      suppressed_warnings: [],
   });

   assert.equal(result.status, 'success');
});

test('Test_NormalizeItineraryTimeSetResponse_TestPayload_ExpectResult', () => {
   ItineraryErrorTypes.syncSuppressedItineraryErrorTypes({
      suppressedErrorTypes: [],
   });

   const result = ItineraryApiNormalizer.normalizeItineraryTimeSetResponse({
      status: 'success',
      reasons: [],
      adjustments: [],
      suppressed_warnings: [],
   });

   assert.equal(result.status, 'success');
});
