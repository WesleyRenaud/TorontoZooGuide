import { suppressItineraryWarningRequest } from '../api/itineraryApi.js';
import { isItinerarySuccess } from './itineraryErrorTypes.js';

export async function persistItineraryWarningSuppression(warningType) {
   if (!warningType) {
      return;
   }

   const result = await suppressItineraryWarningRequest(warningType);

   if (!isItinerarySuccess(result.errorType)) {
      throw new Error('Could not save itinerary warning preference.');
   }

   return result;
}
