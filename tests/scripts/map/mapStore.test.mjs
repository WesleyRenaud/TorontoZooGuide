import assert from 'node:assert/strict';
import test from 'node:test';

import { MapStore } from '../../../scripts/map/mapStore.js';

test('Test_CreateMapStore_TestDefaults_ExpectTypedCollections', () => {
   const store = MapStore.createMapStore();
   assert.deepEqual(store.byType.animal, []);
   assert.equal(store.cache.pavilion.loaded, false);
   assert.equal(store.cache.restroom.inFlight, null);
});
