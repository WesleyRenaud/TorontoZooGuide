import assert from 'node:assert/strict';
import { afterEach, beforeEach, test } from 'node:test';

import {
   createItineraryRegionSelectorController,
   shouldSkipRegionSelectionSync,
} from '../../scripts/itinerary/selectors/regionSelector.js';
import { removeAnimalFromItineraryAnimalDraft } from '../../scripts/itinerary/draftStorage.js';
import { ANIMALS_KEY, SELECTED_EXHIBITS_KEY } from '../../scripts/itinerary/storageKeys.js';
import {
   createDomNode,
   installDocument,
   installTestWindow,
   teardownDocument,
} from './helpers/domMock.mjs';

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

function findChoiceButton(root, { action, exhibitName = '' } = {}) {
   const stack = [root];

   while (stack.length > 0) {
      const node = stack.shift();

      if (
         node.dataset?.action === action
         && (!exhibitName || node.dataset.exhibit === exhibitName)
      ) {
         return node;
      }

      stack.push(...(node.children ?? []));
   }

   return null;
}

function clickExhibitToggle(resultsEl, exhibitName) {
   const button = findChoiceButton(resultsEl, {
      action: 'toggle-exhibit',
      exhibitName,
   });

   assert.ok(button, `Expected exhibit toggle for ${exhibitName}`);

   dispatchResultsClick(resultsEl, button);
}

function dispatchResultsClick(resultsEl, button) {
   resultsEl.listeners.click({
      target: button,
      preventDefault() {},
      stopPropagation() {},
   });
}

async function flushAsyncWork() {
   await new Promise((resolve) => {
      setImmediate(resolve);
   });
   await new Promise((resolve) => {
      setImmediate(resolve);
   });
}

function mockRegionSelectorFetch({
   regions = [{ name: 'Africa', exhibits: ['Africa Savanna'] }],
   animals = [],
} = {}) {
   globalThis.fetch = async (url) => {
      if (url === '/get-exhibits-by-region') {
         return {
            ok: true,
            status: 200,
            statusText: 'OK',
            text: async () => JSON.stringify({ regions }),
         };
      }

      if (url === '/get-animals-by-exhibit') {
         return {
            ok: true,
            status: 200,
            statusText: 'OK',
            text: async () => JSON.stringify({ animals }),
         };
      }

      throw new Error(`Unexpected fetch url: ${url}`);
   };
}

beforeEach(() => {
   installDocument();
   installTestWindow();
   globalThis.localStorage = createLocalStorageMock();
});

afterEach(() => {
   teardownDocument();
   delete globalThis.localStorage;
   delete globalThis.fetch;
});

test('shouldSkipRegionSelectionSync ignores matching fingerprint after UI toggles', () => {
   const fingerprint = ['Africa Savanna', 'Eurasia Wilds'].join('\0');

   assert.equal(
      shouldSkipRegionSelectionSync({
         fingerprintAtShow: fingerprint,
         fingerprintNow: fingerprint,
         selectionChangedSinceShow: false,
      }),
      true
   );
   assert.equal(
      shouldSkipRegionSelectionSync({
         fingerprintAtShow: fingerprint,
         fingerprintNow: fingerprint,
         selectionChangedSinceShow: true,
      }),
      false
   );
});

test('region selector skips animal rebuild when exhibit selection is unchanged', async () => {
   localStorage.setItem(
      ANIMALS_KEY,
      JSON.stringify([{ species: 'African Lion', exhibit: 'Africa Savanna' }])
   );
   localStorage.setItem(
      SELECTED_EXHIBITS_KEY,
      JSON.stringify(['Africa Savanna'])
   );

   mockRegionSelectorFetch();

   const mountEl = createDomNode('div');
   let nextPayload;

   const controller = createItineraryRegionSelectorController({
      mountEl,
      onNext: (animals) => {
         nextPayload = animals;
      },
   });

   await controller.show();
   assert.equal(controller.shouldSkipClosingSelectionSync(), true);

   mountEl.querySelector('.itin-next').click();
   await flushAsyncWork();

   assert.equal(nextPayload, null);
});

test('region selector rebuilds animals after re-selecting an exhibit in the UI', async () => {
   localStorage.setItem(
      ANIMALS_KEY,
      JSON.stringify([{ species: 'African Lion', exhibit: 'Africa Savanna' }])
   );
   localStorage.setItem(
      SELECTED_EXHIBITS_KEY,
      JSON.stringify(['Africa Savanna'])
   );

   mockRegionSelectorFetch({
      animals: [
         { species: 'African Lion', exhibit: 'Africa Savanna' },
         { species: 'African Penguin', exhibit: 'Africa Savanna' },
      ],
   });

   removeAnimalFromItineraryAnimalDraft(
      'animals',
      'African Penguin||Africa Savanna'
   );

   const mountEl = createDomNode('div');
   let nextPayload;

   const controller = createItineraryRegionSelectorController({
      mountEl,
      onNext: (animals) => {
         nextPayload = animals;
      },
   });

   await controller.show();

   const resultsEl = mountEl.querySelector('.itin-region-results');

   clickExhibitToggle(resultsEl, 'Africa Savanna');
   clickExhibitToggle(resultsEl, 'Africa Savanna');

   assert.equal(controller.shouldSkipClosingSelectionSync(), false);

   const animals = await controller.getSelectionSnapshot();

   assert.deepEqual(
      animals.map((animal) => animal.species).sort(),
      ['African Lion', 'African Penguin']
   );

   mountEl.querySelector('.itin-next').click();
   await flushAsyncWork();

   assert.deepEqual(
      nextPayload.map((animal) => animal.species).sort(),
      ['African Lion', 'African Penguin']
   );
   assert.equal(controller.shouldSkipClosingSelectionSync(), true);
});

test('region selector hide clears the mount element', async () => {
   mockRegionSelectorFetch();

   const mountEl = createDomNode('div');
   const controller = createItineraryRegionSelectorController({ mountEl });

   await controller.show();
   assert.equal(mountEl.children.length, 1);

   controller.hide();
   assert.equal(mountEl.children.length, 0);
});
