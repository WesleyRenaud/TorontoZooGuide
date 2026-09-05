import { MapApi } from '../api/mapApi.js';
import { ExploreEventCard } from './exploreEventCard.js';
import { ExploreTabs } from './exploreTabs.js';
import { ExploreUpdateCard } from './exploreUpdateCard.js';
import { ExploreUpdatesChrome } from './exploreUpdatesChrome.js';

function buildDatePayload(dateCtx) {
   return {
      month: dateCtx.month,
      day: dateCtx.day,
      year: dateCtx.year,
   };
}

function resolveActiveTab(activeTab, updates, events) {
   if (activeTab === ExploreTabs.EXPLORE_TAB.UPDATES && !updates.length && events.length) {
      return ExploreTabs.EXPLORE_TAB.EVENTS;
   }

   if (activeTab === ExploreTabs.EXPLORE_TAB.EVENTS && !events.length && updates.length) {
      return ExploreTabs.EXPLORE_TAB.UPDATES;
   }

   return activeTab;
}

export function createExploreUpdates({
   listEl,
} = {}) {
   if (!listEl) {
      return null;
   }

   let updates = [];
   let events = [];
   let activeTab = ExploreTabs.EXPLORE_TAB.UPDATES;
   let currentIndex = 0;
   let isCollapsed = false;

   function getActiveItems() {
      return activeTab === ExploreTabs.EXPLORE_TAB.EVENTS ? events : updates;
   }

   function getSafeIndex(items) {
      return Math.max(0, Math.min(items.length - 1, currentIndex));
   }

   function renderCurrentItem() {
      if (!updates.length && !events.length) {
         listEl.replaceChildren();
         ExploreUpdatesChrome.setExploreSectionVisibility(listEl, false);
         ExploreUpdatesChrome.clearExploreNav(ExploreUpdatesChrome.getExploreHeaderEl(listEl));
         return;
      }

      const items = getActiveItems();

      ExploreUpdatesChrome.setExploreSectionVisibility(listEl, true);
      ExploreUpdatesChrome.syncExploreTabs({
         listEl,
         activeTab,
         updatesCount: updates.length,
         eventsCount: events.length,
      });
      currentIndex = items.length ? getSafeIndex(items) : 0;

      // Keep cards from both tabs in the grid so section height stays stable.
      listEl.replaceChildren(
         ...updates.map((update, index) => ExploreUpdateCard.createUpdateCard(
            update,
            activeTab === ExploreTabs.EXPLORE_TAB.UPDATES && index === currentIndex
         )),
         ...events.map((event, index) => ExploreEventCard.createEventCard(
            event,
            activeTab === ExploreTabs.EXPLORE_TAB.EVENTS && index === currentIndex
         ))
      );
      ExploreUpdatesChrome.renderExploreNav({
         listEl,
         itemCount: items.length,
         activeTab,
         onStep: step,
      });
      ExploreUpdatesChrome.syncExploreCollapsedState({
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
      activeTab = resolveActiveTab(activeTab, updates, events);
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
      if (tab !== ExploreTabs.EXPLORE_TAB.UPDATES && tab !== ExploreTabs.EXPLORE_TAB.EVENTS) {
         return;
      }

      if (activeTab === tab) {
         return;
      }

      if (tab === ExploreTabs.EXPLORE_TAB.UPDATES && !updates.length) {
         return;
      }

      if (tab === ExploreTabs.EXPLORE_TAB.EVENTS && !events.length) {
         return;
      }

      activeTab = tab;
      currentIndex = 0;
      renderCurrentItem();
   }

   function toggleCollapsed() {
      isCollapsed = !isCollapsed;
      ExploreUpdatesChrome.syncExploreCollapsedState({
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
            MapApi.getUpdates(buildDatePayload(dateCtx)),
            MapApi.getEvents(buildDatePayload(dateCtx)),
         ]);

         renderItems({
            nextUpdates,
            nextEvents,
         });
      }
      catch (err) {
         listEl.replaceChildren();
         ExploreUpdatesChrome.setExploreSectionVisibility(listEl, false);
         ExploreUpdatesChrome.clearExploreNav(ExploreUpdatesChrome.getExploreHeaderEl(listEl));
      }
   }

   renderItems({
      nextUpdates: [],
      nextEvents: [],
   });
   ExploreUpdatesChrome.getExploreToggleEl(listEl)?.addEventListener('click', toggleCollapsed);
   ExploreUpdatesChrome.getExploreTabEl(listEl, ExploreTabs.EXPLORE_TAB.UPDATES)?.addEventListener(
      'click',
      () => selectTab(ExploreTabs.EXPLORE_TAB.UPDATES)
   );
   ExploreUpdatesChrome.getExploreTabEl(listEl, ExploreTabs.EXPLORE_TAB.EVENTS)?.addEventListener(
      'click',
      () => selectTab(ExploreTabs.EXPLORE_TAB.EVENTS)
   );

   return { refresh };
}
