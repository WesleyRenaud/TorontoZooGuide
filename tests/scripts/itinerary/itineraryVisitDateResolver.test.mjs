import assert from 'node:assert/strict';
import { test } from 'node:test';

import { ItineraryVisitDateResolver } from '../../../scripts/itinerary/itineraryVisitDateResolver.js';
import { DraftStore } from '../../../scripts/itinerary/draftStore.js';
import { ItineraryErrorTypes } from '../../../scripts/itinerary/itineraryErrorTypes.js';
import { installDomTestHooks } from '../helpers/domTestSetup.mjs';
import { mockJsonResponse } from '../helpers/fetchMock.mjs';
import { createLocalStorageMock } from '../helpers/localStorageMock.mjs';

installDomTestHooks({
   before: () => {
      globalThis.localStorage = createLocalStorageMock();
      ItineraryErrorTypes.syncSuppressedItineraryErrorTypes({
         suppressedErrorTypes: [],
      });
   },
   after: () => {
      delete globalThis.localStorage;
      delete globalThis.fetch;
   },
});


test('Test_EnsureItineraryVisitDate_TestServerDate_ExpectSameItinerary', async () => {
   const date = '2026-06-15';
   const itinerary = {
      date,
      animals: [],
      attractions: [],
   };
   globalThis.fetch = async (url) => {
      if (url === '/get-itinerary-date') {
         return mockJsonResponse({ date });
      }

      throw new Error(`Unexpected fetch: ${url}`);
   };

   const result = await ItineraryVisitDateResolver.ensureItineraryVisitDate(itinerary);

   assert.equal(result, itinerary);
});


test('Test_EnsureItineraryVisitDate_TestNoSavedDate_ExpectPersisted', async () => {
   const requests = [];
   const itinerary = { animals: [], attractions: [] };
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
               animals: itinerary.animals,
               attractions: itinerary.attractions,
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

   const result = await ItineraryVisitDateResolver.ensureItineraryVisitDate(itinerary);

   const setItineraryRequest = requests.find((request) => request.url === '/set-itinerary');
   assert.ok(result.date);
   assert.equal(Boolean(setItineraryRequest), true);
   assert.equal(setItineraryRequest?.body?.date, result.date);
});


test('Test_EnsureItineraryVisitDate_TestLocalDraftOnly_ExpectPersisted', async () => {
   const date = '2026-06-18';
   const requests = [];
   const itinerary = { animals: [], attractions: [] };
   DraftStore.setStoredItineraryDate(date);
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
               animals: itinerary.animals,
               attractions: itinerary.attractions,
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

   const result = await ItineraryVisitDateResolver.ensureItineraryVisitDate(itinerary);

   assert.ok(result.date);
   assert.equal(requests.some((request) => request.url === '/set-itinerary'), true);
});


test('Test_EnsureItineraryVisitDate_TestServerDateMismatch_ExpectUpdatedDate', async () => {
   const itineraryDate = '2026-06-15';
   const serverDate = '2026-07-01';
   const animals = [];
   globalThis.fetch = async (url) => {
      if (url === '/get-itinerary-date') {
         return mockJsonResponse({ date: serverDate });
      }

      throw new Error(`Unexpected fetch: ${url}`);
   };

   const result = await ItineraryVisitDateResolver.ensureItineraryVisitDate({
      date: itineraryDate,
      animals,
   });

   assert.equal(result.date, serverDate);
   assert.equal(result.animals, animals);
});


test('Test_EnsureItineraryVisitDate_TestSetItineraryFails_ExpectThrows', async () => {
   const itinerary = { animals: [] };
   globalThis.fetch = async (url) => {
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
            status: 'error',
            errorType: 'saveFailed',
            reasons: [],
         });
      }

      throw new Error(`Unexpected fetch: ${url}`);
   };

   await assert.rejects(
      () => ItineraryVisitDateResolver.ensureItineraryVisitDate(itinerary),
      (error) => {
         assert.equal(error instanceof Error, true);
         assert.match(error.message, /itinerary/i);
         return true;
      }
   );
});
