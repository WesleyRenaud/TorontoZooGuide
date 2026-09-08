import assert from 'node:assert/strict';
import test from 'node:test';

import { MapStore } from '../../../scripts/map/mapStore.js';
import { TransportationRouteSourceFactory } from '../../../scripts/map/transportationRouteSourceFactory.js';

test('Test_CreateNoCacheSource_TestFetcher_ExpectSource', async () => {
   const source = TransportationRouteSourceFactory.createNoCacheSource(async () => [{ id: 1 }]);
   assert.equal(source.cachePolicy, 'no-cache');
   assert.deepEqual(await source.fetch(), [{ id: 1 }]);
});

test('Test_BuildDatePayload_TestContext_ExpectMerged', () => {
   assert.deepEqual(
      TransportationRouteSourceFactory.buildDatePayload({ month: 9, day: 8 }, { year: 2026 }),
      { month: 9, day: 8, year: 2026 }
   );
});

test('Test_ClearAndNormalizeStations_TestStore_ExpectUpdated', () => {
   const store = MapStore.createMapStore();
   store.byType.transportationStation = [{ id: 'old' }];
   store.byType.transportationRoute = [{ id: 'route' }];

   TransportationRouteSourceFactory.clearTransportationRouteRows(store);
   assert.deepEqual(store.byType.transportationStation, []);
   assert.deepEqual(store.byType.transportationRoute, []);

   assert.deepEqual(
      TransportationRouteSourceFactory.normalizeTransportationStations([{ name: 'Main' }]),
      [{ name: 'Main', type: 'transportationStation' }]
   );
});
