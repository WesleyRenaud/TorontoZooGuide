import { ItineraryClient } from '../api/itineraryClient.js';
import { DraftStore } from './draftStore.js';
import { ItineraryErrorTypes } from './itineraryErrorTypes.js';
import { ItineraryNormalizer } from './itineraryNormalizer.js';
import { ItinerarySearchContext } from './itinerarySearchContext.js';
import { ItineraryService } from './itineraryService.js';
import { ItineraryShape } from './itineraryShape.js';
import { VisitDateResolver } from './visitDateResolver.js';

export class ItineraryVisitDateResolver {
   static async ensureItineraryVisitDate(itinerary = {}) {
      const { date: serverDate } = await ItineraryClient.getItineraryDateRequest();

      if (serverDate) {
         DraftStore.setStoredItineraryDate(serverDate);

         if (itinerary?.date === serverDate) {
            return itinerary;
         }

         return {
            ...itinerary,
            date: serverDate,
         };
      }

      const date = await VisitDateResolver.resolveEffectiveItineraryHoursDateIso(itinerary);
      const { temp } = await ItinerarySearchContext.getItineraryDateSearchContext({ date, includeTemp: false });
      const result = await ItineraryClient.setItineraryRequest({
         ...ItineraryShape.toSetItineraryPayload(ItineraryShape.normalizeItineraryDraft({
            ...itinerary,
            date,
         })),
         temp,
      });

      if (!ItineraryErrorTypes.isItinerarySuccess(result.errorType)) {
         throw new Error(ItineraryErrorTypes.resolveItineraryErrorMessage(result.errorType));
      }

      DraftStore.setStoredItineraryDate(date);

      const normalizedItinerary = ItineraryNormalizer.normalizeItineraryFromApiResult(result);

      ItineraryService.dispatchItineraryUpdated(normalizedItinerary);

      return normalizedItinerary;
   }
}
