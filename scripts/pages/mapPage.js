import { loadInlineZooMap } from '../map/loadInlineZooMap.js';
import { initMapControls } from '../map/controls.js';
import { initExploreTypeFilter } from '../search/exploreFilter.js';
import { initSearch } from '../search/search.js';
import { initFocusFromQuery } from '../focus/focusFromQuery.js';
import { buildMapDateContext } from '../map/dateContext.js';
import { createMapRuntime } from '../map/mapRuntime.js';

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
   const urlParams = new URLSearchParams(window.location.search);
   const enableCoordinateEditing = urlParams.get('editCoords') === '1';

   if (!mapInner || !mapPreset || !mapDateInput || !tooltipEl) return;

   await loadInlineZooMap();

   let explore = null;
   let search = null;

   const runtime = createMapRuntime({
      mapInner,
      tooltipEl,
      hoverTooltipEl,
      showMapLabelsCheckbox,
      enableCoordinateEditing,
      getIncludeOffDisplay: () => includeOffDisplayCheckbox?.checked ?? false,
      getIncludeClosedRestaurants: () => includeClosedRestaurantsCheckbox?.checked ?? false,
      getIncludeClosedGiftShops: () => includeClosedGiftShopsCheckbox?.checked ?? false,
      getIncludeClosedAttractions: () => includeClosedAttractionsCheckbox?.checked ?? false,
      getZoomobileRoute: () => Array.from(zoomobileRouteRadios).find((r) => r.checked)?.value ?? 'none',
      getSelectedTypes: () => explore?.getSelectedTypes?.() || [],
   });

   if (!runtime) return;

   const { updater } = runtime;

   explore = initExploreTypeFilter({
      onChange: () => {
         updater.refetchWithCurrentControls(null);
         search?.refresh?.();
      },
      onAnimalsUnchecked: () => {
         const resultsEl = document.getElementById('animalSearchResults');
         if (resultsEl) resultsEl.innerHTML = '';
      },
   });

   search = initSearch({
      inputEl: animalSearchInput,
      getIncludeFlags: () => explore.buildSearchIncludeFlags(),
      getContext: async () => {
         const preset = mapPreset?.value || '';
         const dateStr = mapDateInput?.value?.trim?.() || '';
         return await buildMapDateContext(preset, dateStr);
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
         search?.refresh?.();
      },
   });

   initFocusFromQuery({
      onFocus: (rowOrSpec) => {
         updater.focusFromDeepLink(rowOrSpec);
      },
   });

   mapPreset.dispatchEvent(new Event('change'));
}
