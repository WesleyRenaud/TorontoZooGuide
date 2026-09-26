import assert from 'node:assert/strict';
import test from 'node:test';

import { SearchController } from '../../../scripts/search/searchController.js';
import { SearchQueryRunner } from '../../../scripts/search/searchQueryRunner.js';
import { installDomTestHooks } from '../helpers/domTestSetup.mjs';

installDomTestHooks();


test('Test_InitSearch_TestMissingElements_ExpectNoop', () => {
   const original = SearchQueryRunner.createNoopSearch;
   const noop = { noop: true };
   SearchQueryRunner.createNoopSearch = () => noop;

   try {
      const controller = SearchController.initSearch({});

      assert.deepEqual(controller, noop);
   } finally {
      SearchQueryRunner.createNoopSearch = original;
   }
});


test('Test_InitSearch_TestWiredInput_ExpectRefresh', () => {
   const originalCreate = SearchQueryRunner.createSearchRunner;
   const originalDebounce = SearchQueryRunner.debounce;
   const runs = [];
   const runLabel = 'run';
   SearchQueryRunner.createSearchRunner = () => () => { runs.push(runLabel); };
   SearchQueryRunner.debounce = (fn) => fn;

   try {
      const inputEl = document.createElement('input');
      const resultsEl = document.createElement('div');
      const controller = SearchController.initSearch({
         inputEl,
         resultsEl,
         getIncludeFlags: () => ({}),
         getContext: () => ({}),
         onFocusRow: () => {},
      });

      controller.refresh();

      assert.equal(typeof inputEl.listeners.input, 'function');
      assert.deepEqual(runs, [runLabel]);
   } finally {
      SearchQueryRunner.createSearchRunner = originalCreate;
      SearchQueryRunner.debounce = originalDebounce;
   }
});
