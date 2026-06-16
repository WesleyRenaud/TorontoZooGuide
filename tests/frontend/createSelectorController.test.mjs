import assert from 'node:assert/strict';
import { afterEach, beforeEach, test } from 'node:test';

import { createItinerarySelectorController } from '../../scripts/itinerary/selectors/createSelectorController.js';
import { createDomNode } from './helpers/domNodeMock.mjs';
import { installDocument, installTestWindow, teardownDocument } from './helpers/domMock.mjs';
import { createLocalStorageMock } from './helpers/localStorageMock.mjs';

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

test.describe('createItinerarySelectorController', () => {
   beforeEach(() => {
      globalThis.localStorage = createLocalStorageMock();
      installTestWindow();
      installDocument();
   });

   afterEach(() => {
      teardownDocument();
      delete globalThis.window;
      delete globalThis.localStorage;
   });

   test('show and hide manage the mount element and run an initial search', async () => {
      const mountEl = createDomNode('div', 'wizard-mount');
      const searchedQueries = [];
      const controller = createItinerarySelectorController({
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

   test('shouldSkipClosingSelectionSync detects unchanged selections after show', () => {
      const mountEl = createDomNode('div', 'wizard-mount');
      const controller = createItinerarySelectorController({
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

   test('next and close handlers receive the current selection snapshot', async () => {
      const mountEl = createDomNode('div', 'wizard-mount');
      const nextSnapshots = [];
      const closeCalls = [];
      let builtElements = null;
      const controller = createItinerarySelectorController({
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

   test('prev and finish handlers receive the current selection snapshot', async () => {
      const mountEl = createDomNode('div', 'wizard-mount');
      const prevSnapshots = [];
      const finishSnapshots = [];
      let builtElements = null;
      const controller = createItinerarySelectorController({
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

   test('renderExtraControls can rerun the current search', async () => {
      const mountEl = createDomNode('div', 'wizard-mount');
      const searchedQueries = [];
      const controller = createItinerarySelectorController({
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

   test('show reuses the built shell on subsequent opens', () => {
      const mountEl = createDomNode('div', 'wizard-mount');
      const controller = createItinerarySelectorController({
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
