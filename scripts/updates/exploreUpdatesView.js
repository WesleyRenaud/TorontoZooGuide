import { ExploreFragment } from './exploreFragment.js';
import { ExploreUpdatesChromeHelper } from './exploreUpdatesChromeHelper.js';
import { Strings } from '../strings.js';

export class ExploreUpdatesView {
   static getExploreSectionEl(listEl) {
      return listEl.closest('.explore-updates') ?? null;
   }

   static getExploreHeaderEl(listEl) {
      return ExploreUpdatesView.getExploreSectionEl(listEl)?.querySelector('.explore-updates-header') ?? null;
   }

   static getExploreToggleEl(listEl) {
      return ExploreUpdatesView.getExploreSectionEl(listEl)?.querySelector('.explore-updates-toggle') ?? null;
   }

   static getExploreTabEl(listEl, tab) {
      const sectionEl = ExploreUpdatesView.getExploreSectionEl(listEl);

      if (!sectionEl) {
         return null;
      }

      return tab === ExploreFragment.EXPLORE_TAB.EVENTS
         ? sectionEl.querySelector('#exploreEventsTab')
         : sectionEl.querySelector('#exploreUpdatesTab');
   }

   static setExploreSectionVisibility(listEl, isVisible) {
      const sectionEl = ExploreUpdatesView.getExploreSectionEl(listEl);

      if (!sectionEl) {
         return;
      }

      sectionEl.hidden = !isVisible;
   }

   static clearExploreNav(listEl) {
      const sectionEl = ExploreUpdatesView.getExploreSectionEl(listEl);

      sectionEl?.querySelector('.explore-update-nav')?.remove();
   }

   static renderExploreNav({
      listEl,
      itemCount,
      activeIndex = 0,
      activeTab,
      onStep,
   } = {}) {
      const sectionEl = ExploreUpdatesView.getExploreSectionEl(listEl);

      ExploreUpdatesView.clearExploreNav(listEl);

      if (!sectionEl || itemCount <= 1) {
         return;
      }

      const navEl = document.createElement('div');
      navEl.className = 'explore-update-nav';
      const isEventsTab = activeTab === ExploreFragment.EXPLORE_TAB.EVENTS;
      const countEl = document.createElement('span');
      countEl.className = 'explore-update-count';
      countEl.textContent = Strings.map.itemPosition(activeIndex + 1, itemCount);

      navEl.append(
         ExploreUpdatesChromeHelper.createArrowButton({
            label: isEventsTab ? Strings.map.previousEvent : Strings.map.previousUpdate,
            symbol: Strings.common.previousSymbol,
            onClick: () => onStep(-1),
         }),
         countEl,
         ExploreUpdatesChromeHelper.createArrowButton({
            label: isEventsTab ? Strings.map.nextEvent : Strings.map.nextUpdate,
            symbol: Strings.common.nextSymbol,
            onClick: () => onStep(1),
         })
      );

      sectionEl.appendChild(navEl);
   }

   static syncExploreCollapsedState({
      listEl,
      isCollapsed,
   } = {}) {
      const sectionEl = ExploreUpdatesView.getExploreSectionEl(listEl);
      const toggleEl = ExploreUpdatesView.getExploreToggleEl(listEl);

      sectionEl?.classList.toggle('is-collapsed', isCollapsed);

      if (!toggleEl) {
         return;
      }

      toggleEl.setAttribute(
         'aria-label',
         isCollapsed ? Strings.map.showUpdates : Strings.map.hideUpdates
      );
      toggleEl.setAttribute('aria-expanded', String(!isCollapsed));
   }

   static syncExploreTabs({
      listEl,
      activeTab,
      updatesCount,
      eventsCount,
   } = {}) {
      const updatesTabEl = ExploreUpdatesView.getExploreTabEl(listEl, ExploreFragment.EXPLORE_TAB.UPDATES);
      const eventsTabEl = ExploreUpdatesView.getExploreTabEl(listEl, ExploreFragment.EXPLORE_TAB.EVENTS);
      const isEventsTab = activeTab === ExploreFragment.EXPLORE_TAB.EVENTS;

      updatesTabEl?.classList.toggle('is-active', !isEventsTab);
      eventsTabEl?.classList.toggle('is-active', isEventsTab);
      updatesTabEl?.setAttribute('aria-selected', String(!isEventsTab));
      eventsTabEl?.setAttribute('aria-selected', String(isEventsTab));

      if (updatesTabEl) {
         updatesTabEl.disabled = updatesCount === 0;
         const updatesCountEl = updatesTabEl.querySelector('.explore-updates-tab-count');

         if (updatesCountEl) {
            updatesCountEl.textContent = String(updatesCount);
         }
      }

      if (eventsTabEl) {
         eventsTabEl.disabled = eventsCount === 0;
         const eventsCountEl = eventsTabEl.querySelector('.explore-updates-tab-count');

         if (eventsCountEl) {
            eventsCountEl.textContent = String(eventsCount);
         }
      }
   }
}
