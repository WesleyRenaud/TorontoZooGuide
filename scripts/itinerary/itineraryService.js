import {
   acceptItineraryRequest,
   bulkScheduleAnimalsRequest,
   clearItineraryRequest,
   getItineraryDateRequest,
   getItineraryRequest,
   getZooHoursRequest,
   unscheduleAllItineraryItemsRequest,
} from '../api/itineraryApi.js';
import { setStoredItineraryDate } from './draftStorage.js';
import {
   isItinerarySuccess,
   resolveItineraryErrorMessage,
} from './itineraryErrorTypes.js';
import {
   createEmptyItinerary,
   isItineraryEmpty,
   normalizeItinerary,
} from './itineraryNormalization.js';
import { getItineraryDateSearchContext } from './itinerarySearchContext.js';
import {
   getDay,
   getMonth,
   getYear,
} from '../visitDates/visitDateRules.js';

export { isItineraryEmpty, normalizeItinerary };

export function dispatchItineraryUpdated(itinerary) {
   window.dispatchEvent(new CustomEvent('tzg:itineraryUpdated', {
      detail: { itinerary },
   }));
}

export function dispatchScheduleItineraryItemResult(result) {
   if (!result?.itinerary) {
      return;
   }

   dispatchItineraryUpdated(normalizeItinerary({
      ...result.itinerary,
      itineraryConfig: result.itineraryConfig,
   }));
}

async function fetchSavedItineraryVisitDate() {
   const { date } = await getItineraryDateRequest();

   if (date) {
      setStoredItineraryDate(date);
   }

   return date;
}

export async function getItinerary() {
   const date = await fetchSavedItineraryVisitDate();
   const { temp } = await getItineraryDateSearchContext({ date });
   const result = await getItineraryRequest(temp);
   return normalizeItinerary({
      ...result?.itinerary,
      itineraryConfig: result?.itineraryConfig,
   });
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

   const result = await getZooHoursRequest({ day, month, year });
   return result?.hours || null;
}

export async function clearItinerary() {
   const result = await clearItineraryRequest();
   const clearedItinerary = createEmptyItinerary();

   window.dispatchEvent(new CustomEvent('tzg:itineraryCleared'));
   dispatchItineraryUpdated(clearedItinerary);

   return result;
}

export async function bulkScheduleAnimals() {
   const date = await fetchSavedItineraryVisitDate();
   const { temp } = await getItineraryDateSearchContext({ date });
   const result = await bulkScheduleAnimalsRequest(temp);

   if (!isItinerarySuccess(result.errorType)) {
      throw new Error(resolveItineraryErrorMessage(result.errorType));
   }

   const normalizedItinerary = normalizeItinerary({
      ...result?.itinerary,
      itineraryConfig: result?.itineraryConfig,
   });
   dispatchItineraryUpdated(normalizedItinerary);

   return {
      itinerary: normalizedItinerary,
      issues: result.issues ?? [],
   };
}

export async function unscheduleAllItineraryItems() {
   const date = await fetchSavedItineraryVisitDate();
   const { temp } = await getItineraryDateSearchContext({ date });
   const result = await unscheduleAllItineraryItemsRequest(temp);

   if (!isItinerarySuccess(result.errorType)) {
      return {
         errorType: result.errorType,
         message: resolveItineraryErrorMessage(result.errorType),
      };
   }

   const normalizedItinerary = normalizeItinerary({
      ...result?.itinerary,
      itineraryConfig: result?.itineraryConfig,
   });
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
   const { temp } = await getItineraryDateSearchContext({ date });
   const result = await acceptItineraryRequest(
      temp,
      { animalsToKeep, attractionsToKeep }
   );
   const acceptedItinerary = normalizeItinerary({
      ...result?.itinerary,
      itineraryConfig: result?.itineraryConfig,
   });

   dispatchItineraryUpdated(acceptedItinerary);

   return acceptedItinerary;
}

export async function hasActiveItinerary() {
   const itin = await getItinerary();
   return Boolean(itin.isActive) && !isItineraryEmpty(itin);
}
