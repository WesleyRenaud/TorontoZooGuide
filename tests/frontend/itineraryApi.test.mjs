import assert from 'node:assert/strict';
import { afterEach, test } from 'node:test';

import {
   acceptItineraryRequest,
   bulkScheduleAnimalsRequest,
   getItineraryDateRequest,
   getItineraryRequest,
   getZooHoursRequest,
   removeItemFromItineraryRequest,
   scheduleItineraryItemRequest,
   unscheduleItineraryItemRequest,
   unscheduleAllItineraryItemsRequest,
   setItineraryArrivalTimeRequest,
   setItineraryDepartureTimeRequest,
   setItineraryRequest,
   suppressItineraryWarningRequest,
} from '../../scripts/api/itineraryApi.js';
import { mockJsonResponse } from './helpers/fetchMock.mjs';

const MOCK_ITINERARY_ERROR_TYPES = Object.freeze({
   SUCCESS: 'success',
   ITINERARY_DATE_NOT_SET: 'itineraryDateNotSet',
   TIME_OUT_OF_BOUNDS: 'timeOutOfBounds',
   TIME_ORDER_INVALID: 'timeOrderInvalid',
   SAVE_FAILED: 'saveFailed',
   ARRIVAL_DEPARTURE_TOO_CLOSE: 'arrivalDepartureTooClose',
   NO_AVAILABLE_SLOT: 'noAvailableSlot',
   ITEM_NOT_ON_ITINERARY: 'itemNotOnItinerary',
});

function normalizedItineraryConfig(overrides = {}) {
   return {
      animalVisibilityChangeThreshold: overrides.animalVisibilityChangeThreshold,
      itineraryAnimalMinLikelihood: overrides.itineraryAnimalMinLikelihood,
      eventTypes: overrides.eventTypes ?? [],
      visitBoundaryEventTypes: overrides.visitBoundaryEventTypes ?? {
         arrival: 'arrival',
         departure: 'departure',
      },
      errorTypes: overrides.errorTypes ?? MOCK_ITINERARY_ERROR_TYPES,
      adjustmentTypes: overrides.adjustmentTypes ?? {
         ARRIVAL_TIME_ADJUSTED: 'arrivalTimeAdjusted',
         DEPARTURE_TIME_ADJUSTED: 'departureTimeAdjusted',
      },
      statuses: overrides.statuses ?? [],
      suppressedErrorTypes: overrides.suppressedErrorTypes ?? [],
   };
}

function normalizedItineraryResultFields(status, reasons = []) {
   return {
      status,
      reasons,
      adjustments: [],
      errorType: status,
      issues: reasons,
      suppressedWarnings: [],
   };
}

function normalizedItineraryPath(overrides = {}) {
   return {
      stops: overrides.stops ?? [],
      legs: overrides.legs ?? [],
      points: overrides.points ?? [],
   };
}

function mockItineraryPathResponse(overrides = {}) {
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

function mockItineraryConfigResponse(overrides = {}) {
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
         itinerary_error_types: overrides.errorTypes ?? MOCK_ITINERARY_ERROR_TYPES,
         itinerary_adjustment_types: overrides.adjustmentTypes ?? {
            ARRIVAL_TIME_ADJUSTED: 'arrivalTimeAdjusted',
            DEPARTURE_TIME_ADJUSTED: 'departureTimeAdjusted',
         },
         itinerary_statuses: overrides.statuses ?? [],
         suppressed_error_types: overrides.suppressedErrorTypes ?? [],
      },
   };
}

afterEach(() => {
   delete globalThis.fetch;
});

test('normalizes empty itinerary date as null', async () => {
   globalThis.fetch = async () => mockJsonResponse({ date: null });

   assert.deepEqual(await getItineraryDateRequest(), {
      date: null,
   });
});

test('normalizes stored itinerary date response', async () => {
   globalThis.fetch = async (url, options) => {
      assert.equal(url, '/get-itinerary-date');
      assert.equal(options.method, 'POST');
      assert.deepEqual(JSON.parse(options.body), {});

      return mockJsonResponse({
         date: '  2026-06-15  ',
      });
   };

   assert.deepEqual(await getItineraryDateRequest(), {
      date: '2026-06-15',
   });
});

test('normalizes stored itinerary response from snake case backend keys', async () => {
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
         ...mockItineraryConfigResponse(),
         ...mockItineraryPathResponse(),
      });
   };

   assert.deepEqual(await getItineraryRequest(), {
      ...normalizedItineraryResultFields('success'),
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
         events: [{ event_type: 'lunch', start_time: '12:00 PM', end_time: '12:40 PM' }],
      },
      itineraryPath: normalizedItineraryPath({
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
      itineraryConfig: normalizedItineraryConfig(),
   });
});

test('defaults itinerary path to empty arrays when itinerary is returned without itinerary_path', async () => {
   globalThis.fetch = async () => mockJsonResponse({
      status: 'success',
      itinerary: {
         date: '2026-06-15',
         animals: [],
      },
      ...mockItineraryConfigResponse(),
   });

   assert.deepEqual(
      (await setItineraryRequest({ date: '2026-06-15' })).itineraryPath,
      normalizedItineraryPath()
   );
});

test('normalizes set itinerary failures without dropping returned itinerary data', async () => {
   globalThis.fetch = async () => mockJsonResponse({
      success: false,
      status: 'arrivalDepartureTooClose',
      itinerary: {
         date: '2026-06-15',
         animals: 'African Lion',
         attractions: [{ name: 'Conservation Carousel' }],
      },
      ...mockItineraryConfigResponse(),
   });

   assert.deepEqual(await setItineraryRequest({ date: '2026-06-15' }), {
      ...normalizedItineraryResultFields('arrivalDepartureTooClose'),
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
         events: [],
      },
      itineraryPath: normalizedItineraryPath(),
      itineraryConfig: normalizedItineraryConfig(),
   });
});

