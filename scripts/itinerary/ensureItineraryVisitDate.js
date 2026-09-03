import { ItineraryApi } from '../api/itineraryApi.js';
import { setStoredItineraryDate } from './draftStorage.js';
import {
   isItinerarySuccess,
   resolveItineraryErrorMessage,
} from './itineraryErrorTypes.js';
import { ItineraryNormalizer } from './itineraryNormalizer.js';
import { getItineraryDateSearchContext } from './itinerarySearchContext.js';
import { dispatchItineraryUpdated } from './itineraryService.js';
import {
   normalizeItineraryDraft,
   toSetItineraryPayload,
} from './itineraryShape.js';
import { resolveEffectiveItineraryHoursDateIso } from './visitDateEarliest.js';

export async function ensureItineraryVisitDate(itinerary = {}) {
   const { date: serverDate } = await ItineraryApi.getItineraryDateRequest();

   if (serverDate) {
      setStoredItineraryDate(serverDate);

      if (itinerary?.date === serverDate) {
         return itinerary;
      }

      return {
         ...itinerary,
         date: serverDate,
      };
   }

   const date = await resolveEffectiveItineraryHoursDateIso(itinerary);
   const { temp } = await getItineraryDateSearchContext({ date, includeTemp: false });
   const result = await ItineraryApi.setItineraryRequest({
      ...toSetItineraryPayload(normalizeItineraryDraft({
         ...itinerary,
         date,
      })),
      temp,
   });

   if (!isItinerarySuccess(result.errorType)) {
      throw new Error(resolveItineraryErrorMessage(result.errorType));
   }

   setStoredItineraryDate(date);

   const normalizedItinerary = ItineraryNormalizer.normalizeItineraryFromApiResult(result);

   dispatchItineraryUpdated(normalizedItinerary);

   return normalizedItinerary;
}
