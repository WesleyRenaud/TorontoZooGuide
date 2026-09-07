import { SourceHelpers } from './sourceHelpers.js';

export class TransportationRouteSourceFactory {
   static createNoCacheSource(fetchRows) {
      return {
         fetch: fetchRows,
         cachePolicy: 'no-cache',
      };
   }

   static buildDatePayload(ctx, extra = {}) {
      return {
         month: ctx.month,
         day: ctx.day,
         ...extra,
      };
   }

   static clearTransportationRouteRows(store) {
      SourceHelpers.setSourceRows(store, 'transportationStation', []);
      SourceHelpers.setSourceRows(store, 'transportationRoute', []);
   }

   static normalizeTransportationStations(transportationStations) {
      return SourceHelpers.normalizeTypedRows(transportationStations, 'transportationStation');
   }
}