test('sets itinerary arrival and departure times through focused endpoints', async () => {
   const calls = [];

   globalThis.fetch = async (url, options) => {
      calls.push([url, JSON.parse(options.body)]);
      return mockJsonResponse({
         status: 'success',
         ...mockItineraryConfigResponse(),
      });
   };

   assert.deepEqual(await setItineraryArrivalTimeRequest(' 09:45 '), {
      ...normalizedItineraryResultFields('success'),
      itineraryConfig: normalizedItineraryConfig(),
   });
   assert.deepEqual(await setItineraryDepartureTimeRequest(''), {
      ...normalizedItineraryResultFields('success'),
      itineraryConfig: normalizedItineraryConfig(),
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

test('suppress itinerary warning request posts warning type', async () => {
   globalThis.fetch = async (url, options) => {
      assert.equal(url, '/suppress-itinerary-warning');
      assert.deepEqual(JSON.parse(options.body), {
         warningType: 'arrivalDepartureTooClose',
      });

      return mockJsonResponse({
         status: 'success',
         suppressed_warnings: [],
         ...mockItineraryConfigResponse({
            suppressedErrorTypes: ['arrivalDepartureTooClose'],
         }),
      });
   };

   assert.deepEqual(
      await suppressItineraryWarningRequest('arrivalDepartureTooClose'),
      {
         ...normalizedItineraryResultFields('success'),
         itineraryConfig: normalizedItineraryConfig({
            suppressedErrorTypes: ['arrivalDepartureTooClose'],
         }),
      }
   );
});

test('normalizes suppressed warnings on itinerary results', async () => {
   globalThis.fetch = async () => mockJsonResponse({
      status: 'success',
      suppressed_warnings: ['arrivalDepartureTooClose'],
      ...mockItineraryConfigResponse(),
   });

   assert.deepEqual(await setItineraryArrivalTimeRequest('09:45'), {
      ...normalizedItineraryResultFields('success'),
      suppressedWarnings: ['arrivalDepartureTooClose'],
      itineraryConfig: normalizedItineraryConfig(),
   });
});

test('normalizes itinerary adjustments on save results', async () => {
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
      ...mockItineraryConfigResponse(),
   });

   const result = await setItineraryRequest({
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

test('normalizes short visit warning from itinerary time endpoints', async () => {
   globalThis.fetch = async () => mockJsonResponse({
      success: false,
      status: 'arrivalDepartureTooClose',
      ...mockItineraryConfigResponse(),
   });

   assert.deepEqual(await setItineraryArrivalTimeRequest('11:35', {
      confirmingShortVisit: true,
   }), {
      ...normalizedItineraryResultFields('arrivalDepartureTooClose'),
      itineraryConfig: normalizedItineraryConfig(),
   });
});

test('normalizes accept itinerary response', async () => {
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
         ...mockItineraryConfigResponse(),
      });
   };

   assert.deepEqual(await acceptItineraryRequest(), {
      ...normalizedItineraryResultFields('success', [
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
         events: [],
      },
      itineraryPath: normalizedItineraryPath(),
      itineraryConfig: normalizedItineraryConfig(),
   });
});

test('normalizes itinerary config from itinerary responses', async () => {
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
      ...mockItineraryConfigResponse({
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

   assert.deepEqual(await getItineraryRequest(), {
      ...normalizedItineraryResultFields('success'),
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
         events: [],
      },
      itineraryPath: normalizedItineraryPath(),
      itineraryConfig: normalizedItineraryConfig({
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

test('normalizes zoo hours response', async () => {
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
      await getZooHoursRequest({ day: 20, month: 'JUN', year: 2026 }),
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

test('normalizes unschedule itinerary item response', async () => {
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
      await unscheduleItineraryItemRequest({
         itemType: 'animals',
         key: 'African Lion||Africa Savanna',
      }),
      normalizedItineraryResultFields('success')
   );
});

test('normalizes remove item from itinerary response', async () => {
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
      await removeItemFromItineraryRequest({
         itemType: 'attractions',
         key: 'Conservation Carousel',
      }),
      normalizedItineraryResultFields('success')
   );
});

test('normalizes schedule itinerary item response', async () => {
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
      await scheduleItineraryItemRequest({ itemType: 'lunch', key: '' }),
      normalizedItineraryResultFields('noAvailableSlot')
   );
});

test('normalizes bulk schedule animals response', async () => {
   globalThis.fetch = async (url, options) => {
      assert.equal(url, '/bulk-schedule-animals');
      assert.deepEqual(JSON.parse(options.body), {
         temp: true,
         confirmingFixedTimeItemLongWait: false,
      });

      return mockJsonResponse({
         status: 'success',
         reasons: [
            {
               code: 'bulkScheduleAnimalsNotEnoughTime',
               items: [
                  {
                     name: 'African Lion',
                     location: 'Africa Savanna',
                     item_type: 'animal',
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
         ...mockItineraryConfigResponse(),
      });
   };

   const result = await bulkScheduleAnimalsRequest(true);

   assert.equal(result.status, 'success');
   assert.equal(result.reasons.length, 1);
   assert.equal(result.reasons[0].code, 'bulkScheduleAnimalsNotEnoughTime');
   assert.equal(result.itinerary.animals.length, 1);
   assert.equal(result.itinerary.animals[0].species, 'African Lion');
});

test('normalizes unschedule all itinerary items response', async () => {
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
         ...mockItineraryConfigResponse(),
      });
   };

   const result = await unscheduleAllItineraryItemsRequest(true);

   assert.equal(result.status, 'success');
   assert.equal(result.itinerary.date, '2026-06-20');
});
