import { buildSpeciesContent } from './speciesOverlayContent.js';
import { APP_STRINGS } from '../strings.js';

function createCloseButton(onClose) {
   const button = document.createElement('button');
   button.className = 'species-close';
   button.type = 'button';
   button.setAttribute('aria-label', APP_STRINGS.common.close);
   button.textContent = APP_STRINGS.common.closeSymbol;
   button.addEventListener('click', onClose);
   return button;
}

function createOverlayHeader(onClose) {
   const header = document.createElement('div');
   header.className = 'species-overlay-header';
   header.appendChild(createCloseButton(onClose));
   return header;
}

function createOverlayScrollContent(animal) {
   const scroll = document.createElement('div');
   scroll.className = 'species-overlay-scroll';
   scroll.appendChild(buildSpeciesContent(animal));
   return scroll;
}

function renderSpeciesOverlayContent(contentEl, animal, onClose) {
   contentEl.replaceChildren(
      createOverlayHeader(onClose),
      createOverlayScrollContent(animal)
   );
}

let speciesOverlayController = null;

export function initSpeciesOverlay() {
   if (speciesOverlayController) {
      return speciesOverlayController;
   }

   const speciesOverlay = document.getElementById('speciesOverlay');
   const speciesOverlayContent = speciesOverlay?.querySelector('.species-overlay-content') ?? null;

   function close() {
      if (!speciesOverlay) return;
      speciesOverlay.classList.add('hidden');
   }

   function openFromAnimal(animal) {
      if (!speciesOverlay || !speciesOverlayContent || !animal) return;

      renderSpeciesOverlayContent(speciesOverlayContent, animal, close);
      speciesOverlay.classList.remove('hidden');
   }

   if (speciesOverlay) {
      speciesOverlay.addEventListener('click', (event) => {
         if (event.target === speciesOverlay) close();
      });
   }

   speciesOverlayController = { openFromAnimal, close };

   return speciesOverlayController;
}

export function openAnimalSpeciesOverlay(animal) {
   const species = String(animal.species).trim();

   if (!species) {
      return;
   }

   initSpeciesOverlay().openFromAnimal(animal);
}
