import { likelihoodToColor, getAnimalIconUrl } from '../utils/icons.js';

function resetMarkerVisual(markerEl) {
   // Clear anything from prior renders
   markerEl.textContent = '';
   markerEl.style.backgroundImage = 'none';
   markerEl.style.backgroundColor = 'transparent';
   markerEl.style.backgroundRepeat = 'no-repeat';
   markerEl.style.backgroundPosition = 'center';
   markerEl.style.backgroundSize = 'cover';
}

function applyGenericIcon(markerEl, iconUrl, count) {
   // If multiple items of this same type share the coordinate, show a count badge
   if (count > 1) {
      markerEl.style.backgroundColor = 'rgba(94,150,0,0.95)';
      markerEl.style.backgroundImage = 'none';
      markerEl.textContent = String(count);
      return;
   }

   markerEl.style.backgroundColor = 'transparent';
   markerEl.style.backgroundImage = `url("${iconUrl}")`;
   markerEl.style.backgroundRepeat = 'no-repeat';
   markerEl.style.backgroundPosition = 'center';
   markerEl.style.backgroundSize = 'cover';
   markerEl.textContent = '';
}

export function applyMarkerVisual(markerEl, itemsAtPoint) {
   if (!markerEl) return;

   resetMarkerVisual(markerEl);

   const items = Array.isArray(itemsAtPoint) ? itemsAtPoint : [];
   if (items.length === 0) return;

   // ✅ Markers are single-type, so just read the first item
   const type = String(items[0]?.type || '');
   const count = items.length;

   if (type === 'animal') {
      const a = items[0];

      const colour = likelihoodToColor(a.likelihood);
      const colourForUrl = String(colour || '').replace('#', '');

      if (count === 1) {
         markerEl.style.backgroundColor = colour;
         markerEl.style.backgroundImage = getAnimalIconUrl(
            a.exhibit,
            a.species,
            colourForUrl
         );
         markerEl.style.backgroundSize = 'cover';
         markerEl.textContent = '';
      } else {
         markerEl.style.backgroundImage = 'none';
         markerEl.style.backgroundColor = colour;
         markerEl.textContent = String(count);
      }
      return;
   }

   if (type === 'pavilion') {
      applyGenericIcon(markerEl, '/images/generic-icons/pavilion.png', count);
      return;
   }

   if (type === 'restaurant') {
      markerEl.classList.add('marker-restaurant');
      applyGenericIcon(markerEl, '/images/generic-icons/restaurant.png', count);
      return;
   }

   if (type === 'restroom') {
      markerEl.classList.add('marker-restroom');
      applyGenericIcon(markerEl, '/images/generic-icons/restroom.png', count);
      return;
   }

   if (type === 'giftShop') {
      markerEl.classList.add('marker-gift-shop');
      applyGenericIcon(markerEl, '/images/generic-icons/gift-shop.png', count);
      return;
   }

   // Fallback for future types
   markerEl.style.backgroundColor = 'rgba(94,150,0,0.95)';
   markerEl.textContent = String(count);
}

export function setMarkerToAnimalIcon(markerEl, animal) {
   if (!markerEl || !animal) return;

   resetMarkerVisual(markerEl);

   const colour = likelihoodToColor(animal.likelihood);
   const colourForUrl = String(colour || '').replace('#', '');

   markerEl.style.backgroundColor = colour;
   markerEl.style.backgroundImage = getAnimalIconUrl(
      animal.exhibit,
      animal.species,
      colourForUrl
   );
   markerEl.style.backgroundRepeat = 'no-repeat';
   markerEl.style.backgroundPosition = 'center';
   markerEl.style.backgroundSize = 'cover';
   markerEl.textContent = '';
}