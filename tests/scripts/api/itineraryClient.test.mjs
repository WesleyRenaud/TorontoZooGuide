import assert from 'node:assert/strict';
import { afterEach, test } from 'node:test';

import { ItineraryClient } from '../../../scripts/api/itineraryClient.js';
import { mockJsonResponse } from '../helpers/fetchMock.mjs';
import { ItineraryAdjustmentType } from '../../../scripts/shared/enums/itineraryAdjustmentType.js';
import { ItineraryErrorType } from '../../../scripts/shared/enums/itineraryErrorType.js';
import { ItineraryPathModel } from '../../../scripts/itinerary/itineraryPathModel.js';
import { ItinerarySaveIssueItemType } from '../../../scripts/shared/enums/itinerarySaveIssueItemType.js';
import { Position } from '../../../scripts/shared/enums/position.js';
import { ScheduleItemKind } from '../../../scripts/shared/enums/scheduleItemKind.js';

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

function _mockItineraryPathResponse(overrides = {}) {
   return {
      itinerary_path: {
         stops: overrides.stops ?? [
            {
               schedule_item_kind: ScheduleItemKind.ANIMAL.itemType,
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
               to_schedule_item_kind: ScheduleItemKind.ANIMAL.itemType,
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
   const date = null;
   globalThis.fetch = async () => mockJsonResponse({ date });

   const result = await ItineraryClient.getItineraryDateRequest();

   assert.deepEqual(result, { date });
});


test('Test_GetItineraryDateRequest_TestStoredDate_ExpectNormalized', async () => {
   const date = '2026-06-15';
   const url = '/get-itinerary-date';
   globalThis.fetch = async (requestedUrl, options) => {
      assert.equal(requestedUrl, url);
      assert.equal(options.method, 'POST');
      assert.deepEqual(JSON.parse(options.body), {});

      return mockJsonResponse({
         date: `  ${date}  `,
      });
   };

   const result = await ItineraryClient.getItineraryDateRequest();

   assert.deepEqual(result, { date });
});


test('Test_GetItineraryRequest_TestSnakeCaseKeys_ExpectNormalized', async () => {
   const date = '2026-06-15';
   const arrivalTime = '09:30';
   const departureTime = '17:00';
   const animal = { species: 'African Lion' };
   const attraction = { name: 'Conservation Carousel' };
   const guardiansTalk = { name: 'Amur Tiger' };
   const wildEncounter = { name: 'African Rainforest' };
   const lunchEvent = { event_type: 'lunch', start_time: '12:00 PM', end_time: '12:40 PM' };
   const url = '/get-itinerary';
   const pathResponse = _mockItineraryPathResponse();
   globalThis.fetch = async (requestedUrl, options) => {
      assert.equal(requestedUrl, url);
      assert.equal(options.method, 'POST');
      assert.deepEqual(JSON.parse(options.body), {});

      return mockJsonResponse({
         success: true,
         error: '',
         itinerary: {
            date: `  ${date}  `,
            arrival_time: ` ${arrivalTime} `,
            departure_time: ` ${departureTime} `,
            animals: [animal],
            attractions: [attraction],
            guardians_talks: [guardiansTalk],
            wild_encounters: [wildEncounter],
            events: [lunchEvent],
         },
         ..._mockItineraryConfigResponse(),
         ...pathResponse,
      });
   };

   const result = await ItineraryClient.getItineraryRequest();

   assert.deepEqual(result, {
      ..._normalizedItineraryResultFields(ItineraryErrorType.SUCCESS),
      itinerary: {
         date,
         arrivalTime,
         departureTime,
         selectedExhibits: [],
         animals: [animal],
         attractions: [attraction],
         guardiansTalks: [guardiansTalk],
         wildEncounters: [wildEncounter],
         transportations: [],
         transportationStations: [],
         events: [lunchEvent],
      },
      itineraryPath: ItineraryPathModel.normalizeItineraryPath(pathResponse.itinerary_path),
      itineraryConfig: _normalizedItineraryConfig(),
   });
});


test('Test_SetItineraryRequest_TestMissingPath_ExpectEmptyArrays', async () => {
   const date = '2026-06-15';
   globalThis.fetch = async () => mockJsonResponse({
      status: ItineraryErrorType.SUCCESS,
      itinerary: {
         date,
         animals: [],
      },
      ..._mockItineraryConfigResponse(),
   });

   const result = await ItineraryClient.setItineraryRequest({ date });

   assert.deepEqual(result.itineraryPath, ItineraryPathModel.EMPTY_ITINERARY_PATH);
});


test('Test_SetItineraryRequest_TestFailurePayload_ExpectItineraryKept', async () => {
   const date = '2026-06-15';
   const status = ItineraryErrorType.ARRIVAL_DEPARTURE_TOO_CLOSE;
   const attraction = { name: 'Conservation Carousel' };
   globalThis.fetch = async () => mockJsonResponse({
      success: false,
      status,
      itinerary: {
         date,
         animals: 'African Lion',
         attractions: [attraction],
      },
      ..._mockItineraryConfigResponse(),
   });

   const result = await ItineraryClient.setItineraryRequest({ date });

   assert.deepEqual(result, {
      ..._normalizedItineraryResultFields(status),
      itinerary: {
         date,
         arrivalTime: '',
         departureTime: '',
         selectedExhibits: [],
         animals: [],
         attractions: [attraction],
         guardiansTalks: [],
         wildEncounters: [],
         transportations: [],
         transportationStations: [],
         events: [],
      },
      itineraryPath: ItineraryPathModel.EMPTY_ITINERARY_PATH,
      itineraryConfig: _normalizedItineraryConfig(),
   });
});


test('Test_SetItineraryArrivalTimeRequest_TestTrimmedTime_ExpectNormalized', async () => {
   const arrivalTime = '09:45';
   const status = ItineraryErrorType.SUCCESS;
   const url = '/set-itinerary-arrival-time';
   const calls = [];
   globalThis.fetch = async (requestedUrl, options) => {
      calls.push([requestedUrl, JSON.parse(options.body)]);
      return mockJsonResponse({
         status,
         ..._mockItineraryConfigResponse(),
      });
   };

   const result = await ItineraryClient.setItineraryArrivalTimeRequest(` ${arrivalTime} `);

   assert.deepEqual(result, {
      ..._normalizedItineraryResultFields(status),
      itineraryConfig: _normalizedItineraryConfig(),
   });
   assert.deepEqual(calls, [
      [
         url,
         {
            arrivalTime,
            confirmingShortVisit: false,
            confirmingEarlyAdmission: false,
            confirmingVisitWindowOverflow: false,
            keptVisitWindowOverflowItems: [],
         },
      ],
   ]);
});


test('Test_SetItineraryDepartureTimeRequest_TestEmptyTime_ExpectNormalized', async () => {
   const departureTime = '';
   const status = ItineraryErrorType.SUCCESS;
   const url = '/set-itinerary-departure-time';
   const calls = [];
   globalThis.fetch = async (requestedUrl, options) => {
      calls.push([requestedUrl, JSON.parse(options.body)]);
      return mockJsonResponse({
         status,
         ..._mockItineraryConfigResponse(),
      });
   };

   const result = await ItineraryClient.setItineraryDepartureTimeRequest(departureTime);

   assert.deepEqual(result, {
      ..._normalizedItineraryResultFields(status),
      itineraryConfig: _normalizedItineraryConfig(),
   });
   assert.deepEqual(calls, [
      [
         url,
         {
            departureTime,
            confirmingShortVisit: false,
            confirmingVisitWindowOverflow: false,
            keptVisitWindowOverflowItems: [],
         },
      ],
   ]);
});


test('Test_SuppressItineraryWarningRequest_TestWarningType_ExpectPosted', async () => {
   const warningType = ItineraryErrorType.ARRIVAL_DEPARTURE_TOO_CLOSE;
   const status = ItineraryErrorType.SUCCESS;
   const url = '/suppress-itinerary-warning';
   globalThis.fetch = async (requestedUrl, options) => {
      assert.equal(requestedUrl, url);
      assert.deepEqual(JSON.parse(options.body), {
         warningType,
      });

      return mockJsonResponse({
         status,
         suppressed_warnings: [],
         ..._mockItineraryConfigResponse({
            suppressedErrorTypes: [warningType],
         }),
      });
   };

   const result = await ItineraryClient.suppressItineraryWarningRequest(warningType);

   assert.deepEqual(result, {
      ..._normalizedItineraryResultFields(status),
      itineraryConfig: _normalizedItineraryConfig({
         suppressedErrorTypes: [warningType],
      }),
   });
});


test('Test_UnsuppressItineraryWarningRequest_TestWarningType_ExpectPosted', async () => {
   const warningType = ItineraryErrorType.ARRIVAL_DEPARTURE_TOO_CLOSE;
   const status = ItineraryErrorType.SUCCESS;
   const url = '/unsuppress-itinerary-warning';
   globalThis.fetch = async (requestedUrl, options) => {
      assert.equal(requestedUrl, url);
      assert.deepEqual(JSON.parse(options.body), {
         warningType,
      });

      return mockJsonResponse({
         status,
         suppressed_warnings: [],
         ..._mockItineraryConfigResponse(),
      });
   };

   const result = await ItineraryClient.unsuppressItineraryWarningRequest(warningType);

   assert.deepEqual(result, {
      ..._normalizedItineraryResultFields(status),
      itineraryConfig: _normalizedItineraryConfig(),
   });
});


test('Test_SetItineraryArrivalTimeRequest_TestSuppressedWarnings_ExpectNormalized', async () => {
   const arrivalTime = '09:45';
   const status = ItineraryErrorType.SUCCESS;
   const warningType = ItineraryErrorType.ARRIVAL_DEPARTURE_TOO_CLOSE;
   globalThis.fetch = async () => mockJsonResponse({
      status,
      suppressed_warnings: [warningType],
      ..._mockItineraryConfigResponse(),
   });

   const result = await ItineraryClient.setItineraryArrivalTimeRequest(arrivalTime);

   assert.deepEqual(result, {
      ..._normalizedItineraryResultFields(status),
      suppressedWarnings: [warningType],
      itineraryConfig: _normalizedItineraryConfig(),
   });
});


test('Test_SetItineraryRequest_TestAdjustments_ExpectNormalized', async () => {
   const date = '2026-06-22';
   const previousArrivalTime = '09:00';
   const arrivalTime = '09:30';
   const departureTime = '17:00';
   const status = ItineraryErrorType.SUCCESS;
   const adjustmentType = ItineraryAdjustmentType.ARRIVAL_TIME_ADJUSTED;
   const field = 'arrivalTime';
   const reason = 'arrivalOutsideAdmissionHours';
   globalThis.fetch = async () => mockJsonResponse({
      status,
      reasons: [],
      adjustments: [
         {
            type: adjustmentType,
            field,
            previous_value: previousArrivalTime,
            value: arrivalTime,
            reason,
         },
      ],
      itinerary: {
         date,
         arrival_time: arrivalTime,
         animals: [],
         attractions: [],
         guardians_talks: [],
         wild_encounters: [],
      },
      ..._mockItineraryConfigResponse(),
   });

   const result = await ItineraryClient.setItineraryRequest({
      date,
      arrivalTime: previousArrivalTime,
      departureTime,
      animals: [],
      attractions: [],
      guardiansTalks: [],
      wildEncounters: [],
   });

   assert.deepEqual(result.adjustments, [
      {
         type: adjustmentType,
         field,
         previousValue: previousArrivalTime,
         value: arrivalTime,
         reason,
      },
   ]);
   assert.equal(result.itinerary.arrivalTime, arrivalTime);
});


test('Test_SetItineraryArrivalTimeRequest_TestShortVisit_ExpectWarning', async () => {
   const arrivalTime = '11:35';
   const status = ItineraryErrorType.ARRIVAL_DEPARTURE_TOO_CLOSE;
   const confirmingShortVisit = true;
   globalThis.fetch = async () => mockJsonResponse({
      success: false,
      status,
      ..._mockItineraryConfigResponse(),
   });

   const result = await ItineraryClient.setItineraryArrivalTimeRequest(arrivalTime, {
      confirmingShortVisit,
   });

   assert.deepEqual(result, {
      ..._normalizedItineraryResultFields(status),
      itineraryConfig: _normalizedItineraryConfig(),
   });
});


test('Test_AcceptItineraryRequest_TestResponse_ExpectNormalized', async () => {
   const date = '2026-06-15';
   const status = ItineraryErrorType.SUCCESS;
   const code = ItineraryErrorType.WILD_ENCOUNTER_TIME_CONFLICT;
   const rainforest = 'African Rainforest';
   const rainforestStart = '14:00';
   const rainforestEnd = '14:45';
   const rainforestSpot = 'Wild Encounter - Africa Meeting Spot';
   const rainforestLink = 'https://www.torontozoo.com/tickets/weafricarainforest';
   const kangaroo = 'Kangaroo';
   const kangarooStart = '14:30';
   const kangarooEnd = '15:15';
   const kangarooSpot = 'Wild Encounter - Eurasia Meeting Spot';
   const kangarooLink = 'https://www.torontozoo.com/tickets/wekangaroo';
   const url = '/accept-itinerary';
   const rainforestItem = {
      name: rainforest,
      start_time: rainforestStart,
      end_time: rainforestEnd,
      meeting_spot: rainforestSpot,
      link: rainforestLink,
   };
   const kangarooItem = {
      name: kangaroo,
      start_time: kangarooStart,
      end_time: kangarooEnd,
      meeting_spot: kangarooSpot,
      link: kangarooLink,
   };
   globalThis.fetch = async (requestedUrl, options) => {
      assert.equal(requestedUrl, url);
      assert.equal(options.method, 'POST');
      assert.deepEqual(JSON.parse(options.body), {
         animalsToKeep: [],
         attractionsToKeep: [],
      });

      return mockJsonResponse({
         success: true,
         reasons: [
            {
               code,
               items: [rainforestItem, kangarooItem],
            },
         ],
         itinerary: {
            date,
            animals: [],
            attractions: [],
            guardians_talks: [],
            wild_encounters: [],
         },
         ..._mockItineraryConfigResponse(),
      });
   };

   const result = await ItineraryClient.acceptItineraryRequest();

   assert.deepEqual(result, {
      ..._normalizedItineraryResultFields(status, [
         {
            code,
            type: code,
            items: [rainforestItem, kangarooItem],
         },
      ]),
      itinerary: {
         date,
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
      itineraryPath: ItineraryPathModel.EMPTY_ITINERARY_PATH,
      itineraryConfig: _normalizedItineraryConfig(),
   });
});


test('Test_GetItineraryRequest_TestConfig_ExpectNormalized', async () => {
   const date = '2026-06-15';
   const emptyTime = '';
   const visibilityThreshold = 25;
   const minLikelihood = 40;
   const eventTypes = [
      'arrival',
      'breakfast',
      'break',
      'departure',
      'dinner',
      'lunch',
      'shopping',
      'snack',
   ];
   globalThis.fetch = async () => mockJsonResponse({
      itinerary: {
         date,
         arrivalTime: emptyTime,
         departureTime: emptyTime,
         animals: [],
         attractions: [],
         guardians_talks: [],
         wild_encounters: [],
      },
      ..._mockItineraryConfigResponse({
         animalVisibilityChangeThreshold: visibilityThreshold,
         itineraryAnimalMinLikelihood: minLikelihood,
         eventTypes,
      }),
   });

   const result = await ItineraryClient.getItineraryRequest();

   assert.deepEqual(result, {
      ..._normalizedItineraryResultFields(ItineraryErrorType.SUCCESS),
      itinerary: {
         date,
         arrivalTime: emptyTime,
         departureTime: emptyTime,
         selectedExhibits: [],
         animals: [],
         attractions: [],
         guardiansTalks: [],
         wildEncounters: [],
         transportations: [],
         transportationStations: [],
         events: [],
      },
      itineraryPath: ItineraryPathModel.EMPTY_ITINERARY_PATH,
      itineraryConfig: _normalizedItineraryConfig({
         animalVisibilityChangeThreshold: visibilityThreshold,
         itineraryAnimalMinLikelihood: minLikelihood,
         eventTypes,
      }),
   });
});


test('Test_GetZooHoursRequest_TestResponse_ExpectNormalized', async () => {
   const day = 20;
   const month = 'JUN';
   const year = 2026;
   const date = '2026-06-20';
   const earlyAdmissionTime = '09:00';
   const openTime = '09:30';
   const lastAdmissionTime = '18:00';
   const closeTime = '19:00';
   const url = '/get-zoo-hours';
   const request = { day, month, year };
   globalThis.fetch = async (requestedUrl, options) => {
      assert.equal(requestedUrl, url);
      assert.equal(options.method, 'POST');
      assert.deepEqual(JSON.parse(options.body), request);

      return mockJsonResponse({
         hours: {
            date: `  ${date}  `,
            earlyAdmissionTime: ` ${earlyAdmissionTime} `,
            openTime: ` ${openTime} `,
            lastAdmissionTime: ` ${lastAdmissionTime}`,
            closeTime: `${closeTime} `,
         },
      });
   };

   const result = await ItineraryClient.getZooHoursRequest(request);

   assert.deepEqual(result, {
      hours: {
         date,
         earlyAdmissionTime,
         openTime,
         lastAdmissionTime,
         closeTime,
      },
   });
});


test('Test_UnscheduleItineraryItemRequest_TestResponse_ExpectNormalized', async () => {
   const itemType = ScheduleItemKind.ANIMAL.itemType;
   const key = 'African Lion||Africa Savanna';
   const status = ItineraryErrorType.SUCCESS;
   const url = '/unschedule-itinerary-item';
   const request = { itemType, key };
   globalThis.fetch = async (requestedUrl, options) => {
      assert.equal(requestedUrl, url);
      assert.deepEqual(JSON.parse(options.body), request);

      return mockJsonResponse({
         status,
      });
   };

   const result = await ItineraryClient.unscheduleItineraryItemRequest(request);

   assert.deepEqual(result, _normalizedItineraryResultFields(status));
});


test('Test_RemoveItemFromItineraryRequest_TestResponse_ExpectNormalized', async () => {
   const itemType = ScheduleItemKind.ATTRACTION.itemType;
   const key = 'Conservation Carousel';
   const status = ItineraryErrorType.SUCCESS;
   const url = '/remove-item-from-itinerary';
   const request = { itemType, key };
   globalThis.fetch = async (requestedUrl, options) => {
      assert.equal(requestedUrl, url);
      assert.deepEqual(JSON.parse(options.body), request);

      return mockJsonResponse({
         status,
      });
   };

   const result = await ItineraryClient.removeItemFromItineraryRequest(request);

   assert.deepEqual(result, _normalizedItineraryResultFields(status));
});


test('Test_ScheduleItineraryItemRequest_TestResponse_ExpectNormalized', async () => {
   const itemType = 'lunch';
   const key = '';
   const status = ItineraryErrorType.NO_AVAILABLE_SLOT;
   const url = '/schedule-itinerary-item';
   const request = { itemType, key };
   globalThis.fetch = async (requestedUrl, options) => {
      assert.equal(requestedUrl, url);
      assert.deepEqual(JSON.parse(options.body), {
         itemType,
         key,
         confirmingScheduleItemNotOnItinerary: false,
         confirmingAttractionOutsideOperatingHours: false,
         confirmingGuardiansTalkUnschedule: false,
         confirmingWildEncounterUnschedule: false,
         confirmingFixedTimeItemLongWait: false,
         confirmingGuardiansTalkWithoutAnimal: false,
      });

      return mockJsonResponse({
         status,
      });
   };

   const result = await ItineraryClient.scheduleItineraryItemRequest(request);

   assert.deepEqual(result, _normalizedItineraryResultFields(status));
});


test('Test_BulkScheduleItineraryRequest_TestAnimals_ExpectNormalized', async () => {
   const temp = true;
   const status = ItineraryErrorType.SUCCESS;
   const code = ItineraryErrorType.BULK_SCHEDULE_ITINERARY_NOT_ENOUGH_TIME;
   const species = 'African Lion';
   const exhibit = 'Africa Savanna';
   const date = '2026-06-20';
   const url = '/bulk-schedule-itinerary';
   globalThis.fetch = async (requestedUrl, options) => {
      assert.equal(requestedUrl, url);
      assert.deepEqual(JSON.parse(options.body), {
         temp,
         confirmingFixedTimeItemLongWait: false,
      });

      return mockJsonResponse({
         status,
         reasons: [
            {
               code,
               items: [
                  {
                     name: species,
                     location: exhibit,
                     item_type: ItinerarySaveIssueItemType.ANIMAL,
                  },
               ],
            },
         ],
         itinerary: {
            date,
            arrival_time: '9:30 AM',
            departure_time: '5:00 PM',
            animals: [
               {
                  species,
                  exhibit,
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

   const result = await ItineraryClient.bulkScheduleItineraryRequest(temp);

   assert.equal(result.status, status);
   assert.equal(result.reasons.length, 1);
   assert.equal(result.reasons[Position.FIRST].code, code);
   assert.equal(result.itinerary.animals.length, 1);
   assert.equal(result.itinerary.animals[Position.FIRST].species, species);
});


test('Test_UnscheduleAllItineraryItemsRequest_TestResponse_ExpectNormalized', async () => {
   const temp = true;
   const status = ItineraryErrorType.SUCCESS;
   const date = '2026-06-20';
   const url = '/unschedule-all-itinerary-items';
   globalThis.fetch = async (requestedUrl, options) => {
      assert.equal(requestedUrl, url);
      assert.deepEqual(JSON.parse(options.body), { temp });

      return mockJsonResponse({
         status,
         itinerary: {
            date,
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

   const result = await ItineraryClient.unscheduleAllItineraryItemsRequest(temp);

   assert.equal(result.status, status);
   assert.equal(result.itinerary.date, date);
});
