import { ExploreTabs } from './exploreTabs.js';

export class ExploreUpdatesHelpers {
   static buildDatePayload(dateCtx) {
      return {
         month: dateCtx.month,
         day: dateCtx.day,
         year: dateCtx.year,
      };
   }

   static resolveActiveTab(activeTab, updates, events) {
      if (activeTab === ExploreTabs.EXPLORE_TAB.UPDATES && !updates.length && events.length) {
         return ExploreTabs.EXPLORE_TAB.EVENTS;
      }

      if (activeTab === ExploreTabs.EXPLORE_TAB.EVENTS && !events.length && updates.length) {
         return ExploreTabs.EXPLORE_TAB.UPDATES;
      }

      return activeTab;
   }
}
