import assert from 'node:assert/strict';
import { test } from 'node:test';

import { scheduleSelectedItineraryItem } from '../../scripts/itinerary/panel/scheduleItemActions.js';
import {
   mockJsonResponse,
   mockScheduleItemFetch,
   installScheduleItemActionsTestHooks,
} from './helpers/scheduleItemActionsTestSetup.mjs';

installScheduleItemActionsTestHooks();

test('scheduleSelectedItineraryItem dispatches itineraryUpdated on success', async () => {
   const events = [];

   globalThis.window.dispatchEvent = (event) => {
      if (event.type === 'tzg:itineraryUpdated') {
         events.push(event.detail?.itinerary ?? null);
      }

      return true;
   };

   globalThis.fetch = mockScheduleItemFetch({
      routes: {
         '/schedule-itinerary-item': {
            status: 'success',
            reasons: [],
            itinerary: {
               date: '2026-06-15',
               animals: [{ species: 'Tiger', exhibit: 'Savanna', start_time: '10:00' }],
               attractions: [],
               guardians_talks: [],
               wild_encounters: [],
            },
         },
      },
   });

   const result = await scheduleSelectedItineraryItem(
      { date: '2026-06-15', animals: [], attractions: [] },
      'animals',
      { species: 'Tiger', exhibit: 'Savanna', scheduleItemKind: 'animals' },
      []
   );

   assert.equal(result.errorType, 'success');
   assert.equal(events.length, 1);
   assert.equal(events[0]?.date, '2026-06-15');
   assert.equal(events[0]?.animals?.length, 1);
   assert.equal(events[0]?.animals?.[0]?.species, 'Tiger');
});

test('scheduleSelectedItineraryItem schedules an event', async () => {
   const requests = [];

   globalThis.fetch = async (url, options = {}) => {
      requests.push({
         url,
         body: JSON.parse(options.body ?? '{}'),
      });

      return mockScheduleItemFetch()(url, options);
   };

   const result = await scheduleSelectedItineraryItem(
      { date: '2026-06-15', animals: [], attractions: [] },
      'lunch',
      null,
      ['lunch'],
      { startTime: '1:30 PM', durationMinutes: 15 }
   );

   assert.equal(result.errorType, 'success');
   assert.deepEqual(
      requests.filter((request) => request.url === '/schedule-itinerary-item'),
      [{
         url: '/schedule-itinerary-item',
         body: {
            itemType: 'lunch',
            key: '',
            startTime: '1:30 PM',
            durationMinutes: 15,
            confirmingScheduleItemNotOnItinerary: false,
            confirmingAttractionOutsideOperatingHours: false,
            confirmingGuardiansTalkUnschedule: false,
            confirmingWildEncounterUnschedule: false,
            confirmingFixedTimeItemLongWait: false,
            confirmingGuardiansTalkWithoutAnimal: false,
         },
      }]
   );
});

test('scheduleSelectedItineraryItem schedules when type is unset but a row is selected', async () => {
   const urls = [];

   globalThis.fetch = async (url, options = {}) => {
      urls.push(url);

      return mockScheduleItemFetch()(url, options);
   };

   const result = await scheduleSelectedItineraryItem(
      {
         date: '2026-06-15',
         animals: [{ species: 'Tiger', exhibit: 'Savanna' }],
         attractions: [],
      },
      '',
      {
         species: 'Tiger',
         exhibit: 'Savanna',
         scheduleItemKind: 'animals',
      },
      []
   );

   assert.equal(result.errorType, 'success');
   assert.deepEqual(urls, ['/get-itinerary-date', '/schedule-itinerary-item']);
});

test('scheduleSelectedItineraryItem returns noAvailableSlot without refreshing', async () => {
   globalThis.fetch = mockScheduleItemFetch({
      routes: {
         '/schedule-itinerary-item': {
            status: 'noAvailableSlot',
            reasons: [],
         },
      },
   });

   const result = await scheduleSelectedItineraryItem(
      {
         date: '2026-06-15',
         animals: [{ species: 'Tiger', exhibit: 'Savanna' }],
         attractions: [],
      },
      'animals',
      { species: 'Tiger', exhibit: 'Savanna', scheduleItemKind: 'animals' },
      []
   );

   assert.equal(result.errorType, 'noAvailableSlot');
});

test('scheduleSelectedItineraryItem surfaces requestedTimeNotAvailable', async () => {
   globalThis.fetch = mockScheduleItemFetch({
      routes: {
         '/schedule-itinerary-item': {
            status: 'requestedTimeNotAvailable',
            reasons: [],
         },
      },
   });

   const result = await scheduleSelectedItineraryItem(
      { date: '2026-06-15', animals: [], attractions: [] },
      'animals',
      {
         species: 'Tiger',
         exhibit: 'Savanna',
         scheduleItemKind: 'animals',
      },
      [],
      { startTime: '12:00 PM' }
   );

   assert.equal(result.errorType, 'requestedTimeNotAvailable');
});

test('scheduleSelectedItineraryItem saves the effective visit date when none is set', async () => {
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

      if (url === '/schedule-itinerary-item') {
         return mockJsonResponse({ status: 'success', reasons: [] });
      }

      throw new Error(`Unexpected fetch: ${url}`);
   };

   const result = await scheduleSelectedItineraryItem(
      { animals: [], attractions: [] },
      'animals',
      {
         species: 'Tiger',
         exhibit: 'Savanna',
         scheduleItemKind: 'animals',
      },
      []
   );

   assert.equal(result.errorType, 'success');
   assert.equal(requests.some((request) => request.url === '/get-zoo-hours'), true);
   assert.equal(requests.some((request) => request.url === '/set-itinerary'), true);
   assert.ok(
      requests.find((request) => request.url === '/set-itinerary')?.body?.date
   );
   assert.equal(requests.at(-1)?.url, '/schedule-itinerary-item');
});
