import assert from 'node:assert/strict';
import test from 'node:test';

import { SearchController } from '../../../scripts/search/searchController.js';
import { SearchQueryRunner } from '../../../scripts/search/searchQueryRunner.js';
import { installDomTestHooks } from '../helpers/domTestSetup.mjs';

installDomTestHooks();

test('Test_InitSearch_TestMissingElements_ExpectNoop', () => {
   const original = SearchQueryRunner.createNoopSearch;
   SearchQueryRunner.createNoopSearch = () => ({ noop: true });

   try {
      assert.deepEqual(SearchController.initSearch({}), { noop: true });
   } finally {
      SearchQueryRunner.createNoopSearch = original;
   }
});

test('Test_InitSearch_TestWiredInput_ExpectRefresh', () => {
   const originalCreate = SearchQueryRunner.createSearchRunner;
   const originalDebounce = SearchQueryRunner.debounce;
   const runs = [];
   SearchQueryRunner.createSearchRunner = () => () => { runs.push('run'); };
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

      assert.equal(typeof inputEl.listeners.input, 'function');
      controller.refresh();
      assert.deepEqual(runs, ['run']);
   } finally {
      SearchQueryRunner.createSearchRunner = originalCreate;
      SearchQueryRunner.debounce = originalDebounce;
   }
});
