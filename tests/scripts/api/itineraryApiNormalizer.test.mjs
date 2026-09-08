import assert from 'node:assert/strict';
import test from 'node:test';

import { ItineraryApiNormalizer } from '../../../scripts/api/itineraryApiNormalizer.js';
import { ItineraryErrorTypes } from '../../../scripts/itinerary/itineraryErrorTypes.js';
import { ItineraryPathModel } from '../../../scripts/itinerary/itineraryPathModel.js';
import { ScheduleItemKind } from '../../../scripts/shared/enums/scheduleItemKind.js';
import { WildEncounterScheduleItemKey } from '../../../scripts/itinerary/selectors/wildEncounterSelector/wildEncounterScheduleItemKey.js';

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

test('Test_NormalizeNamedStringMap_TestValues_ExpectFrozenTrimmed', () => {
   const map = ItineraryApiNormalizer.normalizeNamedStringMap({
      SUCCESS: '  success  ',
      EMPTY: '  ',
   });

   assert.equal(map.SUCCESS, 'success');
   assert.equal(map.EMPTY, undefined);
   assert.throws(() => {
      map.SUCCESS = 'changed';
   });
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
   ItineraryErrorTypes.updateItineraryErrorTypesFromConfig({
      errorTypes: { SUCCESS: 'success' },
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
