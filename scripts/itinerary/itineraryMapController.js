import { ItineraryMapControllerBootstrap } from './itineraryMapControllerBootstrap.js';
import { ItineraryPathFragment } from '../map/itineraryPathFragment.js';
import { TransportationRouteFragment } from '../map/transportationRouteFragment.js';

export class ItineraryMapController {
   static itineraryMapRuntime = null;

   static clearItineraryMapDisplay(runtime) {
      runtime?.markers?.render([]);
      ItineraryPathFragment.clearItineraryPathOverlay();
      TransportationRouteFragment.hideTransportationRouteLayers();
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
