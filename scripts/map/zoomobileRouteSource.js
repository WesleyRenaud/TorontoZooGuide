import {
   normalizeTypedRows,
   setSourceRows,
} from './sourceHelpers.js';

function createNoCacheSource(fetchRows) {
   return {
      fetch: fetchRows,
      cachePolicy: 'no-cache',
   };
}

function buildDatePayload(ctx, extra = {}) {
   return {
      month: ctx.month,
      day: ctx.day,
      ...extra,
   };
}

function clearZoomobileRouteRows(store) {
   setSourceRows(store, 'zoomobileStation', []);
   setSourceRows(store, 'zoomobileRoute', []);
}

function normalizeZoomobileStations(zoomobileStations) {
   return normalizeTypedRows(zoomobileStations, 'zoomobileStation');
}

export function createZoomobileRouteSource(
   store,
   {
      fetchZoomobileRoute,
      hideRouteLayers,
      showRouteLayer,
   } = {}
) {
   return createNoCacheSource(async (ctx) => {
      hideRouteLayers?.();

      if (ctx.zoomobileRoute === 'none') {
         clearZoomobileRouteRows(store);
         return [];
      }

      const {
         route,
         zoomobileStations,
      } = await fetchZoomobileRoute(buildDatePayload(ctx, {
         zoomobileRoute: ctx.zoomobileRoute,
         zoomobileStationsToInclude: ctx.zoomobileStationsToInclude,
      }));

      showRouteLayer?.(route);

      const stations = normalizeZoomobileStations(zoomobileStations);
      setSourceRows(store, 'zoomobileStation', stations);
      setSourceRows(store, 'zoomobileRoute', stations);

      return stations;
   });
}
