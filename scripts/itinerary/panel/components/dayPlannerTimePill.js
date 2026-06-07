import { createSpeciesLinkTitleElement } from '../../../animals/createSpeciesLinkTitle.js';
import { el } from '../dom.js';
import {
   formatScheduledPillTimeRange,
   isExtendedScheduledPill,
} from '../scheduledPillPresentation.js';
import { TIMELINE_SLOT_MINUTES } from '../../../shared/constants.js';

function createPillLabelNode(label, className, onLabelClick = null) {
   return createSpeciesLinkTitleElement({
      text: label,
      className,
      tagName: 'span',
      onClick: onLabelClick,
   });
}

function resolvePillStrip(pill) {
   return pill.closest?.('.itinerary-day-pill-strip') ?? null;
}

function buildPillMenuButtonDots() {
   const dots = el('span', 'itinerary-day-open-pill-menu-dots');

   for (let index = 0; index < 3; index += 1) {
      dots.appendChild(el('span', 'itinerary-day-open-pill-menu-dot'));
   }

   return dots;
}

function buildPillMenuNodes(menuAriaLabel, menuItems = []) {
   const menu = el('div', 'itinerary-day-open-pill-menu');
   const menuButton = document.createElement('button');

   menuButton.type = 'button';
   menuButton.className = 'itinerary-day-open-pill-menu-btn';
   menuButton.setAttribute('aria-label', menuAriaLabel);
   menuButton.setAttribute('aria-haspopup', 'menu');
   menuButton.setAttribute('aria-expanded', 'false');
   menuButton.appendChild(buildPillMenuButtonDots());

   const menuPanel = el('div', 'itinerary-day-open-pill-menu-panel');
   menuPanel.setAttribute('role', 'menu');
   menuPanel.hidden = true;

   menuItems.forEach(({ label }) => {
      const actionButton = document.createElement('button');
      actionButton.type = 'button';
      actionButton.className = 'itinerary-day-open-pill-menu-item';
      actionButton.setAttribute('role', 'menuitem');
      actionButton.textContent = label;
      menuPanel.appendChild(actionButton);
   });

   menu.appendChild(menuButton);
   menu.appendChild(menuPanel);

   return { menu, menuButton, menuPanel };
}

function clearMenuPanel(menuPanel) {
   while (menuPanel.children.length > 0) {
      menuPanel.removeChild(menuPanel.children[0]);
   }
}

function renderMenuPanel(menuPanel, menuItems = []) {
   clearMenuPanel(menuPanel);

   menuItems.forEach(({ label }) => {
      const actionButton = document.createElement('button');
      actionButton.type = 'button';
      actionButton.className = 'itinerary-day-open-pill-menu-item';
      actionButton.setAttribute('role', 'menuitem');
      actionButton.textContent = label;
      menuPanel.appendChild(actionButton);
   });
}

function bindMenuPanelActions(menuPanel, menuItems, closeMenu) {
   menuItems.forEach((menuItem, index) => {
      const actionButton = menuPanel.querySelectorAll(
         '.itinerary-day-open-pill-menu-item'
      )[index];

      if (typeof menuItem?.onAction !== 'function') {
         return;
      }

      actionButton?.addEventListener('click', async (event) => {
         event.stopPropagation();
         closeMenu();
         await menuItem.onAction();
      });
   });
}

function bindPillMenu(
   pill,
   {
      menuButton,
      menuPanel,
      menuItems = [],
      getMenuItems = null,
      menuOpenClass = 'itinerary-day-open-pill--menu-open',
   }
) {
   const resolveMenuItems = () => (
      typeof getMenuItems === 'function'
         ? getMenuItems()
         : menuItems
   );

   function setMenuOpen(isOpen) {
      pill.classList.toggle(menuOpenClass, isOpen);
      resolvePillStrip(pill)?.classList.toggle('itinerary-day-pill-strip--menu-open', isOpen);
   }

   function closeMenu() {
      menuPanel.hidden = true;
      menuButton.setAttribute('aria-expanded', 'false');
      setMenuOpen(false);
   }

   function openMenu() {
      const activeMenuItems = resolveMenuItems();

      renderMenuPanel(menuPanel, activeMenuItems);
      bindMenuPanelActions(menuPanel, activeMenuItems, closeMenu);
      menuPanel.hidden = false;
      menuButton.setAttribute('aria-expanded', 'true');
      setMenuOpen(true);
   }

   menuButton.addEventListener('click', (event) => {
      event.stopPropagation();

      if (menuPanel.hidden) {
         openMenu();
         return;
      }

      closeMenu();
   });

   menuPanel.addEventListener('click', (event) => {
      event.stopPropagation();
   });

   bindMenuPanelActions(menuPanel, resolveMenuItems(), closeMenu);

   const handleDocumentClick = (event) => {
      if (!pill.contains(event.target)) {
         closeMenu();
      }
   };

   document.addEventListener('click', handleDocumentClick);
   pill.__tzgCleanup = () => {
      closeMenu();
      document.removeEventListener('click', handleDocumentClick);
   };
}

