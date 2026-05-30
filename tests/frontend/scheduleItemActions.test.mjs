import assert from 'node:assert/strict';
import { afterEach, beforeEach, test } from 'node:test';

import {
   addAnimalToItinerary,
   addAttractionToItinerary,
   buildAnimalDraftEntry,
   buildAttractionDraftEntry,
} from '../../scripts/itinerary/panel/scheduleItemActions.js';
import { installTestWindow } from './helpers/domMock.mjs';
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

function mockSaveResponse(itineraryOverrides = {}) {
   return {
      ok: true,
      status: 200,
      statusText: 'OK',
      text: async () => JSON.stringify({
         error_type: 'success',
         itinerary: {
            date: '2026-06-15',
            animals: [],
            attractions: [],
            guardians_talks: [],
            wild_encounters: [],
            ...itineraryOverrides,
         },
         itinerary_config: {
            itinerary_event_types: [],
            itinerary_error_types: { SUCCESS: 'success' },
            suppressed_error_types: [],
         },
         issues: [],
      }),
   };
}

beforeEach(() => {
   globalThis.localStorage = createLocalStorageMock();
   installTestWindow();
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

test('addAnimalToItinerary and addAttractionToItinerary persist through saveItinerary', async () => {
   const saveCalls = [];

   globalThis.fetch = async (url, options) => {
      assert.equal(url, '/set-itinerary');
      saveCalls.push(JSON.parse(options.body));
      return mockSaveResponse({
         animals: [{ species: 'Tiger', exhibit: 'Savanna' }],
         attractions: ['Carousel'],
      });
   };

   localStorage.setItem(SELECTED_EXHIBITS_KEY, JSON.stringify([]));

   const animalResult = await addAnimalToItinerary(
      { date: '2026-06-15', animals: [], attractions: [] },
      { species: 'Tiger', exhibit: 'Savanna' }
   );

   assert.deepEqual(saveCalls[0].animals, [{ species: 'Tiger', exhibit: 'Savanna' }]);
   assert.deepEqual(animalResult.animals, [{ species: 'Tiger', exhibit: 'Savanna' }]);

   await addAttractionToItinerary(
      { date: '2026-06-15', animals: [], attractions: [] },
      { name: 'Carousel' }
   );

   assert.deepEqual(saveCalls[1].attractions, ['Carousel']);

   const itinerary = { date: '2026-06-15', animals: [], attractions: ['Carousel'] };
   const unchanged = await addAnimalToItinerary(itinerary, { species: '' });

   assert.equal(unchanged, itinerary);
   assert.equal(saveCalls.length, 2);
});
