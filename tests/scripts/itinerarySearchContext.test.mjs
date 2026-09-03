import assert from 'node:assert/strict';
import { test } from 'node:test';

import { setStoredItineraryDate } from '../../scripts/itinerary/draftStorage.js';
import { getItineraryDateSearchContext } from '../../scripts/itinerary/itinerarySearchContext.js';
import { installDomTestHooks } from './helpers/domTestSetup.mjs';
import { mockJsonResponse } from './helpers/fetchMock.mjs';
import { createLocalStorageMock } from './helpers/localStorageMock.mjs';

installDomTestHooks({
   before: () => {
      globalThis.localStorage = createLocalStorageMock();
   },
   after: () => {
      delete globalThis.localStorage;
      delete globalThis.fetch;
   },
});

test('getItineraryDateSearchContext uses the stored draft date', async () => {
   setStoredItineraryDate('2026-06-18');

   const context = await getItineraryDateSearchContext({ includeTemp: false });

   assert.equal(context.date, '2026-06-18');
   assert.equal(context.month, 'JUN');
   assert.equal(context.day, 18);
   assert.equal(context.year, 2026);
});

test('getItineraryDateSearchContext falls back to the effective visit date when none is stored', async () => {
   globalThis.fetch = async (url) => {
      if (url === '/get-zoo-hours') {
         return mockJsonResponse({
            hours: {
               openTime: '09:30',
               closeTime: '19:00',
            },
         });
      }

      throw new Error(`Unexpected fetch: ${url}`);
   };

   const context = await getItineraryDateSearchContext({ includeTemp: false });

   assert.ok(context.date);
   assert.ok(context.month);
   assert.ok(context.day);
   assert.ok(context.year);
});
