import { EXPLORE_TAB } from './exploreTabs.js';
import { APP_STRINGS } from '../strings.js';

export function getExploreSectionEl(listEl) {
   return listEl.closest('.explore-updates') ?? null;
}

export function getExploreHeaderEl(listEl) {
   return getExploreSectionEl(listEl)?.querySelector('.explore-updates-header') ?? null;
}

export function getExploreToggleEl(listEl) {
   return getExploreSectionEl(listEl)?.querySelector('.explore-updates-toggle') ?? null;
}

export function getExploreTabEl(listEl, tab) {
   const sectionEl = getExploreSectionEl(listEl);

   if (!sectionEl) {
      return null;
   }

   return tab === EXPLORE_TAB.EVENTS
      ? sectionEl.querySelector('#exploreEventsTab')
      : sectionEl.querySelector('#exploreUpdatesTab');
}

export function setExploreSectionVisibility(listEl, isVisible) {
   const sectionEl = getExploreSectionEl(listEl);

   if (!sectionEl) {
      return;
   }

   sectionEl.hidden = !isVisible;
}

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

export function clearExploreNav(headerEl) {
   headerEl?.querySelector('.explore-update-nav')?.remove();
}

export function renderExploreNav({
   listEl,
   itemCount,
   activeTab,
   onStep,
} = {}) {
   const headerEl = getExploreHeaderEl(listEl);

   clearExploreNav(headerEl);

   if (!headerEl || itemCount <= 1) {
      return;
   }

   const navEl = document.createElement('div');
   navEl.className = 'explore-update-nav';
   const isEventsTab = activeTab === EXPLORE_TAB.EVENTS;

   navEl.append(
      createArrowButton({
         label: isEventsTab ? APP_STRINGS.map.previousEvent : APP_STRINGS.map.previousUpdate,
         symbol: APP_STRINGS.common.previousSymbol,
         onClick: () => onStep(-1),
      }),
      createArrowButton({
         label: isEventsTab ? APP_STRINGS.map.nextEvent : APP_STRINGS.map.nextUpdate,
         symbol: APP_STRINGS.common.nextSymbol,
         onClick: () => onStep(1),
      })
   );

   headerEl.appendChild(navEl);
}

export function syncExploreCollapsedState({
   listEl,
   isCollapsed,
} = {}) {
   const sectionEl = getExploreSectionEl(listEl);
   const toggleEl = getExploreToggleEl(listEl);

   sectionEl?.classList.toggle('is-collapsed', isCollapsed);

   if (!toggleEl) {
      return;
   }

   toggleEl.setAttribute(
      'aria-label',
      isCollapsed ? APP_STRINGS.map.showUpdates : APP_STRINGS.map.hideUpdates
   );
   toggleEl.setAttribute('aria-expanded', String(!isCollapsed));
}

export function syncExploreTabs({
   listEl,
   activeTab,
   updatesCount,
   eventsCount,
} = {}) {
   const updatesTabEl = getExploreTabEl(listEl, EXPLORE_TAB.UPDATES);
   const eventsTabEl = getExploreTabEl(listEl, EXPLORE_TAB.EVENTS);
   const isEventsTab = activeTab === EXPLORE_TAB.EVENTS;

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
