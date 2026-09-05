import { AttractionClosedBanner } from '../banners/attractionClosedBanner.js';
import { DrinkingFountainClosedBanner } from '../banners/drinkingFountainClosedBanner.js';
import { GiftShopClosedBanner } from '../banners/giftShopClosedBanner.js';
import { OffDisplayBanner } from '../banners/offDisplayBanner.js';
import { RestaurantClosedBanner } from '../banners/restaurantClosedBanner.js';
import { RestroomMessageBanner } from '../banners/restroomMessageBanner.js';
import { DEFAULT_MAP_CONTAIN } from '../config/appConfig.js';
import { FocusController } from '../focus/focusController.js';
import { OpenGuardiansTalkLinkedAnimal } from '../guardians/openGuardiansTalkLinkedAnimal.js';
import { LabelVisibility } from './labelVisibility.js';
import { HoverTooltip } from '../markers/hoverTooltip.js';
import { Markers } from '../markers/markers.js';
import { initSpeciesOverlay } from '../overlays/speciesOverlay.js';
import { Panzoom } from './panzoom.js';
import { createDataSources } from './sources.js';
import { Store } from './store.js';
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
      offDisplayBanner: OffDisplayBanner.createOffDisplayBanner(),
      restaurantClosedBanner: RestaurantClosedBanner.createRestaurantClosedBanner(),
      restroomMessageBanner: RestroomMessageBanner.createRestroomMessageBanner(),
      giftShopClosedBanner: GiftShopClosedBanner.createGiftShopClosedBanner(),
      attractionClosedBanner: AttractionClosedBanner.createAttractionClosedBanner(),
      drinkingFountainClosedBanner: DrinkingFountainClosedBanner.createDrinkingFountainClosedBanner(),
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
         void OpenGuardiansTalkLinkedAnimal.openGuardiansTalkLinkedAnimal(item);
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
   LabelVisibility.initLabelVisibilityToggle({
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
   return FocusController.createFocusController({
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
   getTransportationRoute = () => 'none',
   getSelectedTypes = () => [],
   onDateContextChange = null,
} = {}) {
   const viewportEl = mapInner?.parentElement;

   if (!hasRequiredRuntimeElements({ mapInner, tooltipEl, viewportEl })) {
      return null;
   }

   const panzoom = Panzoom.createPanzoom(mapInner, { contain: DEFAULT_MAP_CONTAIN });
   const store = Store.createMapStore();
   const sources = createDataSources(store);
   const hover = HoverTooltip.createHoverTooltip(hoverTooltipEl);
   const speciesOverlay = initSpeciesOverlay();

   const tooltip = createMapTooltip({
      tooltipEl,
      speciesOverlay,
   });

   initMapLabels(showMapLabelsCheckbox);

   const markers = Markers.createMarkerLayer({
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
      getTransportationRoute,
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
