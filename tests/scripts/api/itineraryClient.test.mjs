import assert from 'node:assert/strict';
import { afterEach, test } from 'node:test';

import { ItineraryClient } from '../../../scripts/api/itineraryClient.js';
import { mockJsonResponse } from '../helpers/fetchMock.mjs';
import { ItinerarySaveIssueItemType } from '../../../scripts/shared/enums/itinerarySaveIssueItemType.js';

function _normalizedItineraryConfig(overrides = {}) {
   return {
      animalVisibilityChangeThreshold: overrides.animalVisibilityChangeThreshold,
      itineraryAnimalMinLikelihood: overrides.itineraryAnimalMinLikelihood,
      eventTypes: overrides.eventTypes ?? [],
      visitBoundaryEventTypes: overrides.visitBoundaryEventTypes ?? {
         arrival: 'arrival',
         departure: 'departure',
      },
      statuses: overrides.statuses ?? [],
      suppressedErrorTypes: overrides.suppressedErrorTypes ?? [],
   };
}

function _normalizedItineraryResultFields(status, reasons = []) {
   return {
      status,
      reasons,
      adjustments: [],
      errorType: status,
      issues: reasons,
      suppressedWarnings: [],
   };
}

function _normalizedItineraryPath(overrides = {}) {
   return {
      stops: overrides.stops ?? [],
      legs: overrides.legs ?? [],
      points: overrides.points ?? [],
   };
}

function _mockItineraryPathResponse(overrides = {}) {
   return {
      itinerary_path: {
         stops: overrides.stops ?? [
            {
               schedule_item_kind: 'animals',
               item_key: 'African Lion||Africa Savanna',
               walk_node_id: 'v-0255',
               start_time: '10:00 AM',
               end_time: '10:30 AM',
            },
         ],
         legs: overrides.legs ?? [
            {
               from_item_key: 'arrival',
               to_item_key: 'African Lion||Africa Savanna',
               from_schedule_item_kind: 'visit_boundary',
               to_schedule_item_kind: 'animals',
               node_ids: ['n-0001', 'n-0002'],
            },
         ],
         points: overrides.points ?? [
            {
               node_id: 'n-0001',
               x: 1.5,
               y: 2.5,
               x_px: 150,
               y_px: 250,
            },
         ],
      },
   };
}

function _mockItineraryConfigResponse(overrides = {}) {
   return {
      itinerary_config: {
         animal_visibility_change_threshold:
            overrides.animalVisibilityChangeThreshold,
         itinerary_animal_min_likelihood:
            overrides.itineraryAnimalMinLikelihood,
         itinerary_event_types: overrides.eventTypes ?? [],
         itinerary_visit_boundary_event_types:
            overrides.visitBoundaryEventTypes ?? {
               arrival: 'arrival',
               departure: 'departure',
            },
         itinerary_statuses: overrides.statuses ?? [],
         suppressed_error_types: overrides.suppressedErrorTypes ?? [],
      },
   };
}

afterEach(() => {
   delete globalThis.fetch;
});

test('Test_GetItineraryDateRequest_TestEmptyDate_ExpectNull', async () => {
   globalThis.fetch = async () => mockJsonResponse({ date: null });

   assert.deepEqual(await ItineraryClient.getItineraryDateRequest(), {
      date: null,
   });
});

test('Test_GetItineraryDateRequest_TestStoredDate_ExpectNormalized', async () => {
   globalThis.fetch = async (url, options) => {
      assert.equal(url, '/get-itinerary-date');
      assert.equal(options.method, 'POST');
      assert.deepEqual(JSON.parse(options.body), {});

      return mockJsonResponse({
         date: '  2026-06-15  ',
      });
   };

   assert.deepEqual(await ItineraryClient.getItineraryDateRequest(), {
      date: '2026-06-15',
   });
});

