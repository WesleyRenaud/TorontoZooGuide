import assert from 'node:assert/strict';
import { afterEach, test } from 'node:test';

import {
   acceptItineraryRequest,
   getItineraryRequest,
   getZooHoursRequest,
   setItineraryRequest,
} from '../../scripts/api/itineraryApi.js';

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
            animals: [{ species: 'African Lion' }],
            attractions: [{ name: 'Conservation Carousel' }],
            guardians_talks: [{ name: 'Amur Tiger' }],
            wild_encounters: [{ name: 'African Rainforest' }],
         },
      });
   };

   assert.deepEqual(await getItineraryRequest(), {
      success: true,
      error: null,
      issues: [],
      itinerary: {
         date: '2026-06-15',
         animals: [{ species: 'African Lion' }],
         attractions: [{ name: 'Conservation Carousel' }],
         guardiansTalks: [{ name: 'Amur Tiger' }],
         wildEncounters: [{ name: 'African Rainforest' }],
      },
   });
});

test('normalizes set itinerary failures without dropping returned itinerary data', async () => {
   globalThis.fetch = async () => mockJsonResponse({
      success: false,
      error: '  Could not save itinerary.  ',
      itinerary: {
         date: '2026-06-15',
         animals: 'African Lion',
         attractions: [{ name: 'Conservation Carousel' }],
      },
   });

   assert.deepEqual(await setItineraryRequest({ date: '2026-06-15' }), {
      success: false,
      error: 'Could not save itinerary.',
      issues: [],
      itinerary: {
         date: '2026-06-15',
         animals: [],
         attractions: [{ name: 'Conservation Carousel' }],
         guardiansTalks: [],
         wildEncounters: [],
      },
   });
});

test('normalizes accept itinerary response', async () => {
   globalThis.fetch = async (url, options) => {
      assert.equal(url, '/accept-itinerary');
      assert.equal(options.method, 'POST');
      assert.deepEqual(JSON.parse(options.body), {});

      return mockJsonResponse({
         success: true,
         issues: [
            {
               type: 'wildEncounterTimeConflict',
               message: 'African Rainforest overlaps with Kangaroo.',
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
      success: true,
      error: null,
      issues: [
         {
            type: 'wildEncounterTimeConflict',
            message: 'African Rainforest overlaps with Kangaroo.',
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
         guardiansTalks: [],
         wildEncounters: [],
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
