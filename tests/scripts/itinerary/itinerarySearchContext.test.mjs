import assert from 'node:assert/strict';
import { test } from 'node:test';

import { DraftStore } from '../../../scripts/itinerary/draftStore.js';
import { ItinerarySearchContext } from '../../../scripts/itinerary/itinerarySearchContext.js';
import { installDomTestHooks } from '../helpers/domTestSetup.mjs';
import { mockJsonResponse } from '../helpers/fetchMock.mjs';
import { createLocalStorageMock } from '../helpers/localStorageMock.mjs';

installDomTestHooks({
   before: () => {
      globalThis.localStorage = createLocalStorageMock();
   },
   after: () => {
      delete globalThis.localStorage;
      delete globalThis.fetch;
   },
});


test('Test_GetItineraryDateSearchContext_TestStoredDate_ExpectContext', async () => {
   const year = '2026';
   const month = '06';
   const day = '18';
   const date = `${year}-${month}-${day}`;
   DraftStore.setStoredItineraryDate(date);

   const context = await ItinerarySearchContext.getItineraryDateSearchContext({ includeTemp: false });

   assert.equal(context.date, date);
   assert.equal(context.month, 'JUN');
   assert.equal(context.day, Number(day));
   assert.equal(context.year, Number(year));
});


test('Test_GetItineraryDateSearchContext_TestNoStoredDate_ExpectEffectiveDate', async () => {
   const openTime = '09:30';
   const closeTime = '19:00';
   globalThis.fetch = async (url) => {
      if (url === '/get-zoo-hours') {
         return mockJsonResponse({
            hours: {
               openTime,
               closeTime,
            },
         });
      }

      throw new Error(`Unexpected fetch: ${url}`);
   };

   const context = await ItinerarySearchContext.getItineraryDateSearchContext({ includeTemp: false });

   assert.ok(context.date);
   assert.ok(context.month);
   assert.ok(context.day);
   assert.ok(context.year);
});
