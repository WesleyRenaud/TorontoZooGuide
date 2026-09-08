import { SpeciesLinkTitleBuilder } from '../../../animals/speciesLinkTitleBuilder.js';
import { ItineraryPanelHelper } from '../itineraryPanelHelper.js';
import { ItineraryPillView } from './itineraryPillView.js';
import { AnimalSelectorModel } from '../../selectors/animalSelector/animalSelectorModel.js';
import { ItineraryEventType } from '../../../shared/enums/itineraryEventType.js';

export class OpenTimelineView {
   static createPillLabelNode(
      label,
      className,
      onLabelClick = null,
      item = null
   ) {
      if (item?.species) {
         return SpeciesLinkTitleBuilder.createAnimalTitleLinkElement({
            species: AnimalSelectorModel.getAnimalSpecies(item),
            enclosureName: AnimalSelectorModel.getAnimalEnclosureName(item),
            className,
            tagName: 'span',
            onClick: onLabelClick,
         });
      }

      return SpeciesLinkTitleBuilder.createSpeciesLinkTitleElement({
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
         const pill = ItineraryPanelHelper.el('span', 'itinerary-day-open-pill');
         pill.appendChild(
            OpenTimelineView.createPillLabelNode(
               label,
               'itinerary-day-open-pill-label',
               onLabelClick
            )
         );
         return pill;
      }

      const pill = ItineraryPanelHelper.el('span', 'itinerary-day-open-pill itinerary-day-open-pill--with-menu');
      const labelNode = OpenTimelineView.createPillLabelNode(
         label,
         'itinerary-day-open-pill-label',
         onLabelClick
      );
      const menuItems = [{ label: removeLabel, onAction: onRemove }];
      const { menu, menuButton, menuPanel } = ItineraryPillView.buildPillMenuNodes(
         menuAriaLabel,
         menuItems
      );

      pill.appendChild(labelNode);
      pill.appendChild(menu);
      ItineraryPillView.bindPillMenu(pill, { menuButton, menuPanel, menuItems });

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

      const marker = ItineraryPanelHelper.el('span', 'itinerary-day-boundary-marker');
      const markerKind = visitBoundaryPlacement === 'starts-at-anchor'
         ? ItineraryEventType.DEPARTURE
         : ItineraryEventType.ARRIVAL;

      marker.setAttribute('aria-label', label);
      marker.setAttribute('data-boundary-marker-kind', markerKind);

      if (typeof onRemove === 'function') {
         const menuItems = [{ label: removeLabel, onAction: onRemove }];
         const menuButton = document.createElement('button');
         const menuPanel = ItineraryPanelHelper.el('div', 'itinerary-day-open-pill-menu-panel');

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
         ItineraryPillView.bindPillMenu(marker, {
            menuButton,
            menuPanel,
            menuItems,
            menuOpenClass: 'itinerary-day-boundary-marker--menu-open',
         });
         return marker;
      }

      marker.appendChild(ItineraryPanelHelper.el('span', 'itinerary-day-boundary-marker-icon'));

      return marker;
   }
}
