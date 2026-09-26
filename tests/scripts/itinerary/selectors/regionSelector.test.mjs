import assert from 'node:assert/strict';
import { afterEach, beforeEach, test } from 'node:test';

import { RegionSelector } from '../../../../scripts/itinerary/selectors/regionSelector.js';
import { RegionSelectorView } from '../../../../scripts/itinerary/selectors/regionSelectorView.js';
import { RegionStore } from '../../../../scripts/itinerary/selectors/regionSelector/regionStore.js';
import { DraftStore } from '../../../../scripts/itinerary/draftStore.js';
import { ScheduleItemKeySeparator } from '../../../../scripts/itinerary/scheduleItemKeySeparator.js';
import { StorageKeys } from '../../../../scripts/itinerary/storageKeys.js';
import { Position } from '../../../../scripts/shared/enums/position.js';
import { createDomNode, installDocument, installTestWindow, teardownDocument } from '../../helpers/domMock.mjs';
import { createLocalStorageMock } from '../../helpers/localStorageMock.mjs';
import { clickExhibitToggle, clickRegionToggle } from '../../helpers/regionSelectorDom.mjs';
import { mockRegionSelectorFetch } from '../../helpers/fetchMock.mjs';

async function _flushAsyncWork() {
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


test('Test_ShouldSkipRegionSelectionSync_TestUnchangedFingerprint_ExpectTrue', () => {
   const savanna = 'Africa Savanna';
   const eurasia = 'Eurasia Wilds';
   const fingerprint = [savanna, eurasia].join('\0');

   const shouldSkip = RegionSelector.shouldSkipRegionSelectionSync({
      fingerprintAtShow: fingerprint,
      fingerprintNow: fingerprint,
      selectionChangedSinceShow: false,
   });

   assert.equal(shouldSkip, true);
});


test('Test_ShouldSkipRegionSelectionSync_TestUiToggle_ExpectFalse', () => {
   const savanna = 'Africa Savanna';
   const eurasia = 'Eurasia Wilds';
   const fingerprint = [savanna, eurasia].join('\0');

   const shouldSkip = RegionSelector.shouldSkipRegionSelectionSync({
      fingerprintAtShow: fingerprint,
      fingerprintNow: fingerprint,
      selectionChangedSinceShow: true,
   });

   assert.equal(shouldSkip, false);
});


test('Test_CreateItineraryRegionSelectorController_TestUnchangedExhibits_ExpectSkipRebuild', async () => {
   const lion = { species: 'African Lion', exhibit: 'Africa Savanna' };
   localStorage.setItem(StorageKeys.ANIMALS_KEY, JSON.stringify([lion]));
   localStorage.setItem(StorageKeys.SELECTED_EXHIBITS_KEY, JSON.stringify([lion.exhibit]));
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
   mountEl.querySelector('.itin-next').click();
   await _flushAsyncWork();

   assert.equal(controller.shouldSkipClosingSelectionSync(), true);
   assert.equal(nextPayload, null);
});


test('Test_CreateItineraryRegionSelectorController_TestReselectExhibit_ExpectRebuild', async () => {
   const lion = { species: 'African Lion', exhibit: 'Africa Savanna' };
   const penguin = { species: 'African Penguin', exhibit: 'Africa Savanna' };
   localStorage.setItem(StorageKeys.ANIMALS_KEY, JSON.stringify([lion]));
   localStorage.setItem(StorageKeys.SELECTED_EXHIBITS_KEY, JSON.stringify([lion.exhibit]));
   globalThis.fetch = mockRegionSelectorFetch({
      animals: [lion, penguin],
   });
   DraftStore.removeAnimalFromItineraryAnimalDraft(
      'animals',
      [penguin.species, penguin.exhibit].join(ScheduleItemKeySeparator.VALUE)
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
   clickExhibitToggle(resultsEl, lion.exhibit);

   assert.equal(controller.shouldSkipClosingSelectionSync(), false);

   const animals = await controller.getSelectionSnapshot();
   mountEl.querySelector('.itin-next').click();
   await _flushAsyncWork();

   assert.equal(controller.shouldSkipClosingSelectionSync(), true);
   assert.deepEqual(
      animals.map((animal) => animal.species).sort(),
      [lion.species, penguin.species].sort()
   );
   assert.deepEqual(
      nextPayload.map((animal) => animal.species).sort(),
      [lion.species, penguin.species].sort()
   );
});


test('Test_Hide_TestShownSelector_ExpectClearedMount', async () => {
   mockRegionSelectorFetch();
   const mountEl = createDomNode('div');
   const controller = RegionSelector.createItineraryRegionSelectorController({ mountEl });
   await controller.show();

   controller.hide();

   assert.equal(mountEl.children.length, 0);
});


test('Test_ShowAndHide_TestMissingMount_ExpectNoOp', async () => {
   const controller = RegionSelector.createItineraryRegionSelectorController({ mountEl: null });

   await controller.show();
   controller.hide();
});


test('Test_CloseAndPrev_TestActions_ExpectRouted', async () => {
   mockRegionSelectorFetch();
   const mountEl = createDomNode('div');
   const closeCalls = [];
   const prevCalls = [];
   const closed = 'close';
   const controller = RegionSelector.createItineraryRegionSelectorController({
      mountEl,
      onClose: () => {
         closeCalls.push(closed);
      },
      onPrev: (animals) => {
         prevCalls.push(animals);
      },
   });
   await controller.show();

   mountEl.querySelector('.itin-close')?.click();
   mountEl.querySelector('.itin-prev')?.click();
   await _flushAsyncWork();

   assert.deepEqual(closeCalls, [closed]);
   assert.deepEqual(prevCalls, [null]);
});


test('Test_Prev_TestToggledExhibit_ExpectRebuiltAnimals', async () => {
   const lion = { species: 'African Lion', exhibit: 'Africa Savanna' };
   const beaver = {
      species: 'American Beaver',
      exhibit: 'Americas Outdoor Mayan Temple Ruins',
   };
   localStorage.setItem(StorageKeys.ANIMALS_KEY, JSON.stringify([lion]));
   localStorage.setItem(StorageKeys.SELECTED_EXHIBITS_KEY, JSON.stringify([lion.exhibit]));
   mockRegionSelectorFetch({
      animals: [lion, beaver],
      regions: [
         {
            name: 'Africa',
            exhibits: [lion.exhibit],
         },
         {
            name: 'Americas',
            exhibits: [beaver.exhibit],
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
   clickExhibitToggle(resultsEl, beaver.exhibit);

   mountEl.querySelector('.itin-prev')?.click();
   await _flushAsyncWork();

   assert.ok(Array.isArray(prevPayload));
   assert.deepEqual(
      prevPayload.map((animal) => animal.species).sort(),
      [lion.species, beaver.species].sort()
   );
});


test('Test_Finish_TestUnchangedStoredAnimals_ExpectSkipRebuild', async () => {
   const lion = { species: 'African Lion', exhibit: 'Africa Savanna' };
   localStorage.setItem(StorageKeys.ANIMALS_KEY, JSON.stringify([lion]));
   localStorage.setItem(StorageKeys.SELECTED_EXHIBITS_KEY, JSON.stringify([lion.exhibit]));
   mockRegionSelectorFetch({
      animals: [lion],
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
   await _flushAsyncWork();

   assert.deepEqual(finishCalls, [null]);
});


test('Test_Finish_TestCatalogGrew_ExpectRebuiltAnimals', async () => {
   const lion = { species: 'African Lion', exhibit: 'Africa Savanna' };
   const cattle = { species: 'Watusi Cattle', exhibit: 'Africa Savanna' };
   localStorage.setItem(StorageKeys.ANIMALS_KEY, JSON.stringify([lion]));
   localStorage.setItem(StorageKeys.SELECTED_EXHIBITS_KEY, JSON.stringify([lion.exhibit]));
   mockRegionSelectorFetch({
      animals: [lion, cattle],
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
   await _flushAsyncWork();

   assert.equal(finishCalls.length, 1);
   assert.deepEqual(
      finishCalls.at(Position.FIRST).map((animal) => animal.species).sort(),
      [lion.species, cattle.species].sort()
   );
});


test('Test_Finish_TestReselectedExhibit_ExpectRebuiltAnimals', async () => {
   const lion = { species: 'African Lion', exhibit: 'Africa Savanna' };
   mockRegionSelectorFetch({
      animals: [lion],
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
   clickExhibitToggle(mountEl.querySelector('.itin-region-results'), lion.exhibit);

   assert.equal(controller.shouldSkipClosingSelectionSync(), false);

   mountEl.querySelector('.itin-finish')?.click();
   await _flushAsyncWork();
   assert.equal(finishCalls.length, 1);
   assert.deepEqual(
      finishCalls.at(Position.FIRST).map((animal) => animal.species),
      [lion.species]
   );
});


test('Test_ToggleRegion_TestEmptyRegion_ExpectIgnored', async () => {
   const africa = 'Africa';
   const empty = 'Empty';
   const savanna = 'Africa Savanna';
   localStorage.setItem(StorageKeys.SELECTED_EXHIBITS_KEY, JSON.stringify([]));
   mockRegionSelectorFetch({
      regions: [
         { name: africa, exhibits: [savanna] },
         { name: empty, exhibits: [] },
      ],
   });
   const mountEl = createDomNode('div');
   const controller = RegionSelector.createItineraryRegionSelectorController({ mountEl });
   await controller.show();
   const resultsEl = mountEl.querySelector('.itin-region-results');

   clickRegionToggle(resultsEl, africa);
   clickRegionToggle(resultsEl, empty);

   assert.equal(controller.shouldSkipClosingSelectionSync(), false);
});


test('Test_Finish_TestSelectionChanged_ExpectCommittedAnimals', async () => {
   const lion = { species: 'African Lion', exhibit: 'Africa Savanna' };
   localStorage.setItem(StorageKeys.SELECTED_EXHIBITS_KEY, JSON.stringify([]));
   mockRegionSelectorFetch({
      animals: [lion],
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
   clickExhibitToggle(resultsEl, lion.exhibit);

   mountEl.querySelector('.itin-finish')?.click();
   await _flushAsyncWork();

   assert.equal(finishCalls.length, 1);
   assert.deepEqual(
      finishCalls.at(Position.FIRST).map((animal) => animal.species),
      [lion.species]
   );
});


test('Test_Show_TestSubsequentOpens_ExpectReusedView', async () => {
   mockRegionSelectorFetch();
   const mountEl = createDomNode('div');
   const controller = RegionSelector.createItineraryRegionSelectorController({ mountEl });
   await controller.show();
   const firstRoot = mountEl.children.at(Position.FIRST);

   await controller.show();

   assert.equal(mountEl.children.at(Position.FIRST), firstRoot);
});


test('Test_Show_TestMissingResultsEl_ExpectMounted', async () => {
   const originalBuild = RegionSelectorView.createRegionSelectorElements;
   RegionSelectorView.createRegionSelectorElements = () => ({
      rootEl: createDomNode('div', 'root'),
      resultsEl: null,
   });

   try {
      mockRegionSelectorFetch();
      const mountEl = createDomNode('div');
      const controller = RegionSelector.createItineraryRegionSelectorController({ mountEl });

      await controller.show();

      assert.equal(mountEl.children.length, 1);
   } finally {
      RegionSelectorView.createRegionSelectorElements = originalBuild;
   }
});


test('Test_Show_TestMissingRootEl_ExpectNoMount', async () => {
   const originalBuild = RegionSelectorView.createRegionSelectorElements;
   RegionSelectorView.createRegionSelectorElements = () => ({
      rootEl: null,
      resultsEl: createDomNode('div', 'results'),
   });

   try {
      mockRegionSelectorFetch();
      const mountEl = createDomNode('div');
      const controller = RegionSelector.createItineraryRegionSelectorController({ mountEl });

      await controller.show();

      assert.equal(mountEl.children.length, 0);
   } finally {
      RegionSelectorView.createRegionSelectorElements = originalBuild;
   }
});


test('Test_ShouldSkipClosingSelectionSync_TestAnimalsNeedRebuild_ExpectFalse', async () => {
   const originalNeedRebuild = RegionStore.selectedExhibitsNeedAnimalRebuild;
   RegionStore.selectedExhibitsNeedAnimalRebuild = () => true;
   const lion = { species: 'African Lion', exhibit: 'Africa Savanna' };

   try {
      localStorage.setItem(StorageKeys.ANIMALS_KEY, JSON.stringify([lion]));
      localStorage.setItem(StorageKeys.SELECTED_EXHIBITS_KEY, JSON.stringify([lion.exhibit]));
      mockRegionSelectorFetch();
      const mountEl = createDomNode('div');
      const controller = RegionSelector.createItineraryRegionSelectorController({ mountEl });

      await controller.show();

      assert.equal(controller.shouldSkipClosingSelectionSync(), false);
   } finally {
      RegionStore.selectedExhibitsNeedAnimalRebuild = originalNeedRebuild;
   }
});
