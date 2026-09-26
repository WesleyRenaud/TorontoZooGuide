import assert from 'node:assert/strict';
import test from 'node:test';

import { SearchClient } from '../../../scripts/api/searchClient.js';
import { SearchBuilder } from '../../../scripts/search/searchBuilder.js';
import { SearchQueryRunner } from '../../../scripts/search/searchQueryRunner.js';
import { SearchResultsRenderer } from '../../../scripts/search/searchResultsRenderer.js';
import { Position } from '../../../scripts/shared/enums/position.js';
import { installDomTestHooks } from '../helpers/domTestSetup.mjs';

installDomTestHooks();


test('Test_CreateNoopSearch_TestRefresh_ExpectNoop', () => {
   const noop = SearchQueryRunner.createNoopSearch();

   noop.refresh();

   assert.equal(typeof noop.refresh, 'function');
});


test('Test_Debounce_TestDelay_ExpectSingleCall', async () => {
   const calls = [];
   const first = 1;
   const second = 2;
   const debounced = SearchQueryRunner.debounce((value) => calls.push(value), 20);

   debounced(first);
   debounced(second);
   await new Promise((resolve) => setTimeout(resolve, 40));

   assert.deepEqual(calls, [second]);
});


test('Test_GetSearchQuery_TestWhitespace_ExpectTrimmed', () => {
   const query = 'lion';
   const inputEl = document.createElement('input');
   inputEl.value = `  ${query}  `;

   const searchQuery = SearchQueryRunner.getSearchQuery(inputEl);

   assert.equal(searchQuery, query);
});


test('Test_ShouldClearForEmptyQuery_TestEmptyDisallowed_ExpectTrue', () => {
   const shouldClear = SearchQueryRunner.shouldClearForEmptyQuery('', false);

   assert.equal(shouldClear, true);
});


test('Test_ShouldClearForEmptyQuery_TestEmptyAllowed_ExpectFalse', () => {
   const shouldClear = SearchQueryRunner.shouldClearForEmptyQuery('', true);

   assert.equal(shouldClear, false);
});


test('Test_ShouldClearForEmptyQuery_TestValue_ExpectFalse', () => {
   const shouldClear = SearchQueryRunner.shouldClearForEmptyQuery('x', false);

   assert.equal(shouldClear, false);
});


test('Test_ClearSearchResults_TestChildren_ExpectEmpty', () => {
   const resultsEl = document.createElement('div');
   resultsEl.appendChild(document.createElement('div'));

   SearchQueryRunner.clearSearchResults(resultsEl);

   assert.equal(resultsEl.children.length, Position.FIRST);
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

      assert.match(String(warns.at(Position.FIRST).at(Position.FIRST)), /failed to fetch results/);
   } finally {
      console.warn = originalWarn;
   }
});


test('Test_BuildSearchRequest_TestFlagsAndContext_ExpectMerged', async () => {
   const query = 'lion';
   const includeAnimals = true;
   const date = '2026-01-01';

   const request = await SearchQueryRunner.buildSearchRequest({
      query,
      getIncludeFlags: () => ({ includeAnimals }),
      getContext: async () => ({ date }),
   });

   assert.deepEqual(request, {
      query,
      includeAnimals,
      date,
   });
});


test('Test_CreateSearchRunner_TestSuccess_ExpectRendered', async () => {
   const originalSearch = SearchClient.searchZoo;
   const originalFlatten = SearchBuilder.flattenSearchRows;
   const originalRender = SearchResultsRenderer.renderSearchResults;
   const renders = [];
   const lion = { species: 'African Lion' };

   SearchClient.searchZoo = async () => ({ animals: [lion] });
   SearchBuilder.flattenSearchRows = (response) => response.animals;
   SearchResultsRenderer.renderSearchResults = (_resultsEl, rows) => {
      renders.push(rows);
   };

   try {
      const inputEl = document.createElement('input');
      inputEl.value = 'lion';
      const runSearch = SearchQueryRunner.createSearchRunner({
         inputEl,
         resultsEl: document.createElement('div'),
         getIncludeFlags: () => ({ includeAnimals: true }),
         getContext: async () => ({}),
         onFocusRow: () => {},
         allowEmptyQuery: false,
         onError: () => {},
      });
      await runSearch();

      assert.deepEqual(renders, [[lion]]);
   } finally {
      SearchClient.searchZoo = originalSearch;
      SearchBuilder.flattenSearchRows = originalFlatten;
      SearchResultsRenderer.renderSearchResults = originalRender;
   }
});


test('Test_CreateSearchRunner_TestEmptyQuery_ExpectCleared', async () => {
   const originalSearch = SearchClient.searchZoo;
   const originalFlatten = SearchBuilder.flattenSearchRows;
   const originalRender = SearchResultsRenderer.renderSearchResults;
   SearchClient.searchZoo = async () => ({ animals: [] });
   SearchBuilder.flattenSearchRows = (response) => response.animals;
   SearchResultsRenderer.renderSearchResults = () => {};

   try {
      const inputEl = document.createElement('input');
      const resultsEl = document.createElement('div');
      resultsEl.appendChild(document.createElement('div'));
      inputEl.value = '';
      const runSearch = SearchQueryRunner.createSearchRunner({
         inputEl,
         resultsEl,
         getIncludeFlags: () => ({}),
         getContext: async () => ({}),
         onFocusRow: () => {},
         allowEmptyQuery: false,
         onError: () => {},
      });
      await runSearch();

      assert.equal(resultsEl.children.length, Position.FIRST);
   } finally {
      SearchClient.searchZoo = originalSearch;
      SearchBuilder.flattenSearchRows = originalFlatten;
      SearchResultsRenderer.renderSearchResults = originalRender;
   }
});


