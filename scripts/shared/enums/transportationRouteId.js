import transportationRouteIdValues from '../../../shared/enums/transportationRouteId.json' with { type: 'json' };

export class TransportationRouteId {
   static {
      Object.assign(TransportationRouteId, transportationRouteIdValues);
   }
}
