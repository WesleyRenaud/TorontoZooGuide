import { createAttractionClosedBanner } from '../banners/attractionClosedBanner.js';
import { createDrinkingFountainClosedBanner } from '../banners/drinkingFountainClosedBanner.js';
import { createGiftShopClosedBanner } from '../banners/giftShopClosedBanner.js';
import { createOffDisplayBanner } from '../banners/offDisplayBanner.js';
import { createRestaurantClosedBanner } from '../banners/restaurantClosedBanner.js';
import { createRestroomMessageBanner } from '../banners/restroomMessageBanner.js';
import { DEFAULT_MAP_CONTAIN } from '../config/appConfig.js';
import { createFocusController } from '../focus/focusController.js';
import { openGuardiansTalkLinkedAnimal } from '../guardians/openGuardiansTalkLinkedAnimal.js';
import { initLabelVisibilityToggle } from './labelVisibility.js';
import { createHoverTooltip } from '../markers/hoverTooltip.js';
import { createMarkerLayer } from '../markers/markers.js';
import { initSpeciesOverlay } from '../overlays/speciesOverlay.js';
import { createPanzoom } from './panzoom.js';
import { createDataSources } from './sources.js';
import { createMapStore } from './store.js';
import { createTooltipController } from '../tooltips/tooltipController.js';
import { createMapUpdater } from './updater.js';

function hasRequiredRuntimeElements({
   mapInner,
   tooltipEl,
   viewportEl,
} = {}) {
   return Boolean(mapInner && tooltipEl && viewportEl);
}

function createMapBannerSet() {
   return {
      offDisplayBanner: createOffDisplayBanner(),
      restaurantClosedBanner: createRestaurantClosedBanner(),
      restroomMessageBanner: createRestroomMessageBanner(),
      giftShopClosedBanner: createGiftShopClosedBanner(),
      attractionClosedBanner: createAttractionClosedBanner(),
      drinkingFountainClosedBanner: createDrinkingFountainClosedBanner(),
   };
}

function createAnimalCardClickHandler(speciesOverlay) {
   return (item) => {
      const itemType = String(item?.type || '');

      if (itemType === 'animal') {
         speciesOverlay.openFromAnimal(item);
         return;
      }

      if (itemType === 'guardiansTalk') {
         void openGuardiansTalkLinkedAnimal(item);
      }
   };
}

function createMapTooltip({
   tooltipEl,
   speciesOverlay,
} = {}) {
   return createTooltipController({
      tooltipEl,
      onAnimalCardClick: createAnimalCardClickHandler(speciesOverlay),
      ...createMapBannerSet(),
   });
}

function initMapLabels(showMapLabelsCheckbox) {
   initLabelVisibilityToggle({
      checkboxEl: showMapLabelsCheckbox,
      rootEl: document.body,
   });
}

function createMapFocus({
   panzoom,
   markers,
   tooltip,
   viewportEl,
} = {}) {
   return createFocusController({
      panzoom,
      getMarkerByCoord: (key) => markers.getMarkerByCoord(key),
      getViewportEl: () => viewportEl,
      tooltip,
      getAllMarkers: () => markers.getAllMarkers(),
   });
}

function createTooltipRepositioner({
   tooltip,
   hover,
} = {}) {
   return function repositionTooltips() {
      tooltip?.reposition?.();
      hover?.reposition?.();

      requestAnimationFrame(() => {
         tooltip?.reposition?.();
         hover?.reposition?.();
      });
   };
}

export function createMapRuntime({
   mapInner,
   tooltipEl,
   hoverTooltipEl,
   showMapLabelsCheckbox = null,
   enableCoordinateEditing = false,
   getIncludeOffDisplay = () => false,
   getIncludeClosedRestaurants = () => false,
   getIncludeClosedRestrooms = () => false,
   getIncludeClosedGiftShops = () => false,
   getIncludeClosedAttractions = () => false,
   getZoomobileRoute = () => 'none',
   getSelectedTypes = () => [],
   onDateContextChange = null,
} = {}) {
   const viewportEl = mapInner?.parentElement;

   if (!hasRequiredRuntimeElements({ mapInner, tooltipEl, viewportEl })) {
      return null;
   }

   const panzoom = createPanzoom(mapInner, { contain: DEFAULT_MAP_CONTAIN });
   const store = createMapStore();
   const sources = createDataSources(store);
   const hover = createHoverTooltip(hoverTooltipEl);
   const speciesOverlay = initSpeciesOverlay();

   const tooltip = createMapTooltip({
      tooltipEl,
      speciesOverlay,
   });

   initMapLabels(showMapLabelsCheckbox);

   const markers = createMarkerLayer({
      mapInner,
      tooltip,
      hover,
      enableCoordinateEditing,
   });

   const focus = createMapFocus({
      panzoom,
      markers,
      tooltip,
      viewportEl,
   });

   const updater = createMapUpdater({
      store,
      sources,
      markers,
      focus,
      getIncludeOffDisplay,
      getIncludeClosedRestaurants,
      getIncludeClosedRestrooms,
      getIncludeClosedGiftShops,
      getIncludeClosedAttractions,
      getZoomobileRoute,
      getSelectedTypes,
      onDateContextChange,
   });

   return {
      panzoom,
      store,
      sources,
      hover,
      tooltip,
      markers,
      focus,
      updater,
      repositionTooltips: createTooltipRepositioner({
         tooltip,
         hover,
      }),
   };
}
