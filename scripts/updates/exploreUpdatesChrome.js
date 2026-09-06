import { ExploreTabs } from './exploreTabs.js';
import { Strings } from '../strings.js';

function createArrowButton({
   label,
   symbol,
   onClick,
} = {}) {
   const buttonEl = document.createElement('button');
   buttonEl.type = 'button';
   buttonEl.className = 'explore-update-arrow';
   buttonEl.textContent = symbol;
   buttonEl.setAttribute('aria-label', label);
   buttonEl.addEventListener('click', onClick);
   return buttonEl;
}

export class ExploreUpdatesChrome {
   static getExploreSectionEl(listEl) {
      return listEl.closest('.explore-updates') ?? null;
   }

   static getExploreHeaderEl(listEl) {
      return ExploreUpdatesChrome.getExploreSectionEl(listEl)?.querySelector('.explore-updates-header') ?? null;
   }

   static getExploreToggleEl(listEl) {
      return ExploreUpdatesChrome.getExploreSectionEl(listEl)?.querySelector('.explore-updates-toggle') ?? null;
   }

   static getExploreTabEl(listEl, tab) {
      const sectionEl = ExploreUpdatesChrome.getExploreSectionEl(listEl);

      if (!sectionEl) {
         return null;
      }

      return tab === ExploreTabs.EXPLORE_TAB.EVENTS
         ? sectionEl.querySelector('#exploreEventsTab')
         : sectionEl.querySelector('#exploreUpdatesTab');
   }

   static setExploreSectionVisibility(listEl, isVisible) {
      const sectionEl = ExploreUpdatesChrome.getExploreSectionEl(listEl);

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
      const headerEl = ExploreUpdatesChrome.getExploreHeaderEl(listEl);

      ExploreUpdatesChrome.clearExploreNav(headerEl);

      if (!headerEl || itemCount <= 1) {
         return;
      }

      const navEl = document.createElement('div');
      navEl.className = 'explore-update-nav';
      const isEventsTab = activeTab === ExploreTabs.EXPLORE_TAB.EVENTS;

      navEl.append(
         createArrowButton({
            label: isEventsTab ? Strings.map.previousEvent : Strings.map.previousUpdate,
            symbol: Strings.common.previousSymbol,
            onClick: () => onStep(-1),
         }),
         createArrowButton({
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
      const sectionEl = ExploreUpdatesChrome.getExploreSectionEl(listEl);
      const toggleEl = ExploreUpdatesChrome.getExploreToggleEl(listEl);

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
      const updatesTabEl = ExploreUpdatesChrome.getExploreTabEl(listEl, ExploreTabs.EXPLORE_TAB.UPDATES);
      const eventsTabEl = ExploreUpdatesChrome.getExploreTabEl(listEl, ExploreTabs.EXPLORE_TAB.EVENTS);
      const isEventsTab = activeTab === ExploreTabs.EXPLORE_TAB.EVENTS;

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
