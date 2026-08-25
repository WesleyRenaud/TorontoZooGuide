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

function clearTransportationRouteRows(store) {
   setSourceRows(store, 'transportationStation', []);
   setSourceRows(store, 'transportationRoute', []);
}

function normalizeTransportationStations(transportationStations) {
   return normalizeTypedRows(transportationStations, 'transportationStation');
}

export function createTransportationRouteSource(
   store,
   {
      fetchTransportationRoute,
      hideRouteLayers,
      showRouteLayer,
   } = {}
) {
   return createNoCacheSource(async (ctx) => {
      hideRouteLayers?.();

      if (ctx.transportationRoute === 'none') {
         clearTransportationRouteRows(store);
         return [];
      }

      const {
         route,
         transportationStations,
      } = await fetchTransportationRoute(buildDatePayload(ctx, {
         transportationRoute: ctx.transportationRoute,
         transportationStationsToInclude: ctx.transportationStationsToInclude,
      }));

      showRouteLayer?.(route);

      const stations = normalizeTransportationStations(transportationStations);
      setSourceRows(store, 'transportationStation', stations);
      setSourceRows(store, 'transportationRoute', stations);

      return stations;
   });
}
