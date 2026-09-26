import assert from 'node:assert/strict';
import test from 'node:test';

import { SelectorSearchRunner } from '../../../../scripts/itinerary/selectors/selectorSearchRunner.js';
import { Position } from '../../../../scripts/shared/enums/position.js';


test('Test_CreateSelectorSearchRunner_TestCurrentQuery_ExpectRows', async () => {
   const renderedRows = [];
   const query = 'lion';
   const animals = [{ id: query, name: 'Lion' }];
   const runner = SelectorSearchRunner.createSelectorSearchRunner({
      searchEndpoint: '/search',
      buildSearchPayload: (value) => ({ query: value, includeAnimals: true }),
      extractRows: (response) => response.animals,
      getContext: async () => ({ temp: null }),
      getQuery: () => query,
      onRows: (rows) => {
         renderedRows.push(rows);
      },
      searchItems: async (_endpoint, payload) => {
         assert.deepEqual(payload, {
            query,
            includeAnimals: true,
            temp: null,
         });
         return { animals };
      },
      debounceMs: 0,
   });

   await runner.runCurrentQuery();

   assert.deepEqual(renderedRows.at(Position.FIRST), animals);
});


test('Test_CreateSelectorSearchRunner_TestStaleResponse_ExpectIgnored', async () => {
   const renderedRows = [];
   let resolveFirst = null;
   const fresh = 'fresh';
   const stale = 'stale';
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

         return { rows: [fresh] };
      },
      debounceMs: 0,
   });

   const firstSearch = runner.runCurrentQuery();
   const secondSearch = runner.runCurrentQuery();
   resolveFirst?.({ rows: [stale] });
   await Promise.all([firstSearch, secondSearch]);

   assert.deepEqual(renderedRows, [[fresh]]);
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


test('Test_CreateSelectorSearchRunner_TestStaleError_ExpectIgnored', async () => {
   const renderedRows = [];
   let resolveFirstError = null;
   const fresh = 'fresh';
   const runner = SelectorSearchRunner.createSelectorSearchRunner({
      searchEndpoint: '/search',
      buildSearchPayload: (query) => ({ query }),
      extractRows: (response) => response.rows,
      getQuery: () => 'query',
      onRows: (rows) => {
         renderedRows.push(rows);
      },
      searchItems: async () => {
         if (!resolveFirstError) {
            return new Promise((_resolve, reject) => {
               resolveFirstError = reject;
            });
         }

         return { rows: [fresh] };
      },
      debounceMs: 0,
   });

   const firstSearch = runner.runCurrentQuery();
   const secondSearch = runner.runCurrentQuery();
   resolveFirstError?.(new Error('stale'));
   await Promise.allSettled([firstSearch, secondSearch]);

   assert.deepEqual(renderedRows, [[fresh]]);
});


test('Test_ScheduleCurrentQuery_TestDebounce_ExpectRun', async () => {
   const renderedRows = [];
   const scheduled = 'scheduled';
   const scheduledRunner = SelectorSearchRunner.createSelectorSearchRunner({
      searchEndpoint: '/search',
      buildSearchPayload: (query) => ({ query }),
      extractRows: (response) => response.rows,
      getQuery: () => scheduled,
      onRows: (rows) => {
         renderedRows.push(rows);
      },
      searchItems: async () => ({ rows: [scheduled] }),
      debounceMs: 0,
   });

   scheduledRunner.scheduleCurrentQuery();
   await new Promise((resolve) => {
      setTimeout(resolve, 5);
   });

   assert.deepEqual(renderedRows, [[scheduled]]);
});
