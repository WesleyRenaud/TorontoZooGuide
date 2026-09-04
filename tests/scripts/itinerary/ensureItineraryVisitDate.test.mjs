import assert from 'node:assert/strict';
import { test } from 'node:test';

import { EnsureItineraryVisitDate } from '../../../scripts/itinerary/ensureItineraryVisitDate.js';
import { DraftStorage } from '../../../scripts/itinerary/draftStorage.js';
import { ItineraryErrorTypes } from '../../../scripts/itinerary/itineraryErrorTypes.js';
import { installDomTestHooks } from '../helpers/domTestSetup.mjs';
import { mockJsonResponse } from '../helpers/fetchMock.mjs';
import { createLocalStorageMock } from '../helpers/localStorageMock.mjs';

installDomTestHooks({
   before: () => {
      globalThis.localStorage = createLocalStorageMock();
      ItineraryErrorTypes.updateItineraryErrorTypesFromConfig({
         errorTypes: { SUCCESS: 'success', SAVE_FAILED: 'saveFailed' },
         suppressedErrorTypes: [],
      });
   },
   after: () => {
      delete globalThis.localStorage;
      delete globalThis.fetch;
   },
});

test('Test_EnsureItineraryVisitDate_TestServerDate_ExpectSameItinerary', async () => {
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

   const result = await EnsureItineraryVisitDate.ensureItineraryVisitDate(itinerary);

   assert.equal(result, itinerary);
});

test('Test_EnsureItineraryVisitDate_TestNoSavedDate_ExpectPersisted', async () => {
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

   const result = await EnsureItineraryVisitDate.ensureItineraryVisitDate({ animals: [], attractions: [] });

   assert.ok(result.date);
   assert.equal(requests.some((request) => request.url === '/set-itinerary'), true);
   assert.equal(
      requests.find((request) => request.url === '/set-itinerary')?.body?.date,
      result.date
   );
});

test('Test_EnsureItineraryVisitDate_TestLocalDraftOnly_ExpectPersisted', async () => {
   DraftStorage.setStoredItineraryDate('2026-06-18');

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

   const result = await EnsureItineraryVisitDate.ensureItineraryVisitDate({ animals: [], attractions: [] });

   assert.ok(result.date);
   assert.equal(requests.some((request) => request.url === '/set-itinerary'), true);
});
