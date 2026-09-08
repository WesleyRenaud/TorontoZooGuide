import { ItineraryErrorTypes } from '../itineraryErrorTypes.js';
import { ItineraryService } from '../itineraryService.js';

export class ItineraryPanelScheduleHandlersHelpers {
   static async notifyItineraryUpdated({
      result,
      dispatchUpdated = ItineraryService.dispatchItineraryUpdated,
      loadItinerary = ItineraryService.getItinerary,
   } = {}) {
      if (!ItineraryErrorTypes.isItinerarySuccess(result?.errorType)) {
         return false;
      }

      dispatchUpdated(await loadItinerary());
      return true;
   }
}
