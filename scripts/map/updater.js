import { getMonth, getDay, isWithinNextNDays } from '../utils/dates.js';
import { fetchForecastTemp } from './weather.js';

export function createMapUpdater({
   store,
   sources,
   markers,
   focus,
   getIncludeOffDisplay,
   getIncludeSeasonalRestaurants,
   getIncludeSeasonalGiftShops,
   getIncludeSeasonalAttractions,
   getZoomobileRouteType,
   getSelectedTypes,
}) {
   let lastPreset = null;
   let lastDateStr = null;

   // ✅ If focus is requested before the first updateMap runs, queue it here
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

   async function run(dateCtx, options = null) {
      const includeOffDisplayAnimals = getIncludeOffDisplay();
      const includeSeasonalRestaurants = getIncludeSeasonalRestaurants();
      const includeSeasonalGiftShops = getIncludeSeasonalGiftShops();
      const includeSeasonalAttractions = getIncludeSeasonalAttractions();

      let selectedTypes = (getSelectedTypes() || []).map(t => String(t));

      // If focusing from search/deeplink, ensure focused type is loaded
      const focusType = String(options?.focus?.type || options?.focus?.row?.type || '');
      const zoomobileRouteType = getZoomobileRouteType(); // you already compute this in run()

      const routeActive = zoomobileRouteType !== 'none';
      const focusIsZoomobileStation = focusType === 'zoomobileStation';

      // If route is active, don't also add zoomobileStation layer on focus,
      // because zoomobileRoute layer already contains those same stations.
      if (
         focusType &&
         !selectedTypes.includes(focusType) &&
         !(routeActive && focusIsZoomobileStation && selectedTypes.includes('zoomobileRoute'))
      ) {
         selectedTypes = [focusType, ...selectedTypes];
      }

      // If none selected, clear markers
      if (selectedTypes.length === 0) {
         markers.render([]);
         return;
      }

      // ✅ If focusing an object, force-include that object in the data fetch
      let speciesToInclude = [];
      let restaurantsToInclude = [];
      let giftShopsToInclude = [];
      let attractionsToInclude = [];
      let zoomobileStationsToInclude = [];

      const focusRow = options?.focus?.row || null;
      const focusRowType = String(options?.focus?.type || focusRow?.type || '');

      if (focusRow) {
         if (focusRowType === 'animal') {
            const s = String(focusRow.species ?? focusRow.SPECIES ?? '').trim();
            if (s) speciesToInclude = [s];
         }

         if (focusRowType === 'restaurant') {
            const r = focusRow.name ?? focusRow.NAME ?? null;
            if (r != null) restaurantsToInclude = [r];
         }

         if (focusRowType === 'giftShop') {
            const g = focusRow.name ?? focusRow.NAME ?? null;
            if (g != null) giftShopsToInclude = [g];
         }

         if (focusRowType === 'attraction') {
            const g = focusRow.name ?? focusRow.NAME ?? null;
            if (g != null) attractionsToInclude = [g];
         }

         if (focusRowType === 'zoomobileStation') {
            const g = focusRow.name ?? focusRow.NAME ?? null;
            if (g != null) zoomobileStationsToInclude = [g];
         }
      }

      const ctx = {
         month: dateCtx.month,
         day: dateCtx.day,
         temp: dateCtx.temp ?? null,
         includeOffDisplayAnimals,
         includeSeasonalRestaurants,
         includeSeasonalGiftShops,
         includeSeasonalAttractions,
         zoomobileRouteType,
         speciesToInclude,
         restaurantsToInclude,
         giftShopsToInclude,
         attractionsToInclude,
         zoomobileStationsToInclude
      };

      await fetchAll(selectedTypes, ctx);

      // render current selected layers
      markers.render(combine(selectedTypes));

      // universal focus flow
      if (options?.focus?.row) {
         const row = options.focus.row;
         const type = String(options.focus.type || row.type || '');

         setTimeout(() => {
            focus.focus({ row, type });
         }, 0);
      }
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
      // ✅ Too early (e.g., deeplink runs before first updateMap) — queue it
      if (!lastPreset) {
         pendingOptions = options;
         return;
      }

      updateMap(lastPreset, lastDateStr, options);
   }

   function focusFromSearchRow(payload) {
      if (!payload) return;

      // ✅ Unwrap { type, x, y, row: {...} } into a real row object
      const base = payload.row && typeof payload.row === 'object' ? payload.row : payload;

      const type = String(payload.type || base.type || payload.TYPE || base.TYPE || '');

      // ✅ Ensure coords are on the row we pass down
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

      // ✅ New style: { row, type }
      if (payload && typeof payload === 'object' && payload.row) {
         focus.focus({
            row: payload.row,
            type: payload.type || payload.row.type
         });
         return;
      }

      // Old style: { species, exhibit } -> convert to a focus row
      if (payload.species) {
         const row = {
            type: 'animal',
            species: payload.species,
            exhibit: payload.exhibit ?? null,
         };
         refetchWithCurrentControls({ focus: { type: 'animal', row } });
         return;
      }

      // (Redundant but harmless)
      if (payload.row) {
         const type = String(payload.type || payload.row.type || '');
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