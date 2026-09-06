import { Dom } from '../dom.js';

function resolvePillStrip(pill) {
   return pill.closest?.('.itinerary-day-pill-strip') ?? null;
}

function buildPillMenuButtonDots() {
   const dots = Dom.el('span', 'itinerary-day-open-pill-menu-dots');

   for (let index = 0; index < 3; index += 1) {
      dots.appendChild(Dom.el('span', 'itinerary-day-open-pill-menu-dot'));
   }

   return dots;
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

export class ItineraryPillMenu {
   static buildPillMenuNodes(menuAriaLabel, menuItems = []) {
      const menu = Dom.el('div', 'itinerary-day-open-pill-menu');
      const menuButton = document.createElement('button');

      menuButton.type = 'button';
      menuButton.className = 'itinerary-day-open-pill-menu-btn';
      menuButton.setAttribute('aria-label', menuAriaLabel);
      menuButton.setAttribute('aria-haspopup', 'menu');
      menuButton.setAttribute('aria-expanded', 'false');
      menuButton.appendChild(buildPillMenuButtonDots());

      const menuPanel = Dom.el('div', 'itinerary-day-open-pill-menu-panel');
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

   static bindPillMenu(
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
}
