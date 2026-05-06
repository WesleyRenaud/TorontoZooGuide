import {
   renderAnimalIcon,
   renderMarkerByType,
} from './markerTypeRenderers.js';
import {
   applyCountMarker,
   resetMarkerVisual,
} from './markerVisualUtils.js';

export function applyMarkerVisual(markerEl, itemsAtPoint) {
   if (!markerEl) return;

   resetMarkerVisual(markerEl);

   const items = Array.isArray(itemsAtPoint) ? itemsAtPoint : [];

   if (items.length === 0) {
      return;
   }

   if (renderMarkerByType(markerEl, items)) {
      return;
   }

   applyCountMarker(markerEl, items.length);
}

export function setMarkerToAnimalIcon(markerEl, animal) {
   if (!markerEl || !animal) return;

   resetMarkerVisual(markerEl);
   renderAnimalIcon(markerEl, animal);
}
