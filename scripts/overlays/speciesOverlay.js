import { buildSpeciesContent } from './speciesOverlayContent.js';

function createCloseButton(onClose) {
   const button = document.createElement('button');
   button.className = 'species-close';
   button.type = 'button';
   button.setAttribute('aria-label', 'Close');
   button.textContent = '×';
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

export function initSpeciesOverlay() {
   const speciesOverlay = document.getElementById('speciesOverlay');
   const speciesOverlayContent = speciesOverlay?.querySelector('.species-overlay-content') ?? null;

   if (speciesOverlay) {
      speciesOverlay.addEventListener('click', (event) => {
         if (event.target === speciesOverlay) close();
      });
   }

   function openFromAnimal(animal) {
      if (!speciesOverlay || !speciesOverlayContent || !animal) return;

      renderSpeciesOverlayContent(speciesOverlayContent, animal, close);
      speciesOverlay.classList.remove('hidden');
   }

   function close() {
      if (!speciesOverlay) return;
      speciesOverlay.classList.add('hidden');
   }

   return { openFromAnimal, close };
}
