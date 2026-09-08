import { MapClient } from '../api/mapClient.js';
import { ExploreEventView } from './exploreEventView.js';
import { ExploreUpdatesHelper } from './exploreUpdatesHelper.js';
import { ExploreUpdatesView } from './exploreUpdatesView.js';
import { ExploreUpdateView } from './exploreUpdateView.js';

export class ExploreFragment {
   static EXPLORE_TAB = {
      UPDATES: 'updates',
      EVENTS: 'events',
   };

   static createExploreUpdates({
      listEl,
   } = {}) {
      if (!listEl) {
         return null;
      }

      let updates = [];
      let events = [];
      let activeTab = ExploreFragment.EXPLORE_TAB.UPDATES;
      let currentIndex = 0;
      let isCollapsed = false;

      function getActiveItems() {
         return activeTab === ExploreFragment.EXPLORE_TAB.EVENTS ? events : updates;
      }

      function getSafeIndex(items) {
         return Math.max(0, Math.min(items.length - 1, currentIndex));
      }

      function renderCurrentItem() {
         if (!updates.length && !events.length) {
            listEl.replaceChildren();
            ExploreUpdatesView.setExploreSectionVisibility(listEl, false);
            ExploreUpdatesView.clearExploreNav(ExploreUpdatesView.getExploreHeaderEl(listEl));
            return;
         }

         const items = getActiveItems();

         ExploreUpdatesView.setExploreSectionVisibility(listEl, true);
         ExploreUpdatesView.syncExploreTabs({
            listEl,
            activeTab,
            updatesCount: updates.length,
            eventsCount: events.length,
         });
         currentIndex = items.length ? getSafeIndex(items) : 0;

         // Keep cards from both tabs in the grid so section height stays stable.
         listEl.replaceChildren(
            ...updates.map((update, index) => ExploreUpdateView.createUpdateCard(
               update,
               activeTab === ExploreFragment.EXPLORE_TAB.UPDATES && index === currentIndex
            )),
            ...events.map((event, index) => ExploreEventView.createEventCard(
               event,
               activeTab === ExploreFragment.EXPLORE_TAB.EVENTS && index === currentIndex
            ))
         );
         ExploreUpdatesView.renderExploreNav({
            listEl,
            itemCount: items.length,
            activeTab,
            onStep: step,
         });
         ExploreUpdatesView.syncExploreCollapsedState({
            listEl,
            isCollapsed,
         });
      }

      function renderItems({
         nextUpdates = updates,
         nextEvents = events,
      } = {}) {
         updates = nextUpdates;
         events = nextEvents;
         currentIndex = 0;
         activeTab = ExploreUpdatesHelper.resolveActiveTab(activeTab, updates, events);
         renderCurrentItem();
      }

      function step(delta) {
         const items = getActiveItems();

         if (items.length <= 1) {
            return;
         }

         currentIndex = (currentIndex + delta + items.length) % items.length;
         renderCurrentItem();
      }

      function selectTab(tab) {
         if (tab !== ExploreFragment.EXPLORE_TAB.UPDATES && tab !== ExploreFragment.EXPLORE_TAB.EVENTS) {
            return;
         }

         if (activeTab === tab) {
            return;
         }

         if (tab === ExploreFragment.EXPLORE_TAB.UPDATES && !updates.length) {
            return;
         }

         if (tab === ExploreFragment.EXPLORE_TAB.EVENTS && !events.length) {
            return;
         }

         activeTab = tab;
         currentIndex = 0;
         renderCurrentItem();
      }

      function toggleCollapsed() {
         isCollapsed = !isCollapsed;
         ExploreUpdatesView.syncExploreCollapsedState({
            listEl,
            isCollapsed,
         });
      }

      async function refresh(dateCtx) {
         if (!dateCtx?.month || !dateCtx?.day) {
            renderItems({
               nextUpdates: [],
               nextEvents: [],
            });
            return;
         }

         try {
            const [nextUpdates, nextEvents] = await Promise.all([
               MapClient.getUpdates(ExploreUpdatesHelper.buildDatePayload(dateCtx)),
               MapClient.getEvents(ExploreUpdatesHelper.buildDatePayload(dateCtx)),
            ]);

            renderItems({
               nextUpdates,
               nextEvents,
            });
         }
         catch (err) {
            listEl.replaceChildren();
            ExploreUpdatesView.setExploreSectionVisibility(listEl, false);
            ExploreUpdatesView.clearExploreNav(ExploreUpdatesView.getExploreHeaderEl(listEl));
         }
      }

      renderItems({
         nextUpdates: [],
         nextEvents: [],
      });
      ExploreUpdatesView.getExploreToggleEl(listEl)?.addEventListener('click', toggleCollapsed);
      ExploreUpdatesView.getExploreTabEl(listEl, ExploreFragment.EXPLORE_TAB.UPDATES)?.addEventListener(
         'click',
         () => selectTab(ExploreFragment.EXPLORE_TAB.UPDATES)
      );
      ExploreUpdatesView.getExploreTabEl(listEl, ExploreFragment.EXPLORE_TAB.EVENTS)?.addEventListener(
         'click',
         () => selectTab(ExploreFragment.EXPLORE_TAB.EVENTS)
      );

      return { refresh };
   }
}
