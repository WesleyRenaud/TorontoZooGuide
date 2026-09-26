import assert from 'node:assert/strict';
import { test } from 'node:test';

import { ItineraryService } from '../../../scripts/itinerary/itineraryService.js';
import { Position } from '../../../scripts/shared/enums/position.js';
import { installItineraryServiceTestHooks } from '../helpers/itineraryServiceTestSetup.mjs';
import { mockJsonResponse } from '../helpers/fetchMock.mjs';

installItineraryServiceTestHooks();


test('Test_ItineraryService_TestItineraryServiceGetItineraryNormalizesSavedItineraryResponses_ExpectOk', async () => {
   const date = '2026-06-15';
   const species = 'African Lion';
   const exhibit = 'African Savanna';
   globalThis.fetch = async (url) => {
      if (url === '/get-itinerary-date') {
         return mockJsonResponse({ date });
      }

      if (url === '/get-itinerary') {
         return mockJsonResponse({
            itinerary: {
               date,
               animals: [{ species, exhibit }],
               attractions: [],
               guardians_talks: [],
               wild_encounters: [],
            },
            itineraryConfig: {
               isActive: true,
            },
         });
      }

      throw new Error(`Unexpected fetch: ${url}`);
   };

   const itinerary = await ItineraryService.getItinerary();

   assert.equal(itinerary.date, date);
   assert.equal(itinerary.animals[Position.FIRST].species, species);
   assert.equal(itinerary.isActive, true);
});


test('Test_GetZooHours_TestNull_ExpectNull', async () => {
   const date = null;

   const hours = await ItineraryService.getZooHours(date);

   assert.equal(hours, null);
});


test('Test_GetZooHours_TestInvalidDate_ExpectNull', async () => {
   const date = 'not-a-date';

   const hours = await ItineraryService.getZooHours(date);

   assert.equal(hours, null);
});


test('Test_GetZooHours_TestValidDate_ExpectHours', async () => {
   const date = '2026-06-15';
   const day = 15;
   const month = 'JUN';
   const year = 2026;
   const openTime = '09:30';
   const closeTime = '19:00';
   globalThis.fetch = async (url, options) => {
      assert.equal(url, '/get-zoo-hours');
      assert.deepEqual(JSON.parse(options.body), { day, month, year });

      return mockJsonResponse({
         hours: { openTime, closeTime },
      });
   };

   const hours = await ItineraryService.getZooHours(date);

   assert.equal(hours.openTime, openTime);
   assert.equal(hours.closeTime, closeTime);
});


test('Test_ItineraryService_TestItineraryServiceClearItineraryDispatchesClearedItineraryEvents_ExpectOk', async () => {
   const events = [];
   const cleared = { success: true };
   window.addEventListener = (type, handler) => {
      window.__handler = handler;
   };
   window.dispatchEvent = (event) => {
      events.push(event.type);
      return true;
   };
   globalThis.fetch = async (url) => {
      assert.equal(url, '/clear-itinerary');
      return mockJsonResponse(cleared);
   };

   const result = await ItineraryService.clearItinerary();

   assert.deepEqual(events, ['tzg:itineraryCleared', 'tzg:itineraryUpdated']);
   assert.deepEqual(result, cleared);
});


test('Test_ItineraryService_TestItineraryServiceBulkScheduleItineraryReturnsNormalizedItineraryAndIssues_ExpectOk', async () => {
   const date = '2026-06-15';
   const species = 'African Lion';
   const issueCode = 'bulkScheduleItineraryNotEnoughTime';
   globalThis.fetch = async (url, options) => {
      if (url === '/get-itinerary-date') {
         return mockJsonResponse({ date });
      }

      if (url === '/bulk-schedule-itinerary') {
         assert.deepEqual(JSON.parse(options.body), {
            temp: null,
            confirmingFixedTimeItemLongWait: false,
         });
         return mockJsonResponse({
            status: 'success',
            itinerary: {
               date,
               animals: [{ species, exhibit: 'African Savanna' }],
               attractions: [],
               guardians_talks: [],
               wild_encounters: [],
            },
            reasons: [{ code: issueCode, items: [] }],
         });
      }

      throw new Error(`Unexpected fetch: ${url}`);
   };

   const result = await ItineraryService.bulkScheduleItinerary();

   assert.equal(result.itinerary.animals[Position.FIRST].species, species);
   assert.equal(result.issues[Position.FIRST].code, issueCode);
});


