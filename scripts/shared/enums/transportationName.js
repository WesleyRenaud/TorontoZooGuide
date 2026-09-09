import transportationNameValues from '../../../shared/enums/transportationName.json' with { type: 'json' };

export class TransportationName {
   static {
      Object.assign(TransportationName, transportationNameValues);
   }
}