test('Test_CreateSearchRunner_TestStaleThenFresh_ExpectFreshOnly', async () => {
   const originalSearch = SearchClient.searchZoo;
   const originalFlatten = SearchBuilder.flattenSearchRows;
   const originalRender = SearchResultsRenderer.renderSearchResults;
   const renders = [];
   const fresh = { species: 'Fresh' };
   let resolveFirst;

   SearchBuilder.flattenSearchRows = (response) => response.animals;
   SearchResultsRenderer.renderSearchResults = (_resultsEl, rows) => {
      renders.push(rows);
   };

   try {
      const inputEl = document.createElement('input');
      const runSearch = SearchQueryRunner.createSearchRunner({
         inputEl,
         resultsEl: document.createElement('div'),
         getIncludeFlags: () => ({}),
         getContext: async () => ({}),
         onFocusRow: () => {},
         allowEmptyQuery: false,
         onError: () => {},
      });
      inputEl.value = 'stale';
      SearchClient.searchZoo = () => new Promise((resolve) => {
         resolveFirst = resolve;
      });
      const firstRun = runSearch();
      inputEl.value = 'fresh';
      SearchClient.searchZoo = async () => ({ animals: [fresh] });
      await runSearch();
      resolveFirst({ animals: [{ species: 'Stale' }] });
      await firstRun;

      assert.deepEqual(renders.at(Position.LAST), [fresh]);
      assert.equal(renders.some((rows) => rows.at(Position.FIRST)?.species === 'Stale'), false);
   } finally {
      SearchClient.searchZoo = originalSearch;
      SearchBuilder.flattenSearchRows = originalFlatten;
      SearchResultsRenderer.renderSearchResults = originalRender;
   }
});


test('Test_CreateSearchRunner_TestError_ExpectOnError', async () => {
   const originalSearch = SearchClient.searchZoo;
   const originalFlatten = SearchBuilder.flattenSearchRows;
   const originalRender = SearchResultsRenderer.renderSearchResults;
   const errors = [];
   SearchClient.searchZoo = async () => {
      throw new Error('network');
   };
   SearchBuilder.flattenSearchRows = (response) => response.animals;
   SearchResultsRenderer.renderSearchResults = () => {};

   try {
      const inputEl = document.createElement('input');
      inputEl.value = 'tiger';
      const runSearch = SearchQueryRunner.createSearchRunner({
         inputEl,
         resultsEl: document.createElement('div'),
         getIncludeFlags: () => ({}),
         getContext: async () => ({}),
         onFocusRow: () => {},
         allowEmptyQuery: false,
         onError: (error) => errors.push(error),
      });
      await runSearch();

      assert.equal(errors.length, Position.SECOND);
   } finally {
      SearchClient.searchZoo = originalSearch;
      SearchBuilder.flattenSearchRows = originalFlatten;
      SearchResultsRenderer.renderSearchResults = originalRender;
   }
});


test('Test_CreateSearchRunner_TestStaleSuccess_ExpectSkipRender', async () => {
   const originalSearch = SearchClient.searchZoo;
   const originalFlatten = SearchBuilder.flattenSearchRows;
   const originalRender = SearchResultsRenderer.renderSearchResults;
   const renders = [];
   const lionQuery = 'lion';
   const tigerQuery = 'tiger';
   const tiger = { species: 'Amur Tiger' };
   let resolveFirstSearch;
   const lionResult = new Promise((resolve) => {
      resolveFirstSearch = resolve;
   });

   SearchClient.searchZoo = async (request) => {
      if (request.query === lionQuery) {
         return lionResult;
      }

      return { animals: [tiger] };
   };
   SearchBuilder.flattenSearchRows = (response) => response.animals;
   SearchResultsRenderer.renderSearchResults = (_resultsEl, rows) => {
      renders.push(rows);
   };

   try {
      const inputEl = document.createElement('input');
      inputEl.value = lionQuery;
      const runSearch = SearchQueryRunner.createSearchRunner({
         inputEl,
         resultsEl: document.createElement('div'),
         getIncludeFlags: () => ({}),
         getContext: async () => ({}),
         onFocusRow: () => {},
         allowEmptyQuery: false,
         onError: () => {},
      });
      const firstSearch = runSearch();
      inputEl.value = tigerQuery;
      const secondSearch = runSearch();
      resolveFirstSearch({ animals: [{ species: 'African Lion' }] });
      await firstSearch;
      await secondSearch;

      assert.deepEqual(renders, [[tiger]]);
   } finally {
      SearchClient.searchZoo = originalSearch;
      SearchBuilder.flattenSearchRows = originalFlatten;
      SearchResultsRenderer.renderSearchResults = originalRender;
   }
});
