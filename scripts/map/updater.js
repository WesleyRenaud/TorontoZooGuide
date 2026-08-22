import { syncClosedExhibitOverlays } from './closedExhibitOverlay.js';
import { buildMapDateContext } from './dateContext.js';
import {
   normalizeSearchFocusRequest,
   resolveDeepLinkFocus,
   scheduleFocusRequest,
} from './focusRequest.js';
import { resolveItineraryPath } from '../itinerary/itineraryPathModel.js';
import {
   clearItineraryPathOverlay,
   renderItineraryPathOverlay,
} from './itineraryPathOverlay.js';
import {
   buildItineraryRows,
   buildLayerRequest,
   resolveItineraryTransportationRouteMarkers,
} from './layerRequest.js';
import { setSourceRows } from './sourceHelpers.js';
import {
   hideZoomobileRouteLayers,
   showZoomobileRouteMarkers,
} from './zoomobileRouteOverlay.js';

function buildUniqueTypes(types = []) {
   return Array.from(new Set(types));
}

export function createMapUpdater({
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
   onDateContextChange = null,
}) {
   let lastPreset = null;
   let lastDateStr = null;
   let pendingOptions = null;

   function rememberLastMapRequest(preset, dateStr) {
      lastPreset = preset;
      lastDateStr = dateStr;
   }

   function focusIfRequested(options) {
      scheduleFocusRequest(focus, options?.focus || null);
   }

   function clearRenderedMarkers() {
      markers.render([]);
      clearItineraryPathOverlay();
      hideZoomobileRouteLayers();
   }

   function resolvePendingUpdateOptions(options) {
      if (options) {
         return options;
      }

      if (!pendingOptions) {
         return null;
      }

      const resolvedOptions = pendingOptions;
      pendingOptions = null;
      return resolvedOptions;
   }

   function getControlSnapshot() {
      return {
         includeOffDisplayAnimals: getIncludeOffDisplay(),
         includeClosedRestaurants: getIncludeClosedRestaurants(),
         includeClosedRestrooms: getIncludeClosedRestrooms(),
         includeClosedGiftShops: getIncludeClosedGiftShops(),
         includeClosedAttractions: getIncludeClosedAttractions(),
         zoomobileRoute: getZoomobileRoute(),
         selectedTypes: getSelectedTypes(),
      };
   }

   function buildFocusContext(options) {
      const focusRow = options?.focus?.row || null;
      const focusType = String(options?.focus?.type || focusRow?.type || '').trim();

      return {
         focusRow,
         focusType,
      };
   }

   function buildRequestedLayers(dateCtx, options) {
      const controls = getControlSnapshot();
      const { focusRow, focusType } = buildFocusContext(options);

      const {
         ctx,
         selectedTypes,
      } = buildLayerRequest({
         dateCtx,
         selectedTypes: controls.selectedTypes,
         zoomobileRoute: controls.zoomobileRoute,
         focusRow,
         focusType,
         includeOffDisplayAnimals: controls.includeOffDisplayAnimals,
         includeClosedRestaurants: controls.includeClosedRestaurants,
         includeClosedRestrooms: controls.includeClosedRestrooms,
         includeClosedGiftShops: controls.includeClosedGiftShops,
         includeClosedAttractions: controls.includeClosedAttractions,
      });

      return {
         ctx,
         selectedTypes,
      };
   }

   function syncItineraryTransportationRoute(itinerary) {
      const routeMarkers = resolveItineraryTransportationRouteMarkers(itinerary);

      if (!routeMarkers) {
         hideZoomobileRouteLayers();
         return;
      }

      showZoomobileRouteMarkers(
         routeMarkers.route,
         routeMarkers.markerSequences
      );
   }

   async function renderItineraryOnly(dateCtx, itinerary, options) {
      try {
         syncItineraryTransportationRoute(itinerary);
         markers.render(buildItineraryRows(itinerary));
         renderItineraryPathOverlay(
            resolveItineraryPath(options, itinerary)
         );
         focusIfRequested(options);
         return true;
      } catch (err) {
         console.warn('Failed to render itinerary layers:', err);
         clearRenderedMarkers();
         return true;
      }
   }

   function getStoredLayerRows(type) {
      return store.byType[type] || [];
   }

   async function fetchLayerRows(layer, ctx) {
      const source = sources[layer];

      if (!source) {
         return setSourceRows(store, layer, getStoredLayerRows(layer));
      }

      try {
         return await source.fetch(ctx);
      } catch {
         return setSourceRows(store, layer, getStoredLayerRows(layer));
      }
   }

   async function fetchSelectedLayers(selectedTypes, ctx) {
      const uniqueTypes = buildUniqueTypes(selectedTypes);

      await Promise.all(
         uniqueTypes.map((layer) => fetchLayerRows(layer, ctx))
      );

      return uniqueTypes;
   }

   function combineLayerRows(selectedTypes = []) {
      return buildUniqueTypes(selectedTypes)
         .flatMap((type) => getStoredLayerRows(type));
   }

   async function renderSelectedLayers(dateCtx, options = null) {
      const {
         ctx,
         selectedTypes,
      } = buildRequestedLayers(dateCtx, options);

      await syncClosedExhibitOverlays(sources, ctx);
      clearItineraryPathOverlay();

      if (selectedTypes.length === 0) {
         clearRenderedMarkers();
         return;
      }

      const fetchedTypes = await fetchSelectedLayers(selectedTypes, ctx);
      markers.render(combineLayerRows(fetchedTypes));
      focusIfRequested(options);
   }

   async function run(dateCtx, options = null) {
      const itinerary = options?.itinerary || null;

      if (itinerary) {
         await renderItineraryOnly(dateCtx, itinerary, options);
         return;
      }

      await renderSelectedLayers(dateCtx, options);
   }

   async function updateMap(preset, dateStr, options = null) {
      rememberLastMapRequest(preset, dateStr);

      const resolvedOptions = resolvePendingUpdateOptions(options);
      const dateContext = await buildMapDateContext(preset, dateStr);
      onDateContextChange?.(dateContext);

      return run(dateContext, resolvedOptions);
   }

   function refetchWithCurrentControls(options) {
      if (!lastPreset) {
         pendingOptions = options;
         return null;
      }

      return updateMap(lastPreset, lastDateStr, options);
   }

   function focusFromSearchRow(payload) {
      const focusRequest = normalizeSearchFocusRequest(payload);

      if (!focusRequest) {
         return;
      }

      return refetchWithCurrentControls({ focus: focusRequest });
   }

   function focusFromDeepLink(payload) {
      const resolved = resolveDeepLinkFocus(payload);

      if (!resolved) {
         return;
      }

      if (resolved.mode === 'direct') {
         scheduleFocusRequest(focus, resolved.focusRequest);
         return null;
      }

      return refetchWithCurrentControls({ focus: resolved.focusRequest });
   }

   return {
      updateMap,
      refetchWithCurrentControls,
      focusFromSearchRow,
      focusFromDeepLink,
   };
}
