import { ValueNormalizer } from '../../api/valueNormalizer.js';
import itineraryAdjustmentTypeValues from '../../../shared/enums/itineraryAdjustmentType.json' with { type: 'json' };

export class ItineraryAdjustmentType {
   static {
      Object.assign(ItineraryAdjustmentType, itineraryAdjustmentTypeValues);
      ItineraryAdjustmentType.VALUES = Object.freeze(
         Object.keys(itineraryAdjustmentTypeValues).map(
            memberName => ItineraryAdjustmentType[memberName]
         )
      );
   }

   static normalize(adjustmentType) {
      const normalizedAdjustmentType = ValueNormalizer.asTrimmedString(adjustmentType);

      return ItineraryAdjustmentType.VALUES.find(
         value => value === normalizedAdjustmentType
      ) ?? normalizedAdjustmentType;
   }
}
