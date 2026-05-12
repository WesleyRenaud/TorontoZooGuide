import assert from 'node:assert/strict';
import { afterEach, beforeEach, test } from 'node:test';

import { createRegionSelectorState } from '../../scripts/itinerary/selectors/regionSelector/state.js';
import { DATE_KEY } from '../../scripts/itinerary/storageKeys.js';

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
});

afterEach(() => {
   delete globalThis.localStorage;
   delete globalThis.fetch;
});

test('getAnimalsByExhibit receives month and day from stored visit date', async () => {
   localStorage.setItem(DATE_KEY, '2026-08-12');

   globalThis.fetch = async (url, options) => {
      assert.equal(url, '/get-animals-by-exhibit');
      const body = JSON.parse(options.body);
      assert.equal(body.month, 'AUG');
      assert.equal(body.day, 12);
      assert.ok(Array.isArray(body.exhibitsToInclude));

      return {
         ok: true,
         status: 200,
         statusText: 'OK',
         text: async () => '{"animals":[]}',
      };
   };

   const state = createRegionSelectorState();
   state.setRegions([{ name: 'R1', exhibits: ['E1'] }]);
   assert.equal(state.toggleRegion('R1'), true);

   await state.buildUpdatedAnimalsFromSelection();
});

test('getAnimalsByExhibit falls back to today when no visit date is stored', async () => {
   globalThis.fetch = async (url, options) => {
      assert.equal(url, '/get-animals-by-exhibit');
      const body = JSON.parse(options.body);
      assert.equal(typeof body.month, 'string');
      assert.equal(typeof body.day, 'number');
      assert.ok(body.month.length >= 3);
      assert.ok(body.day >= 1 && body.day <= 31);

      return {
         ok: true,
         status: 200,
         statusText: 'OK',
         text: async () => '{"animals":[]}',
      };
   };

   const state = createRegionSelectorState();
   state.setRegions([{ name: 'R1', exhibits: ['E1'] }]);
   assert.equal(state.toggleRegion('R1'), true);

   await state.buildUpdatedAnimalsFromSelection();
});
