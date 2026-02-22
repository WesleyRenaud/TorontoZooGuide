import { CONFIG } from '../shared/config.js';
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
import { createOffDisplayBanner } from '../ui/offDisplayBanner.js';
import { initSpeciesOverlay } from '../ui/speciesOverlay.js';
import { initLabelVisibilityToggle } from '../map/labelVisibility.js';

export function initMapPage() {
   const mapInner = document.getElementById('mapInner');
   const mapPreset = document.getElementById('mapPreset');
   const mapDateInput = document.getElementById('mapDate');
   const showMapLabelsCheckbox = document.getElementById('showMapLabels');
   const includeOffDisplayCheckbox = document.getElementById('includeOffDisplayAnimals');
   const includeSeasonalRestaurantsCheckbox = document.getElementById('includeSeasonalRestaurants');
   const animalSearchInput = document.getElementById('animalSearch');

   const tooltipEl = document.getElementById('tooltip');
   const hoverTooltipEl = document.getElementById('hoverTooltip');
   const viewportEl = mapInner?.parentElement;

   if (!mapInner || !mapPreset || !mapDateInput || !tooltipEl || !viewportEl) return;

   const panzoom = createPanzoom(mapInner, { contain: CONFIG.DEFAULT_CONTAIN });

   const store = createMapStore();
   const sources = createDataSources(store);

   const hover = createHoverTooltip(hoverTooltipEl);

   const offDisplay = createOffDisplayBanner();
   const speciesOverlay = initSpeciesOverlay();

   const tooltip = createTooltipController({
      tooltipEl,
      onAnimalCardClick: (item) => {
         if (!item || String(item.type || '').toLowerCase() !== 'animal') return;
         speciesOverlay.openFromAnimal(item);
      },
      offDisplayBanner: offDisplay   // ✅ THIS is what was missing
   });

   initLabelVisibilityToggle({
      checkboxEl: showMapLabelsCheckbox,
      rootEl: document.body
   });

   const markers = createMarkerLayer({
      mapInner,
      tooltip,
      hover,
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
      getIncludeSeasonalRestaurants: () => includeSeasonalRestaurantsCheckbox?.checked ?? false,
      getSelectedTypes: () => initExploreTypeFilter.getSelectedTypes(),
   });

   // Search (✅ keep this before we wire change handlers that call search.refresh)
   const search = initSearch({
      inputEl: animalSearchInput,
      getIncludeFlags: () => explore.buildSearchIncludeFlags(),
      onFocusRow: (row) => updater.focusFromSearchRow(row),
   });

   // Wire controls (✅ refresh search after map updates)
   initMapControls({
      mapPreset,
      mapDateInput,
      includeOffDisplayCheckbox,
      includeSeasonalRestaurantsCheckbox,
      onUpdate: (preset, dateStr) => {
         updater.updateMap(preset, dateStr, null);
         search.refresh();
      },
   });

   // Explore multi-select (✅ refresh search after refetch)
   const explore = initExploreTypeFilter({
      onChange: () => {
         updater.refetchWithCurrentControls(null);
         search.refresh();
      },
      onAnimalsUnchecked: () => {
         const resultsEl = document.getElementById('animalSearchResults');
         if (resultsEl) resultsEl.innerHTML = '';
      }
   });

   initExploreTypeFilter.getSelectedTypes = explore.getSelectedTypes;

   // Deep link focus
   initFocusFromQuery({
      onFocus: (rowOrSpec) => {
         updater.focusFromDeepLink(rowOrSpec);
      }
   });

   mapPreset.dispatchEvent(new Event('change'));
}