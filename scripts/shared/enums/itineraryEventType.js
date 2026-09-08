import itineraryEventTypeValues from '../../../shared/enums/itineraryEventType.json' with { type: 'json' };

export class ItineraryEventType {
   static {
      Object.assign(ItineraryEventType, itineraryEventTypeValues);
   }
}
