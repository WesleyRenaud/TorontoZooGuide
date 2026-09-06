import { ItineraryApi } from '../api/itineraryApi.js';
import { DraftStorage } from './draftStorage.js';
import { ItineraryErrorTypes } from './itineraryErrorTypes.js';
import { ItineraryNormalizer } from './itineraryNormalizer.js';
import { ItinerarySearchContext } from './itinerarySearchContext.js';
import { ItineraryShape } from './itineraryShape.js';
import { VisitDateRules } from '../visitDates/visitDateRules.js';

async function fetchSavedItineraryVisitDate() {
   const { date } = await ItineraryApi.getItineraryDateRequest();

   if (date) {
      DraftStorage.setStoredItineraryDate(date);
   }

   return date;
}

export class ItineraryService {
   static isItineraryEmpty = ItineraryNormalizer.isItineraryEmpty;

   static normalizeItinerary = ItineraryNormalizer.normalizeItinerary;

   static dispatchItineraryUpdated(itinerary) {
      window.dispatchEvent(new CustomEvent('tzg:itineraryUpdated', {
         detail: { itinerary },
      }));
   }

   static dispatchScheduleItineraryItemResult(result) {
      if (!result?.itinerary) {
         return;
      }

      ItineraryService.dispatchItineraryUpdated(ItineraryNormalizer.normalizeItineraryFromApiResult(result));
   }

   static async getItinerary() {
      const date = await fetchSavedItineraryVisitDate();
      const { temp } = await ItinerarySearchContext.getItineraryDateSearchContext({ date });
      const result = await ItineraryApi.getItineraryRequest(temp);
      return ItineraryNormalizer.normalizeItineraryFromApiResult(result);
   }

   static async getZooHours(date) {
      if (!date) {
         return null;
      }

      const month = VisitDateRules.getMonth(date);
      const day = VisitDateRules.getDay(date);
      const year = VisitDateRules.getYear(date);

      if (month == null || day == null || year == null) {
         return null;
      }

      const result = await ItineraryApi.getZooHoursRequest({ day, month, year });
      return result?.hours || null;
   }

   static async clearItinerary() {
      const result = await ItineraryApi.clearItineraryRequest();
      const clearedItinerary = ItineraryNormalizer.createEmptyItinerary();

      window.dispatchEvent(new CustomEvent('tzg:itineraryCleared'));
      ItineraryService.dispatchItineraryUpdated(clearedItinerary);

      return result;
   }

   static async bulkScheduleItinerary({
   confirmingFixedTimeItemLongWait = false,
} = {}) {
      const date = await fetchSavedItineraryVisitDate();
      const { temp } = await ItinerarySearchContext.getItineraryDateSearchContext({ date });
      const result = await ItineraryApi.bulkScheduleItineraryRequest(temp, {
         confirmingFixedTimeItemLongWait,
      });

      if (!ItineraryErrorTypes.isItinerarySuccess(result.errorType)) {
         return {
            errorType: result.errorType,
            message: ItineraryErrorTypes.resolveItineraryErrorMessage(result.errorType),
            issues: result.issues ?? [],
         };
      }

      const normalizedItinerary = ItineraryNormalizer.normalizeItineraryFromApiResult(result);
      ItineraryService.dispatchItineraryUpdated(normalizedItinerary);

      return {
         itinerary: normalizedItinerary,
         issues: result.issues ?? [],
      };
   }

   static async unscheduleAllItineraryItems() {
      const date = await fetchSavedItineraryVisitDate();
      const { temp } = await ItinerarySearchContext.getItineraryDateSearchContext({ date });
      const result = await ItineraryApi.unscheduleAllItineraryItemsRequest(temp);

      if (!ItineraryErrorTypes.isItinerarySuccess(result.errorType)) {
         return {
            errorType: result.errorType,
            message: ItineraryErrorTypes.resolveItineraryErrorMessage(result.errorType),
         };
      }

      const normalizedItinerary = ItineraryNormalizer.normalizeItineraryFromApiResult(result);
      ItineraryService.dispatchItineraryUpdated(normalizedItinerary);

      return {
         itinerary: normalizedItinerary,
      };
   }

   static async acceptItinerary({
   animalsToKeep = [],
   attractionsToKeep = [],
} = {}) {
      const date = await fetchSavedItineraryVisitDate();
      const { temp } = await ItinerarySearchContext.getItineraryDateSearchContext({ date });
      const result = await ItineraryApi.acceptItineraryRequest(
         temp,
         { animalsToKeep, attractionsToKeep }
      );
      const acceptedItinerary = ItineraryNormalizer.normalizeItineraryFromApiResult(result);

      ItineraryService.dispatchItineraryUpdated(acceptedItinerary);

      return acceptedItinerary;
   }

   static async hasActiveItinerary() {
      const itin = await ItineraryService.getItinerary();
      return Boolean(itin.isActive) && ItineraryShape.hasSavedItineraryContent(itin);
   }
}
