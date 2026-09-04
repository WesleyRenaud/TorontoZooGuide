/**
 * Visit-day defaults shared by the map (specific-day picker), itinerary wizard (date floor),
 * and panel day planner (which ISO day to load zoo hours for when nothing is saved).
 */
import { DraftStorage } from './draftStorage.js';
import { getZooHours } from './itineraryService.js';
import { VisitDateRules } from '../visitDates/visitDateRules.js';

/**
 * First calendar day the visitor may pick as a visit date: normally today at local noon,
 * or tomorrow at local noon when local time is at or after today's zoo closeTime.
 */
export class VisitDateEarliest {
   static async resolveEarliestSelectableVisitDateNoon(deps = {}) {
      const {
         getTodayFn = VisitDateRules.getToday,
         getZooHoursFn = getZooHours,
         isPastClose = VisitDateRules.isLocalTimeAtOrPastZooClose,
         addDays = VisitDateRules.addLocalCalendarDays,
         toIso = VisitDateRules.toISODate,
      } = deps;

      const today = getTodayFn();
      const todayIso = toIso(today);

      try {
         const hours = await getZooHoursFn(todayIso);

         if (hours?.closeTime && isPastClose(hours.closeTime)) {
            return addDays(today, 1);
         }
      } catch {
         /* ignore network / parse errors; fall back to today */
      }

      return today;
   }

   /**
    * ISO calendar day for itinerary-adjacent API calls (e.g. getZooHours): use the server
    * itinerary date when present, else the locally stored draft date, else the same
    * post-close-aware default as the map date picker and wizard date floor.
    */
   static async resolveEffectiveItineraryHoursDateIso(
      itinerary,
      deps = {}
   ) {
      const {
         getStoredDate = DraftStorage.getStoredItineraryDate,
         resolveEarliest = VisitDateEarliest.resolveEarliestSelectableVisitDateNoon,
         toIso = VisitDateRules.toISODate,
      } = deps;

      const fromItin = typeof itinerary?.date === 'string' && itinerary.date.trim();

      if (fromItin) {
         return fromItin;
      }

      const stored = getStoredDate()?.trim?.();

      if (stored) {
         return stored;
      }

      return toIso(await resolveEarliest(deps));
   }
}
