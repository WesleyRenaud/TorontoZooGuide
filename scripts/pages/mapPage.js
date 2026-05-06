import { initFocusFromQuery } from '../focus/focusFromQuery.js';
import { initMapControls } from '../map/controls.js';
import { buildMapDateContext } from '../map/dateContext.js';
import { loadInlineZooMap } from '../map/loadInlineZooMap.js';
import { createMapRuntime } from '../map/mapRuntime.js';
import { initExploreTypeFilter } from '../search/exploreFilter.js';
import { initSearch } from '../search/search.js';
import { createExploreUpdates } from '../updates/exploreUpdates.js';

function getMapPageElements() {
   return {
      mapInner: document.getElementById('mapInner'),
      mapPreset: document.getElementById('mapPreset'),
      mapDateInput: document.getElementById('mapDate'),
      showMapLabelsCheckbox: document.getElementById('showMapLabels'),
      includeOffDisplayCheckbox: document.getElementById('includeOffDisplayAnimals'),
      includeClosedRestaurantsCheckbox: document.getElementById('includeClosedRestaurants'),
      includeClosedRestroomsCheckbox: document.getElementById('includeClosedRestrooms'),
      includeClosedGiftShopsCheckbox: document.getElementById('includeClosedGiftShops'),
      includeClosedAttractionsCheckbox: document.getElementById('includeClosedAttractions'),
      zoomobileRouteRadios: document.querySelectorAll?.('input[name="zoomobileRoute"]') ?? [],
      animalSearchInput: document.getElementById('animalSearch'),
      animalSearchResultsEl: document.getElementById('animalSearchResults'),
      exploreUpdatesListEl: document.getElementById('exploreUpdatesList'),
      tooltipEl: document.getElementById('tooltip'),
      hoverTooltipEl: document.getElementById('hoverTooltip'),
   };
}

function hasRequiredMapPageElements({
   mapInner,
   mapPreset,
   mapDateInput,
   tooltipEl,
} = {}) {
   return Boolean(mapInner && mapPreset && mapDateInput && tooltipEl);
}

function isCoordinateEditingEnabled() {
   const urlParams = new URLSearchParams(window.location.search);
   return urlParams.get('editCoords') === '1';
}

function getSelectedZoomobileRoute(zoomobileRouteRadios) {
   return Array.from(zoomobileRouteRadios)
      .find((radio) => radio.checked)
      ?.value ?? 'none';
}

function clearAnimalSearchResults(resultsEl) {
   resultsEl?.replaceChildren();
}

function createMapDateContextGetter({
   mapPreset,
   mapDateInput,
} = {}) {
   return async () => {
      const preset = mapPreset?.value || '';
      const dateStr = mapDateInput?.value?.trim?.() || '';
      return await buildMapDateContext(preset, dateStr);
   };
}

function createRuntimeOptions(elements, {
   getSelectedTypes,
   updates,
} = {}) {
   return {
      mapInner: elements.mapInner,
      tooltipEl: elements.tooltipEl,
      hoverTooltipEl: elements.hoverTooltipEl,
      showMapLabelsCheckbox: elements.showMapLabelsCheckbox,
      enableCoordinateEditing: isCoordinateEditingEnabled(),
      getIncludeOffDisplay: () => elements.includeOffDisplayCheckbox?.checked ?? false,
      getIncludeClosedRestaurants: () => elements.includeClosedRestaurantsCheckbox?.checked ?? false,
      getIncludeClosedRestrooms: () => elements.includeClosedRestroomsCheckbox?.checked ?? false,
      getIncludeClosedGiftShops: () => elements.includeClosedGiftShopsCheckbox?.checked ?? false,
      getIncludeClosedAttractions: () => elements.includeClosedAttractionsCheckbox?.checked ?? false,
      getZoomobileRoute: () => getSelectedZoomobileRoute(elements.zoomobileRouteRadios),
      getSelectedTypes,
      onDateContextChange: (dateCtx) => updates?.refresh?.(dateCtx),
   };
}

function initMapExploreFilter({
   updater,
   getSearch,
   animalSearchResultsEl,
} = {}) {
   return initExploreTypeFilter({
      onChange: () => {
         updater.refetchWithCurrentControls(null);
         getSearch()?.refresh?.();
      },
      onAnimalsUnchecked: () => {
         clearAnimalSearchResults(animalSearchResultsEl);
      },
   });
}

function initMapSearch({
   elements,
   explore,
   updater,
} = {}) {
   return initSearch({
      inputEl: elements.animalSearchInput,
      resultsEl: elements.animalSearchResultsEl,
      getIncludeFlags: () => ({
         ...explore.buildSearchIncludeFlags(),
         includeClosedRestaurants: elements.includeClosedRestaurantsCheckbox?.checked ?? false,
         includeClosedRestrooms: elements.includeClosedRestroomsCheckbox?.checked ?? false,
         includeClosedGiftShops: elements.includeClosedGiftShopsCheckbox?.checked ?? false,
         includeClosedAttractions: elements.includeClosedAttractionsCheckbox?.checked ?? false,
      }),
      getContext: createMapDateContextGetter(elements),
      onFocusRow: (row) => updater.focusFromSearchRow(row),
   });
}

function initMapPageControls({
   elements,
   updater,
   getSearch,
} = {}) {
   initMapControls({
      mapPreset: elements.mapPreset,
      mapDateInput: elements.mapDateInput,
      includeOffDisplayCheckbox: elements.includeOffDisplayCheckbox,
      includeClosedRestaurantsCheckbox: elements.includeClosedRestaurantsCheckbox,
      includeClosedRestroomsCheckbox: elements.includeClosedRestroomsCheckbox,
      includeClosedGiftShopsCheckbox: elements.includeClosedGiftShopsCheckbox,
      includeClosedAttractionsCheckbox: elements.includeClosedAttractionsCheckbox,
      zoomobileRouteRadios: elements.zoomobileRouteRadios,
      onUpdate: (preset, dateStr) => {
         updater.updateMap(preset, dateStr, null);
         getSearch()?.refresh?.();
      },
   });
}

function initMapDeepLinkFocus(updater) {
   initFocusFromQuery({
      onFocus: (rowOrSpec) => {
         updater.focusFromDeepLink(rowOrSpec);
      },
   });
}

function triggerInitialMapUpdate(mapPreset) {
   mapPreset.dispatchEvent(new Event('change'));
}

export async function initMapPage() {
   const elements = getMapPageElements();

   if (!hasRequiredMapPageElements(elements)) return;

   await loadInlineZooMap();

   let explore = null;
   let search = null;
   const updates = createExploreUpdates({
      listEl: elements.exploreUpdatesListEl,
   });

   const runtime = createMapRuntime(createRuntimeOptions(elements, {
      getSelectedTypes: () => explore?.getSelectedTypes?.() || [],
      updates,
   }));

   if (!runtime) return;

   const { updater } = runtime;
   const getSearch = () => search;

   explore = initMapExploreFilter({
      updater,
      getSearch,
      animalSearchResultsEl: elements.animalSearchResultsEl,
   });

   search = initMapSearch({
      elements,
      explore,
      updater,
   });

   initMapPageControls({
      elements,
      updater,
      getSearch,
   });

   initMapDeepLinkFocus(updater);

   triggerInitialMapUpdate(elements.mapPreset);
}