export function makeOpenPill(
   label,
   { onRemove = null, menuAriaLabel = '', removeLabel = '', onLabelClick = null } = {}
) {
   if (!label) {
      return null;
   }

   if (typeof onRemove !== 'function') {
      const pill = el('span', 'itinerary-day-open-pill');
      pill.appendChild(
         createPillLabelNode(label, 'itinerary-day-open-pill-label', onLabelClick)
      );
      return pill;
   }

   const pill = el('span', 'itinerary-day-open-pill itinerary-day-open-pill--with-menu');
   const labelNode = createPillLabelNode(
      label,
      'itinerary-day-open-pill-label',
      onLabelClick
   );
   const menuItems = [{ label: removeLabel, onAction: onRemove }];
   const { menu, menuButton, menuPanel } = buildPillMenuNodes(menuAriaLabel, menuItems);

   pill.appendChild(labelNode);
   pill.appendChild(menu);
   bindPillMenu(pill, { menuButton, menuPanel, menuItems });

   return pill;
}

export function makeBoundaryMarker(
   label,
   {
      onRemove = null,
      menuAriaLabel = '',
      removeLabel = '',
      visitBoundaryPlacement = '',
   } = {}
) {
   if (!label) {
      return null;
   }

   const marker = el('span', 'itinerary-day-boundary-marker');
   const markerKind = visitBoundaryPlacement === 'starts-at-anchor'
      ? 'departure'
      : 'arrival';

   marker.setAttribute('aria-label', label);
   marker.setAttribute('data-boundary-marker-kind', markerKind);

   if (typeof onRemove === 'function') {
      const menuItems = [{ label: removeLabel, onAction: onRemove }];
      const menuButton = document.createElement('button');
      const menuPanel = el('div', 'itinerary-day-open-pill-menu-panel');

      menuButton.type = 'button';
      menuButton.className = 'itinerary-day-boundary-marker-btn';
      menuButton.setAttribute('aria-label', menuAriaLabel || label);
      menuButton.setAttribute('aria-haspopup', 'menu');
      menuButton.setAttribute('aria-expanded', 'false');

      menuPanel.setAttribute('role', 'menu');
      menuPanel.hidden = true;

      menuItems.forEach(({ label: itemLabel }) => {
         const actionButton = document.createElement('button');

         actionButton.type = 'button';
         actionButton.className = 'itinerary-day-open-pill-menu-item';
         actionButton.setAttribute('role', 'menuitem');
         actionButton.textContent = itemLabel;
         menuPanel.appendChild(actionButton);
      });

      marker.classList.add('itinerary-day-boundary-marker--with-menu');
      marker.appendChild(menuButton);
      marker.appendChild(menuPanel);
      bindPillMenu(marker, {
         menuButton,
         menuPanel,
         menuItems,
         menuOpenClass: 'itinerary-day-boundary-marker--menu-open',
      });
      return marker;
   }

   marker.appendChild(el('span', 'itinerary-day-boundary-marker-icon'));

   return marker;
}

function applyScheduledPillDuration(
   pill,
   durationMinutes,
   slotSpanMinutes = TIMELINE_SLOT_MINUTES
) {
   const slotSpan = Number.isFinite(slotSpanMinutes) && slotSpanMinutes > 0
      ? slotSpanMinutes
      : TIMELINE_SLOT_MINUTES;
   const durationFraction = durationMinutes / slotSpan;

   pill.style.setProperty(
      '--itinerary-scheduled-pill-duration-fraction',
      String(durationFraction)
   );
   pill.setAttribute('data-duration-fraction', String(durationFraction));
}

