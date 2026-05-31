import { el } from '../dom.js';

const PILL_MENU_BUTTON_SYMBOL = '\u22EE';

function resolvePillStrip(pill) {
   return pill.closest?.('.itinerary-day-pill-strip') ?? null;
}

function bindPillMenu(pill, { menuButton, menuPanel, onRemove }) {
   function setMenuOpen(isOpen) {
      pill.classList.toggle('itinerary-day-open-pill--menu-open', isOpen);
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

   const removeButton = menuPanel.querySelector(
      '.itinerary-day-open-pill-menu-item'
   );

   removeButton?.addEventListener('click', async (event) => {
      event.stopPropagation();
      closeMenu();
      await onRemove();
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

export function makeOpenPill(label, { onRemove = null, menuAriaLabel = '', removeLabel = '' } = {}) {
   if (!label) {
      return null;
   }

   if (typeof onRemove !== 'function') {
      return el('span', 'itinerary-day-open-pill', label);
   }

   const pill = el('span', 'itinerary-day-open-pill itinerary-day-open-pill--with-menu');
   const labelNode = el('span', 'itinerary-day-open-pill-label', label);
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

   const removeButton = document.createElement('button');
   removeButton.type = 'button';
   removeButton.className = 'itinerary-day-open-pill-menu-item';
   removeButton.setAttribute('role', 'menuitem');
   removeButton.textContent = removeLabel;
   menuPanel.appendChild(removeButton);

   menu.appendChild(menuButton);
   menu.appendChild(menuPanel);
   pill.appendChild(labelNode);
   pill.appendChild(menu);
   bindPillMenu(pill, { menuButton, menuPanel, onRemove });

   return pill;
}
