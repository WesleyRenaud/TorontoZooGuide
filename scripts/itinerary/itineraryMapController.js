import { createMapRuntime } from '../map/mapRuntime.js';
import { getItinerary, isItineraryEmpty } from './itineraryService.js';

function todayISO() {
   const d = new Date();
   const y = d.getFullYear();
   const m = String(d.getMonth() + 1).padStart(2, '0');
   const day = String(d.getDate()).padStart(2, '0');
   return `${y}-${m}-${day}`;
}

let didInitializeItineraryMap = false;

export function initItineraryMap() {
   if (didInitializeItineraryMap) return;
   didInitializeItineraryMap = true;

   const mapInner = document.getElementById('mapInner');
   const tooltipEl = document.getElementById('tooltip');
   const hoverTooltipEl = document.getElementById('hoverTooltip');
   const urlParams = new URLSearchParams(window.location.search);
   const enableCoordinateEditing = urlParams.get('editCoords') === '1';

   const runtime = createMapRuntime({
      mapInner,
      tooltipEl,
      hoverTooltipEl,
      showMapLabelsCheckbox: document.getElementById('showMapLabels'),
      enableCoordinateEditing,
      getIncludeOffDisplay: () => false,
      getIncludeClosedRestaurants: () => false,
      getIncludeClosedGiftShops: () => false,
      getIncludeClosedAttractions: () => false,
      getZoomobileRoute: () => 'none',
      getSelectedTypes: () => [],
   });

   if (!runtime) return;

   const {
      markers,
      updater,
      repositionTooltips,
   } = runtime;

   mapInner.addEventListener('panzoomchange', repositionTooltips);

   window.addEventListener('resize', repositionTooltips);

   async function applyItineraryToMap() {
      try {
         const itin = await getItinerary();

         if (!itin || isItineraryEmpty(itin)) {
            markers.render([]);
            return;
         }

         const dateStr = String(itin.date || todayISO());

         await updater.updateMap('custom', dateStr, { itinerary: itin });
      } catch(err) {
         console.error('Failed to load itinerary:', err);
         markers.render([]);
      }
   }

   applyItineraryToMap();

   window.addEventListener('tzg:itineraryUpdated', applyItineraryToMap);
}
