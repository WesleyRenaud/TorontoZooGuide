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

function buildPillMenuNodes(menuAriaLabel, actionLabel) {
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

   const actionButton = document.createElement('button');
   actionButton.type = 'button';
   actionButton.className = 'itinerary-day-open-pill-menu-item';
   actionButton.setAttribute('role', 'menuitem');
   actionButton.textContent = actionLabel;
   menuPanel.appendChild(actionButton);

   menu.appendChild(menuButton);
   menu.appendChild(menuPanel);

   return { menu, menuButton, menuPanel, actionButton };
}

function bindPillMenu(
   pill,
   { menuButton, menuPanel, onAction, menuOpenClass = 'itinerary-day-open-pill--menu-open' }
) {
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

   const actionButton = menuPanel.querySelector(
      '.itinerary-day-open-pill-menu-item'
   );

   actionButton?.addEventListener('click', async (event) => {
      event.stopPropagation();
      closeMenu();
      await onAction();
   });

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
   const { menu, menuButton, menuPanel } = buildPillMenuNodes(menuAriaLabel, removeLabel);

   pill.appendChild(labelNode);
   pill.appendChild(menu);
   bindPillMenu(pill, { menuButton, menuPanel, onAction: onRemove });

   return pill;
}

function applyScheduledPillDuration(pill, durationMinutes) {
   const durationFraction = durationMinutes / TIMELINE_SLOT_MINUTES;

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

function buildScheduledPillWithMenu(
   label,
   durationMinutes,
   {
      startTime,
      endTime,
      onUnschedule,
      menuAriaLabel,
      unscheduleLabel,
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
      unscheduleLabel
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
      onAction: onUnschedule,
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
      onUnschedule = null,
      menuAriaLabel = '',
      unscheduleLabel = '',
      onLabelClick = null,
   } = {}
) {
   if (!label || !Number.isFinite(durationMinutes) || durationMinutes <= 0) {
      return null;
   }

   let pill;

   if (typeof onUnschedule === 'function') {
      pill = buildScheduledPillWithMenu(label, durationMinutes, {
         startTime,
         endTime,
         onUnschedule,
         menuAriaLabel,
         unscheduleLabel,
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

   applyScheduledPillDuration(pill, durationMinutes);

   return pill;
}
