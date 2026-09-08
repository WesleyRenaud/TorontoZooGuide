import { ItemType } from '../shared/enums/itemType.js';
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
      SourceHelper.setSourceRows(store, ItemType.TRANSPORTATION_STATION, []);
      SourceHelper.setSourceRows(store, ItemType.TRANSPORTATION_ROUTE, []);
   }

   static normalizeTransportationStations(transportationStations) {
      return SourceHelper.normalizeTypedRows(
         transportationStations,
         ItemType.TRANSPORTATION_STATION
      );
   }
}
