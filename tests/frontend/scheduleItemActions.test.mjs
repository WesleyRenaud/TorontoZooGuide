import assert from 'node:assert/strict';
import { afterEach, beforeEach, test } from 'node:test';

import {
   buildAnimalDraftEntry,
   buildAttractionDraftEntry,
   buildScheduleItemRequest,
   scheduleSelectedItineraryItem,
} from '../../scripts/itinerary/panel/scheduleItemActions.js';
import {
   resolveItineraryErrorMessage,
   updateItineraryErrorTypesFromConfig,
} from '../../scripts/itinerary/itineraryErrorTypes.js';
import { installDocument, installTestWindow, teardownDocument } from './helpers/domMock.mjs';

const MOCK_ERROR_TYPES = Object.freeze({
   SUCCESS: 'success',
   SAVE_FAILED: 'saveFailed',
   NO_AVAILABLE_SLOT: 'noAvailableSlot',
   REQUESTED_TIME_NOT_AVAILABLE: 'requestedTimeNotAvailable',
   ITEM_NOT_ON_ITINERARY: 'itemNotOnItinerary',
});

function mockJsonResponse(payload) {
   return {
      ok: true,
      status: 200,
      statusText: 'OK',
      text: async () => JSON.stringify(payload),
   };
}

beforeEach(() => {
   installTestWindow();
   installDocument();
   updateItineraryErrorTypesFromConfig({
      errorTypes: MOCK_ERROR_TYPES,
      suppressedErrorTypes: [],
   });
});

afterEach(() => {
   teardownDocument();
   delete globalThis.fetch;
   delete globalThis.window;
});

test('buildAnimalDraftEntry and buildAttractionDraftEntry normalize rows', () => {
   assert.deepEqual(
      buildAnimalDraftEntry({ species: 'Tiger', exhibit: 'Savanna' }),
      { species: 'Tiger', exhibit: 'Savanna' }
   );
   assert.equal(buildAnimalDraftEntry({ species: 'Tiger' }), null);
   assert.equal(buildAttractionDraftEntry({ name: 'Carousel' }), 'Carousel');
   assert.equal(buildAttractionDraftEntry({ name: '' }), null);
});

test('buildScheduleItemRequest maps event and animal rows', () => {
   assert.deepEqual(
      buildScheduleItemRequest('lunch', null, ['lunch']),
      { itemType: 'lunch', key: '' }
   );
   assert.deepEqual(
      buildScheduleItemRequest('animals', {
         species: 'Tiger',
         exhibit: 'Savanna',
         scheduleItemKind: 'animals',
      }, []),
      { itemType: 'animals', key: 'Tiger||Savanna' }
   );
});

test('buildScheduleItemRequest includes optional schedule times', () => {
   assert.deepEqual(
      buildScheduleItemRequest('lunch', null, ['lunch'], {
         startTime: '10:00 AM',
         durationMinutes: 20,
      }),
      {
         itemType: 'lunch',
         key: '',
         startTime: '10:00 AM',
         durationMinutes: 20,
      }
   );
   assert.equal(
      buildScheduleItemRequest('animals', {
         species: 'Tiger',
         exhibit: 'Savanna',
         scheduleItemKind: 'animals',
      }, [], { durationMinutes: 20 }),
      null
   );
});

test('scheduleSelectedItineraryItem schedules an event', async () => {
   const requests = [];

   globalThis.fetch = async (url, options = {}) => {
      requests.push({
         url,
         body: JSON.parse(options.body ?? '{}'),
      });

      return mockJsonResponse({ errorType: 'success' });
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
         suppressScheduleItemNotOnItineraryWarning: false,
      },
   }]);
});

test('scheduleSelectedItineraryItem schedules when type is unset but a row is selected', async () => {
   const urls = [];

   globalThis.fetch = async (url) => {
      urls.push(url);

      return mockJsonResponse({ errorType: 'success' });
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

test('scheduleSelectedItineraryItem confirms before scheduling a new animal', async () => {
   const requests = [];

   globalThis.fetch = async (url, options = {}) => {
      requests.push({
         url,
         body: JSON.parse(options.body ?? '{}'),
      });

      const isConfirmed = Boolean(
         requests.at(-1)?.body?.confirmingScheduleItemNotOnItinerary
      );

      return mockJsonResponse({
         errorType: isConfirmed ? 'success' : 'itemNotOnItinerary',
      });
   };

   const schedulePromise = scheduleSelectedItineraryItem(
      { date: '2026-06-15', animals: [], attractions: [] },
      'animals',
      { species: 'Tiger', exhibit: 'Savanna', scheduleItemKind: 'animals' },
      []
   );

   await new Promise((resolve) => {
      setTimeout(resolve, 0);
   });

   const confirmButton = document.querySelector('.tzg-popup-confirm');

   assert.ok(confirmButton);
   confirmButton.click();

   await new Promise((resolve) => {
      setTimeout(resolve, 0);
   });

   const result = await schedulePromise;

   assert.equal(result.errorType, 'success');
   assert.equal(requests.length, 2);
   assert.equal(requests[0].body.confirmingScheduleItemNotOnItinerary, false);
   assert.equal(requests[1].body.confirmingScheduleItemNotOnItinerary, true);
});

test('scheduleSelectedItineraryItem returns noAvailableSlot without refreshing', async () => {
   globalThis.fetch = async (url) => {
      if (url === '/schedule-itinerary-item') {
         return mockJsonResponse({ errorType: 'noAvailableSlot' });
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

test('resolveItineraryErrorMessage maps noAvailableSlot', () => {
   assert.match(
      resolveItineraryErrorMessage('noAvailableSlot'),
      /No open time slot/
   );
});

test('resolveItineraryErrorMessage maps requestedTimeNotAvailable', () => {
   assert.match(
      resolveItineraryErrorMessage('requestedTimeNotAvailable'),
      /That time is not available/
   );
});

test('scheduleSelectedItineraryItem surfaces requestedTimeNotAvailable', async () => {
   globalThis.fetch = async () => mockJsonResponse({
      errorType: 'requestedTimeNotAvailable',
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
