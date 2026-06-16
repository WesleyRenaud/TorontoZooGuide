import assert from 'node:assert/strict';
import { test } from 'node:test';

import {
   acceptItinerary,
   bulkScheduleAnimals,
   clearItinerary,
   getItinerary,
   getZooHours,
   hasActiveItinerary,
} from '../../scripts/itinerary/itineraryService.js';
import { installItineraryServiceTestHooks } from './helpers/itineraryServiceTestSetup.mjs';
import { mockJsonResponse } from './helpers/fetchMock.mjs';

installItineraryServiceTestHooks();

test('getItinerary normalizes saved itinerary responses', async () => {
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

   const itinerary = await getItinerary();

   assert.equal(itinerary.date, '2026-06-15');
   assert.equal(itinerary.animals[0].species, 'African Lion');
   assert.equal(itinerary.isActive, true);
});

test('getZooHours returns null for invalid dates and normalized hours otherwise', async () => {
   assert.equal(await getZooHours(null), null);
   assert.equal(await getZooHours('not-a-date'), null);

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

   assert.deepEqual(await getZooHours('2026-06-15'), {
      date: '',
      earlyAdmissionTime: '',
      openTime: '09:30',
      lastAdmissionTime: '',
      closeTime: '19:00',
   });
});

test('clearItinerary dispatches cleared itinerary events', async () => {
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

   const result = await clearItinerary();

   assert.deepEqual(events, ['tzg:itineraryCleared', 'tzg:itineraryUpdated']);
   assert.deepEqual(result, { success: true });
});

test('bulkScheduleAnimals returns normalized itinerary and issues', async () => {
   globalThis.fetch = async (url, options) => {
      if (url === '/get-itinerary-date') {
         return mockJsonResponse({ date: '2026-06-15' });
      }

      if (url === '/bulk-schedule-animals') {
         assert.deepEqual(JSON.parse(options.body), { temp: null });
         return mockJsonResponse({
            status: 'success',
            itinerary: {
               date: '2026-06-15',
               animals: [{ species: 'African Lion', exhibit: 'African Savanna' }],
               attractions: [],
               guardians_talks: [],
               wild_encounters: [],
            },
            reasons: [{ code: 'bulkScheduleAnimalsNotEnoughTime', items: [] }],
         });
      }

      throw new Error(`Unexpected fetch: ${url}`);
   };

   const result = await bulkScheduleAnimals();

   assert.equal(result.itinerary.animals[0].species, 'African Lion');
   assert.equal(result.issues[0].code, 'bulkScheduleAnimalsNotEnoughTime');
});

test('acceptItinerary keeps selected animals and attractions', async () => {
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

   const itinerary = await acceptItinerary({
      animalsToKeep: ['African Lion'],
      attractionsToKeep: ['Zoomobile'],
   });

   assert.equal(itinerary.animals[0].species, 'African Lion');
   assert.equal(itinerary.attractions[0].name, 'Zoomobile');
});

test('hasActiveItinerary is false for empty inactive itineraries', async () => {
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
            itineraryConfig: {
               isActive: false,
            },
         });
      }

      throw new Error(`Unexpected fetch: ${url}`);
   };

   assert.equal(await hasActiveItinerary(), false);
});

test('hasActiveItinerary is true when itinerary is active and populated', async () => {
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

   assert.equal(await hasActiveItinerary(), true);
});
