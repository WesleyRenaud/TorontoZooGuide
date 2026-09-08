import { ItineraryClient } from '../api/itineraryClient.js';
import { ItineraryErrorTypes } from './itineraryErrorTypes.js';
import { ItineraryNormalizer } from './itineraryNormalizer.js';
import { ItinerarySearchContext } from './itinerarySearchContext.js';
import { ItineraryServiceHelper } from './itineraryServiceHelper.js';
import { ItineraryShape } from './itineraryShape.js';
import { VisitDateValidator } from '../visitDates/visitDateValidator.js';

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
      const date = await ItineraryServiceHelper.fetchSavedItineraryVisitDate();
      const { temp } = await ItinerarySearchContext.getItineraryDateSearchContext({ date });
      const result = await ItineraryClient.getItineraryRequest(temp);
      return ItineraryNormalizer.normalizeItineraryFromApiResult(result);
   }

   static async getZooHours(date) {
      if (!date) {
         return null;
      }

      const month = VisitDateValidator.getMonth(date);
      const day = VisitDateValidator.getDay(date);
      const year = VisitDateValidator.getYear(date);

      if (month == null || day == null || year == null) {
         return null;
      }

      const result = await ItineraryClient.getZooHoursRequest({ day, month, year });
      return result?.hours || null;
   }

   static async clearItinerary() {
      const result = await ItineraryClient.clearItineraryRequest();
      const clearedItinerary = ItineraryNormalizer.createEmptyItinerary();

      window.dispatchEvent(new CustomEvent('tzg:itineraryCleared'));
      ItineraryService.dispatchItineraryUpdated(clearedItinerary);

      return result;
   }

   static async bulkScheduleItinerary({
   confirmingFixedTimeItemLongWait = false,
} = {}) {
      const date = await ItineraryServiceHelper.fetchSavedItineraryVisitDate();
      const { temp } = await ItinerarySearchContext.getItineraryDateSearchContext({ date });
      const result = await ItineraryClient.bulkScheduleItineraryRequest(temp, {
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
      const date = await ItineraryServiceHelper.fetchSavedItineraryVisitDate();
      const { temp } = await ItinerarySearchContext.getItineraryDateSearchContext({ date });
      const result = await ItineraryClient.unscheduleAllItineraryItemsRequest(temp);

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
      const date = await ItineraryServiceHelper.fetchSavedItineraryVisitDate();
      const { temp } = await ItinerarySearchContext.getItineraryDateSearchContext({ date });
      const result = await ItineraryClient.acceptItineraryRequest(
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
