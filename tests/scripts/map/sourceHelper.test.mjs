import assert from 'node:assert/strict';
import test from 'node:test';

import { SourceHelper } from '../../../scripts/map/sourceHelper.js';
import { ItemType } from '../../../scripts/shared/enums/itemType.js';
import { Position } from '../../../scripts/shared/enums/position.js';

const africanLion = { species: 'African Lion' };
const conservationCarousel = { name: 'Conservation Carousel' };
const zootique = { name: 'Zootique' };
const africanRainforest = { name: 'African Rainforest' };


function _createStore() {
   return {
      byType: {},
      cache: {},
   };
}


test('Test_NormalizeTypedRows_TestValidRows_ExpectTypedRows', () => {
   const rows = [africanLion, conservationCarousel];
   const type = 'itineraryItem';

   const typed = SourceHelper.normalizeTypedRows(rows, type);

   assert.deepEqual(typed, [
      { ...africanLion, type },
      { ...conservationCarousel, type },
   ]);
});


test('Test_NormalizeTypedRows_TestNull_ExpectEmpty', () => {
   const typed = SourceHelper.normalizeTypedRows(null, ItemType.ANIMAL);

   assert.deepEqual(typed, []);
});


test('Test_SetSourceRows_TestArrayRows_ExpectStored', () => {
   const store = _createStore();
   const rows = [africanLion];

   const stored = SourceHelper.setSourceRows(store, ItemType.ANIMAL, rows);

   assert.deepEqual(stored, rows);
   assert.deepEqual(store.byType[ItemType.ANIMAL], rows);
});


test('Test_SetSourceRows_TestString_ExpectEmpty', () => {
   const store = _createStore();

   const stored = SourceHelper.setSourceRows(store, ItemType.GIFT_SHOP, zootique.name);

   assert.deepEqual(stored, []);
});


test('Test_CreateDynamicTypedSource_TestRepeatedFetch_ExpectRefetchEachTime', async () => {
   const store = _createStore();
   let calls = 0;

   const source = SourceHelper.createDynamicTypedSource(store, ItemType.ATTRACTION, async () => {
      calls += 1;
      return [{ name: `${conservationCarousel.name} ${calls}` }];
   });
   const first = await source.fetch({ month: 'JUN' });
   const second = await source.fetch({ month: 'JUN' });

   assert.equal(source.cachePolicy, 'no-cache');
   assert.deepEqual(first, [{ name: `${conservationCarousel.name} 1` }]);
   assert.deepEqual(second, [{ name: `${conservationCarousel.name} 2` }]);
});


test('Test_CreateStaticTypedSource_TestSuccessfulFetch_ExpectCached', async () => {
   const store = _createStore();
   let calls = 0;

   const source = SourceHelper.createStaticTypedSource(store, ItemType.GIFT_SHOP, async () => {
      calls += 1;
      return [zootique];
   });
   const first = await source.fetch();
   const second = await source.fetch();

   assert.equal(source.cachePolicy, 'static');
   assert.deepEqual(first, [zootique]);
   assert.deepEqual(second, [zootique]);
   assert.equal(calls, Position.SECOND);
});


test('Test_CreateStaticTypedSource_TestInFlightFailure_ExpectDedupeThenReset', async () => {
   const store = _createStore();
   let calls = 0;
   let rejectFirstCall;
   const firstCall = new Promise((_resolve, reject) => {
      rejectFirstCall = reject;
   });

   const source = SourceHelper.createStaticTypedSource(store, ItemType.WILD_ENCOUNTER, async () => {
      calls += 1;

      if (calls === Position.SECOND) {
         return firstCall;
      }

      return [africanRainforest];
   });
   const firstFetch = source.fetch();
   const duplicateFetch = source.fetch();
   rejectFirstCall(new Error('Temporary failure'));
   const failedResults = await Promise.allSettled([firstFetch, duplicateFetch]);
   const recovered = await source.fetch();

   assert.equal(calls, 2);
   assert.equal(failedResults.at(Position.FIRST).status, 'rejected');
   assert.equal(failedResults.at(Position.SECOND).status, 'rejected');
   assert.deepEqual(recovered, [africanRainforest]);
});
