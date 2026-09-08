import { SourceHelper } from './sourceHelper.js';
import { TransportationRouteSourceFactory } from './transportationRouteSourceFactory.js';

export class TransportationRouteProvider {
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
         SourceHelper.setSourceRows(store, 'transportationStation', stations);
         SourceHelper.setSourceRows(store, 'transportationRoute', stations);

         return stations;
      });
   }
}
