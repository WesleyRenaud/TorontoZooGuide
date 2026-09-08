import { ValueNormalizer } from '../api/valueNormalizer.js';
import { ItineraryErrorTypes } from './itineraryErrorTypes.js';

export class ItineraryErrorTypesHelpers {
   static normalizeItineraryErrorType(errorType, legacySuccess) {
      const types = ItineraryErrorTypes.getItineraryErrorTypes();

      const normalizedErrorType = ValueNormalizer.asTrimmedString(errorType);

      if (normalizedErrorType) {
         return normalizedErrorType;
      }

      if (legacySuccess === false) {
         return types?.SAVE_FAILED;
      }

      return types?.SUCCESS;
   }
}
