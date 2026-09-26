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
   const pathCleared = 'path';
   const routesCleared = 'routes';
   ItineraryPathFragment.clearItineraryPathOverlay = () => { renders.push(pathCleared); };
   TransportationRouteFragment.hideTransportationRouteLayers = () => { renders.push(routesCleared); };
   const runtime = {
      markers: { render: (items) => { renders.push(items); } },
   };

   try {
      ItineraryMapController.clearItineraryMapDisplay(runtime);

      assert.deepEqual(renders, [[], pathCleared, routesCleared]);
   } finally {
      ItineraryPathFragment.clearItineraryPathOverlay = originalPath;
      TransportationRouteFragment.hideTransportationRouteLayers = originalRoutes;
   }
});


test('Test_InitItineraryMap_TestRuntime_ExpectCached', () => {
   const originalRuntime = ItineraryMapController.itineraryMapRuntime;
   const originalCreate = ItineraryMapControllerBootstrap.createItineraryMapRuntime;
   const originalBind = ItineraryMapControllerBootstrap.bindItineraryMapEvents;
   const runtimeId = 'runtime';
   ItineraryMapController.itineraryMapRuntime = null;
   ItineraryMapControllerBootstrap.createItineraryMapRuntime = () => ({ id: runtimeId });
   ItineraryMapControllerBootstrap.bindItineraryMapEvents = () => async () => {};

   try {
      const first = ItineraryMapController.initItineraryMap();
      const second = ItineraryMapController.initItineraryMap();

      assert.equal(first.id, runtimeId);
      assert.equal(second, first);
   } finally {
      ItineraryMapController.itineraryMapRuntime = originalRuntime;
      ItineraryMapControllerBootstrap.createItineraryMapRuntime = originalCreate;
      ItineraryMapControllerBootstrap.bindItineraryMapEvents = originalBind;
   }
});
