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
import { createLocalStorageMock } from './helpers/localStorageMock.mjs';
import {
   clickExhibitToggle,
   clickRegionToggle,
} from './helpers/regionSelectorDom.mjs';
import { mockRegionSelectorFetch } from './helpers/fetchMock.mjs';

async function flushAsyncWork() {
   await new Promise((resolve) => {
      setImmediate(resolve);
   });
   await new Promise((resolve) => {
      setImmediate(resolve);
   });
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

   globalThis.fetch = mockRegionSelectorFetch({
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

test('region selector no-ops show and hide without a mount element', async () => {
   const controller = createItineraryRegionSelectorController({ mountEl: null });

   await controller.show();
   controller.hide();
});

test('region selector routes close and prev actions', async () => {
   mockRegionSelectorFetch();

   const mountEl = createDomNode('div');
   const closeCalls = [];
   const prevCalls = [];

   const controller = createItineraryRegionSelectorController({
      mountEl,
      onClose: () => {
         closeCalls.push('close');
      },
      onPrev: () => {
         prevCalls.push('prev');
      },
   });

   await controller.show();

   mountEl.querySelector('.itin-close')?.click();
   mountEl.querySelector('.itin-prev')?.click();

   assert.deepEqual(closeCalls, ['close']);
   assert.deepEqual(prevCalls, ['prev']);
});

test('region selector finish skips rebuild when selection is unchanged', async () => {
   localStorage.setItem(
      SELECTED_EXHIBITS_KEY,
      JSON.stringify(['Africa Savanna'])
   );

   mockRegionSelectorFetch();

   const mountEl = createDomNode('div');
   const finishCalls = [];

   const controller = createItineraryRegionSelectorController({
      mountEl,
      onFinish: (animals) => {
         finishCalls.push(animals);
      },
   });

   await controller.show();
   mountEl.querySelector('.itin-finish')?.click();
   await flushAsyncWork();

   assert.deepEqual(finishCalls, [null]);
});

test('region selector toggles regions and ignores empty regions', async () => {
   localStorage.setItem(
      SELECTED_EXHIBITS_KEY,
      JSON.stringify([])
   );

   mockRegionSelectorFetch({
      regions: [
         { name: 'Africa', exhibits: ['Africa Savanna'] },
         { name: 'Empty', exhibits: [] },
      ],
   });

   const mountEl = createDomNode('div');
   const controller = createItineraryRegionSelectorController({ mountEl });

   await controller.show();

   const resultsEl = mountEl.querySelector('.itin-region-results');

   clickRegionToggle(resultsEl, 'Africa');
   clickRegionToggle(resultsEl, 'Empty');

   assert.equal(controller.shouldSkipClosingSelectionSync(), false);
});

test('region selector finish commits animals when selection changed', async () => {
   localStorage.setItem(
      SELECTED_EXHIBITS_KEY,
      JSON.stringify([])
   );

   mockRegionSelectorFetch({
      animals: [
         { species: 'African Lion', exhibit: 'Africa Savanna' },
      ],
   });

   const mountEl = createDomNode('div');
   const finishCalls = [];

   const controller = createItineraryRegionSelectorController({
      mountEl,
      onFinish: (animals) => {
         finishCalls.push(animals);
      },
   });

   await controller.show();

   const resultsEl = mountEl.querySelector('.itin-region-results');

   clickExhibitToggle(resultsEl, 'Africa Savanna');
   mountEl.querySelector('.itin-finish')?.click();
   await flushAsyncWork();

   assert.equal(finishCalls.length, 1);
   assert.deepEqual(
      finishCalls[0].map((animal) => animal.species),
      ['African Lion']
   );
});

test('region selector reuses the built view on subsequent show calls', async () => {
   mockRegionSelectorFetch();

   const mountEl = createDomNode('div');
   const controller = createItineraryRegionSelectorController({ mountEl });

   await controller.show();
   const firstRoot = mountEl.children[0];

   await controller.show();

   assert.equal(mountEl.children[0], firstRoot);
});
