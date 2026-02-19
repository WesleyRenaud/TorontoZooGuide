import { likelihoodToColor, getAnimalIconUrl } from '../utils/icons.js';

export function applyMarkerVisual(markerEl, itemsAtPoint) {
   const animals = itemsAtPoint.filter(i => String(i.type || '').toLowerCase() === 'animal');
   const pavilions = itemsAtPoint.filter(i => String(i.type || '').toLowerCase() === 'pavilion');

   if (animals.length > 0 && pavilions.length === 0) {
      const colour = likelihoodToColor(animals[0].likelihood);
      const colourForUrl = colour.replace('#', '');

      if (animals.length === 1) {
         markerEl.style.backgroundColor = colour;
         markerEl.style.backgroundImage = getAnimalIconUrl(
         animals[0].exhibit,
         animals[0].species,
         colourForUrl
         );
         markerEl.style.backgroundSize = 'cover';
         markerEl.textContent = '';
      } else {
         markerEl.style.backgroundImage = 'none';
         markerEl.style.backgroundColor = colour;
         markerEl.textContent = String(animals.length);
      }
      return;
   }

   if (pavilions.length > 0 && animals.length === 0) {
      markerEl.textContent = '';
      markerEl.style.backgroundColor = 'transparent';
      markerEl.style.backgroundImage = 'url("/images/generic-icons/pavilion.png")';
      markerEl.style.backgroundRepeat = 'no-repeat';
      markerEl.style.backgroundPosition = 'center';
      markerEl.style.backgroundSize = 'cover';

      if (pavilions.length > 1) {
         markerEl.style.backgroundColor = 'rgba(94,150,0,0.95)';
         markerEl.style.backgroundImage = 'none';
         markerEl.textContent = String(pavilions.length);
      }
      return;
   }

   markerEl.style.backgroundImage = 'none';
   markerEl.style.backgroundColor = 'rgba(94,150,0,0.95)';
   markerEl.textContent = String(itemsAtPoint.length);
}


export function setMarkerToAnimalIcon(markerEl, animal) {
   if (!markerEl || !animal) return;

   const colour = likelihoodToColor(animal.likelihood);
   const colourForUrl = String(colour || '').replace('#', '');

   markerEl.textContent = '';
   markerEl.style.backgroundColor = colour;
   markerEl.style.backgroundImage = getAnimalIconUrl(
      animal.exhibit,
      animal.species,
      colourForUrl
   );
   markerEl.style.backgroundRepeat = 'no-repeat';
   markerEl.style.backgroundPosition = 'center';
   markerEl.style.backgroundSize = 'cover';
}