test('Test_ItineraryService_TestItineraryServiceAcceptItineraryKeepsSelectedAnimalsAndAttractions_ExpectOk', async () => {
   const date = '2026-06-15';
   const species = 'African Lion';
   const attractionName = 'Zoomobile';
   globalThis.fetch = async (url, options) => {
      if (url === '/get-itinerary-date') {
         return mockJsonResponse({ date });
      }

      if (url === '/accept-itinerary') {
         assert.deepEqual(JSON.parse(options.body), {
            temp: null,
            animalsToKeep: [species],
            attractionsToKeep: [attractionName],
         });

         return mockJsonResponse({
            itinerary: {
               date,
               animals: [{ species, exhibit: 'African Savanna' }],
               attractions: [{ name: attractionName }],
               guardians_talks: [],
               wild_encounters: [],
            },
         });
      }

      throw new Error(`Unexpected fetch: ${url}`);
   };

   const itinerary = await ItineraryService.acceptItinerary({
      animalsToKeep: [species],
      attractionsToKeep: [attractionName],
   });

   assert.equal(itinerary.animals[Position.FIRST].species, species);
   assert.equal(itinerary.attractions[Position.FIRST].name, attractionName);
});


test('Test_ItineraryService_TestItineraryServiceHasActiveItineraryIsTrueWhenOnlyAVisit_ExpectOk', async () => {
   const date = '2026-06-15';
   globalThis.fetch = async (url) => {
      if (url === '/get-itinerary-date') {
         return mockJsonResponse({ date });
      }

      if (url === '/get-itinerary') {
         return mockJsonResponse({
            itinerary: {
               date,
               animals: [],
               attractions: [],
               guardians_talks: [],
               wild_encounters: [],
            },
            itineraryConfig: {},
         });
      }

      throw new Error(`Unexpected fetch: ${url}`);
   };

   const isActive = await ItineraryService.hasActiveItinerary();

   assert.equal(isActive, true);
});


test('Test_ItineraryService_TestItineraryServiceHasActiveItineraryIsFalseWhenNoItineraryIs_ExpectOk', async () => {
   const date = null;
   globalThis.fetch = async (url) => {
      if (url === '/get-itinerary-date') {
         return mockJsonResponse({ date });
      }

      if (url === '/get-itinerary') {
         return mockJsonResponse({
            itinerary: {
               date,
               animals: [],
               attractions: [],
               guardians_talks: [],
               wild_encounters: [],
            },
            itineraryConfig: {},
         });
      }

      throw new Error(`Unexpected fetch: ${url}`);
   };

   const isActive = await ItineraryService.hasActiveItinerary();

   assert.equal(isActive, false);
});


test('Test_ItineraryService_TestItineraryServiceHasActiveItineraryIsTrueWhenItineraryIsActive_ExpectOk', async () => {
   const date = '2026-06-15';
   const species = 'African Lion';
   globalThis.fetch = async (url) => {
      if (url === '/get-itinerary-date') {
         return mockJsonResponse({ date });
      }

      if (url === '/get-itinerary') {
         return mockJsonResponse({
            itinerary: {
               date,
               animals: [{ species, exhibit: 'African Savanna' }],
               attractions: [],
               guardians_talks: [],
               wild_encounters: [],
            },
            itineraryConfig: {
               isActive: true,
            },
         });
      }

      throw new Error(`Unexpected fetch: ${url}`);
   };

   const isActive = await ItineraryService.hasActiveItinerary();

   assert.equal(isActive, true);
});
