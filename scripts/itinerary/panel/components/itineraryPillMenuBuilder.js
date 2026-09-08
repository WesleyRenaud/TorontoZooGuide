import { ItineraryPanelHelper } from '../itineraryPanelHelper.js';

export class ItineraryPillMenuBuilder {
   static resolvePillStrip(pill) {
      return pill.closest?.('.itinerary-day-pill-strip') ?? null;
   }

   static buildPillMenuButtonDots() {
      const dots = ItineraryPanelHelper.el('span', 'itinerary-day-open-pill-menu-dots');

      for (let index = 0; index < 3; index += 1) {
         dots.appendChild(ItineraryPanelHelper.el('span', 'itinerary-day-open-pill-menu-dot'));
      }

      return dots;
   }

   static clearMenuPanel(menuPanel) {
      while (menuPanel.children.length > 0) {
         menuPanel.removeChild(menuPanel.children[0]);
      }
   }

   static renderMenuPanel(menuPanel, menuItems = []) {
      ItineraryPillMenuBuilder.clearMenuPanel(menuPanel);

      menuItems.forEach(({ label }) => {
         const actionButton = document.createElement('button');
         actionButton.type = 'button';
         actionButton.className = 'itinerary-day-open-pill-menu-item';
         actionButton.setAttribute('role', 'menuitem');
         actionButton.textContent = label;
         menuPanel.appendChild(actionButton);
      });
   }

   static bindMenuPanelActions(menuPanel, menuItems, closeMenu) {
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
}
