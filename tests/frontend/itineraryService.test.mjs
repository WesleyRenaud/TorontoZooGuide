import assert from 'node:assert/strict';
import {
   afterEach,
   beforeEach,
   test,
} from 'node:test';

import {
   isItineraryEmpty,
   normalizeItinerary,
   saveItinerary,
} from '../../scripts/itinerary/itineraryService.js';
import { updateItineraryErrorTypesFromConfig } from '../../scripts/itinerary/itineraryErrorTypes.js';
import { installDocument, installTestWindow, teardownDocument } from './helpers/domMock.mjs';
import { SELECTED_EXHIBITS_KEY } from '../../scripts/itinerary/storageKeys.js';

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

beforeEach(() => {
   globalThis.localStorage = createLocalStorageMock();
   installTestWindow();
   installDocument();
   updateItineraryErrorTypesFromConfig({
      errorTypes: {
         SUCCESS: 'success',
         GUARDIANS_TALK_WILL_UNSCHEDULE_ITEMS: 'guardiansTalkWillUnscheduleItems',
      },
      suppressedErrorTypes: [],
   });
   globalThis.CustomEvent = class CustomEvent {
      constructor(type, options = {}) {
         this.type = type;
         this.detail = options.detail;
      }
   };
});

afterEach(() => {
   teardownDocument();
   delete globalThis.CustomEvent;
   delete globalThis.fetch;
   delete globalThis.localStorage;
   delete globalThis.window;
});

test('normalizeItinerary exposes itineraryConfig and active state', () => {
   const config = {
      eventTypes: ['lunch'],
      errorTypes: { SUCCESS: 'success' },
      suppressedErrorTypes: [],
   };

   const normalized = normalizeItinerary({
      date: '2026-06-15',
      animals: [{ species: 'Tiger', exhibit: 'Savanna' }],
      itineraryConfig: config,
   });

   assert.equal(normalized.itineraryConfig, config);
   assert.equal(normalized.isActive, true);
   assert.equal(isItineraryEmpty(normalized), false);
});

test('normalizeItinerary preserves scheduled generic events', () => {
   const normalized = normalizeItinerary({
      date: '2026-06-15',
      events: [{ event_type: 'lunch', start_time: '12:00', end_time: '12:40' }],
   });

   assert.deepEqual(normalized.events, [{
      event_type: 'lunch',
      start_time: '12:00',
      end_time: '12:40',
   }]);
   assert.equal(isItineraryEmpty(normalized), false);
});

test('normalizeItinerary treats missing collections as empty', () => {
   const normalized = normalizeItinerary({
      animals: 'not-an-array',
      attractions: null,
   });

   assert.deepEqual(normalized.animals, []);
   assert.deepEqual(normalized.attractions, []);
   assert.deepEqual(normalized.events, []);
   assert.equal(normalized.itineraryConfig, null);
   assert.equal(normalized.isActive, false);
});

test('saveItinerary includes selected exhibits in the backend payload', async () => {
   localStorage.setItem(
      SELECTED_EXHIBITS_KEY,
      JSON.stringify(['Africa Savanna', '  ', 'Eurasia'])
   );

   globalThis.fetch = async (url, options) => {
      assert.equal(url, '/set-itinerary');
      assert.deepEqual(JSON.parse(options.body), {
         date: '2026-06-15',
         arrivalTime: '',
         departureTime: '',
         animals: [],
         attractions: [],
         guardiansTalks: [],
         wildEncounters: [],
         selectedExhibits: ['Africa Savanna', 'Eurasia'],
         temp: null,
         overridingConflictingGuardiansTalks: false,
      });

      return {
         ok: true,
         status: 200,
         statusText: 'OK',
         text: async () => JSON.stringify({
            itinerary: {
               date: '2026-06-15',
               animals: [],
               attractions: [],
               guardians_talks: [],
               wild_encounters: [],
            },
            issues: [],
         }),
      };
   };

   await saveItinerary({
      date: '2026-06-15',
      animals: [],
      attractions: [],
      guardiansTalks: [],
      wildEncounters: [],
   }, {
      selectedExhibits: ['Africa Savanna', 'Eurasia'],
   });
});

test('saveItinerary omits selected exhibits by default', async () => {
   localStorage.setItem(
      SELECTED_EXHIBITS_KEY,
      JSON.stringify(['Africa Savanna'])
   );

   globalThis.fetch = async (url, options) => {
      assert.equal(url, '/set-itinerary');
      assert.deepEqual(JSON.parse(options.body).selectedExhibits, []);

      return {
         ok: true,
         status: 200,
         statusText: 'OK',
         text: async () => JSON.stringify({
            itinerary: {
               date: '2026-06-15',
               animals: [],
               attractions: [],
               guardians_talks: [],
               wild_encounters: [],
            },
            issues: [],
         }),
      };
   };

   await saveItinerary({
      date: '2026-06-15',
      animals: [],
      attractions: [],
      guardiansTalks: [],
      wildEncounters: [],
   });
});

test('saveItinerary confirms before saving a guardians talk that unschedules items', async () => {
   const requests = [];
   const itineraryConfig = {
      itinerary_error_types: {
         SUCCESS: 'success',
         GUARDIANS_TALK_WILL_UNSCHEDULE_ITEMS: 'guardiansTalkWillUnscheduleItems',
      },
      suppressed_error_types: [],
   };

   globalThis.fetch = async (url, options) => {
      requests.push({
         url,
         body: JSON.parse(options.body ?? '{}'),
      });

      const isConfirmed = Boolean(
         requests.at(-1)?.body?.confirmingGuardiansTalkUnschedule
      );

      return {
         ok: true,
         status: 200,
         statusText: 'OK',
         text: async () => JSON.stringify({
            errorType: isConfirmed ? 'success' : 'guardiansTalkWillUnscheduleItems',
            issues: isConfirmed ? [] : [{
               type: 'guardiansTalkWillUnscheduleItems',
               items: [{
                  name: 'African Lion',
                  item_type: 'guardiansTalk',
               }],
            }],
            itinerary_config: itineraryConfig,
            itinerary: {
               date: '2026-06-15',
               animals: [],
               attractions: [],
               guardians_talks: [],
               wild_encounters: [],
            },
         }),
      };
   };

   const savePromise = saveItinerary({
      date: '2026-06-15',
      animals: [],
      attractions: [],
      guardiansTalks: [{ name: 'African Lion' }],
      wildEncounters: [],
   });

   await new Promise((resolve) => {
      setTimeout(resolve, 0);
   });

   const popupMessage = document.querySelector('.tzg-popup-message');

   assert.match(
      popupMessage?.textContent ?? '',
      /Adding these Meet the Guardians Talks: African Lion will unschedule other items/
   );

   document.querySelector('.tzg-popup-confirm')?.click();

   await new Promise((resolve) => {
      setTimeout(resolve, 0);
   });

   await savePromise;

   assert.equal(requests.length, 2);
   assert.equal(requests[0].body.confirmingGuardiansTalkUnschedule, undefined);
   assert.equal(requests[1].body.confirmingGuardiansTalkUnschedule, true);
});