function appendScheduledPillTimeRange(pill, startTime, endTime, durationMinutes) {
   const timeRange = formatScheduledPillTimeRange(startTime, endTime);

   if (!isExtendedScheduledPill(durationMinutes) || !timeRange) {
      return;
   }

   pill.appendChild(
      el('span', 'itinerary-day-scheduled-pill-time-range', timeRange)
   );
}

function makeScheduledPillArrowButton(label, direction) {
   const button = document.createElement('button');

   button.type = 'button';
   button.className = `itinerary-day-scheduled-pill-toggle itinerary-day-scheduled-pill-toggle--${direction}`;
   button.setAttribute('aria-label', label);
   button.textContent = direction === 'previous' ? '‹' : '›';

   return button;
}

function replaceGroupedScheduledPillLabel(
   labelMount,
   {
      label = '',
      suffixCount = 0,
      onLabelClick = null,
   } = {}
) {
   const labelNode = createPillLabelNode(
      label,
      'itinerary-day-scheduled-pill-label itinerary-day-scheduled-pill-label-name',
      onLabelClick
   );

   while (labelMount.children.length > 0) {
      labelMount.removeChild(labelMount.children[0]);
   }

   labelMount.textContent = '';
   labelMount.appendChild(labelNode);

   if (suffixCount > 0) {
      labelMount.appendChild(
         el('span', 'itinerary-day-scheduled-pill-count', `+ ${suffixCount}`)
      );
   }
}

function syncScheduledPillTimeRange(
   pill,
   timeRangeNode,
   startTime,
   endTime,
   durationMinutes
) {
   const timeRange = formatScheduledPillTimeRange(startTime, endTime);

   if (!isExtendedScheduledPill(durationMinutes) || !timeRange) {
      timeRangeNode.hidden = true;
      timeRangeNode.textContent = '';
      return;
   }

   timeRangeNode.hidden = false;
   timeRangeNode.textContent = timeRange;

   if (!timeRangeNode.parentElement) {
      pill.appendChild(timeRangeNode);
   }
}

function resolveWrappedGroupIndex(index, groupSize) {
   if (groupSize <= 0) {
      return 0;
   }

   return ((index % groupSize) + groupSize) % groupSize;
}

function buildGroupedScheduledPill(
   groupItems,
   durationMinutes,
   {
      menuAriaLabel,
   }
) {
   let activeIndex = 0;
   const groupSize = groupItems.length;
   const suffixCount = groupSize - 1;
   const longestLabelLength = Math.max(
      ...groupItems.map((groupItem) => String(groupItem.label ?? '').length)
   );
   const hasMenuItems = groupItems.some((groupItem) => (
      (groupItem.menuItems ?? []).length > 0
   ));
   const pill = el('div', 'itinerary-day-scheduled-pill itinerary-day-scheduled-pill--with-menu itinerary-day-scheduled-pill--grouped');
   const header = el('div', 'itinerary-day-scheduled-pill-header itinerary-day-scheduled-pill-header--grouped');
   const previousButton = makeScheduledPillArrowButton(
      'Previous scheduled item',
      'previous'
   );
   const nextButton = makeScheduledPillArrowButton(
      'Next scheduled item',
      'next'
   );
   const labelMount = el('div', 'itinerary-day-scheduled-pill-label-mount');
   const menuNodes = hasMenuItems
      ? buildPillMenuNodes(menuAriaLabel, groupItems[0]?.menuItems ?? [])
      : null;
   const timeRangeNode = el('span', 'itinerary-day-scheduled-pill-time-range');

   if (isExtendedScheduledPill(durationMinutes)) {
      pill.classList.add('itinerary-day-scheduled-pill--extended');
   }

   pill.style.setProperty(
      '--itinerary-scheduled-pill-group-label-chars',
      String(longestLabelLength)
   );

   function getActiveItem() {
      return groupItems[activeIndex] ?? groupItems[0];
   }

   function syncActiveItem() {
      const activeItem = getActiveItem();

      replaceGroupedScheduledPillLabel(
         labelMount,
         {
            label: activeItem.label,
            suffixCount,
            onLabelClick: activeItem.onLabelClick,
         }
      );
      syncScheduledPillTimeRange(
         pill,
         timeRangeNode,
         activeItem.startTime,
         activeItem.endTime,
         durationMinutes
      );
      pill.setAttribute('data-active-group-index', String(activeIndex));
   }

   previousButton.addEventListener('click', (event) => {
      event.stopPropagation();
      activeIndex = resolveWrappedGroupIndex(activeIndex - 1, groupSize);
      syncActiveItem();
   });
   nextButton.addEventListener('click', (event) => {
      event.stopPropagation();
      activeIndex = resolveWrappedGroupIndex(activeIndex + 1, groupSize);
      syncActiveItem();
   });

   const trailingControls = el('div', 'itinerary-day-scheduled-pill-trailing-controls');

   header.appendChild(previousButton);
   header.appendChild(labelMount);
   trailingControls.appendChild(nextButton);

   if (menuNodes) {
      trailingControls.appendChild(menuNodes.menu);
   }

   header.appendChild(trailingControls);

   pill.appendChild(header);
   pill.appendChild(timeRangeNode);
   pill.setAttribute('data-group-size', String(groupSize));
   syncActiveItem();

   if (menuNodes) {
      bindPillMenu(pill, {
         menuButton: menuNodes.menuButton,
         menuPanel: menuNodes.menuPanel,
         getMenuItems: () => getActiveItem()?.menuItems ?? [],
         menuOpenClass: 'itinerary-day-scheduled-pill--menu-open',
      });
   }

   return pill;
}

