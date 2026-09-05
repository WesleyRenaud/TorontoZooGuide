import { CreateSpeciesLinkTitle } from '../../../animals/createSpeciesLinkTitle.js';
import { el } from '../dom.js';
import { ItineraryPillMenu } from './itineraryPillMenu.js';
import { AnimalSelectorModel } from '../../selectors/animalSelector/animalSelectorModel.js';

export class OpenTimelinePill {
   static createPillLabelNode(
      label,
      className,
      onLabelClick = null,
      item = null
   ) {
      if (item?.species) {
         return CreateSpeciesLinkTitle.createAnimalTitleLinkElement({
            species: AnimalSelectorModel.getAnimalSpecies(item),
            enclosureName: AnimalSelectorModel.getAnimalEnclosureName(item),
            className,
            tagName: 'span',
            onClick: onLabelClick,
         });
      }

      return CreateSpeciesLinkTitle.createSpeciesLinkTitleElement({
         text: label,
         className,
         tagName: 'span',
         onClick: onLabelClick,
      });
   }

   static makeOpenPill(
      label,
      { onRemove = null, menuAriaLabel = '', removeLabel = '', onLabelClick = null } = {}
   ) {
      if (!label) {
         return null;
      }

      if (typeof onRemove !== 'function') {
         const pill = el('span', 'itinerary-day-open-pill');
         pill.appendChild(
            OpenTimelinePill.createPillLabelNode(
               label,
               'itinerary-day-open-pill-label',
               onLabelClick
            )
         );
         return pill;
      }

      const pill = el('span', 'itinerary-day-open-pill itinerary-day-open-pill--with-menu');
      const labelNode = OpenTimelinePill.createPillLabelNode(
         label,
         'itinerary-day-open-pill-label',
         onLabelClick
      );
      const menuItems = [{ label: removeLabel, onAction: onRemove }];
      const { menu, menuButton, menuPanel } = ItineraryPillMenu.buildPillMenuNodes(
         menuAriaLabel,
         menuItems
      );

      pill.appendChild(labelNode);
      pill.appendChild(menu);
      ItineraryPillMenu.bindPillMenu(pill, { menuButton, menuPanel, menuItems });

      return pill;
   }

   static makeBoundaryMarker(
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
         ItineraryPillMenu.bindPillMenu(marker, {
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
}
