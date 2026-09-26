import assert from 'node:assert/strict';
import test from 'node:test';

import { MapStore } from '../../../scripts/map/mapStore.js';
import { TransportationRouteSourceFactory } from '../../../scripts/map/transportationRouteSourceFactory.js';
import { ItemType } from '../../../scripts/shared/enums/itemType.js';


test('Test_CreateNoCacheSource_TestFetcher_ExpectSource', async () => {
   const rows = [{ id: 1 }];

   const source = TransportationRouteSourceFactory.createNoCacheSource(async () => rows);
   const fetched = await source.fetch();

   assert.equal(source.cachePolicy, 'no-cache');
   assert.deepEqual(fetched, rows);
});


test('Test_BuildDatePayload_TestContext_ExpectMerged', () => {
   const month = 9;
   const day = 8;
   const year = 2026;
   const context = { month, day };
   const extra = { year };

   const payload = TransportationRouteSourceFactory.buildDatePayload(context, extra);

   assert.deepEqual(payload, { month, day, year });
});


test('Test_ClearTransportationRouteRows_TestStore_ExpectCleared', () => {
   const store = MapStore.createMapStore();
   store.byType.transportationStation = [{ id: 'old' }];
   store.byType.transportationRoute = [{ id: 'route' }];

   TransportationRouteSourceFactory.clearTransportationRouteRows(store);

   assert.deepEqual(store.byType.transportationStation, []);
   assert.deepEqual(store.byType.transportationRoute, []);
});


test('Test_NormalizeTransportationStations_TestRows_ExpectTyped', () => {
   const name = 'Main';
   const stations = [{ name }];

   const normalized = TransportationRouteSourceFactory.normalizeTransportationStations(stations);

   assert.deepEqual(normalized, [{ name, type: ItemType.TRANSPORTATION_STATION }]);
});
