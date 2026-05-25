import assert from 'node:assert/strict';
import {
   afterEach,
   beforeEach,
   test,
} from 'node:test';

import { saveItinerary } from '../../scripts/itinerary/itineraryService.js';
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
   globalThis.window = {
      dispatchEvent: () => {},
   };
   globalThis.CustomEvent = class CustomEvent {
      constructor(type, options = {}) {
         this.type = type;
         this.detail = options.detail;
      }
   };
});

afterEach(() => {
   delete globalThis.CustomEvent;
   delete globalThis.fetch;
   delete globalThis.localStorage;
   delete globalThis.window;
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
         animals: [],
         attractions: [],
         guardiansTalks: [],
         wildEncounters: [],
         selectedExhibits: ['Africa Savanna', 'Eurasia'],
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
   });
});
