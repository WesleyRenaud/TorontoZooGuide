import assert from 'node:assert/strict';
import test from 'node:test';

import { createSelectorSearchRunner } from '../../scripts/itinerary/selectors/selectorSearchRunner.js';

test('createSelectorSearchRunner fetches rows for the current query', async () => {
   const renderedRows = [];
   const runner = createSelectorSearchRunner({
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

test('createSelectorSearchRunner ignores stale responses', async () => {
   const renderedRows = [];
   let resolveFirst = null;
   const runner = createSelectorSearchRunner({
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

test('createSelectorSearchRunner clears rows when search fails', async () => {
   const renderedRows = [];
   const runner = createSelectorSearchRunner({
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
