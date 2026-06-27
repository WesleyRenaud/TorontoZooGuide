import assert from 'node:assert/strict';
import { test } from 'node:test';

import { ensureItineraryVisitDate } from '../../scripts/itinerary/ensureItineraryVisitDate.js';
import { setStoredItineraryDate } from '../../scripts/itinerary/draftStorage.js';
import { updateItineraryErrorTypesFromConfig } from '../../scripts/itinerary/itineraryErrorTypes.js';
import { installDomTestHooks } from './helpers/domTestSetup.mjs';
import { mockJsonResponse } from './helpers/fetchMock.mjs';
import { createLocalStorageMock } from './helpers/localStorageMock.mjs';

installDomTestHooks({
   before: () => {
      globalThis.localStorage = createLocalStorageMock();
      updateItineraryErrorTypesFromConfig({
         errorTypes: { SUCCESS: 'success', SAVE_FAILED: 'saveFailed' },
         suppressedErrorTypes: [],
      });
   },
   after: () => {
      delete globalThis.localStorage;
      delete globalThis.fetch;
   },
});

test('ensureItineraryVisitDate returns the itinerary when the server already has a date', async () => {
   globalThis.fetch = async (url) => {
      if (url === '/get-itinerary-date') {
         return mockJsonResponse({ date: '2026-06-15' });
      }

      throw new Error(`Unexpected fetch: ${url}`);
   };

   const itinerary = {
      date: '2026-06-15',
      animals: [],
      attractions: [],
   };

   const result = await ensureItineraryVisitDate(itinerary);

   assert.equal(result, itinerary);
});

test('ensureItineraryVisitDate persists the effective visit date when none is saved', async () => {
   const requests = [];

   globalThis.fetch = async (url, options = {}) => {
      requests.push({
         url,
         body: JSON.parse(options.body ?? '{}'),
      });

      if (url === '/get-itinerary-date') {
         return mockJsonResponse({ date: null });
      }

      if (url === '/get-zoo-hours') {
         return mockJsonResponse({
            hours: {
               openTime: '09:30',
               closeTime: '19:00',
            },
         });
      }

      if (url === '/set-itinerary') {
         return mockJsonResponse({
            status: 'success',
            reasons: [],
            itinerary: {
               date: JSON.parse(options.body).date,
               animals: [],
               attractions: [],
               guardians_talks: [],
               wild_encounters: [],
            },
            itinerary_config: {
               itinerary_error_types: { SUCCESS: 'success' },
            },
         });
      }

      throw new Error(`Unexpected fetch: ${url}`);
   };

   const result = await ensureItineraryVisitDate({ animals: [], attractions: [] });

   assert.ok(result.date);
   assert.equal(requests.some((request) => request.url === '/set-itinerary'), true);
   assert.equal(
      requests.find((request) => request.url === '/set-itinerary')?.body?.date,
      result.date
   );
});

test('ensureItineraryVisitDate persists when only the draft date is set locally', async () => {
   setStoredItineraryDate('2026-06-18');

   const requests = [];

   globalThis.fetch = async (url, options = {}) => {
      requests.push({ url });

      if (url === '/get-itinerary-date') {
         return mockJsonResponse({ date: null });
      }

      if (url === '/get-zoo-hours') {
         return mockJsonResponse({
            hours: {
               openTime: '09:30',
               closeTime: '19:00',
            },
         });
      }

      if (url === '/set-itinerary') {
         return mockJsonResponse({
            status: 'success',
            reasons: [],
            itinerary: {
               date: JSON.parse(options.body).date,
               animals: [],
               attractions: [],
               guardians_talks: [],
               wild_encounters: [],
            },
            itinerary_config: {
               itinerary_error_types: { SUCCESS: 'success' },
            },
         });
      }

      throw new Error(`Unexpected fetch: ${url}`);
   };

   const result = await ensureItineraryVisitDate({ animals: [], attractions: [] });

   assert.ok(result.date);
   assert.equal(requests.some((request) => request.url === '/set-itinerary'), true);
});
