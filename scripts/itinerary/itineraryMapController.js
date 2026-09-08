import { ItineraryMapControllerBootstrap } from './itineraryMapControllerBootstrap.js';
import { ItineraryPathOverlay } from '../map/itineraryPathOverlay.js';
import { TransportationRouteOverlay } from '../map/transportationRouteOverlay.js';

export class ItineraryMapController {
   static itineraryMapRuntime = null;

   static clearItineraryMapDisplay(runtime) {
      runtime?.markers?.render([]);
      ItineraryPathOverlay.clearItineraryPathOverlay();
      TransportationRouteOverlay.hideTransportationRouteLayers();
   }

   static initItineraryMap() {
      if (ItineraryMapController.itineraryMapRuntime) {
         return ItineraryMapController.itineraryMapRuntime;
      }

      const runtime = ItineraryMapControllerBootstrap.createItineraryMapRuntime();

      if (!runtime) return;

      ItineraryMapController.itineraryMapRuntime = runtime;

      const refreshMap = ItineraryMapControllerBootstrap.bindItineraryMapEvents(runtime);
      void refreshMap();

      return runtime;
   }
}
