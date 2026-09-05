import { SourceHelpers } from './sourceHelpers.js';

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
   SourceHelpers.setSourceRows(store, 'transportationStation', []);
   SourceHelpers.setSourceRows(store, 'transportationRoute', []);
}

function normalizeTransportationStations(transportationStations) {
   return SourceHelpers.normalizeTypedRows(transportationStations, 'transportationStation');
}

export class TransportationRouteSource {
   static createTransportationRouteSource(
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
         SourceHelpers.setSourceRows(store, 'transportationStation', stations);
         SourceHelpers.setSourceRows(store, 'transportationRoute', stations);

         return stations;
      });
   }
}
