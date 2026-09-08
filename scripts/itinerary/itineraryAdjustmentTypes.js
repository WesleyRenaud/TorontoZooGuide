export class ItineraryAdjustmentTypes {
   static itineraryAdjustmentTypes = null;

   static updateItineraryAdjustmentTypesFromConfig(itineraryConfig = {}) {
      const adjustmentTypes = itineraryConfig?.adjustmentTypes;

      if (adjustmentTypes && typeof adjustmentTypes === 'object') {
         ItineraryAdjustmentTypes.itineraryAdjustmentTypes = Object.freeze({ ...adjustmentTypes });
      }
   }

   static getItineraryAdjustmentTypes() {
      return ItineraryAdjustmentTypes.itineraryAdjustmentTypes;
   }

   static normalizeItineraryAdjustmentType(adjustmentType) {
      const normalizedAdjustmentType = typeof adjustmentType === 'string'
         ? adjustmentType.trim()
         : '';

      if (!normalizedAdjustmentType || !ItineraryAdjustmentTypes.itineraryAdjustmentTypes) {
         return normalizedAdjustmentType;
      }

      const matchingEntry = Object.entries(ItineraryAdjustmentTypes.itineraryAdjustmentTypes).find(
         ([, value]) => value === normalizedAdjustmentType
      );

      return matchingEntry?.[1] ?? normalizedAdjustmentType;
   }
}
