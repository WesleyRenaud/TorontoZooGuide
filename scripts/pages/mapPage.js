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
import { coordKey } from '../utils/coords.js';

export function initMapPage() {
   const mapInner = document.getElementById('mapInner');
   const mapPreset = document.getElementById('mapPreset');
   const mapDateInput = document.getElementById('mapDate');
   const includeOffDisplayCheckbox = document.getElementById('includeOffDisplayAnimals');
   const animalSearchInput = document.getElementById('animalSearch');

   const tooltipEl = document.getElementById('tooltip');
   const hoverTooltipEl = document.getElementById('hoverTooltip');
   const viewportEl = mapInner?.parentElement;

   if (!mapInner || !mapPreset || !mapDateInput || !tooltipEl || !viewportEl) return;

   // Core systems
   const panzoom = createPanzoom(mapInner, { contain: CONFIG.DEFAULT_CONTAIN });

   const store = createMapStore();
   const sources = createDataSources(store);

   const hover = createHoverTooltip(hoverTooltipEl);

   const offDisplay = createOffDisplayBanner();
   const speciesOverlay = initSpeciesOverlay(); // returns { openFromAnimal(animal) }

   const tooltip = createTooltipController({
      tooltipEl,
      onAnimalCardClick: (item) => {
         // keep this behavior animals-only
         if (!item || String(item.type || '').toLowerCase() !== 'animal') return;
         speciesOverlay.openFromAnimal(item);
      },
      onOpenItemsChanged: (items) => {
         // show/hide banner using the first animal (or currently displayed animal if you prefer)
         const firstAnimal = (items || []).find(i => String(i.type || '').toLowerCase() === 'animal') || null;
         offDisplay.sync(firstAnimal);
      }
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
      getSelectedTypes: () => initExploreTypeFilter.getSelectedTypes(), // injected below
   });

   // Wire controls
   initMapControls({
      mapPreset,
      mapDateInput,
      includeOffDisplayCheckbox,
      onUpdate: (preset, dateStr) => updater.updateMap(preset, dateStr, null),
   });

   // Explore multi-select
   const explore = initExploreTypeFilter({
      onChange: () => updater.refetchWithCurrentControls(null),
      onAnimalsUnchecked: () => {
         const resultsEl = document.getElementById('animalSearchResults');
         if (resultsEl) resultsEl.innerHTML = '';
      }
   });
   // allow updater to read selected types
   initExploreTypeFilter.getSelectedTypes = explore.getSelectedTypes;

   // Search
   initSearch({
      inputEl: animalSearchInput,
      getIncludeFlags: () => explore.buildSearchIncludeFlags(),
      onFocusRow: (row) => updater.focusFromSearchRow(row),
   });

   // Deep link focus (?focus=... etc)
   initFocusFromQuery({
      onFocus: (rowOrSpec) => {
         // If the deep link is the old animals-only pattern, updater handles it.
         updater.focusFromDeepLink(rowOrSpec);
      }
   });

   // Initial fetch (trigger preset change handler)
   mapPreset.dispatchEvent(new Event('change'));
}