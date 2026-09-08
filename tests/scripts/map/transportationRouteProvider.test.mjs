import assert from 'node:assert/strict';
import test from 'node:test';

import { TransportationRouteProvider } from '../../../scripts/map/transportationRouteProvider.js';

function _createStore() {
   return {
      byType: {
         transportationStation: [],
         transportationRoute: [],
      },
      cache: {},
   };
}

test('Test_CreateTransportationRouteSource_TestSelectedRoute_ExpectStationsStored', async () => {
   const store = _createStore();
   const shownRoutes = [];
   const source = TransportationRouteProvider.createTransportationRouteSource(store, {
      fetchTransportationRoute: async (payload) => {
         assert.deepEqual(payload, {
            month: 'JUN',
            day: 15,
            transportationRoute: 'summer',
            transportationStationsToInclude: ['Main Station'],
         });

         return {
            route: 'summer',
            transportationStations: [{ name: 'Main Station' }],
         };
      },
      hideRouteLayers: () => {},
      showRouteLayer: route => shownRoutes.push(route),
   });

   assert.deepEqual(await source.fetch({
      month: 'JUN',
      day: 15,
      transportationRoute: 'summer',
      transportationStationsToInclude: ['Main Station'],
   }), [
      { name: 'Main Station', type: 'transportationStation' },
   ]);
   assert.deepEqual(store.byType.transportationStation, [
      { name: 'Main Station', type: 'transportationStation' },
   ]);
   assert.deepEqual(store.byType.transportationRoute, [
      { name: 'Main Station', type: 'transportationStation' },
   ]);
   assert.deepEqual(shownRoutes, ['summer']);
});

test('Test_CreateTransportationRouteSource_TestNoRoute_ExpectStationsCleared', async () => {
   const store = _createStore();
   store.byType.transportationStation = [{ name: 'Main Station', type: 'transportationStation' }];
   store.byType.transportationRoute = [{ name: 'Main Station', type: 'transportationStation' }];

   const source = TransportationRouteProvider.createTransportationRouteSource(store, {
      fetchTransportationRoute: async () => {
         throw new Error('Route should not be fetched');
      },
      hideRouteLayers: () => {},
      showRouteLayer: () => {},
   });

   assert.deepEqual(await source.fetch({ transportationRoute: 'none' }), []);
   assert.deepEqual(store.byType.transportationStation, []);
   assert.deepEqual(store.byType.transportationRoute, []);
});
