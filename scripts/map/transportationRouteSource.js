import { SourceHelpers } from './sourceHelpers.js';
import { TransportationRouteSourceFactory } from './transportationRouteSourceFactory.js';

export class TransportationRouteSource {
   static createTransportationRouteSource(
      store,
      {
         fetchTransportationRoute,
         hideRouteLayers,
         showRouteLayer,
      } = {}
   ) {
      return TransportationRouteSourceFactory.createNoCacheSource(async (ctx) => {
         hideRouteLayers?.();

         if (ctx.transportationRoute === 'none') {
            TransportationRouteSourceFactory.clearTransportationRouteRows(store);
            return [];
         }

         const {
            route,
            transportationStations,
         } = await fetchTransportationRoute(TransportationRouteSourceFactory.buildDatePayload(ctx, {
            transportationRoute: ctx.transportationRoute,
            transportationStationsToInclude: ctx.transportationStationsToInclude,
         }));

         showRouteLayer?.(route);

         const stations = TransportationRouteSourceFactory.normalizeTransportationStations(transportationStations);
         SourceHelpers.setSourceRows(store, 'transportationStation', stations);
         SourceHelpers.setSourceRows(store, 'transportationRoute', stations);

         return stations;
      });
   }
}
