import itineraryErrorTypeValues from '../../../shared/enums/itineraryErrorType.json' with { type: 'json' };

export class ItineraryErrorType {
   static {
      Object.assign(ItineraryErrorType, itineraryErrorTypeValues);
   }
}
