import assert from 'node:assert/strict';
import { test } from 'node:test';

import { ItineraryService } from '../../../scripts/itinerary/itineraryService.js';
import { installItineraryServiceTestHooks } from '../helpers/itineraryServiceTestSetup.mjs';
import { mockJsonResponse } from '../helpers/fetchMock.mjs';

installItineraryServiceTestHooks();

test('Test_ItineraryService_TestItineraryServiceGetItineraryNormalizesSavedItineraryResponses_ExpectOk', async () => {
   globalThis.fetch = async (url) => {
      if (url === '/get-itinerary-date') {
         return mockJsonResponse({ date: '2026-06-15' });
      }

      if (url === '/get-itinerary') {
         return mockJsonResponse({
            itinerary: {
               date: '2026-06-15',
               animals: [{ species: 'African Lion', exhibit: 'African Savanna' }],
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

   assert.equal(itinerary.date, '2026-06-15');
   assert.equal(itinerary.animals[0].species, 'African Lion');
   assert.equal(itinerary.isActive, true);
});

test('Test_ItineraryService_TestItineraryServiceGetZooHoursReturnsNullForInvalidDatesAnd_ExpectOk', async () => {
   assert.equal(await ItineraryService.getZooHours(null), null);
   assert.equal(await ItineraryService.getZooHours('not-a-date'), null);

   globalThis.fetch = async (url, options) => {
      assert.equal(url, '/get-zoo-hours');
      assert.deepEqual(JSON.parse(options.body), {
         day: 15,
         month: 'JUN',
         year: 2026,
      });

      return mockJsonResponse({
         hours: {
            openTime: '09:30',
            closeTime: '19:00',
         },
      });
   };

   assert.deepEqual(await ItineraryService.getZooHours('2026-06-15'), {
      date: '',
      earlyAdmissionTime: '',
      openTime: '09:30',
      lastAdmissionTime: '',
      closeTime: '19:00',
   });
});

test('Test_ItineraryService_TestItineraryServiceClearItineraryDispatchesClearedItineraryEvents_ExpectOk', async () => {
   const events = [];
   window.addEventListener = (type, handler) => {
      window.__handler = handler;
   };
   window.dispatchEvent = (event) => {
      events.push(event.type);
      return true;
   };

   globalThis.fetch = async (url) => {
      assert.equal(url, '/clear-itinerary');
      return mockJsonResponse({ success: true });
   };

   const result = await ItineraryService.clearItinerary();

   assert.deepEqual(events, ['tzg:itineraryCleared', 'tzg:itineraryUpdated']);
   assert.deepEqual(result, { success: true });
});

test('Test_ItineraryService_TestItineraryServiceBulkScheduleItineraryReturnsNormalizedItineraryAndIssues_ExpectOk', async () => {
   globalThis.fetch = async (url, options) => {
      if (url === '/get-itinerary-date') {
         return mockJsonResponse({ date: '2026-06-15' });
      }

      if (url === '/bulk-schedule-itinerary') {
         assert.deepEqual(JSON.parse(options.body), {
            temp: null,
            confirmingFixedTimeItemLongWait: false,
         });
         return mockJsonResponse({
            status: 'success',
            itinerary: {
               date: '2026-06-15',
               animals: [{ species: 'African Lion', exhibit: 'African Savanna' }],
               attractions: [],
               guardians_talks: [],
               wild_encounters: [],
            },
            reasons: [{ code: 'bulkScheduleItineraryNotEnoughTime', items: [] }],
         });
      }

      throw new Error(`Unexpected fetch: ${url}`);
   };

   const result = await ItineraryService.bulkScheduleItinerary();

   assert.equal(result.itinerary.animals[0].species, 'African Lion');
   assert.equal(result.issues[0].code, 'bulkScheduleItineraryNotEnoughTime');
});

test('Test_ItineraryService_TestItineraryServiceAcceptItineraryKeepsSelectedAnimalsAndAttractions_ExpectOk', async () => {
   globalThis.fetch = async (url, options) => {
      if (url === '/get-itinerary-date') {
         return mockJsonResponse({ date: '2026-06-15' });
      }

      if (url === '/accept-itinerary') {
         assert.deepEqual(JSON.parse(options.body), {
            temp: null,
            animalsToKeep: ['African Lion'],
            attractionsToKeep: ['Zoomobile'],
         });

         return mockJsonResponse({
            itinerary: {
               date: '2026-06-15',
               animals: [{ species: 'African Lion', exhibit: 'African Savanna' }],
               attractions: [{ name: 'Zoomobile' }],
               guardians_talks: [],
               wild_encounters: [],
            },
         });
      }

      throw new Error(`Unexpected fetch: ${url}`);
   };

   const itinerary = await ItineraryService.acceptItinerary({
      animalsToKeep: ['African Lion'],
      attractionsToKeep: ['Zoomobile'],
   });

   assert.equal(itinerary.animals[0].species, 'African Lion');
   assert.equal(itinerary.attractions[0].name, 'Zoomobile');
});

test('Test_ItineraryService_TestItineraryServiceHasActiveItineraryIsTrueWhenOnlyAVisit_ExpectOk', async () => {
   globalThis.fetch = async (url) => {
      if (url === '/get-itinerary-date') {
         return mockJsonResponse({ date: '2026-06-15' });
      }

      if (url === '/get-itinerary') {
         return mockJsonResponse({
            itinerary: {
               date: '2026-06-15',
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

   assert.equal(await ItineraryService.hasActiveItinerary(), true);
});

test('Test_ItineraryService_TestItineraryServiceHasActiveItineraryIsFalseWhenNoItineraryIs_ExpectOk', async () => {
   globalThis.fetch = async (url) => {
      if (url === '/get-itinerary-date') {
         return mockJsonResponse({ date: null });
      }

      if (url === '/get-itinerary') {
         return mockJsonResponse({
            itinerary: {
               date: null,
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

   assert.equal(await ItineraryService.hasActiveItinerary(), false);
});

test('Test_ItineraryService_TestItineraryServiceHasActiveItineraryIsTrueWhenItineraryIsActive_ExpectOk', async () => {
   globalThis.fetch = async (url) => {
      if (url === '/get-itinerary-date') {
         return mockJsonResponse({ date: '2026-06-15' });
      }

      if (url === '/get-itinerary') {
         return mockJsonResponse({
            itinerary: {
               date: '2026-06-15',
               animals: [{ species: 'African Lion', exhibit: 'African Savanna' }],
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

   assert.equal(await ItineraryService.hasActiveItinerary(), true);
});
