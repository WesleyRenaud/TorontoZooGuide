import { CONFIG } from '../config/appConfig.js';
import { loadInlineZooMap } from '../map/loadInlineZooMap.js';
import { createPanzoom } from '../map/panzoom.js';
import { initMapControls } from '../map/controls.js';
import { initExploreTypeFilter } from '../search/exploreFilter.js';
import { initSearch } from '../search/search.js';
import { createMapStore } from '../map/store.js';
import { createDataSources } from '../map/sources.js';
import { createMapUpdater } from '../map/updater.js';
import { createMarkerLayer } from '../markers/markers.js';
import { createHoverTooltip } from '../markers/hoverTooltip.js';
import { createTooltipController } from '../tooltips/tooltipController.js';
import { createFocusController } from '../focus/focusController.js';
import { initFocusFromQuery } from '../focus/focusFromQuery.js';
import { createOffDisplayBanner } from '../banners/offDisplayBanner.js';
import { createRestaurantClosedBanner } from '../banners/restaurantClosedBanner.js';
import { createGiftShopClosedBanner } from '../banners/giftShopClosedBanner.js';
import { createAttractionClosedBanner } from '../banners/attractionClosedBanner.js';
import { initSpeciesOverlay } from '../overlays/speciesOverlay.js';
import { initLabelVisibilityToggle } from '../map/labelVisibility.js';
import { buildDateSearchContext } from '../search/searchContext.js';

export async function initMapPage() {
   const mapInner = document.getElementById('mapInner');
   const mapPreset = document.getElementById('mapPreset');
   const mapDateInput = document.getElementById('mapDate');
   const showMapLabelsCheckbox = document.getElementById('showMapLabels');
   const includeOffDisplayCheckbox = document.getElementById('includeOffDisplayAnimals');
   const includeClosedRestaurantsCheckbox = document.getElementById('includeClosedRestaurants');
   const includeClosedGiftShopsCheckbox = document.getElementById('includeClosedGiftShops');
   const includeClosedAttractionsCheckbox = document.getElementById('includeClosedAttractions');
   const zoomobileRouteRadios = document.querySelectorAll?.('input[name="zoomobileRoute"]');
   const animalSearchInput = document.getElementById('animalSearch');

   const tooltipEl = document.getElementById('tooltip');
   const hoverTooltipEl = document.getElementById('hoverTooltip');
   const viewportEl = mapInner?.parentElement;
   const urlParams = new URLSearchParams(window.location.search);
   const enableCoordinateEditing = urlParams.get('editCoords') === '1';

   if (!mapInner || !mapPreset || !mapDateInput || !tooltipEl || !viewportEl) return;

   await loadInlineZooMap();

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
         if (!item || String(item.type || '') !== 'animal') return;
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
      config: CONFIG,
      store,
      sources,
      markers,
      focus,
      getIncludeOffDisplay: () => includeOffDisplayCheckbox?.checked ?? false,
      getIncludeClosedRestaurants: () => includeClosedRestaurantsCheckbox?.checked ?? false,
      getIncludeClosedGiftShops: () => includeClosedGiftShopsCheckbox?.checked ?? false,
      getIncludeClosedAttractions: () => includeClosedAttractionsCheckbox?.checked ?? false,
      getZoomobileRoute: () => Array.from(zoomobileRouteRadios).find((r) => r.checked)?.value ?? 'none',
      getSelectedTypes: () => initExploreTypeFilter.getSelectedTypes(),
   });

   const explore = initExploreTypeFilter({
      onChange: () => {
         updater.refetchWithCurrentControls(null);
         search.refresh();
      },
      onAnimalsUnchecked: () => {
         const resultsEl = document.getElementById('animalSearchResults');
         if (resultsEl) resultsEl.innerHTML = '';
      },
   });

   initExploreTypeFilter.getSelectedTypes = explore.getSelectedTypes;

   const search = initSearch({
      inputEl: animalSearchInput,
      getIncludeFlags: () => explore.buildSearchIncludeFlags(),
      getContext: async () => {
         const preset = mapPreset?.value || '';
         const dateStr = mapDateInput?.value?.trim?.() || '';

         if (preset === 'summer') {
            return { month: 'JUL', day: 20, temp: null };
         }

         if (preset === 'winter') {
            return { month: 'JAN', day: 30, temp: null };
         }

         return await buildDateSearchContext(dateStr);
      },
      onFocusRow: (row) => updater.focusFromSearchRow(row),
   });

   initMapControls({
      mapPreset,
      mapDateInput,
      includeOffDisplayCheckbox,
      includeClosedRestaurantsCheckbox,
      includeClosedGiftShopsCheckbox,
      includeClosedAttractionsCheckbox,
      zoomobileRouteRadios,
      onUpdate: (preset, dateStr) => {
         updater.updateMap(preset, dateStr, null);
         search.refresh();
      },
   });

   initFocusFromQuery({
      onFocus: (rowOrSpec) => {
         updater.focusFromDeepLink(rowOrSpec);
      },
   });

   mapPreset.dispatchEvent(new Event('change'));
}
