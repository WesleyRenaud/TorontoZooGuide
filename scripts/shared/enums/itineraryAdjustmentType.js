import itineraryAdjustmentTypeValues from '../../../shared/enums/itineraryAdjustmentType.json' with { type: 'json' };

export class ItineraryAdjustmentType {
   static {
      Object.assign(ItineraryAdjustmentType, itineraryAdjustmentTypeValues);
   }
}
