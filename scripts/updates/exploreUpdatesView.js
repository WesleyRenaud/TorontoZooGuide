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

   static clearExploreNav(headerEl) {
      headerEl?.querySelector('.explore-update-nav')?.remove();
   }

   static renderExploreNav({
      listEl,
      itemCount,
      activeTab,
      onStep,
   } = {}) {
      const headerEl = ExploreUpdatesView.getExploreHeaderEl(listEl);

      ExploreUpdatesView.clearExploreNav(headerEl);

      if (!headerEl || itemCount <= 1) {
         return;
      }

      const navEl = document.createElement('div');
      navEl.className = 'explore-update-nav';
      const isEventsTab = activeTab === ExploreFragment.EXPLORE_TAB.EVENTS;

      navEl.append(
         ExploreUpdatesChromeHelper.createArrowButton({
            label: isEventsTab ? Strings.map.previousEvent : Strings.map.previousUpdate,
            symbol: Strings.common.previousSymbol,
            onClick: () => onStep(-1),
         }),
         ExploreUpdatesChromeHelper.createArrowButton({
            label: isEventsTab ? Strings.map.nextEvent : Strings.map.nextUpdate,
            symbol: Strings.common.nextSymbol,
            onClick: () => onStep(1),
         })
      );

      headerEl.appendChild(navEl);
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
      }

      if (eventsTabEl) {
         eventsTabEl.disabled = eventsCount === 0;
      }
   }
}
