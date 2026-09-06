import { ItineraryApi } from '../api/itineraryApi.js';
import { DraftStorage } from './draftStorage.js';
import { ItineraryErrorTypes } from './itineraryErrorTypes.js';
import { ItineraryNormalizer } from './itineraryNormalizer.js';
import { ItinerarySearchContext } from './itinerarySearchContext.js';
import { ItineraryService } from './itineraryService.js';
import { ItineraryShape } from './itineraryShape.js';
import { VisitDateEarliest } from './visitDateEarliest.js';

export class EnsureItineraryVisitDate {
   static async ensureItineraryVisitDate(itinerary = {}) {
      const { date: serverDate } = await ItineraryApi.getItineraryDateRequest();

      if (serverDate) {
         DraftStorage.setStoredItineraryDate(serverDate);

         if (itinerary?.date === serverDate) {
            return itinerary;
         }

         return {
            ...itinerary,
            date: serverDate,
         };
      }

      const date = await VisitDateEarliest.resolveEffectiveItineraryHoursDateIso(itinerary);
      const { temp } = await ItinerarySearchContext.getItineraryDateSearchContext({ date, includeTemp: false });
      const result = await ItineraryApi.setItineraryRequest({
         ...ItineraryShape.toSetItineraryPayload(ItineraryShape.normalizeItineraryDraft({
            ...itinerary,
            date,
         })),
         temp,
      });

      if (!ItineraryErrorTypes.isItinerarySuccess(result.errorType)) {
         throw new Error(ItineraryErrorTypes.resolveItineraryErrorMessage(result.errorType));
      }

      DraftStorage.setStoredItineraryDate(date);

      const normalizedItinerary = ItineraryNormalizer.normalizeItineraryFromApiResult(result);

      ItineraryService.dispatchItineraryUpdated(normalizedItinerary);

      return normalizedItinerary;
   }
}
