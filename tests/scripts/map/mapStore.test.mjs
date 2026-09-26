import assert from 'node:assert/strict';
import test from 'node:test';

import { MapStore } from '../../../scripts/map/mapStore.js';


test('Test_CreateMapStore_TestAnimalCollection_ExpectEmpty', () => {
   const store = MapStore.createMapStore();

   assert.deepEqual(store.byType.animal, []);
});


test('Test_CreateMapStore_TestPavilionCache_ExpectUnloaded', () => {
   const store = MapStore.createMapStore();

   assert.equal(store.cache.pavilion.loaded, false);
});


test('Test_CreateMapStore_TestRestroomCache_ExpectIdle', () => {
   const store = MapStore.createMapStore();

   assert.equal(store.cache.restroom.inFlight, null);
});
