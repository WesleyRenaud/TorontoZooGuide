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
   setItineraryArrivalTimeRequest,
   setItineraryDepartureTimeRequest,
   setItineraryRequest,
   suppressItineraryWarningRequest,
} from '../../scripts/api/itineraryApi.js';

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
      eventTypes: overrides.eventTypes ?? [],
      visitBoundaryEventTypes: overrides.visitBoundaryEventTypes ?? {
         arrival: 'arrival',
         departure: 'departure',
      },
      errorTypes: overrides.errorTypes ?? MOCK_ITINERARY_ERROR_TYPES,
      suppressedErrorTypes: overrides.suppressedErrorTypes ?? [],
   };
}

function normalizedItineraryResultFields(status, reasons = []) {
   return {
      status,
      reasons,
      errorType: status,
      issues: reasons,
      suppressedWarnings: [],
   };
}

function mockItineraryConfigResponse(overrides = {}) {
   return {
      itinerary_config: {
         animal_visibility_change_threshold:
            overrides.animalVisibilityChangeThreshold,
         itinerary_event_types: overrides.eventTypes ?? [],
         itinerary_visit_boundary_event_types:
            overrides.visitBoundaryEventTypes ?? {
               arrival: 'arrival',
               departure: 'departure',
            },
         itinerary_error_types: overrides.errorTypes ?? MOCK_ITINERARY_ERROR_TYPES,
         suppressed_error_types: overrides.suppressedErrorTypes ?? [],
      },
   };
}

function mockJsonResponse(payload, { ok = true, status = 200, statusText = 'OK' } = {}) {
   return {
      ok,
      status,
      statusText,
      text: async () => JSON.stringify(payload),
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
      });
   };

   assert.deepEqual(await getItineraryRequest(), {
      ...normalizedItineraryResultFields('success'),
      itinerary: {
         date: '2026-06-15',
         arrivalTime: '09:30',
         departureTime: '17:00',
         animals: [{ species: 'African Lion' }],
         attractions: [{ name: 'Conservation Carousel' }],
         guardiansTalks: [{ name: 'Amur Tiger' }],
         wildEncounters: [{ name: 'African Rainforest' }],
         events: [{ event_type: 'lunch', start_time: '12:00 PM', end_time: '12:40 PM' }],
      },
      itineraryConfig: normalizedItineraryConfig(),
   });
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
         animals: [],
         attractions: [{ name: 'Conservation Carousel' }],
         guardiansTalks: [],
         wildEncounters: [],
         events: [],
      },
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
         animals: [],
         attractions: [],
         guardiansTalks: [],
         wildEncounters: [],
         events: [],
      },
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
         animals: [],
         attractions: [],
         guardiansTalks: [],
         wildEncounters: [],
         events: [],
      },
      itineraryConfig: normalizedItineraryConfig({
         animalVisibilityChangeThreshold: 25,
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
         confirmingGuardiansTalkUnschedule: false,
         confirmingWildEncounterUnschedule: false,
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
      assert.deepEqual(JSON.parse(options.body), { temp: true });

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
