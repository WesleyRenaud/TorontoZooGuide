import assert from 'node:assert/strict';
import { test } from 'node:test';

import { scheduleSelectedItineraryItem } from '../../scripts/itinerary/panel/scheduleItemActions.js';
import {
   mockJsonResponse,
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

   globalThis.fetch = async () => mockJsonResponse({
      status: 'success',
      reasons: [],
      itinerary: {
         date: '2026-06-15',
         animals: [{ species: 'Tiger', exhibit: 'Savanna', start_time: '10:00' }],
         attractions: [],
         guardians_talks: [],
         wild_encounters: [],
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

      return mockJsonResponse({ status: 'success', reasons: [] });
   };

   const result = await scheduleSelectedItineraryItem(
      { date: '2026-06-15', animals: [], attractions: [] },
      'lunch',
      null,
      ['lunch'],
      { startTime: '1:30 PM', durationMinutes: 15 }
   );

   assert.equal(result.errorType, 'success');
   assert.deepEqual(requests, [{
      url: '/schedule-itinerary-item',
      body: {
         itemType: 'lunch',
         key: '',
         startTime: '1:30 PM',
         durationMinutes: 15,
         confirmingScheduleItemNotOnItinerary: false,
         confirmingGuardiansTalkUnschedule: false,
         confirmingWildEncounterUnschedule: false,
      },
   }]);
});

test('scheduleSelectedItineraryItem schedules when type is unset but a row is selected', async () => {
   const urls = [];

   globalThis.fetch = async (url) => {
      urls.push(url);

      return mockJsonResponse({ status: 'success', reasons: [] });
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
   assert.deepEqual(urls, ['/schedule-itinerary-item']);
});

test('scheduleSelectedItineraryItem returns noAvailableSlot without refreshing', async () => {
   globalThis.fetch = async (url) => {
      if (url === '/schedule-itinerary-item') {
         return mockJsonResponse({ status: 'noAvailableSlot', reasons: [] });
      }

      throw new Error(`unexpected ${url}`);
   };

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
   globalThis.fetch = async () => mockJsonResponse({
      status: 'requestedTimeNotAvailable',
      reasons: [],
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
