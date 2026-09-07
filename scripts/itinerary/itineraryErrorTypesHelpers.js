import { ItineraryErrorTypes } from './itineraryErrorTypes.js';

export class ItineraryErrorTypesHelpers {
   static normalizeItineraryErrorType(errorType, legacySuccess) {
      const types = ItineraryErrorTypes.getItineraryErrorTypes();

      if (typeof errorType === 'string' && errorType.trim()) {
         return errorType.trim();
      }

      if (legacySuccess === false) {
         return types?.SAVE_FAILED;
      }

      return types?.SUCCESS;
   }
}
