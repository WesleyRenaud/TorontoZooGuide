import { SourceHelper } from './sourceHelper.js';

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
      SourceHelper.setSourceRows(store, 'transportationStation', []);
      SourceHelper.setSourceRows(store, 'transportationRoute', []);
   }

   static normalizeTransportationStations(transportationStations) {
      return SourceHelper.normalizeTypedRows(transportationStations, 'transportationStation');
   }
}
