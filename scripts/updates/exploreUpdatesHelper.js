import { ExploreFragment } from './exploreFragment.js';

export class ExploreUpdatesHelper {
   static buildDatePayload(dateCtx) {
      return {
         month: dateCtx.month,
         day: dateCtx.day,
         year: dateCtx.year,
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
