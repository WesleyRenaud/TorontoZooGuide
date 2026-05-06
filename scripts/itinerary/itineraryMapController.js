import {
   getItinerary,
   isItineraryEmpty,
} from './itineraryService.js';
import { createMapRuntime } from '../map/mapRuntime.js';

const ITINERARY_MAP_FILTERS = Object.freeze({
   getIncludeOffDisplay: () => false,
   getIncludeClosedRestaurants: () => false,
   getIncludeClosedGiftShops: () => false,
   getIncludeClosedAttractions: () => false,
   getZoomobileRoute: () => 'none',
   getSelectedTypes: () => [],
});

let itineraryMapRuntime = null;

function getTodayISO() {
   const date = new Date();
   const year = date.getFullYear();
   const month = String(date.getMonth() + 1).padStart(2, '0');
   const day = String(date.getDate()).padStart(2, '0');

   return `${year}-${month}-${day}`;
}

function getItineraryMapElements() {
   return {
      mapInner: document.getElementById('mapInner'),
      tooltipEl: document.getElementById('tooltip'),
      hoverTooltipEl: document.getElementById('hoverTooltip'),
      showMapLabelsCheckbox: document.getElementById('showMapLabels'),
   };
}

function isCoordinateEditingEnabled() {
   const urlParams = new URLSearchParams(window.location.search);
   return urlParams.get('editCoords') === '1';
}

function createItineraryMapRuntime() {
   return createMapRuntime({
      ...getItineraryMapElements(),
      enableCoordinateEditing: isCoordinateEditingEnabled(),
      ...ITINERARY_MAP_FILTERS,
   });
}

function clearItineraryMarkers(runtime) {
   runtime?.markers?.render([]);
}

function getItineraryMapDate(itinerary) {
   return String(itinerary?.date || getTodayISO());
}

async function refreshItineraryMap(runtime) {
   try {
      const itinerary = await getItinerary();

      if (!itinerary || isItineraryEmpty(itinerary)) {
         clearItineraryMarkers(runtime);
         return;
      }

      await runtime.updater.updateMap(
         'custom',
         getItineraryMapDate(itinerary),
         { itinerary }
      );
   }
   catch (err) {
      console.error('Failed to load itinerary:', err);
      clearItineraryMarkers(runtime);
   }
}

function bindItineraryMapEvents(runtime) {
   const { mapInner } = getItineraryMapElements();
   const { repositionTooltips } = runtime;
   const refreshMap = () => refreshItineraryMap(runtime);

   mapInner?.addEventListener('panzoomchange', repositionTooltips);
   window.addEventListener('resize', repositionTooltips);
   window.addEventListener('tzg:itineraryUpdated', refreshMap);

   return refreshMap;
}

export function initItineraryMap() {
   if (itineraryMapRuntime) {
      return itineraryMapRuntime;
   }

   const runtime = createItineraryMapRuntime();

   if (!runtime) return;

   itineraryMapRuntime = runtime;

   const refreshMap = bindItineraryMapEvents(runtime);
   void refreshMap();

   return runtime;
}
