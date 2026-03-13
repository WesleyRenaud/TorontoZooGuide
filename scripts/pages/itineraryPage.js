// scripts/pages/itineraryPage.js
import { CONFIG } from '../shared/config.js';
import { createPanzoom } from '../map/panzoom.js';
import { createMapStore } from '../map/store.js';
import { createDataSources } from '../map/sources.js';
import { createMapUpdater } from '../map/updater.js';
import { createMarkerLayer } from '../markers/markers.js';
import { createHoverTooltip } from '../markers/hoverTooltip.js';
import { createTooltipController } from '../tooltips/tooltipController.js';
import { createFocusController } from '../focus/focusController.js';
import { createOffDisplayBanner } from '../ui/offDisplayBanner.js';
import { createAttractionClosedBanner } from '../ui/attractionClosedBanner.js';
import { initSpeciesOverlay } from '../ui/speciesOverlay.js';
import { initLabelVisibilityToggle } from '../map/labelVisibility.js';

const ITIN_KEY = 'tzg.itinerary';

function safeParseJSON(raw, fallback) {
   try { return JSON.parse(raw); } catch { return fallback; }
}

function todayISO() {
   const d = new Date();
   const y = d.getFullYear();
   const m = String(d.getMonth() + 1).padStart(2, '0');
   const day = String(d.getDate()).padStart(2, '0');
   return `${y}-${m}-${day}`;
}

// ✅ idempotent init
let _didInit = false;

export function initItineraryPage() {
   if (_didInit) return;
   _didInit = true;

   const mapInner = document.getElementById('mapInner');
   const tooltipEl = document.getElementById('tooltip');
   const hoverTooltipEl = document.getElementById('hoverTooltip');
   const viewportEl = mapInner?.parentElement;

   if (!mapInner || !tooltipEl || !viewportEl) return;

   // ✅ match mapPage.js behavior
   const panzoom = createPanzoom(mapInner, { contain: CONFIG.DEFAULT_CONTAIN });

   const store = createMapStore();
   const sources = createDataSources(store);

   const hover = hoverTooltipEl ? createHoverTooltip(hoverTooltipEl) : null;

   const offDisplay = createOffDisplayBanner();
   const attractionClosed = createAttractionClosedBanner();
   const speciesOverlay = initSpeciesOverlay();

   const tooltip = createTooltipController({
      tooltipEl,
      onAnimalCardClick: (item) => {
         if (!item || String(item.type || '') !== 'animal') return;
         speciesOverlay.openFromAnimal(item);
      },
      offDisplayBanner: offDisplay,
      attractionClosedBanner: attractionClosed,
   });

   initLabelVisibilityToggle({
      checkboxEl: document.getElementById('showMapLabels'),
      rootEl: document.body,
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

   // ✅ No explore filter on itinerary page.
   const updater = createMapUpdater({
      store,
      sources,
      markers,
      focus,
      getIncludeOffDisplay: () => false,
      getIncludeSeasonalRestaurants: () => false,
      getIncludeSeasonalGiftShops: () => false,
      getIncludeClosedAttractions: () => false,
      getZoomobileRouteType: () => 'none',
      getSelectedTypes: () => [],
   });

   function repositionTooltips() {
      if (typeof tooltip?.reposition === 'function') tooltip.reposition();
      if (typeof hover?.reposition === 'function') hover.reposition();

      // Some implementations compute layout before transforms fully apply.
      // This second pass helps keep the anchor correct.
      requestAnimationFrame(() => {
         if (typeof tooltip?.reposition === 'function') tooltip.reposition();
         if (typeof hover?.reposition === 'function') hover.reposition();
      });
   }

   // ✅ Keep tooltips anchored while pan/zoom changes the map transform
   mapInner.addEventListener('panzoomchange', repositionTooltips);

   // ✅ Also reposition on viewport changes
   window.addEventListener('resize', repositionTooltips);

   function applyItineraryToMap() {
      const itin = safeParseJSON(localStorage.getItem(ITIN_KEY) || '', null);

      if (!itin) {
         markers.render([]);
         return;
      }

      const dateStr = String(itin.dateISO || todayISO());

      // ✅ ensures updater uses itinerary mode path (/build-itinerary)
      updater.updateMap('custom', dateStr, { itinerary: itin });
   }

   // initial
   applyItineraryToMap();

   // re-apply on save/edit/clear
   window.addEventListener('tzg:itineraryUpdated', applyItineraryToMap);
   window.addEventListener('storage', (e) => {
      if (e.key === ITIN_KEY) applyItineraryToMap();
   });
}