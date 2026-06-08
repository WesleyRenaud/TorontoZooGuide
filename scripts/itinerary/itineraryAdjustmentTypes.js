let itineraryAdjustmentTypes = null;

export function updateItineraryAdjustmentTypesFromConfig(itineraryConfig = {}) {
   const adjustmentTypes = itineraryConfig?.adjustmentTypes;

   if (adjustmentTypes && typeof adjustmentTypes === 'object') {
      itineraryAdjustmentTypes = Object.freeze({ ...adjustmentTypes });
   }
}

export function getItineraryAdjustmentTypes() {
   return itineraryAdjustmentTypes;
}

export function normalizeItineraryAdjustmentType(adjustmentType) {
   const normalizedAdjustmentType = typeof adjustmentType === 'string'
      ? adjustmentType.trim()
      : '';

   if (!normalizedAdjustmentType || !itineraryAdjustmentTypes) {
      return normalizedAdjustmentType;
   }

   const matchingEntry = Object.entries(itineraryAdjustmentTypes).find(
      ([, value]) => value === normalizedAdjustmentType
   );

   return matchingEntry?.[1] ?? normalizedAdjustmentType;
}
