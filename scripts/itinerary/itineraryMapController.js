import { ItineraryMapControllerBootstrap } from './itineraryMapControllerBootstrap.js';
import { ItineraryPathOverlay } from '../map/itineraryPathOverlay.js';
import { TransportationRouteOverlay } from '../map/transportationRouteOverlay.js';

let itineraryMapRuntime = null;

export class ItineraryMapController {
   static clearItineraryMapDisplay(runtime) {
      runtime?.markers?.render([]);
      ItineraryPathOverlay.clearItineraryPathOverlay();
      TransportationRouteOverlay.hideTransportationRouteLayers();
   }

   static initItineraryMap() {
      if (itineraryMapRuntime) {
         return itineraryMapRuntime;
      }

      const runtime = ItineraryMapControllerBootstrap.createItineraryMapRuntime();

      if (!runtime) return;

      itineraryMapRuntime = runtime;

      const refreshMap = ItineraryMapControllerBootstrap.bindItineraryMapEvents(runtime);
      void refreshMap();

      return runtime;
   }
}
