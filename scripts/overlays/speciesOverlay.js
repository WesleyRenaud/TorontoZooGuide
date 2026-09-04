import { AnimalsApi } from '../api/animalsApi.js';
import { normalizeGuardiansTalkLinkedAnimals } from '../guardians/normalizeGuardiansTalkLinkedAnimals.js';
import { AnimalIdentity } from '../itinerary/animalIdentity.js';
import { buildSpeciesContent } from './speciesOverlayContent.js';
import { APP_STRINGS } from '../strings.js';

function resolveOverlayElements() {
   const overlay = document.getElementById('speciesOverlay');

   return {
      overlay,
      content: overlay?.querySelector('.species-overlay-content') ?? null,
      closeButton: overlay?.querySelector('.species-close') ?? null,
   };
}

function findLinkedAnimalIndex(linkedAnimals, animal) {
   const { species, exhibit } = AnimalIdentity.normalizeAnimalIdentityFields(animal);

   return linkedAnimals.findIndex((linkedAnimal) => (
      linkedAnimal.species === species
      && linkedAnimal.exhibit === exhibit
   ));
}

function createNavButton({ className, label, symbol, onClick }) {
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

function createOverlayHeader({ linkedAnimals, index, onNavigate }) {
   const header = document.createElement('div');
   header.className = 'species-overlay-header';

   if (linkedAnimals.length < 2) {
      return header;
   }

   const nav = document.createElement('div');
   nav.className = 'species-overlay-nav';

   const position = document.createElement('span');
   position.className = 'species-overlay-nav-position';
   position.textContent = APP_STRINGS.common.animalPosition(
      index + 1,
      linkedAnimals.length
   );

   nav.append(
      createNavButton({
         className: 'species-overlay-nav-btn species-overlay-nav-prev',
         label: APP_STRINGS.common.previousAnimal,
         symbol: APP_STRINGS.common.previousSymbol,
         onClick: () => onNavigate(-1),
      }),
      position,
      createNavButton({
         className: 'species-overlay-nav-btn species-overlay-nav-next',
         label: APP_STRINGS.common.nextAnimal,
         symbol: APP_STRINGS.common.nextSymbol,
         onClick: () => onNavigate(1),
      })
   );
   header.appendChild(nav);
   return header;
}

function createOverlayScrollContent(animal) {
   const scroll = document.createElement('div');
   scroll.className = 'species-overlay-scroll';
   scroll.appendChild(buildSpeciesContent(animal));
   return scroll;
}

let speciesOverlayController = null;

export function initSpeciesOverlay() {
   if (speciesOverlayController) {
      return speciesOverlayController;
   }

   let boundOverlay = null;
   let boundCloseButton = null;
   const state = {
      linkedAnimals: [],
      index: 0,
      isNavigating: false,
      navigationToken: 0,
   };

   function close() {
      resolveOverlayElements().overlay?.classList.add('hidden');
   }

   function bindShell({ overlay, closeButton }) {
      if (boundOverlay !== overlay) {
         boundOverlay = overlay;
         overlay.addEventListener('click', (event) => {
            if (event.target === overlay) {
               close();
            }
         });
      }

      if (!closeButton || boundCloseButton === closeButton) {
         return;
      }

      boundCloseButton = closeButton;
      closeButton.type = 'button';
      closeButton.setAttribute('aria-label', APP_STRINGS.common.close);
      closeButton.textContent = APP_STRINGS.common.closeSymbol;
      closeButton.addEventListener('click', (event) => {
         event.stopPropagation();
         close();
      });
   }

   function render(animal) {
      const { overlay, content, closeButton } = resolveOverlayElements();

      if (!overlay || !content || !animal) {
         return;
      }

      bindShell({ overlay, closeButton });
      content.replaceChildren(
         createOverlayHeader({
            linkedAnimals: state.linkedAnimals,
            index: state.index,
            onNavigate: (delta) => {
               void navigate(delta);
            },
         }),
         createOverlayScrollContent(animal)
      );
      overlay.classList.remove('hidden');
   }

   async function navigate(delta) {
      if (state.isNavigating || state.linkedAnimals.length < 2) {
         return;
      }

      const nextIndex = (
         state.index + delta + state.linkedAnimals.length
      ) % state.linkedAnimals.length;
      const token = ++state.navigationToken;

      state.isNavigating = true;

      try {
         const animal = await AnimalsApi.getAnimalInformation(
            state.linkedAnimals[nextIndex]
         );

         if (token !== state.navigationToken || !animal) {
            return;
         }

         state.index = nextIndex;
         render(animal);
      }
      finally {
         if (token === state.navigationToken) {
            state.isNavigating = false;
         }
      }
   }

   function openFromAnimal(animal, options = {}) {
      if (!animal) {
         return;
      }

      state.linkedAnimals = normalizeGuardiansTalkLinkedAnimals(
         options.linkedAnimals
      );
      const matchedIndex = findLinkedAnimalIndex(state.linkedAnimals, animal);
      state.index = matchedIndex >= 0 ? matchedIndex : 0;
      state.isNavigating = false;
      state.navigationToken += 1;
      render(animal);
   }

   speciesOverlayController = { openFromAnimal, close };
   return speciesOverlayController;
}

export function openAnimalSpeciesOverlay(animal, options = {}) {
   const { species } = AnimalIdentity.normalizeAnimalIdentityFields(animal);

   if (!species) {
      return;
   }

   initSpeciesOverlay().openFromAnimal(animal, options);
}
