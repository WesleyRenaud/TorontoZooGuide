import assert from 'node:assert/strict';
import test from 'node:test';

import { SelectorSearchRunner } from '../../../../scripts/itinerary/selectors/selectorSearchRunner.js';

test('Test_CreateSelectorSearchRunner_TestCurrentQuery_ExpectRows', async () => {
   const renderedRows = [];
   const runner = SelectorSearchRunner.createSelectorSearchRunner({
      searchEndpoint: '/search',
      buildSearchPayload: (query) => ({ query, includeAnimals: true }),
      extractRows: (response) => response.animals,
      getContext: async () => ({ temp: null }),
      getQuery: () => 'lion',
      onRows: (rows) => {
         renderedRows.push(rows);
      },
      searchItems: async (_endpoint, payload) => {
         assert.deepEqual(payload, {
            query: 'lion',
            includeAnimals: true,
            temp: null,
         });
         return { animals: [{ id: 'lion', name: 'Lion' }] };
      },
      debounceMs: 0,
   });

   await runner.runCurrentQuery();

   assert.deepEqual(renderedRows, [[{ id: 'lion', name: 'Lion' }]]);
});

test('Test_CreateSelectorSearchRunner_TestStaleResponse_ExpectIgnored', async () => {
   const renderedRows = [];
   let resolveFirst = null;
   const runner = SelectorSearchRunner.createSelectorSearchRunner({
      searchEndpoint: '/search',
      buildSearchPayload: (query) => ({ query }),
      extractRows: (response) => response.rows,
      getQuery: () => 'query',
      onRows: (rows) => {
         renderedRows.push(rows);
      },
      searchItems: async () => {
         if (!resolveFirst) {
            return new Promise((resolve) => {
               resolveFirst = resolve;
            });
         }

         return { rows: ['fresh'] };
      },
      debounceMs: 0,
   });

   const firstSearch = runner.runCurrentQuery();
   const secondSearch = runner.runCurrentQuery();

   resolveFirst?.({ rows: ['stale'] });
   await Promise.all([firstSearch, secondSearch]);

   assert.deepEqual(renderedRows, [['fresh']]);
});

test('Test_CreateSelectorSearchRunner_TestSearchFails_ExpectCleared', async () => {
   const renderedRows = [];
   const runner = SelectorSearchRunner.createSelectorSearchRunner({
      searchEndpoint: '/search',
      buildSearchPayload: (query) => ({ query }),
      extractRows: (response) => response.rows,
      getQuery: () => 'query',
      onRows: (rows) => {
         renderedRows.push(rows);
      },
      searchItems: async () => {
         throw new Error('search failed');
      },
      debounceMs: 0,
   });

   await runner.runCurrentQuery();

   assert.deepEqual(renderedRows, [[]]);
});
