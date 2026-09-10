import { ExploreFragment } from './exploreFragment.js';
import { VisitDateValidator } from '../visitDates/visitDateValidator.js';

export class ExploreUpdatesHelper {
   static buildDatePayload(dateCtx) {
      return {
         month: dateCtx.month,
         day: dateCtx.day,
         year: dateCtx.year,
      };
   }

   static buildTodayDatePayload(referenceToday = VisitDateValidator.getToday()) {
      const iso = VisitDateValidator.toISODate(referenceToday);

      return {
         month: VisitDateValidator.getMonth(iso),
         day: VisitDateValidator.getDay(iso),
         year: VisitDateValidator.getYear(iso),
      };
   }

   static resolveActiveTab(activeTab, updates, events) {
      if (activeTab === ExploreFragment.EXPLORE_TAB.UPDATES && !updates.length && events.length) {
         return ExploreFragment.EXPLORE_TAB.EVENTS;
      }

      if (activeTab === ExploreFragment.EXPLORE_TAB.EVENTS && !events.length && updates.length) {
         return ExploreFragment.EXPLORE_TAB.UPDATES;
      }

      return activeTab;
   }
}
