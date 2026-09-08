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
         throw new Error('Could not save itinerary warning preference.');
      }

      return result;
   }
}
