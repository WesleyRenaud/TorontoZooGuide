import { CONFIG } from '../config/appConfig.js';
import { createPanzoom } from './panzoom.js';
import { createMapStore } from './store.js';
import { createDataSources } from './sources.js';
import { createMapUpdater } from './updater.js';
import { createMarkerLayer } from '../markers/markers.js';
import { createHoverTooltip } from '../markers/hoverTooltip.js';
import { createTooltipController } from '../tooltips/tooltipController.js';
import { createFocusController } from '../focus/focusController.js';
import { createOffDisplayBanner } from '../banners/offDisplayBanner.js';
import { createRestaurantClosedBanner } from '../banners/restaurantClosedBanner.js';
import { createGiftShopClosedBanner } from '../banners/giftShopClosedBanner.js';
import { createAttractionClosedBanner } from '../banners/attractionClosedBanner.js';
import { initSpeciesOverlay } from '../overlays/speciesOverlay.js';
import { initLabelVisibilityToggle } from './labelVisibility.js';

export function createMapRuntime({
   mapInner,
   tooltipEl,
   hoverTooltipEl,
   showMapLabelsCheckbox = null,
   enableCoordinateEditing = false,
   getIncludeOffDisplay = () => false,
   getIncludeClosedRestaurants = () => false,
   getIncludeClosedGiftShops = () => false,
   getIncludeClosedAttractions = () => false,
   getZoomobileRoute = () => 'none',
   getSelectedTypes = () => [],
} = {}) {
   const viewportEl = mapInner?.parentElement;

   if (!mapInner || !tooltipEl || !viewportEl) {
      return null;
   }

   const panzoom = createPanzoom(mapInner, { contain: CONFIG.DEFAULT_CONTAIN });
   const store = createMapStore();
   const sources = createDataSources(store);
   const hover = createHoverTooltip(hoverTooltipEl);

   const offDisplay = createOffDisplayBanner();
   const restaurantClosed = createRestaurantClosedBanner();
   const giftShopClosed = createGiftShopClosedBanner();
   const attractionClosed = createAttractionClosedBanner();
   const speciesOverlay = initSpeciesOverlay();

   const tooltip = createTooltipController({
      tooltipEl,
      onAnimalCardClick: (item) => {
         if (!item || String(item.type || '') !== 'animal') {
            return;
         }

         speciesOverlay.openFromAnimal(item);
      },
      offDisplayBanner: offDisplay,
      restaurantClosedBanner: restaurantClosed,
      giftShopClosedBanner: giftShopClosed,
      attractionClosedBanner: attractionClosed,
   });

   initLabelVisibilityToggle({
      checkboxEl: showMapLabelsCheckbox,
      rootEl: document.body,
   });

   const markers = createMarkerLayer({
      mapInner,
      tooltip,
      hover,
      enableCoordinateEditing,
   });

   const focus = createFocusController({
      panzoom,
      getMarkerByCoord: (key) => markers.getMarkerByCoord(key),
      getViewportEl: () => viewportEl,
      tooltip,
      getAllMarkers: () => markers.getAllMarkers(),
   });

   const updater = createMapUpdater({
      store,
      sources,
      markers,
      focus,
      getIncludeOffDisplay,
      getIncludeClosedRestaurants,
      getIncludeClosedGiftShops,
      getIncludeClosedAttractions,
      getZoomobileRoute,
      getSelectedTypes,
   });

   function repositionTooltips() {
      tooltip?.reposition?.();
      hover?.reposition?.();

      requestAnimationFrame(() => {
         tooltip?.reposition?.();
         hover?.reposition?.();
      });
   }

   return {
      panzoom,
      store,
      sources,
      hover,
      tooltip,
      markers,
      focus,
      updater,
      repositionTooltips,
   };
}
