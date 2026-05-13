/**
 * Visit-day defaults shared by the map (specific-day picker), itinerary wizard (date floor),
 * and panel day planner (which ISO day to load zoo hours for when nothing is saved).
 */
import { getStoredItineraryDate } from './draftStorage.js';
import { getZooHours } from './itineraryService.js';
import {
   addLocalCalendarDays,
   getToday,
   isLocalTimeAtOrPastZooClose,
   toISODate,
} from '../visitDates/visitDateRules.js';

/**
 * First calendar day the visitor may pick as a visit date: normally today at local noon,
 * or tomorrow at local noon when local time is at or after today's zoo closeTime.
 */
export async function resolveEarliestSelectableVisitDateNoon() {
   const todayIso = toISODate(getToday());

   try {
      const hours = await getZooHours(todayIso);

      if (hours?.closeTime && isLocalTimeAtOrPastZooClose(hours.closeTime)) {
         return addLocalCalendarDays(getToday(), 1);
      }
   } catch {
      /* ignore network / parse errors; fall back to today */
   }

   return getToday();
}

/**
 * ISO calendar day for itinerary-adjacent API calls (e.g. getZooHours): use the server
 * itinerary date when present, else the locally stored draft date, else the same
 * post-close-aware default as the map date picker and wizard date floor.
 */
export async function resolveEffectiveItineraryHoursDateIso(itinerary) {
   const fromItin = typeof itinerary?.date === 'string' && itinerary.date.trim();

   if (fromItin) {
      return fromItin;
   }

   const stored = getStoredItineraryDate()?.trim?.();

   if (stored) {
      return stored;
   }

   return toISODate(await resolveEarliestSelectableVisitDateNoon());
}