test('Test_GetItineraryRequest_TestSnakeCaseKeys_ExpectNormalized', async () => {
   globalThis.fetch = async (url, options) => {
      assert.equal(url, '/get-itinerary');
      assert.equal(options.method, 'POST');
      assert.deepEqual(JSON.parse(options.body), {});

      return mockJsonResponse({
         success: true,
         error: '',
         itinerary: {
            date: '  2026-06-15  ',
            arrival_time: ' 09:30 ',
            departure_time: ' 17:00 ',
            animals: [{ species: 'African Lion' }],
            attractions: [{ name: 'Conservation Carousel' }],
            guardians_talks: [{ name: 'Amur Tiger' }],
            wild_encounters: [{ name: 'African Rainforest' }],
            events: [{ event_type: 'lunch', start_time: '12:00 PM', end_time: '12:40 PM' }],
         },
         ..._mockItineraryConfigResponse(),
         ..._mockItineraryPathResponse(),
      });
   };

   assert.deepEqual(await ItineraryClient.getItineraryRequest(), {
      ..._normalizedItineraryResultFields('success'),
      itinerary: {
         date: '2026-06-15',
         arrivalTime: '09:30',
         departureTime: '17:00',
         selectedExhibits: [],
         animals: [{ species: 'African Lion' }],
         attractions: [{ name: 'Conservation Carousel' }],
         guardiansTalks: [{ name: 'Amur Tiger' }],
         wildEncounters: [{ name: 'African Rainforest' }],
         transportations: [],
         transportationStations: [],
         events: [{ event_type: 'lunch', start_time: '12:00 PM', end_time: '12:40 PM' }],
      },
      itineraryPath: _normalizedItineraryPath({
         stops: [
            {
               scheduleItemKind: 'animals',
               itemKey: 'African Lion||Africa Savanna',
               walkNodeId: 'v-0255',
               startTime: '10:00 AM',
               endTime: '10:30 AM',
            },
         ],
         legs: [
            {
               fromItemKey: 'arrival',
               toItemKey: 'African Lion||Africa Savanna',
               fromScheduleItemKind: 'visit_boundary',
               toScheduleItemKind: 'animals',
               nodeIds: ['n-0001', 'n-0002'],
            },
         ],
         points: [
            {
               nodeId: 'n-0001',
               x: 1.5,
               y: 2.5,
               xPx: 150,
               yPx: 250,
            },
         ],
      }),
      itineraryConfig: _normalizedItineraryConfig(),
   });
});

test('Test_SetItineraryRequest_TestMissingPath_ExpectEmptyArrays', async () => {
   globalThis.fetch = async () => mockJsonResponse({
      status: 'success',
      itinerary: {
         date: '2026-06-15',
         animals: [],
      },
      ..._mockItineraryConfigResponse(),
   });

   assert.deepEqual(
      (await ItineraryClient.setItineraryRequest({ date: '2026-06-15' })).itineraryPath,
      _normalizedItineraryPath()
   );
});

test('Test_SetItineraryRequest_TestFailurePayload_ExpectItineraryKept', async () => {
   globalThis.fetch = async () => mockJsonResponse({
      success: false,
      status: 'arrivalDepartureTooClose',
      itinerary: {
         date: '2026-06-15',
         animals: 'African Lion',
         attractions: [{ name: 'Conservation Carousel' }],
      },
      ..._mockItineraryConfigResponse(),
   });

   assert.deepEqual(await ItineraryClient.setItineraryRequest({ date: '2026-06-15' }), {
      ..._normalizedItineraryResultFields('arrivalDepartureTooClose'),
      itinerary: {
         date: '2026-06-15',
         arrivalTime: '',
         departureTime: '',
         selectedExhibits: [],
         animals: [],
         attractions: [{ name: 'Conservation Carousel' }],
         guardiansTalks: [],
         wildEncounters: [],
         transportations: [],
         transportationStations: [],
         events: [],
      },
      itineraryPath: _normalizedItineraryPath(),
      itineraryConfig: _normalizedItineraryConfig(),
   });
});

test('Test_SetItineraryArrivalTimeRequest_TestFocusedEndpoints_ExpectNormalized', async () => {
   const calls = [];

   globalThis.fetch = async (url, options) => {
      calls.push([url, JSON.parse(options.body)]);
      return mockJsonResponse({
         status: 'success',
         ..._mockItineraryConfigResponse(),
      });
   };

   assert.deepEqual(await ItineraryClient.setItineraryArrivalTimeRequest(' 09:45 '), {
      ..._normalizedItineraryResultFields('success'),
      itineraryConfig: _normalizedItineraryConfig(),
   });
   assert.deepEqual(await ItineraryClient.setItineraryDepartureTimeRequest(''), {
      ..._normalizedItineraryResultFields('success'),
      itineraryConfig: _normalizedItineraryConfig(),
   });
   assert.deepEqual(calls, [
      [
         '/set-itinerary-arrival-time',
         {
            arrivalTime: '09:45',
            confirmingShortVisit: false,
            confirmingEarlyAdmission: false,
         },
      ],
      [
         '/set-itinerary-departure-time',
         {
            departureTime: '',
            confirmingShortVisit: false,
         },
      ],
   ]);
});

