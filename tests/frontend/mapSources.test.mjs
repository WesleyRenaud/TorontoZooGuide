import assert from 'node:assert/strict';
import test from 'node:test';

import { createTransportationRouteSource } from '../../scripts/map/transportationRouteSource.js';

function createStore() {
   return {
      byType: {
         transportationStation: [],
         transportationRoute: [],
      },
      cache: {},
   };
}

test('zoomobile route source stores station markers under the selected route layer', async () => {
   const store = createStore();
   const shownRoutes = [];
   const source = createTransportationRouteSource(store, {
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

test('zoomobile route source clears station markers when no route is selected', async () => {
   const store = createStore();
   store.byType.transportationStation = [{ name: 'Main Station', type: 'transportationStation' }];
   store.byType.transportationRoute = [{ name: 'Main Station', type: 'transportationStation' }];

   const source = createTransportationRouteSource(store, {
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
