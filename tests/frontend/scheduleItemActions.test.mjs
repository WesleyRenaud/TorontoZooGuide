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
import { installTestWindow } from './helpers/domMock.mjs';
import { SELECTED_EXHIBITS_KEY } from '../../scripts/itinerary/storageKeys.js';

const MOCK_ERROR_TYPES = Object.freeze({
   SUCCESS: 'success',
   SAVE_FAILED: 'saveFailed',
   NO_AVAILABLE_SLOT: 'noAvailableSlot',
});

function createLocalStorageMock() {
   const values = new Map();

   return {
      getItem: (key) => values.get(key) ?? null,
      setItem: (key, value) => {
         values.set(key, String(value));
      },
      removeItem: (key) => {
         values.delete(key);
      },
   };
}

function mockJsonResponse(payload) {
   return {
      ok: true,
      status: 200,
      statusText: 'OK',
      text: async () => JSON.stringify(payload),
   };
}

function mockSetItineraryResponse() {
   return mockJsonResponse({
      error_type: 'success',
      itinerary: {
         date: '2026-06-15',
         animals: [{ species: 'Tiger', exhibit: 'Savanna' }],
         attractions: [],
         guardians_talks: [],
         wild_encounters: [],
      },
      itinerary_config: {
         itinerary_event_types: [],
         itinerary_error_types: MOCK_ERROR_TYPES,
         suppressed_error_types: [],
      },
      issues: [],
   });
}

beforeEach(() => {
   globalThis.localStorage = createLocalStorageMock();
   installTestWindow();
   updateItineraryErrorTypesFromConfig({
      errorTypes: MOCK_ERROR_TYPES,
      suppressedErrorTypes: [],
   });
   localStorage.setItem(SELECTED_EXHIBITS_KEY, JSON.stringify([]));
});

afterEach(() => {
   delete globalThis.fetch;
   delete globalThis.localStorage;
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

test('scheduleSelectedItineraryItem schedules an event', async () => {
   const urls = [];

   globalThis.fetch = async (url) => {
      urls.push(url);

      return mockJsonResponse({ errorType: 'success' });
   };

   const result = await scheduleSelectedItineraryItem(
      { date: '2026-06-15', animals: [], attractions: [] },
      'lunch',
      null,
      ['lunch']
   );

   assert.equal(result.errorType, 'success');
   assert.deepEqual(urls, ['/schedule-itinerary-item']);
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

test('scheduleSelectedItineraryItem adds animal then schedules', async () => {
   const urls = [];

   globalThis.fetch = async (url) => {
      urls.push(url);

      if (url === '/set-itinerary') {
         return mockSetItineraryResponse();
      }

      return mockJsonResponse({ errorType: 'success' });
   };

   const result = await scheduleSelectedItineraryItem(
      { date: '2026-06-15', animals: [], attractions: [] },
      'animals',
      { species: 'Tiger', exhibit: 'Savanna', scheduleItemKind: 'animals' },
      []
   );

   assert.equal(result.errorType, 'success');
   assert.deepEqual(urls, ['/set-itinerary', '/schedule-itinerary-item']);
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
   updateItineraryErrorTypesFromConfig({
      errorTypes: MOCK_ERROR_TYPES,
      suppressedErrorTypes: [],
   });

   assert.match(
      resolveItineraryErrorMessage('noAvailableSlot'),
      /No open time slot/
   );
});
