import assert from 'node:assert/strict';
import { afterEach, test } from 'node:test';

import {
   acceptItineraryRequest,
   getItineraryDateRequest,
   getItineraryRequest,
   getZooHoursRequest,
   scheduleItineraryItemRequest,
   setItineraryArrivalTimeRequest,
   setItineraryDepartureTimeRequest,
   setItineraryRequest,
} from '../../scripts/api/itineraryApi.js';

const MOCK_ITINERARY_ERROR_TYPES = Object.freeze({
   SUCCESS: 'success',
   ITINERARY_DATE_NOT_SET: 'itineraryDateNotSet',
   TIME_OUT_OF_BOUNDS: 'timeOutOfBounds',
   TIME_ORDER_INVALID: 'timeOrderInvalid',
   SAVE_FAILED: 'saveFailed',
   ARRIVAL_DEPARTURE_TOO_CLOSE: 'arrivalDepartureTooClose',
   NO_AVAILABLE_SLOT: 'noAvailableSlot',
});

const EMPTY_ITINERARY_CONFIG = {
   animalVisibilityChangeThreshold: undefined,
   eventTypes: [],
   errorTypes: Object.freeze({}),
   suppressedErrorTypes: [],
};

function mockItineraryConfigResponse(overrides = {}) {
   return {
      itinerary_config: {
         animal_visibility_change_threshold:
            overrides.animalVisibilityChangeThreshold,
         itinerary_event_types: overrides.eventTypes ?? [],
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
         },
      });
   };

   assert.deepEqual(await getItineraryRequest(), {
      errorType: 'success',
      issues: [],
      itinerary: {
         date: '2026-06-15',
         arrivalTime: '09:30',
         departureTime: '17:00',
         animals: [{ species: 'African Lion' }],
         attractions: [{ name: 'Conservation Carousel' }],
         guardiansTalks: [{ name: 'Amur Tiger' }],
         wildEncounters: [{ name: 'African Rainforest' }],
      },
      itineraryConfig: EMPTY_ITINERARY_CONFIG,
   });
});

test('normalizes set itinerary failures without dropping returned itinerary data', async () => {
   globalThis.fetch = async () => mockJsonResponse({
      success: false,
      errorType: 'arrivalDepartureTooClose',
      itinerary: {
         date: '2026-06-15',
         animals: 'African Lion',
         attractions: [{ name: 'Conservation Carousel' }],
      },
   });

   assert.deepEqual(await setItineraryRequest({ date: '2026-06-15' }), {
      errorType: 'arrivalDepartureTooClose',
      issues: [],
      itinerary: {
         date: '2026-06-15',
         arrivalTime: '',
         departureTime: '',
         animals: [],
         attractions: [{ name: 'Conservation Carousel' }],
         guardiansTalks: [],
         wildEncounters: [],
      },
      itineraryConfig: EMPTY_ITINERARY_CONFIG,
   });
});

test('sets itinerary arrival and departure times through focused endpoints', async () => {
   const calls = [];

   globalThis.fetch = async (url, options) => {
      calls.push([url, JSON.parse(options.body)]);
      return mockJsonResponse({
         errorType: 'success',
         ...mockItineraryConfigResponse(),
      });
   };

   assert.deepEqual(await setItineraryArrivalTimeRequest(' 09:45 '), {
      errorType: 'success',
      itineraryConfig: {
         ...EMPTY_ITINERARY_CONFIG,
         errorTypes: MOCK_ITINERARY_ERROR_TYPES,
      },
   });
   assert.deepEqual(await setItineraryDepartureTimeRequest(''), {
      errorType: 'success',
      itineraryConfig: {
         ...EMPTY_ITINERARY_CONFIG,
         errorTypes: MOCK_ITINERARY_ERROR_TYPES,
      },
   });
   assert.deepEqual(calls, [
      [
         '/set-itinerary-arrival-time',
         {
            arrivalTime: '09:45',
            confirmingShortVisit: false,
            suppressShortVisitWarning: false,
         },
      ],
      [
         '/set-itinerary-departure-time',
         {
            departureTime: '',
            confirmingShortVisit: false,
            suppressShortVisitWarning: false,
         },
      ],
   ]);
});

test('normalizes short visit warning from itinerary time endpoints', async () => {
   globalThis.fetch = async () => mockJsonResponse({
      success: false,
      errorType: 'arrivalDepartureTooClose',
      ...mockItineraryConfigResponse(),
   });

   assert.deepEqual(await setItineraryArrivalTimeRequest('11:35', {
      confirmingShortVisit: true,
   }), {
      errorType: 'arrivalDepartureTooClose',
      itineraryConfig: {
         ...EMPTY_ITINERARY_CONFIG,
         errorTypes: MOCK_ITINERARY_ERROR_TYPES,
      },
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
         issues: [
            {
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
         ],
         itinerary: {
            date: '2026-06-15',
            animals: [],
            attractions: [],
            guardians_talks: [],
            wild_encounters: [],
         },
      });
   };

   assert.deepEqual(await acceptItineraryRequest(), {
      errorType: 'success',
      issues: [
         {
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
      ],
      itinerary: {
         date: '2026-06-15',
         arrivalTime: '',
         departureTime: '',
         animals: [],
         attractions: [],
         guardiansTalks: [],
         wildEncounters: [],
      },
      itineraryConfig: EMPTY_ITINERARY_CONFIG,
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
      errorType: 'success',
      issues: [],
      itinerary: {
         date: '2026-06-15',
         arrivalTime: '',
         departureTime: '',
         animals: [],
         attractions: [],
         guardiansTalks: [],
         wildEncounters: [],
      },
      itineraryConfig: {
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
         errorTypes: MOCK_ITINERARY_ERROR_TYPES,
         suppressedErrorTypes: [],
      },
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

test('normalizes schedule itinerary item response', async () => {
   globalThis.fetch = async (url, options) => {
      assert.equal(url, '/schedule-itinerary-item');
      assert.deepEqual(JSON.parse(options.body), {
         itemType: 'lunch',
         key: '',
      });

      return mockJsonResponse({
         errorType: 'noAvailableSlot',
      });
   };

   assert.deepEqual(
      await scheduleItineraryItemRequest({ itemType: 'lunch', key: '' }),
      { errorType: 'noAvailableSlot' }
   );
});
