import assert from 'node:assert/strict';
import { afterEach, beforeEach, test } from 'node:test';

import { RegionSelector } from '../../../../scripts/itinerary/selectors/regionSelector.js';
import { DraftStorage } from '../../../../scripts/itinerary/draftStorage.js';
import { StorageKeys } from '../../../../scripts/itinerary/storageKeys.js';
import { createDomNode, installDocument, installTestWindow, teardownDocument } from '../../helpers/domMock.mjs';
import { createLocalStorageMock } from '../../helpers/localStorageMock.mjs';
import { clickExhibitToggle, clickRegionToggle } from '../../helpers/regionSelectorDom.mjs';
import { mockRegionSelectorFetch } from '../../helpers/fetchMock.mjs';

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

test('Test_RegionSelector_TestRegionSelectorShouldSkipRegionSelectionSyncIgnoresMatchingFingerprintAfterUIToggles_ExpectOk', () => {
   const fingerprint = ['Africa Savanna', 'Eurasia Wilds'].join('\0');

   assert.equal(
      RegionSelector.shouldSkipRegionSelectionSync({
         fingerprintAtShow: fingerprint,
         fingerprintNow: fingerprint,
         selectionChangedSinceShow: false,
      }),
      true
   );
   assert.equal(
      RegionSelector.shouldSkipRegionSelectionSync({
         fingerprintAtShow: fingerprint,
         fingerprintNow: fingerprint,
         selectionChangedSinceShow: true,
      }),
      false
   );
});

