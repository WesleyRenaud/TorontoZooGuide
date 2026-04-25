import assert from 'node:assert/strict';
import test from 'node:test';

import {
   createDynamicTypedSource,
   createStaticTypedSource,
   normalizeTypedRows,
   setSourceRows,
} from '../../scripts/map/sourceHelpers.js';

function createStore() {
   return {
      byType: {},
      cache: {},
   };
}

test('normalizes typed rows without accepting malformed collections', () => {
   assert.deepEqual(normalizeTypedRows([
      { species: 'African Lion' },
      { name: 'Conservation Carousel' },
   ], 'itineraryItem'), [
      { species: 'African Lion', type: 'itineraryItem' },
      { name: 'Conservation Carousel', type: 'itineraryItem' },
   ]);
   assert.deepEqual(normalizeTypedRows(null, 'animal'), []);
});

test('setSourceRows stores only array rows', () => {
   const store = createStore();

   assert.deepEqual(setSourceRows(store, 'animal', [{ species: 'African Lion' }]), [
      { species: 'African Lion' },
   ]);
   assert.deepEqual(store.byType.animal, [{ species: 'African Lion' }]);
   assert.deepEqual(setSourceRows(store, 'giftShop', 'Zootique'), []);
});

test('dynamic typed sources refetch each time', async () => {
   const store = createStore();
   let calls = 0;
   const source = createDynamicTypedSource(store, 'attraction', async () => {
      calls += 1;
      return [{ name: `Conservation Carousel ${calls}` }];
   });

   assert.equal(source.cachePolicy, 'no-cache');
   assert.deepEqual(await source.fetch({ month: 'JUN' }), [
      { name: 'Conservation Carousel 1' },
   ]);
   assert.deepEqual(await source.fetch({ month: 'JUN' }), [
      { name: 'Conservation Carousel 2' },
   ]);
});

test('static typed sources cache successful fetches', async () => {
   const store = createStore();
   let calls = 0;
   const source = createStaticTypedSource(store, 'giftShop', async () => {
      calls += 1;
      return [{ name: 'Zootique' }];
   });

   assert.equal(source.cachePolicy, 'static');
   assert.deepEqual(await source.fetch(), [{ name: 'Zootique' }]);
   assert.deepEqual(await source.fetch(), [{ name: 'Zootique' }]);
   assert.equal(calls, 1);
});

test('static typed sources dedupe in-flight fetches and reset after failures', async () => {
   const store = createStore();
   let calls = 0;
   let rejectFirstCall;
   const firstCall = new Promise((resolve, reject) => {
      rejectFirstCall = reject;
   });

   const source = createStaticTypedSource(store, 'wildEncounter', async () => {
      calls += 1;

      if (calls === 1) {
         return firstCall;
      }

      return [{ name: 'African Rainforest' }];
   });

   const firstFetch = source.fetch();
   const duplicateFetch = source.fetch();
   assert.equal(calls, 1);

   rejectFirstCall(new Error('Temporary failure'));

   const failedResults = await Promise.allSettled([firstFetch, duplicateFetch]);
   assert.equal(failedResults[0].status, 'rejected');
   assert.equal(failedResults[1].status, 'rejected');
   assert.deepEqual(await source.fetch(), [{ name: 'African Rainforest' }]);
   assert.equal(calls, 2);
});