function buildScheduledPillWithMenu(
   label,
   durationMinutes,
   {
      startTime,
      endTime,
      menuItems = [],
      menuAriaLabel,
      onLabelClick = null,
   }
) {
   const pill = el('div', 'itinerary-day-scheduled-pill itinerary-day-scheduled-pill--with-menu');
   const header = el('div', 'itinerary-day-scheduled-pill-header');
   const labelNode = createPillLabelNode(
      label,
      'itinerary-day-scheduled-pill-label',
      onLabelClick
   );
   const { menu, menuButton, menuPanel } = buildPillMenuNodes(
      menuAriaLabel,
      menuItems
   );

   if (isExtendedScheduledPill(durationMinutes)) {
      pill.classList.add('itinerary-day-scheduled-pill--extended');
   }

   header.appendChild(labelNode);
   header.appendChild(menu);
   pill.appendChild(header);
   appendScheduledPillTimeRange(pill, startTime, endTime, durationMinutes);
   bindPillMenu(pill, {
      menuButton,
      menuPanel,
      menuItems,
      menuOpenClass: 'itinerary-day-scheduled-pill--menu-open',
   });

   return pill;
}

function buildScheduledPillWithoutMenu(
   label,
   durationMinutes,
   {
      startTime,
      endTime,
      onLabelClick = null,
   }
) {
   if (!isExtendedScheduledPill(durationMinutes)) {
      const pill = el('span', 'itinerary-day-scheduled-pill');
      pill.appendChild(
         createPillLabelNode(label, 'itinerary-day-scheduled-pill-label', onLabelClick)
      );
      return pill;
   }

   const pill = el('div', 'itinerary-day-scheduled-pill itinerary-day-scheduled-pill--extended');
   const header = el('div', 'itinerary-day-scheduled-pill-header');

   header.appendChild(
      createPillLabelNode(label, 'itinerary-day-scheduled-pill-label', onLabelClick)
   );
   pill.appendChild(header);
   appendScheduledPillTimeRange(pill, startTime, endTime, durationMinutes);

   return pill;
}

export function makeScheduledPill(
   label,
   durationMinutes,
   {
      startTime,
      endTime,
      groupItems = [],
      menuItems = [],
      menuAriaLabel = '',
      onLabelClick = null,
      slotSpanMinutes = TIMELINE_SLOT_MINUTES,
      displayDurationMinutes = durationMinutes,
   } = {}
) {
   if (!label || !Number.isFinite(durationMinutes) || durationMinutes <= 0) {
      return null;
   }

   let pill;

   if (groupItems.length > 1) {
      pill = buildGroupedScheduledPill(groupItems, durationMinutes, {
         menuAriaLabel,
      });
   }
   else if (menuItems.length > 0) {
      pill = buildScheduledPillWithMenu(label, durationMinutes, {
         startTime,
         endTime,
         menuItems,
         menuAriaLabel,
         onLabelClick,
      });
   }
   else {
      pill = buildScheduledPillWithoutMenu(label, durationMinutes, {
         startTime,
         endTime,
         onLabelClick,
      });
   }

   applyScheduledPillDuration(pill, displayDurationMinutes, slotSpanMinutes);

   return pill;
}
