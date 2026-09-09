import { ValueNormalizer } from '../api/valueNormalizer.js';
import { ItineraryErrorType } from '../shared/enums/itineraryErrorType.js';

export class ItineraryErrorTypesHelper {
   static normalizeItineraryErrorType(errorType, legacySuccess) {
      const normalizedErrorType = ValueNormalizer.asTrimmedString(errorType);

      if (normalizedErrorType) {
         return normalizedErrorType;
      }

      if (legacySuccess === false) {
         return ItineraryErrorType.SAVE_FAILED;
      }

      return ItineraryErrorType.SUCCESS;
   }
}
