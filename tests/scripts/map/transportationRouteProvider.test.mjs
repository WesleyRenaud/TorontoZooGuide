import assert from 'node:assert/strict';
import test from 'node:test';

import { TransportationRouteProvider } from '../../../scripts/map/transportationRouteProvider.js';
import { ItemType } from '../../../scripts/shared/enums/itemType.js';

const mainStationName = 'Main Station';
const stationRow = { name: mainStationName, type: ItemType.TRANSPORTATION_STATION };


function _createStore() {
   return {
      byType: {
         [ItemType.TRANSPORTATION_STATION]: [],
         [ItemType.TRANSPORTATION_ROUTE]: [],
      },
      cache: {},
   };
}


test('Test_CreateTransportationRouteSource_TestSelectedRoute_ExpectStationsStored', async () => {
   const store = _createStore();
   const shownRoutes = [];
   const month = 'JUN';
   const day = 15;
   const transportationRoute = 'summer';
   const transportationStationsToInclude = [mainStationName];
   const payload = {
      month,
      day,
      transportationRoute,
      transportationStationsToInclude,
   };

   const source = TransportationRouteProvider.createTransportationRouteSource(store, {
      fetchTransportationRoute: async (request) => {
         assert.deepEqual(request, payload);
         return {
            route: transportationRoute,
            transportationStations: [{ name: mainStationName }],
         };
      },
      hideRouteLayers: () => {},
      showRouteLayer: (route) => shownRoutes.push(route),
   });
   const rows = await source.fetch(payload);

   assert.deepEqual(rows, [stationRow]);
   assert.deepEqual(store.byType[ItemType.TRANSPORTATION_STATION], [stationRow]);
   assert.deepEqual(store.byType[ItemType.TRANSPORTATION_ROUTE], [stationRow]);
   assert.deepEqual(shownRoutes, [transportationRoute]);
});


test('Test_CreateTransportationRouteSource_TestNoRoute_ExpectStationsCleared', async () => {
   const store = _createStore();
   store.byType[ItemType.TRANSPORTATION_STATION] = [stationRow];
   store.byType[ItemType.TRANSPORTATION_ROUTE] = [stationRow];

   const source = TransportationRouteProvider.createTransportationRouteSource(store, {
      fetchTransportationRoute: async () => {
         throw new Error('Route should not be fetched');
      },
      hideRouteLayers: () => {},
      showRouteLayer: () => {},
   });
   const rows = await source.fetch({ transportationRoute: 'none' });

   assert.deepEqual(rows, []);
   assert.deepEqual(store.byType[ItemType.TRANSPORTATION_STATION], []);
   assert.deepEqual(store.byType[ItemType.TRANSPORTATION_ROUTE], []);
});
