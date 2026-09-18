import { ItineraryClient } from '../api/itineraryClient.js';
import { ItineraryErrorTypes } from './itineraryErrorTypes.js';

export class PersistItineraryWarningSuppressor {
   static async persistItineraryWarningSuppression(
      warningType,
      deps = {}
   ) {
      const {
         suppressWarning = ItineraryClient.suppressItineraryWarningRequest,
         isSuccess = ItineraryErrorTypes.isItinerarySuccess,
      } = deps;

      if (!warningType) {
         return;
      }

      const result = await suppressWarning(warningType);

      if (!isSuccess(result.errorType)) {
         throw new Error(ItineraryErrorTypes.resolveItineraryErrorMessage(result.errorType));
      }

      return result;
   }

   static async persistItineraryWarningUnsuppression(
      warningType,
      deps = {}
   ) {
      const {
         unsuppressWarning = ItineraryClient.unsuppressItineraryWarningRequest,
         isSuccess = ItineraryErrorTypes.isItinerarySuccess,
      } = deps;

      if (!warningType) {
         return;
      }

      const result = await unsuppressWarning(warningType);

      if (!isSuccess(result.errorType)) {
         throw new Error(ItineraryErrorTypes.resolveItineraryErrorMessage(result.errorType));
      }

      return result;
   }
}