test('Test_SuppressItineraryWarningRequest_TestWarningType_ExpectPosted', async () => {
   globalThis.fetch = async (url, options) => {
      assert.equal(url, '/suppress-itinerary-warning');
      assert.deepEqual(JSON.parse(options.body), {
         warningType: 'arrivalDepartureTooClose',
      });

      return mockJsonResponse({
         status: 'success',
         suppressed_warnings: [],
         ..._mockItineraryConfigResponse({
            suppressedErrorTypes: ['arrivalDepartureTooClose'],
         }),
      });
   };

   assert.deepEqual(
      await ItineraryClient.suppressItineraryWarningRequest('arrivalDepartureTooClose'),
      {
         ..._normalizedItineraryResultFields('success'),
         itineraryConfig: _normalizedItineraryConfig({
            suppressedErrorTypes: ['arrivalDepartureTooClose'],
         }),
      }
   );
});

test('Test_SetItineraryArrivalTimeRequest_TestSuppressedWarnings_ExpectNormalized', async () => {
   globalThis.fetch = async () => mockJsonResponse({
      status: 'success',
      suppressed_warnings: ['arrivalDepartureTooClose'],
      ..._mockItineraryConfigResponse(),
   });

   assert.deepEqual(await ItineraryClient.setItineraryArrivalTimeRequest('09:45'), {
      ..._normalizedItineraryResultFields('success'),
      suppressedWarnings: ['arrivalDepartureTooClose'],
      itineraryConfig: _normalizedItineraryConfig(),
   });
});

test('Test_SetItineraryRequest_TestAdjustments_ExpectNormalized', async () => {
   globalThis.fetch = async () => mockJsonResponse({
      status: 'success',
      reasons: [],
      adjustments: [
         {
            type: 'arrivalTimeAdjusted',
            field: 'arrivalTime',
            previous_value: '09:00',
            value: '09:30',
            reason: 'arrivalOutsideAdmissionHours',
         },
      ],
      itinerary: {
         date: '2026-06-22',
         arrival_time: '09:30',
         animals: [],
         attractions: [],
         guardians_talks: [],
         wild_encounters: [],
      },
      ..._mockItineraryConfigResponse(),
   });

   const result = await ItineraryClient.setItineraryRequest({
      date: '2026-06-22',
      arrivalTime: '09:00',
      departureTime: '17:00',
      animals: [],
      attractions: [],
      guardiansTalks: [],
      wildEncounters: [],
   });

   assert.deepEqual(result.adjustments, [
      {
         type: 'arrivalTimeAdjusted',
         field: 'arrivalTime',
         previousValue: '09:00',
         value: '09:30',
         reason: 'arrivalOutsideAdmissionHours',
      },
   ]);
   assert.equal(result.itinerary.arrivalTime, '09:30');
});

test('Test_SetItineraryArrivalTimeRequest_TestShortVisit_ExpectWarning', async () => {
   globalThis.fetch = async () => mockJsonResponse({
      success: false,
      status: 'arrivalDepartureTooClose',
      ..._mockItineraryConfigResponse(),
   });

   assert.deepEqual(await ItineraryClient.setItineraryArrivalTimeRequest('11:35', {
      confirmingShortVisit: true,
   }), {
      ..._normalizedItineraryResultFields('arrivalDepartureTooClose'),
      itineraryConfig: _normalizedItineraryConfig(),
   });
});

