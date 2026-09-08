import assert from 'node:assert/strict';
import test from 'node:test';

import { ItineraryMapController } from '../../../scripts/itinerary/itineraryMapController.js';
import { ItineraryMapControllerBootstrap } from '../../../scripts/itinerary/itineraryMapControllerBootstrap.js';
import { ItineraryPathFragment } from '../../../scripts/map/itineraryPathFragment.js';
import { TransportationRouteFragment } from '../../../scripts/map/transportationRouteFragment.js';

test('Test_ClearItineraryMapDisplay_TestRuntime_ExpectCleared', () => {
   const renders = [];
   const originalPath = ItineraryPathFragment.clearItineraryPathOverlay;
   const originalRoutes = TransportationRouteFragment.hideTransportationRouteLayers;
   ItineraryPathFragment.clearItineraryPathOverlay = () => { renders.push('path'); };
   TransportationRouteFragment.hideTransportationRouteLayers = () => { renders.push('routes'); };

   try {
      ItineraryMapController.clearItineraryMapDisplay({
         markers: { render: (items) => { renders.push(items); } },
      });
      assert.deepEqual(renders, [[], 'path', 'routes']);
   } finally {
      ItineraryPathFragment.clearItineraryPathOverlay = originalPath;
      TransportationRouteFragment.hideTransportationRouteLayers = originalRoutes;
   }
});

test('Test_InitItineraryMap_TestRuntime_ExpectCached', () => {
   const originalRuntime = ItineraryMapController.itineraryMapRuntime;
   const originalCreate = ItineraryMapControllerBootstrap.createItineraryMapRuntime;
   const originalBind = ItineraryMapControllerBootstrap.bindItineraryMapEvents;
   const refreshes = [];

   ItineraryMapController.itineraryMapRuntime = null;
   ItineraryMapControllerBootstrap.createItineraryMapRuntime = () => ({ id: 'runtime' });
   ItineraryMapControllerBootstrap.bindItineraryMapEvents = () => async () => {
      refreshes.push(true);
   };

   try {
      const first = ItineraryMapController.initItineraryMap();
      const second = ItineraryMapController.initItineraryMap();
      assert.equal(first.id, 'runtime');
      assert.equal(second, first);
   } finally {
      ItineraryMapController.itineraryMapRuntime = originalRuntime;
      ItineraryMapControllerBootstrap.createItineraryMapRuntime = originalCreate;
      ItineraryMapControllerBootstrap.bindItineraryMapEvents = originalBind;
   }
});
