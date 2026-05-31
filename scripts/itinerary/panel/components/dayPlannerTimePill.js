import { el } from '../dom.js';
import { TIMELINE_SLOT_MINUTES } from '../../../shared/constants.js';

const PILL_MENU_BUTTON_SYMBOL = '\u22EE';

function resolvePillStrip(pill) {
   return pill.closest?.('.itinerary-day-pill-strip') ?? null;
}

function buildPillMenuNodes(menuAriaLabel, actionLabel) {
   const menu = el('div', 'itinerary-day-open-pill-menu');
   const menuButton = document.createElement('button');

   menuButton.type = 'button';
   menuButton.className = 'itinerary-day-open-pill-menu-btn';
   menuButton.setAttribute('aria-label', menuAriaLabel);
   menuButton.setAttribute('aria-haspopup', 'menu');
   menuButton.setAttribute('aria-expanded', 'false');
   menuButton.textContent = PILL_MENU_BUTTON_SYMBOL;

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
   { onRemove = null, menuAriaLabel = '', removeLabel = '' } = {}
) {
   if (!label) {
      return null;
   }

   if (typeof onRemove !== 'function') {
      return el('span', 'itinerary-day-open-pill', label);
   }

   const pill = el('span', 'itinerary-day-open-pill itinerary-day-open-pill--with-menu');
   const labelNode = el('span', 'itinerary-day-open-pill-label', label);
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

export function makeScheduledPill(
   label,
   durationMinutes,
   {
      onUnschedule = null,
      menuAriaLabel = '',
      unscheduleLabel = '',
   } = {}
) {
   if (!label || !Number.isFinite(durationMinutes) || durationMinutes <= 0) {
      return null;
   }

   let pill;

   if (typeof onUnschedule !== 'function') {
      pill = el('span', 'itinerary-day-scheduled-pill', label);
   } else {
      pill = el('span', 'itinerary-day-scheduled-pill itinerary-day-scheduled-pill--with-menu');
      const header = el('div', 'itinerary-day-scheduled-pill-header');
      const labelNode = el('span', 'itinerary-day-scheduled-pill-label', label);
      const { menu, menuButton, menuPanel } = buildPillMenuNodes(
         menuAriaLabel,
         unscheduleLabel
      );

      header.appendChild(labelNode);
      header.appendChild(menu);
      pill.appendChild(header);
      bindPillMenu(pill, {
         menuButton,
         menuPanel,
         onAction: onUnschedule,
         menuOpenClass: 'itinerary-day-scheduled-pill--menu-open',
      });
   }

   applyScheduledPillDuration(pill, durationMinutes);

   return pill;
}
