import assert from 'node:assert/strict';
import test from 'node:test';

import { createZoomobileRouteSource } from '../../scripts/map/zoomobileRouteSource.js';

function createStore() {
   return {
      byType: {
         zoomobileStation: [],
         zoomobileRoute: [],
      },
      cache: {},
   };
}

test('zoomobile route source stores station markers under the selected route layer', async () => {
   const store = createStore();
   const shownRoutes = [];
   const source = createZoomobileRouteSource(store, {
      fetchZoomobileRoute: async (payload) => {
         assert.deepEqual(payload, {
            month: 'JUN',
            day: 15,
            zoomobileRoute: 'summer',
            zoomobileStationsToInclude: ['Main Station'],
         });

         return {
            route: 'summer',
            zoomobileStations: [{ name: 'Main Station' }],
         };
      },
      hideRouteLayers: () => {},
      showRouteLayer: route => shownRoutes.push(route),
   });

   assert.deepEqual(await source.fetch({
      month: 'JUN',
      day: 15,
      zoomobileRoute: 'summer',
      zoomobileStationsToInclude: ['Main Station'],
   }), [
      { name: 'Main Station', type: 'zoomobileStation' },
   ]);
   assert.deepEqual(store.byType.zoomobileStation, [
      { name: 'Main Station', type: 'zoomobileStation' },
   ]);
   assert.deepEqual(store.byType.zoomobileRoute, [
      { name: 'Main Station', type: 'zoomobileStation' },
   ]);
   assert.deepEqual(shownRoutes, ['summer']);
});

test('zoomobile route source clears station markers when no route is selected', async () => {
   const store = createStore();
   store.byType.zoomobileStation = [{ name: 'Main Station', type: 'zoomobileStation' }];
   store.byType.zoomobileRoute = [{ name: 'Main Station', type: 'zoomobileStation' }];

   const source = createZoomobileRouteSource(store, {
      fetchZoomobileRoute: async () => {
         throw new Error('Route should not be fetched');
      },
      hideRouteLayers: () => {},
      showRouteLayer: () => {},
   });

   assert.deepEqual(await source.fetch({ zoomobileRoute: 'none' }), []);
   assert.deepEqual(store.byType.zoomobileStation, []);
   assert.deepEqual(store.byType.zoomobileRoute, []);
});
