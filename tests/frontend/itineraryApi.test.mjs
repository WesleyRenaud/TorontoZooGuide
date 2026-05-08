import assert from 'node:assert/strict';
import { afterEach, test } from 'node:test';

import {
   getItineraryRequest,
   getZooHoursRequest,
   setItineraryRequest,
   validateItineraryDraftRequest,
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
      itinerary: {
         date: '2026-06-15',
         animals: [],
         attractions: [{ name: 'Conservation Carousel' }],
         guardiansTalks: [],
         wildEncounters: [],
      },
   });
});

test('normalizes zoo hours response', async () => {
   globalThis.fetch = async (url, options) => {
      assert.equal(url, '/get-zoo-hours');
      assert.equal(options.method, 'POST');
      assert.deepEqual(JSON.parse(options.body), { date: '2026-06-20' });

      return mockJsonResponse({
         hours: {
            date: '  2026-06-20  ',
            openTime: ' 09:30 ',
            closeTime: '19:00 ',
            lastAdmissionTime: ' 18:00',
         },
      });
   };

   assert.deepEqual(await getZooHoursRequest('2026-06-20'), {
      hours: {
         date: '2026-06-20',
         openTime: '09:30',
         closeTime: '19:00',
         lastAdmissionTime: '18:00',
      },
   });
});

test('normalizes validated itinerary response buckets', async () => {
   globalThis.fetch = async (url, options) => {
      assert.equal(url, '/validate-itinerary');
      assert.deepEqual(JSON.parse(options.body), {
         date: '2026-06-15',
         month: 'June',
         day: 15,
         animals: ['African Lion'],
      });

      return mockJsonResponse({
         previous: {
            animals: [{ species: 'African Lion' }],
            guardiansTalks: [{ name: 'Amur Tiger' }],
         },
         validated: {
            animals: [{ species: 'African Lion' }],
            attractions: [{ name: 'Greenhouse' }],
            wildEncounters: [],
         },
         removed: {
            attractions: [{ name: 'Conservation Carousel' }],
            wildEncounters: [{ name: 'African Rainforest' }],
         },
      });
   };

   assert.deepEqual(await validateItineraryDraftRequest({
      date: '2026-06-15',
      month: 'June',
      day: 15,
      animals: ['African Lion'],
   }), {
      success: true,
      error: null,
      previous: {
         animals: [{ species: 'African Lion' }],
         attractions: [],
         guardiansTalks: [{ name: 'Amur Tiger' }],
         wildEncounters: [],
      },
      validated: {
         animals: [{ species: 'African Lion' }],
         attractions: [{ name: 'Greenhouse' }],
         guardiansTalks: [],
         wildEncounters: [],
      },
      removed: {
         animals: [],
         attractions: [{ name: 'Conservation Carousel' }],
         guardiansTalks: [],
         wildEncounters: [{ name: 'African Rainforest' }],
      },
   });
});
