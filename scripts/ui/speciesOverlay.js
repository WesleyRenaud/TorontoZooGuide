import { buildSpeciesContentHTML } from './speciesOverlayContent.js';

export function initSpeciesOverlay() {
   const speciesOverlay = document.getElementById('speciesOverlay');
   const speciesOverlayContent = speciesOverlay?.querySelector('.species-overlay-content') ?? null;

   if (speciesOverlay) {
      speciesOverlay.addEventListener('click', e => {
         if (e.target === speciesOverlay) close();
      });
   }

   function openFromAnimal(animal) {
      if (!speciesOverlay || !speciesOverlayContent || !animal) return;

      const contentHTML = buildSpeciesContentHTML(animal);

      speciesOverlayContent.innerHTML = `
         <div class="species-overlay-header">
         <button class="species-close" type="button" aria-label="Close">×</button>
         </div>
         <div class="species-overlay-scroll">
         ${contentHTML}
         </div>
      `;

      speciesOverlayContent
         .querySelector('.species-close')
         .addEventListener('click', close);

      speciesOverlay.classList.remove('hidden');
   }

   function close() {
      if (!speciesOverlay) return;
      speciesOverlay.classList.add('hidden');
   }

   return { openFromAnimal, close };
}