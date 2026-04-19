import { buildMapDateContext } from './dateContext.js';
import { buildLayerRequest, buildItineraryRows } from './layerRequest.js';
import {
   normalizeSearchFocusRequest,
   resolveDeepLinkFocus,
   scheduleFocusRequest,
} from './focusRequest.js';
import { syncClosedExhibitOverlays } from './closedExhibitOverlay.js';

export function createMapUpdater({
   store,
   sources,
   markers,
   focus,
   getIncludeOffDisplay,
   getIncludeClosedRestaurants,
   getIncludeClosedGiftShops,
   getIncludeClosedAttractions,
   getZoomobileRoute,
   getSelectedTypes,
}) {
   let lastPreset = null;
   let lastDateStr = null;

   let pendingOptions = null;

   async function updateMap(preset, dateStr, options = null) {
      lastPreset = preset;
      lastDateStr = dateStr;

      if (!options && pendingOptions) {
         options = pendingOptions;
         pendingOptions = null;
      }

      return run(await buildMapDateContext(preset, dateStr), options);
   }

   function focusIfRequested(options) {
      scheduleFocusRequest(focus, options?.focus || null);
   }

   async function run(dateCtx, options = null) {
      const includeOffDisplayAnimals = getIncludeOffDisplay();
      const includeClosedRestaurants = getIncludeClosedRestaurants();
      const includeClosedGiftShops = getIncludeClosedGiftShops();
      const includeClosedAttractions = getIncludeClosedAttractions();

      const zoomobileRoute = getZoomobileRoute();

      const itin = options?.itinerary || null;
      const itineraryOnly = !!itin;

      if (itineraryOnly) {
         try {
            markers.render(buildItineraryRows(itin));
            focusIfRequested(options);
            return;
         } catch (err) {
            console.warn('Failed to render itinerary layers:', err);
            markers.render([]);
            return;
         }
      }

      const focusRow = options?.focus?.row || null;
      const focusType = String(options?.focus?.type || focusRow?.type || '').trim();
      const {
         ctx,
         selectedTypes,
      } = buildLayerRequest({
         dateCtx,
         selectedTypes: getSelectedTypes(),
         zoomobileRoute,
         focusRow,
         focusType,
         includeOffDisplayAnimals,
         includeClosedRestaurants,
         includeClosedGiftShops,
         includeClosedAttractions,
      });

      await syncClosedExhibitOverlays(sources, ctx);

      if (selectedTypes.length === 0) {
         markers.render([]);
         return;
      }

      await fetchAll(selectedTypes, ctx);
      markers.render(combine(selectedTypes));
      focusIfRequested(options);
   }

   async function fetchAll(selectedTypes, ctx) {
      const unique = Array.from(new Set(selectedTypes));

      await Promise.all(
         unique.map(async (layer) => {
            const src = sources[layer];

            if (!src) {
               store.byType[layer] = store.byType[layer] || [];
               return;
            }

            try {
               const rows = await src.fetch(ctx);
               store.byType[layer] = Array.isArray(rows) ? rows : [];
            } catch {
               store.byType[layer] = store.byType[layer] || [];
            }
         })
      );
   }

   function combine(selectedTypes) {
      const unique = Array.from(new Set(selectedTypes || []));
      return unique.flatMap((t) => store.byType[t] || []);
   }

   function refetchWithCurrentControls(options) {
      if (!lastPreset) {
         pendingOptions = options;
         return;
      }

      updateMap(lastPreset, lastDateStr, options);
   }

   function focusFromSearchRow(payload) {
      const focusRequest = normalizeSearchFocusRequest(payload);

      if (!focusRequest) {
         return;
      }

      refetchWithCurrentControls({ focus: focusRequest });
   }

   function focusFromDeepLink(payload) {
      const resolved = resolveDeepLinkFocus(payload);

      if (!resolved) {
         return;
      }

      if (resolved.mode === 'direct') {
         scheduleFocusRequest(focus, resolved.focusRequest);
         return;
      }

      refetchWithCurrentControls({ focus: resolved.focusRequest });
   }

   return {
      updateMap,
      refetchWithCurrentControls,
      focusFromSearchRow,
      focusFromDeepLink,
   };
}
