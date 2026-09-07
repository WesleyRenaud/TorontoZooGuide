import { AnimalIdentity } from '../itinerary/animalIdentity.js';
import { SpeciesOverlayContent } from './speciesOverlayContent.js';
import { Strings } from '../strings.js';

export class SpeciesOverlayBuilder {
   static resolveOverlayElements() {
      const overlay = document.getElementById('speciesOverlay');

      return {
         overlay,
         content: overlay?.querySelector('.species-overlay-content') ?? null,
         closeButton: overlay?.querySelector('.species-close') ?? null,
      };
   }

   static findLinkedAnimalIndex(linkedAnimals, animal) {
      const { species, exhibit } = AnimalIdentity.normalizeAnimalIdentityFields(animal);

      return linkedAnimals.findIndex((linkedAnimal) => (
         linkedAnimal.species === species
         && linkedAnimal.exhibit === exhibit
      ));
   }

   static createNavButton({ className, label, symbol, onClick }) {
      const button = document.createElement('button');
      button.type = 'button';
      button.className = className;
      button.setAttribute('aria-label', label);
      button.textContent = symbol;
      button.addEventListener('click', (event) => {
         event.stopPropagation();
         onClick();
      });
      return button;
   }

   static createOverlayHeader({ linkedAnimals, index, onNavigate }) {
      const header = document.createElement('div');
      header.className = 'species-overlay-header';

      if (linkedAnimals.length < 2) {
         return header;
      }

      const nav = document.createElement('div');
      nav.className = 'species-overlay-nav';

      const position = document.createElement('span');
      position.className = 'species-overlay-nav-position';
      position.textContent = Strings.common.animalPosition(
         index + 1,
         linkedAnimals.length
      );

      nav.append(
         SpeciesOverlayBuilder.createNavButton({
            className: 'species-overlay-nav-btn species-overlay-nav-prev',
            label: Strings.common.previousAnimal,
            symbol: Strings.common.previousSymbol,
            onClick: () => onNavigate(-1),
         }),
         position,
         SpeciesOverlayBuilder.createNavButton({
            className: 'species-overlay-nav-btn species-overlay-nav-next',
            label: Strings.common.nextAnimal,
            symbol: Strings.common.nextSymbol,
            onClick: () => onNavigate(1),
         })
      );
      header.appendChild(nav);
      return header;
   }

   static createOverlayScrollContent(animal) {
      const scroll = document.createElement('div');
      scroll.className = 'species-overlay-scroll';
      scroll.appendChild(SpeciesOverlayContent.buildSpeciesContent(animal));
      return scroll;
   }
}
