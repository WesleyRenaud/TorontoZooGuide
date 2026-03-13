// scripts/map/updater.js
import { getMonth, getDay, isWithinNextNDays } from '../utils/dates.js';
import { fetchForecastTemp } from './weather.js';
import {
   uniq,
   isoDateToMonFirstDow,
   parseItineraryIncludes,
} from '../itinerary/itineraryHelpers.js';

export function createMapUpdater({
   store,
   sources,
   markers,
   focus,
   getIncludeOffDisplay,
   getIncludeSeasonalRestaurants,
   getIncludeSeasonalGiftShops,
   getIncludeClosedAttractions,
   getZoomobileRouteType,
   getSelectedTypes,
}) {
   let lastPreset = null;
   let lastDateStr = null;

   // ✅ If focus/options are requested before the first updateMap runs, queue it here
   let pendingOptions = null;

   async function updateMap(preset, dateStr, options = null) {
      lastPreset = preset;
      lastDateStr = dateStr;

      // ✅ Apply any queued focus/options on the first real update
      if (!options && pendingOptions) {
         options = pendingOptions;
         pendingOptions = null;
      }

      if (preset === 'summer') return run({ preset, month: 'JUL', day: 20, date: null, temp: null }, options);
      if (preset === 'winter') return run({ preset, month: 'JAN', day: 30, date: null, temp: null }, options);

      const month = getMonth(dateStr);
      const day = getDay(dateStr);

      if (isWithinNextNDays(dateStr, 7)) {
         try {
            const temp = await fetchForecastTemp(dateStr);
            return run({ preset, month, day, date: dateStr, temp }, options);
         } catch {
            return run({ preset, month, day, date: dateStr, temp: null }, options);
         }
      }

      return run({ preset, month, day, date: dateStr, temp: null }, options);
   }

   function addType(selectedTypes, type) {
      const t = String(type || '').trim();
      if (!t) return selectedTypes;
      return selectedTypes.includes(t) ? selectedTypes : [t, ...selectedTypes];
   }

   function focusIfRequested(options) {
      if (!options?.focus?.row) return;
      const row = options.focus.row;
      const type = String(options.focus.type || row.type || '');
      setTimeout(() => {
         focus.focus({ row, type });
      }, 0);
   }

   async function run(dateCtx, options = null) {
      const includeOffDisplayAnimals = getIncludeOffDisplay();
      const includeSeasonalRestaurants = getIncludeSeasonalRestaurants();
      const includeSeasonalGiftShops = getIncludeSeasonalGiftShops();
      const includeClosedAttractions = getIncludeClosedAttractions();

      const zoomobileRouteType = getZoomobileRouteType();

      const itin = options?.itinerary || null;
      const itineraryOnly = !!itin;

      const dayOfWeek = dateCtx?.date ? isoDateToMonFirstDow(dateCtx.date) : 1;

      // ------------------------------------------------------------
      // ITINERARY MODE: only call /build-itinerary via sources.buildItinerary
      // ------------------------------------------------------------
      if (itineraryOnly) {
         const inc = parseItineraryIncludes(itin);

         const ctx = {
            month: dateCtx.month,
            day: dateCtx.day,
            temp: dateCtx.temp ?? null,

            // ✅ these keys should match what sources.buildItinerary sends
            animals: inc.speciesToInclude,
            attractions: inc.attractionsToInclude,
            meetTheGuardiansTalks: inc.guardiansTalksToInclude,
            wildEncounters: inc.wildEncountersToInclude,

            // optional
            dayOfWeek,
            zoomobileRouteType,
         };

         try {
            const src = sources?.buildItinerary;
            if (!src?.fetch) {
               console.warn('Missing sources.buildItinerary — add it to scripts/map/sources.js');
               markers.render([]);
               return;
            }

            const rows = await src.fetch(ctx);
            markers.render(Array.isArray(rows) ? rows : []);
            focusIfRequested(options);
            return;
         } catch (err) {
            console.warn('/build-itinerary failed:', err);
            markers.render([]);
            return;
         }
      }

      // ------------------------------------------------------------
      // NORMAL MODE: existing behavior
      // ------------------------------------------------------------
      const focusRow = options?.focus?.row || null;
      const focusType = String(options?.focus?.type || focusRow?.type || '').trim();

      let speciesToInclude = [];
      let restaurantsToInclude = [];
      let giftShopsToInclude = [];
      let attractionsToInclude = [];
      let zoomobileStationsToInclude = [];

      if (focusRow) {
         if (focusType === 'animal') {
            const s = String(focusRow.species ?? focusRow.SPECIES ?? '').trim();
            if (s) speciesToInclude = uniq([s, ...speciesToInclude]);
         }

         if (focusType === 'restaurant') {
            const r = focusRow.name ?? focusRow.NAME ?? null;
            if (r != null) restaurantsToInclude = uniq([r, ...restaurantsToInclude]);
         }

         if (focusType === 'giftShop') {
            const g = focusRow.name ?? focusRow.NAME ?? null;
            if (g != null) giftShopsToInclude = uniq([g, ...giftShopsToInclude]);
         }

         if (focusType === 'attraction') {
            const a = focusRow.name ?? focusRow.NAME ?? null;
            if (a != null) attractionsToInclude = uniq([a, ...attractionsToInclude]);
         }

         if (focusType === 'zoomobileStation') {
            const z = focusRow.name ?? focusRow.NAME ?? null;
            if (z != null) zoomobileStationsToInclude = uniq([z, ...zoomobileStationsToInclude]);
         }
      }

      let selectedTypes = (getSelectedTypes() || []).map(t => String(t).trim());

      const routeActive = zoomobileRouteType !== 'none';
      const focusIsZoomobileStation = focusType === 'zoomobileStation';

      if (
         focusType &&
         !selectedTypes.includes(focusType) &&
         !(routeActive && focusIsZoomobileStation && selectedTypes.includes('zoomobileRoute'))
      ) {
         selectedTypes = [focusType, ...selectedTypes];
      }

      selectedTypes = uniq(selectedTypes);

      if (selectedTypes.length === 0) {
         markers.render([]);
         return;
      }

      const ctx = {
         month: dateCtx.month,
         day: dateCtx.day,
         dayOfWeek,
         temp: dateCtx.temp ?? null,

         includeOffDisplayAnimals,
         includeSeasonalRestaurants,
         includeSeasonalGiftShops,
         includeClosedAttractions,

         zoomobileRouteType,

         speciesToInclude,
         restaurantsToInclude,
         giftShopsToInclude,
         attractionsToInclude,
         zoomobileStationsToInclude,
      };

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
      return unique.flatMap(t => store.byType[t] || []);
   }

   function refetchWithCurrentControls(options) {
      if (!lastPreset) {
         pendingOptions = options;
         return;
      }
      updateMap(lastPreset, lastDateStr, options);
   }

   function focusFromSearchRow(payload) {
      if (!payload) return;

      const base = payload.row && typeof payload.row === 'object' ? payload.row : payload;
      const type = String(payload.type || base.type || payload.TYPE || base.TYPE || '').trim();

      const row = {
         ...base,
         type,
         x_coord: base.x_coord ?? payload.x_coord ?? payload.x ?? base.x ?? null,
         y_coord: base.y_coord ?? payload.y_coord ?? payload.y ?? base.y ?? null,
      };

      refetchWithCurrentControls({ focus: { type, row } });
   }

   function focusFromDeepLink(payload) {
      if (!payload) return;

      if (payload && typeof payload === 'object' && payload.row) {
         focus.focus({
            row: payload.row,
            type: payload.type || payload.row.type
         });
         return;
      }

      if (payload.species) {
         const row = {
            type: 'animal',
            species: payload.species,
            exhibit: payload.exhibit ?? null,
         };
         refetchWithCurrentControls({ focus: { type: 'animal', row } });
         return;
      }

      if (payload.row) {
         const type = String(payload.type || payload.row.type || '').trim();
         refetchWithCurrentControls({ focus: { type, row: payload.row } });
      }
   }

   return {
      updateMap,
      refetchWithCurrentControls,
      focusFromSearchRow,
      focusFromDeepLink,
   };
}