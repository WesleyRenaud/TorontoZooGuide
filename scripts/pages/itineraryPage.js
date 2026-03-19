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
import { createRestaurantClosedBanner } from '../ui/restaurantClosedBanner.js';
import { createGiftShopClosedBanner } from '../ui/giftShopClosedBanner.js';
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

let _didInit = false;

export function initItineraryPage() {
   if (_didInit) return;
   _didInit = true;

   const mapInner = document.getElementById('mapInner');
   const tooltipEl = document.getElementById('tooltip');
   const hoverTooltipEl = document.getElementById('hoverTooltip');
   const viewportEl = mapInner?.parentElement;

   if (!mapInner || !tooltipEl || !viewportEl) return;

   const panzoom = createPanzoom(mapInner, { contain: CONFIG.DEFAULT_CONTAIN });

   const store = createMapStore();
   const sources = createDataSources(store);

   const hover = hoverTooltipEl ? createHoverTooltip(hoverTooltipEl) : null;

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

   const updater = createMapUpdater({
      store,
      sources,
      markers,
      focus,
      getIncludeOffDisplay: () => false,
      getIncludeClosedRestaurants: () => false,
      getIncludeClosedGiftShops: () => false,
      getIncludeClosedAttractions: () => false,
      getZoomobileRoute: () => 'none',
      getSelectedTypes: () => [],
   });

   function repositionTooltips() {
      if (typeof tooltip?.reposition === 'function') tooltip.reposition();
      if (typeof hover?.reposition === 'function') hover.reposition();

      requestAnimationFrame(() => {
         if (typeof tooltip?.reposition === 'function') tooltip.reposition();
         if (typeof hover?.reposition === 'function') hover.reposition();
      });
   }

   mapInner.addEventListener('panzoomchange', repositionTooltips);

   window.addEventListener('resize', repositionTooltips);

   function applyItineraryToMap() {
      const itin = safeParseJSON(localStorage.getItem(ITIN_KEY) || '', null);

      if (!itin) {
         markers.render([]);
         return;
      }

      const dateStr = String(itin.dateISO || todayISO());

      updater.updateMap('custom', dateStr, { itinerary: itin });
   }

   applyItineraryToMap();

   window.addEventListener('tzg:itineraryUpdated', applyItineraryToMap);
   window.addEventListener('storage', (e) => {
      if (e.key === ITIN_KEY) applyItineraryToMap();
   });
}