test('Test_AcceptItineraryRequest_TestResponse_ExpectNormalized', async () => {
   globalThis.fetch = async (url, options) => {
      assert.equal(url, '/accept-itinerary');
      assert.equal(options.method, 'POST');
      assert.deepEqual(JSON.parse(options.body), {
         animalsToKeep: [],
         attractionsToKeep: [],
      });

      return mockJsonResponse({
         success: true,
         reasons: [
            {
               code: 'wildEncounterTimeConflict',
               items: [
                  {
                     name: 'African Rainforest',
                     start_time: '14:00',
                     end_time: '14:45',
                     meeting_spot: 'Wild Encounter - Africa Meeting Spot',
                     link: 'https://www.torontozoo.com/tickets/weafricarainforest',
                  },
                  {
                     name: 'Kangaroo',
                     start_time: '14:30',
                     end_time: '15:15',
                     meeting_spot: 'Wild Encounter - Eurasia Meeting Spot',
                     link: 'https://www.torontozoo.com/tickets/wekangaroo',
                  },
               ],
            },
         ],
         itinerary: {
            date: '2026-06-15',
            animals: [],
            attractions: [],
            guardians_talks: [],
            wild_encounters: [],
         },
         ..._mockItineraryConfigResponse(),
      });
   };

   assert.deepEqual(await ItineraryClient.acceptItineraryRequest(), {
      ..._normalizedItineraryResultFields('success', [
         {
            code: 'wildEncounterTimeConflict',
            type: 'wildEncounterTimeConflict',
            items: [
               {
                  name: 'African Rainforest',
                  start_time: '14:00',
                  end_time: '14:45',
                  meeting_spot: 'Wild Encounter - Africa Meeting Spot',
                  link: 'https://www.torontozoo.com/tickets/weafricarainforest',
               },
               {
                  name: 'Kangaroo',
                  start_time: '14:30',
                  end_time: '15:15',
                  meeting_spot: 'Wild Encounter - Eurasia Meeting Spot',
                  link: 'https://www.torontozoo.com/tickets/wekangaroo',
               },
            ],
         },
      ]),
      itinerary: {
         date: '2026-06-15',
         arrivalTime: '',
         departureTime: '',
         selectedExhibits: [],
         animals: [],
         attractions: [],
         guardiansTalks: [],
         wildEncounters: [],
         transportations: [],
         transportationStations: [],
         events: [],
      },
      itineraryPath: _normalizedItineraryPath(),
      itineraryConfig: _normalizedItineraryConfig(),
   });
});

test('Test_GetItineraryRequest_TestConfig_ExpectNormalized', async () => {
   globalThis.fetch = async () => mockJsonResponse({
      itinerary: {
         date: '2026-06-15',
         arrivalTime: '',
         departureTime: '',
         animals: [],
         attractions: [],
         guardians_talks: [],
         wild_encounters: [],
      },
      ..._mockItineraryConfigResponse({
         animalVisibilityChangeThreshold: 25,
         itineraryAnimalMinLikelihood: 40,
         eventTypes: [
            'arrival',
            'breakfast',
            'break',
            'departure',
            'dinner',
            'lunch',
            'shopping',
            'snack',
         ],
      }),
   });

   assert.deepEqual(await ItineraryClient.getItineraryRequest(), {
      ..._normalizedItineraryResultFields('success'),
      itinerary: {
         date: '2026-06-15',
         arrivalTime: '',
         departureTime: '',
         selectedExhibits: [],
         animals: [],
         attractions: [],
         guardiansTalks: [],
         wildEncounters: [],
         transportations: [],
         transportationStations: [],
         events: [],
      },
      itineraryPath: _normalizedItineraryPath(),
      itineraryConfig: _normalizedItineraryConfig({
         animalVisibilityChangeThreshold: 25,
         itineraryAnimalMinLikelihood: 40,
         eventTypes: [
            'arrival',
            'breakfast',
            'break',
            'departure',
            'dinner',
            'lunch',
            'shopping',
            'snack',
         ],
      }),
   });
});

test('Test_GetZooHoursRequest_TestResponse_ExpectNormalized', async () => {
   globalThis.fetch = async (url, options) => {
      assert.equal(url, '/get-zoo-hours');
      assert.equal(options.method, 'POST');
      assert.deepEqual(JSON.parse(options.body), {
         day: 20,
         month: 'JUN',
         year: 2026,
      });

      return mockJsonResponse({
         hours: {
            date: '  2026-06-20  ',
            earlyAdmissionTime: ' 09:00 ',
            openTime: ' 09:30 ',
            lastAdmissionTime: ' 18:00',
            closeTime: '19:00 ',
         },
      });
   };

   assert.deepEqual(
      await ItineraryClient.getZooHoursRequest({ day: 20, month: 'JUN', year: 2026 }),
      {
      hours: {
         date: '2026-06-20',
         earlyAdmissionTime: '09:00',
         openTime: '09:30',
         lastAdmissionTime: '18:00',
         closeTime: '19:00',
      },
   });
});

