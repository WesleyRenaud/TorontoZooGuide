import assert from 'node:assert/strict';
import { test } from 'node:test';

import { CreateSelectorController } from '../../../../scripts/itinerary/selectors/createSelectorController.js';
import { createDomNode } from '../../helpers/domNodeMock.mjs';
import { installDomTestHooks } from '../../helpers/domTestSetup.mjs';
import { createLocalStorageMock } from '../../helpers/localStorageMock.mjs';

function buildStubElements() {
   return {
      rootEl: createDomNode('div', 'itin-overlay'),
      bodyEl: createDomNode('div', 'itin-card-body'),
      inputEl: createDomNode('input', 'itin-search-input'),
      resultsEl: createDomNode('div', 'animal-results'),
      prevButtonEl: createDomNode('button', 'itin-prev'),
      nextButtonEl: createDomNode('button', 'itin-next'),
      finishButtonEl: createDomNode('button', 'itin-finish'),
      closeButtonEl: createDomNode('button', 'itin-close'),
   };
}

test.describe('CreateSelectorController.createItinerarySelectorController', () => {
   installDomTestHooks({
      before: () => {
         globalThis.localStorage = createLocalStorageMock();
      },
      after: () => {
         delete globalThis.localStorage;
      },
   });

   test('Test_Show_TestShowAndHideManageTheMountElementAnd_ExpectOk', async () => {
      const mountEl = createDomNode('div', 'wizard-mount');
      const searchedQueries = [];
      const controller = CreateSelectorController.createItinerarySelectorController({
         mountEl,
         storageKey: 'tzg.test-selector',
         getId: (row) => row.id,
         extractRows: (response) => response.rows,
         topTitle: 'Top',
         h1: 'Heading',
         subtitle: 'Subtitle',
         deps: {
            createSearchRunner: (options) => ({
               runCurrentQuery: async () => {
                  searchedQueries.push(options.getQuery());
                  options.onRows([{ id: 'lion', name: 'Lion' }]);
               },
               scheduleCurrentQuery: () => {},
            }),
         },
      });

      controller.show();

      assert.equal(mountEl.children.length, 1);

      await new Promise((resolve) => {
         setTimeout(resolve, 0);
      });

      assert.deepEqual(searchedQueries, ['']);

      controller.hide();

      assert.equal(mountEl.children.length, 0);
   });

   test('Test_ShouldSkipClosingSelectionSync_TestShouldSkipClosingSelectionSyncDetectsUnchangedSelectionsAfterShow_ExpectOk', () => {
      const mountEl = createDomNode('div', 'wizard-mount');
      const controller = CreateSelectorController.createItinerarySelectorController({
         mountEl,
         storageKey: 'tzg.test-selector-skip',
         getId: (row) => row.id,
         extractRows: () => [],
         deps: {
            buildElements: buildStubElements,
            createSearchRunner: () => ({
               runCurrentQuery: async () => {},
               scheduleCurrentQuery: () => {},
            }),
         },
      });

      controller.show();

      assert.equal(controller.shouldSkipClosingSelectionSync(), true);
   });

   test('Test_Next_TestNextAndCloseHandlersReceiveTheCurrentSelection_ExpectOk', async () => {
      const mountEl = createDomNode('div', 'wizard-mount');
      const nextSnapshots = [];
      const closeCalls = [];
      let builtElements = null;
      const controller = CreateSelectorController.createItinerarySelectorController({
         mountEl,
         storageKey: 'tzg.test-selector-handlers',
         getId: (row) => row.id,
         extractRows: () => [],
         onNext: (snapshot) => {
            nextSnapshots.push(snapshot);
         },
         onClose: () => {
            closeCalls.push('closed');
         },
         deps: {
            buildElements: (...args) => {
               builtElements = buildStubElements(...args);
               return builtElements;
            },
            createSearchRunner: (options) => ({
               runCurrentQuery: async () => {
                  options.onRows([{ id: 'lion', name: 'Lion' }]);
               },
               scheduleCurrentQuery: () => {},
            }),
         },
      });

      controller.show();
      builtElements?.nextButtonEl.click();
      builtElements?.closeButtonEl.click();

      assert.deepEqual(nextSnapshots, [[]]);
      assert.deepEqual(closeCalls, ['closed']);
   });

   test('Test_Prev_TestPrevAndFinishHandlersReceiveTheCurrentSelection_ExpectOk', async () => {
      const mountEl = createDomNode('div', 'wizard-mount');
      const prevSnapshots = [];
      const finishSnapshots = [];
      let builtElements = null;
      const controller = CreateSelectorController.createItinerarySelectorController({
         mountEl,
         storageKey: 'tzg.test-selector-prev-finish',
         getId: (row) => row.id,
         extractRows: () => [],
         onPrev: (snapshot) => {
            prevSnapshots.push(snapshot);
         },
         onFinish: (snapshot) => {
            finishSnapshots.push(snapshot);
         },
         deps: {
            buildElements: (...args) => {
               builtElements = buildStubElements(...args);
               return builtElements;
            },
            createSearchRunner: (options) => ({
               runCurrentQuery: async () => {
                  options.onRows([{ id: 'tiger', name: 'Tiger' }]);
               },
               scheduleCurrentQuery: () => {},
            }),
         },
      });

      controller.show();
      builtElements?.prevButtonEl.click();
      builtElements?.finishButtonEl.click();

      assert.deepEqual(prevSnapshots, [[]]);
      assert.deepEqual(finishSnapshots, [[]]);
   });

   test('Test_RenderExtraControls_TestRenderExtraControlsCanRerunTheCurrentSearch_ExpectOk', async () => {
      const mountEl = createDomNode('div', 'wizard-mount');
      const searchedQueries = [];
      const controller = CreateSelectorController.createItinerarySelectorController({
         mountEl,
         storageKey: 'tzg.test-selector-extra',
         getId: (row) => row.id,
         extractRows: () => [],
         topTitle: 'Top',
         h1: 'Heading',
         subtitle: 'Subtitle',
         renderExtraControls: ({ rerunSearch }) => {
            rerunSearch();
         },
         deps: {
            createSearchRunner: (options) => ({
               runCurrentQuery: async () => {
                  searchedQueries.push(options.getQuery());
               },
               scheduleCurrentQuery: () => {},
            }),
         },
      });

      controller.show();

      await new Promise((resolve) => {
         setTimeout(resolve, 0);
      });

      assert.deepEqual(searchedQueries, ['', '']);
   });

   test('Test_Show_TestShowReusesTheBuiltShellOnSubsequentOpens_ExpectOk', () => {
      const mountEl = createDomNode('div', 'wizard-mount');
      const controller = CreateSelectorController.createItinerarySelectorController({
         mountEl,
         storageKey: 'tzg.test-selector-reuse',
         getId: (row) => row.id,
         extractRows: () => [],
         topTitle: 'Top',
         h1: 'Heading',
         subtitle: 'Subtitle',
         deps: {
            createSearchRunner: () => ({
               runCurrentQuery: async () => {},
               scheduleCurrentQuery: () => {},
            }),
         },
      });

      controller.show();
      const firstRoot = mountEl.children[0];

      controller.hide();
      controller.show();

      assert.equal(mountEl.children[0], firstRoot);
   });
});
