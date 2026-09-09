import { ValueNormalizer } from '../api/valueNormalizer.js';
import { ItineraryAdjustmentType } from '../shared/enums/itineraryAdjustmentType.js';

export class ItineraryAdjustmentTypes {
   static itineraryAdjustmentTypes = Object.freeze({ ...ItineraryAdjustmentType });

   static getItineraryAdjustmentTypes() {
      return ItineraryAdjustmentTypes.itineraryAdjustmentTypes;
   }

   static normalizeItineraryAdjustmentType(adjustmentType) {
      const normalizedAdjustmentType = ValueNormalizer.asTrimmedString(adjustmentType);
      const matchingEntry = Object.entries(ItineraryAdjustmentTypes.itineraryAdjustmentTypes).find(
         ([, value]) => value === normalizedAdjustmentType
      );

      return matchingEntry?.[1] ?? normalizedAdjustmentType;
   }
}
