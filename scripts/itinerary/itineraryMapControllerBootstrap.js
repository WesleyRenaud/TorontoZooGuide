import { ItineraryMapController } from './itineraryMapController.js';
import { ItineraryService } from './itineraryService.js';
import { MapRuntime } from '../map/mapRuntime.js';

export class ItineraryMapControllerBootstrap {
   static ITINERARY_MAP_FILTERS = Object.freeze({
      getIncludeOffDisplay: () => false,
      getIncludeClosedRestaurants: () => false,
      getIncludeClosedGiftShops: () => false,
      getIncludeClosedAttractions: () => false,
      getTransportationRoute: () => 'none',
      getSelectedTypes: () => [],
   });

   static getTodayISO() {
      const date = new Date();
      const year = date.getFullYear();
      const month = String(date.getMonth() + 1).padStart(2, '0');
      const day = String(date.getDate()).padStart(2, '0');

      return `${year}-${month}-${day}`;
   }

   static getItineraryMapElements() {
      return {
         mapInner: document.getElementById('mapInner'),
         tooltipEl: document.getElementById('tooltip'),
         hoverTooltipEl: document.getElementById('hoverTooltip'),
         showMapLabelsCheckbox: document.getElementById('showMapLabels'),
      };
   }

   static isCoordinateEditingEnabled() {
      const urlParams = new URLSearchParams(window.location.search);
      return urlParams.get('editCoords') === '1';
   }

   static createItineraryMapRuntime() {
      return MapRuntime.createMapRuntime({
         ...ItineraryMapControllerBootstrap.getItineraryMapElements(),
         enableCoordinateEditing: ItineraryMapControllerBootstrap.isCoordinateEditingEnabled(),
         ...ItineraryMapControllerBootstrap.ITINERARY_MAP_FILTERS,
      });
   }

   static getItineraryMapDate(itinerary) {
      return String(itinerary?.date || ItineraryMapControllerBootstrap.getTodayISO());
   }

   static async refreshItineraryMap(runtime) {
      try {
         const itinerary = await ItineraryService.getItinerary();

         if (!itinerary || ItineraryService.isItineraryEmpty(itinerary)) {
            ItineraryMapController.clearItineraryMapDisplay(runtime);
            return;
         }

         await runtime.updater.updateMap(
            'custom',
            ItineraryMapControllerBootstrap.getItineraryMapDate(itinerary),
            { itinerary }
         );
      }
      catch (err) {
         console.error('Failed to load itinerary:', err);
         ItineraryMapController.clearItineraryMapDisplay(runtime);
      }
   }

   static bindItineraryMapEvents(runtime) {
      const { mapInner } = ItineraryMapControllerBootstrap.getItineraryMapElements();
      const { repositionTooltips } = runtime;
      const refreshMap = () => ItineraryMapControllerBootstrap.refreshItineraryMap(runtime);

      mapInner?.addEventListener('panzoomchange', repositionTooltips);
      window.addEventListener('resize', repositionTooltips);
      window.addEventListener('tzg:itineraryUpdated', refreshMap);

      return refreshMap;
   }
}
