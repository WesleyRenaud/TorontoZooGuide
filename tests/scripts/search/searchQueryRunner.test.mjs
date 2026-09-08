import assert from 'node:assert/strict';
import test from 'node:test';

import { SearchClient } from '../../../scripts/api/searchClient.js';
import { SearchBuilder } from '../../../scripts/search/searchBuilder.js';
import { SearchQueryRunner } from '../../../scripts/search/searchQueryRunner.js';
import { SearchResultsRenderer } from '../../../scripts/search/searchResultsRenderer.js';
import { installDomTestHooks } from '../helpers/domTestSetup.mjs';

installDomTestHooks();

test('Test_CreateNoopSearch_TestRefresh_ExpectNoop', () => {
   const noop = SearchQueryRunner.createNoopSearch();
   assert.equal(typeof noop.refresh, 'function');
   noop.refresh();
});

test('Test_Debounce_TestDelay_ExpectSingleCall', async () => {
   const calls = [];
   const debounced = SearchQueryRunner.debounce((value) => calls.push(value), 20);

   debounced(1);
   debounced(2);
   await new Promise((resolve) => setTimeout(resolve, 40));
   assert.deepEqual(calls, [2]);
});

test('Test_GetSearchQueryAndClearHelpers_TestValues_ExpectTrimAndClear', () => {
   const inputEl = document.createElement('input');
   inputEl.value = '  lion  ';
   assert.equal(SearchQueryRunner.getSearchQuery(inputEl), 'lion');

   assert.equal(SearchQueryRunner.shouldClearForEmptyQuery('', false), true);
   assert.equal(SearchQueryRunner.shouldClearForEmptyQuery('', true), false);
   assert.equal(SearchQueryRunner.shouldClearForEmptyQuery('x', false), false);

   const resultsEl = document.createElement('div');
   resultsEl.appendChild(document.createElement('div'));
   SearchQueryRunner.clearSearchResults(resultsEl);
   assert.equal(resultsEl.children.length, 0);
});

test('Test_CreateRequestTracker_TestIds_ExpectCurrent', () => {
   const tracker = SearchQueryRunner.createRequestTracker();
   const first = tracker.nextRequestId();
   const second = tracker.nextRequestId();
   assert.equal(tracker.isCurrentRequest(first), false);
   assert.equal(tracker.isCurrentRequest(second), true);
});

test('Test_LogSearchError_TestError_ExpectWarn', () => {
   const warns = [];
   const originalWarn = console.warn;
   console.warn = (...args) => warns.push(args);

   try {
      SearchQueryRunner.logSearchError('boom');
      assert.match(String(warns[0][0]), /failed to fetch results/);
   } finally {
      console.warn = originalWarn;
   }
});

test('Test_BuildSearchRequest_TestFlagsAndContext_ExpectMerged', async () => {
   assert.deepEqual(
      await SearchQueryRunner.buildSearchRequest({
         query: 'lion',
         getIncludeFlags: () => ({ includeAnimals: true }),
         getContext: async () => ({ date: '2026-01-01' }),
      }),
      {
         query: 'lion',
         includeAnimals: true,
         date: '2026-01-01',
      }
   );
});

test('Test_CreateSearchRunner_TestSuccessAndStale_ExpectRenderOrSkip', async () => {
   const originalSearch = SearchClient.searchZoo;
   const originalFlatten = SearchBuilder.flattenSearchRows;
   const originalRender = SearchResultsRenderer.renderSearchResults;
   const renders = [];
   const errors = [];

   SearchClient.searchZoo = async () => ({ animals: [{ species: 'Lion' }] });
   SearchBuilder.flattenSearchRows = (response) => response.animals;
   SearchResultsRenderer.renderSearchResults = (resultsEl, rows) => {
      renders.push(rows);
   };

   try {
      const inputEl = document.createElement('input');
      inputEl.value = 'lion';
      const resultsEl = document.createElement('div');
      const runSearch = SearchQueryRunner.createSearchRunner({
         inputEl,
         resultsEl,
         getIncludeFlags: () => ({ includeAnimals: true }),
         getContext: async () => ({}),
         onFocusRow: () => {},
         allowEmptyQuery: false,
         onError: (error) => errors.push(error),
      });

      await runSearch();
      assert.deepEqual(renders, [[{ species: 'Lion' }]]);

      inputEl.value = '';
      await runSearch();
      assert.equal(resultsEl.children.length, 0);

      inputEl.value = 'tiger';
      SearchClient.searchZoo = async () => {
         throw new Error('network');
      };
      await runSearch();
      assert.equal(errors.length, 1);
   } finally {
      SearchClient.searchZoo = originalSearch;
      SearchBuilder.flattenSearchRows = originalFlatten;
      SearchResultsRenderer.renderSearchResults = originalRender;
   }
});
