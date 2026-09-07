import { ItineraryPanelDom } from '../itineraryPanelDom.js';
import { ItineraryPillMenuBuilder } from './itineraryPillMenuBuilder.js';

export class ItineraryPillMenu {
   static buildPillMenuNodes(menuAriaLabel, menuItems = []) {
      const menu = ItineraryPanelDom.el('div', 'itinerary-day-open-pill-menu');
      const menuButton = document.createElement('button');

      menuButton.type = 'button';
      menuButton.className = 'itinerary-day-open-pill-menu-btn';
      menuButton.setAttribute('aria-label', menuAriaLabel);
      menuButton.setAttribute('aria-haspopup', 'menu');
      menuButton.setAttribute('aria-expanded', 'false');
      menuButton.appendChild(ItineraryPillMenuBuilder.buildPillMenuButtonDots());

      const menuPanel = ItineraryPanelDom.el('div', 'itinerary-day-open-pill-menu-panel');
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
         ItineraryPillMenuBuilder.resolvePillStrip(pill)?.classList.toggle('itinerary-day-pill-strip--menu-open', isOpen);
      }

      function closeMenu() {
         menuPanel.hidden = true;
         menuButton.setAttribute('aria-expanded', 'false');
         setMenuOpen(false);
      }

      function openMenu() {
         const activeMenuItems = resolveMenuItems();

         ItineraryPillMenuBuilder.renderMenuPanel(menuPanel, activeMenuItems);
         ItineraryPillMenuBuilder.bindMenuPanelActions(menuPanel, activeMenuItems, closeMenu);
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

      ItineraryPillMenuBuilder.bindMenuPanelActions(menuPanel, resolveMenuItems(), closeMenu);

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
