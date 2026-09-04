import { ItineraryApi } from '../api/itineraryApi.js';
import { setStoredItineraryDate } from './draftStorage.js';
import { ItineraryErrorTypes } from './itineraryErrorTypes.js';
import { ItineraryNormalizer } from './itineraryNormalizer.js';
import { ItinerarySearchContext } from './itinerarySearchContext.js';
import { hasSavedItineraryContent } from './itineraryShape.js';
import {
   getDay,
   getMonth,
   getYear,
} from '../visitDates/visitDateRules.js';

export const isItineraryEmpty = ItineraryNormalizer.isItineraryEmpty;
export const normalizeItinerary = ItineraryNormalizer.normalizeItinerary;

export function dispatchItineraryUpdated(itinerary) {
   window.dispatchEvent(new CustomEvent('tzg:itineraryUpdated', {
      detail: { itinerary },
   }));
}

export function dispatchScheduleItineraryItemResult(result) {
   if (!result?.itinerary) {
      return;
   }

   dispatchItineraryUpdated(ItineraryNormalizer.normalizeItineraryFromApiResult(result));
}

async function fetchSavedItineraryVisitDate() {
   const { date } = await ItineraryApi.getItineraryDateRequest();

   if (date) {
      setStoredItineraryDate(date);
   }

   return date;
}

export async function getItinerary() {
   const date = await fetchSavedItineraryVisitDate();
   const { temp } = await ItinerarySearchContext.getItineraryDateSearchContext({ date });
   const result = await ItineraryApi.getItineraryRequest(temp);
   return ItineraryNormalizer.normalizeItineraryFromApiResult(result);
}

export async function getZooHours(date) {
   if (!date) {
      return null;
   }

   const month = getMonth(date);
   const day = getDay(date);
   const year = getYear(date);

   if (month == null || day == null || year == null) {
      return null;
   }

   const result = await ItineraryApi.getZooHoursRequest({ day, month, year });
   return result?.hours || null;
}

export async function clearItinerary() {
   const result = await ItineraryApi.clearItineraryRequest();
   const clearedItinerary = ItineraryNormalizer.createEmptyItinerary();

   window.dispatchEvent(new CustomEvent('tzg:itineraryCleared'));
   dispatchItineraryUpdated(clearedItinerary);

   return result;
}

export async function bulkScheduleItinerary({
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
   dispatchItineraryUpdated(normalizedItinerary);

   return {
      itinerary: normalizedItinerary,
      issues: result.issues ?? [],
   };
}

export async function unscheduleAllItineraryItems() {
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
   dispatchItineraryUpdated(normalizedItinerary);

   return {
      itinerary: normalizedItinerary,
   };
}

export async function acceptItinerary({
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

   dispatchItineraryUpdated(acceptedItinerary);

   return acceptedItinerary;
}

export async function hasActiveItinerary() {
   const itin = await getItinerary();
   return Boolean(itin.isActive) && hasSavedItineraryContent(itin);
}
