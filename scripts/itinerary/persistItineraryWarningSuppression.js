import { ItineraryApi } from '../api/itineraryApi.js';
import { isItinerarySuccess } from './itineraryErrorTypes.js';

export class PersistItineraryWarningSuppression {
   static async persistItineraryWarningSuppression(
      warningType,
      deps = {}
   ) {
      const {
         suppressWarning = ItineraryApi.suppressItineraryWarningRequest,
         isSuccess = isItinerarySuccess,
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