test('Test_Region_TestRegionSelectorSkipsAnimalRebuildWhenExhibitSelection_ExpectOk', async () => {
   localStorage.setItem(
      StorageKeys.ANIMALS_KEY,
      JSON.stringify([{ species: 'African Lion', exhibit: 'Africa Savanna' }])
   );
   localStorage.setItem(
      StorageKeys.SELECTED_EXHIBITS_KEY,
      JSON.stringify(['Africa Savanna'])
   );

   mockRegionSelectorFetch();

   const mountEl = createDomNode('div');
   let nextPayload;

   const controller = RegionSelector.createItineraryRegionSelectorController({
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

test('Test_Region_TestRegionSelectorRebuildsAnimalsAfterReSelectingAn_ExpectOk', async () => {
   localStorage.setItem(
      StorageKeys.ANIMALS_KEY,
      JSON.stringify([{ species: 'African Lion', exhibit: 'Africa Savanna' }])
   );
   localStorage.setItem(
      StorageKeys.SELECTED_EXHIBITS_KEY,
      JSON.stringify(['Africa Savanna'])
   );

   globalThis.fetch = mockRegionSelectorFetch({
      animals: [
         { species: 'African Lion', exhibit: 'Africa Savanna' },
         { species: 'African Penguin', exhibit: 'Africa Savanna' },
      ],
   });

   DraftStorage.removeAnimalFromItineraryAnimalDraft(
      'animals',
      'African Penguin||Africa Savanna'
   );

   const mountEl = createDomNode('div');
   let nextPayload;

   const controller = RegionSelector.createItineraryRegionSelectorController({
      mountEl,
      onNext: (animals) => {
         nextPayload = animals;
      },
   });

   await controller.show();

   const resultsEl = mountEl.querySelector('.itin-region-results');

   // Hydrate deselects incomplete exhibits; one toggle re-selects the exhibit.
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

test('Test_Region_TestRegionSelectorHideClearsTheMountElement_ExpectOk', async () => {
   mockRegionSelectorFetch();

   const mountEl = createDomNode('div');
   const controller = RegionSelector.createItineraryRegionSelectorController({ mountEl });

   await controller.show();
   assert.equal(mountEl.children.length, 1);

   controller.hide();
   assert.equal(mountEl.children.length, 0);
});

test('Test_Region_TestRegionSelectorNoOpsShowAndHideWithout_ExpectOk', async () => {
   const controller = RegionSelector.createItineraryRegionSelectorController({ mountEl: null });

   await controller.show();
   controller.hide();
});

test('Test_Region_TestRegionSelectorRoutesCloseAndPrevActions_ExpectOk', async () => {
   mockRegionSelectorFetch();

   const mountEl = createDomNode('div');
   const closeCalls = [];
   const prevCalls = [];

   const controller = RegionSelector.createItineraryRegionSelectorController({
      mountEl,
      onClose: () => {
         closeCalls.push('close');
      },
      onPrev: (animals) => {
         prevCalls.push(animals);
      },
   });

   await controller.show();

   mountEl.querySelector('.itin-close')?.click();
   mountEl.querySelector('.itin-prev')?.click();
   await flushAsyncWork();

   assert.deepEqual(closeCalls, ['close']);
   assert.deepEqual(prevCalls, [null]);
});

test('Test_Region_TestRegionSelectorPrevRebuildsAnimalsAfterTogglingAn_ExpectOk', async () => {
   localStorage.setItem(
      StorageKeys.ANIMALS_KEY,
      JSON.stringify([{ species: 'African Lion', exhibit: 'Africa Savanna' }])
   );
   localStorage.setItem(
      StorageKeys.SELECTED_EXHIBITS_KEY,
      JSON.stringify(['Africa Savanna'])
   );

   mockRegionSelectorFetch({
      animals: [
         { species: 'African Lion', exhibit: 'Africa Savanna' },
         { species: 'American Beaver', exhibit: 'Americas Outdoor Mayan Temple Ruins' },
      ],
      regions: [
         {
            name: 'Africa',
            exhibits: ['Africa Savanna'],
         },
         {
            name: 'Americas',
            exhibits: ['Americas Outdoor Mayan Temple Ruins'],
         },
      ],
   });

   const mountEl = createDomNode('div');
   let prevPayload;

   const controller = RegionSelector.createItineraryRegionSelectorController({
      mountEl,
      onPrev: (animals) => {
         prevPayload = animals;
      },
   });

   await controller.show();

   const resultsEl = mountEl.querySelector('.itin-region-results');
   clickExhibitToggle(resultsEl, 'Americas Outdoor Mayan Temple Ruins');

   mountEl.querySelector('.itin-prev')?.click();
   await flushAsyncWork();

   assert.ok(Array.isArray(prevPayload));
   assert.deepEqual(
      prevPayload.map((animal) => animal.species).sort(),
      ['African Lion', 'American Beaver']
   );
});

test('Test_Region_TestRegionSelectorFinishSkipsRebuildWhenStoredAnimals_ExpectOk', async () => {
   localStorage.setItem(
      StorageKeys.ANIMALS_KEY,
      JSON.stringify([{ species: 'African Lion', exhibit: 'Africa Savanna' }])
   );
   localStorage.setItem(
      StorageKeys.SELECTED_EXHIBITS_KEY,
      JSON.stringify(['Africa Savanna'])
   );

   mockRegionSelectorFetch({
      animals: [
         { species: 'African Lion', exhibit: 'Africa Savanna' },
      ],
   });

   const mountEl = createDomNode('div');
   const finishCalls = [];

   const controller = RegionSelector.createItineraryRegionSelectorController({
      mountEl,
      onFinish: (animals) => {
         finishCalls.push(animals);
      },
   });

   await controller.show();
   assert.equal(controller.shouldSkipClosingSelectionSync(), true);

   mountEl.querySelector('.itin-finish')?.click();
   await flushAsyncWork();

   assert.deepEqual(finishCalls, [null]);
});

test('Test_Region_TestRegionSelectorFinishRebuildsAnimalsWhenCatalogGrew_ExpectOk', async () => {
   localStorage.setItem(
      StorageKeys.ANIMALS_KEY,
      JSON.stringify([{ species: 'African Lion', exhibit: 'Africa Savanna' }])
   );
   localStorage.setItem(
      StorageKeys.SELECTED_EXHIBITS_KEY,
      JSON.stringify(['Africa Savanna'])
   );

   mockRegionSelectorFetch({
      animals: [
         { species: 'African Lion', exhibit: 'Africa Savanna' },
         { species: 'Watusi Cattle', exhibit: 'Africa Savanna' },
      ],
   });

   const mountEl = createDomNode('div');
   const finishCalls = [];

   const controller = RegionSelector.createItineraryRegionSelectorController({
      mountEl,
      onFinish: (animals) => {
         finishCalls.push(animals);
      },
   });

   await controller.show();
   assert.equal(controller.shouldSkipClosingSelectionSync(), false);

   mountEl.querySelector('.itin-finish')?.click();
   await flushAsyncWork();

   assert.equal(finishCalls.length, 1);
   assert.deepEqual(
      finishCalls[0].map((animal) => animal.species).sort(),
      ['African Lion', 'Watusi Cattle']
   );
});

test('Test_Region_TestRegionSelectorFinishRebuildsAnimalsWhenExhibitsAre_ExpectOk', async () => {
   mockRegionSelectorFetch({
      animals: [
         { species: 'African Lion', exhibit: 'Africa Savanna' },
      ],
   });

   const mountEl = createDomNode('div');
   const finishCalls = [];

   const controller = RegionSelector.createItineraryRegionSelectorController({
      mountEl,
      onFinish: (animals) => {
         finishCalls.push(animals);
      },
   });

   await controller.show();

   // Stale exhibit selection without itinerary animals is pruned on hydrate; select again.
   clickExhibitToggle(mountEl.querySelector('.itin-region-results'), 'Africa Savanna');
   assert.equal(controller.shouldSkipClosingSelectionSync(), false);

   mountEl.querySelector('.itin-finish')?.click();
   await flushAsyncWork();

   assert.equal(finishCalls.length, 1);
   assert.deepEqual(
      finishCalls[0].map((animal) => animal.species),
      ['African Lion']
   );
});

test('Test_Region_TestRegionSelectorTogglesRegionsAndIgnoresEmptyRegions_ExpectOk', async () => {
   localStorage.setItem(
      StorageKeys.SELECTED_EXHIBITS_KEY,
      JSON.stringify([])
   );

   mockRegionSelectorFetch({
      regions: [
         { name: 'Africa', exhibits: ['Africa Savanna'] },
         { name: 'Empty', exhibits: [] },
      ],
   });

   const mountEl = createDomNode('div');
   const controller = RegionSelector.createItineraryRegionSelectorController({ mountEl });

   await controller.show();

   const resultsEl = mountEl.querySelector('.itin-region-results');

   clickRegionToggle(resultsEl, 'Africa');
   clickRegionToggle(resultsEl, 'Empty');

   assert.equal(controller.shouldSkipClosingSelectionSync(), false);
});

test('Test_Region_TestRegionSelectorFinishCommitsAnimalsWhenSelectionChanged_ExpectOk', async () => {
   localStorage.setItem(
      StorageKeys.SELECTED_EXHIBITS_KEY,
      JSON.stringify([])
   );

   mockRegionSelectorFetch({
      animals: [
         { species: 'African Lion', exhibit: 'Africa Savanna' },
      ],
   });

   const mountEl = createDomNode('div');
   const finishCalls = [];

   const controller = RegionSelector.createItineraryRegionSelectorController({
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

test('Test_Region_TestRegionSelectorReusesTheBuiltViewOnSubsequent_ExpectOk', async () => {
   mockRegionSelectorFetch();

   const mountEl = createDomNode('div');
   const controller = RegionSelector.createItineraryRegionSelectorController({ mountEl });

   await controller.show();
   const firstRoot = mountEl.children[0];

   await controller.show();

   assert.equal(mountEl.children[0], firstRoot);
});