test('Test_UnscheduleItineraryItemRequest_TestResponse_ExpectNormalized', async () => {
   globalThis.fetch = async (url, options) => {
      assert.equal(url, '/unschedule-itinerary-item');
      assert.deepEqual(JSON.parse(options.body), {
         itemType: 'animals',
         key: 'African Lion||Africa Savanna',
      });

      return mockJsonResponse({
         status: 'success',
      });
   };

   assert.deepEqual(
      await ItineraryClient.unscheduleItineraryItemRequest({
         itemType: 'animals',
         key: 'African Lion||Africa Savanna',
      }),
      _normalizedItineraryResultFields('success')
   );
});

test('Test_RemoveItemFromItineraryRequest_TestResponse_ExpectNormalized', async () => {
   globalThis.fetch = async (url, options) => {
      assert.equal(url, '/remove-item-from-itinerary');
      assert.deepEqual(JSON.parse(options.body), {
         itemType: 'attractions',
         key: 'Conservation Carousel',
      });

      return mockJsonResponse({
         status: 'success',
      });
   };

   assert.deepEqual(
      await ItineraryClient.removeItemFromItineraryRequest({
         itemType: 'attractions',
         key: 'Conservation Carousel',
      }),
      _normalizedItineraryResultFields('success')
   );
});

test('Test_ScheduleItineraryItemRequest_TestResponse_ExpectNormalized', async () => {
   globalThis.fetch = async (url, options) => {
      assert.equal(url, '/schedule-itinerary-item');
      assert.deepEqual(JSON.parse(options.body), {
         itemType: 'lunch',
         key: '',
         confirmingScheduleItemNotOnItinerary: false,
         confirmingAttractionOutsideOperatingHours: false,
         confirmingGuardiansTalkUnschedule: false,
         confirmingWildEncounterUnschedule: false,
         confirmingFixedTimeItemLongWait: false,
         confirmingGuardiansTalkWithoutAnimal: false,
      });

      return mockJsonResponse({
         status: 'noAvailableSlot',
      });
   };

   assert.deepEqual(
      await ItineraryClient.scheduleItineraryItemRequest({ itemType: 'lunch', key: '' }),
      _normalizedItineraryResultFields('noAvailableSlot')
   );
});

test('Test_BulkScheduleItineraryRequest_TestAnimals_ExpectNormalized', async () => {
   globalThis.fetch = async (url, options) => {
      assert.equal(url, '/bulk-schedule-itinerary');
      assert.deepEqual(JSON.parse(options.body), {
         temp: true,
         confirmingFixedTimeItemLongWait: false,
      });

      return mockJsonResponse({
         status: 'success',
         reasons: [
            {
               code: 'bulkScheduleItineraryNotEnoughTime',
               items: [
                  {
                     name: 'African Lion',
                     location: 'Africa Savanna',
                     item_type: ItinerarySaveIssueItemType.ANIMAL,
                  },
               ],
            },
         ],
         itinerary: {
            date: '2026-06-20',
            arrival_time: '9:30 AM',
            departure_time: '5:00 PM',
            animals: [
               {
                  species: 'African Lion',
                  exhibit: 'Africa Savanna',
                  start_time: '',
                  end_time: '',
               },
            ],
            attractions: [],
            guardians_talks: [],
            wild_encounters: [],
            events: [],
         },
         ..._mockItineraryConfigResponse(),
      });
   };

   const result = await ItineraryClient.bulkScheduleItineraryRequest(true);

   assert.equal(result.status, 'success');
   assert.equal(result.reasons.length, 1);
   assert.equal(result.reasons[0].code, 'bulkScheduleItineraryNotEnoughTime');
   assert.equal(result.itinerary.animals.length, 1);
   assert.equal(result.itinerary.animals[0].species, 'African Lion');
});

test('Test_UnscheduleAllItineraryItemsRequest_TestResponse_ExpectNormalized', async () => {
   globalThis.fetch = async (url, options) => {
      assert.equal(url, '/unschedule-all-itinerary-items');
      assert.deepEqual(JSON.parse(options.body), { temp: true });

      return mockJsonResponse({
         status: 'success',
         itinerary: {
            date: '2026-06-20',
            arrival_time: '9:30 AM',
            departure_time: '5:00 PM',
            animals: [],
            attractions: [],
            guardians_talks: [],
            wild_encounters: [],
            events: [],
         },
         ..._mockItineraryConfigResponse(),
      });
   };

   const result = await ItineraryClient.unscheduleAllItineraryItemsRequest(true);

   assert.equal(result.status, 'success');
   assert.equal(result.itinerary.date, '2026-06-20');
});
