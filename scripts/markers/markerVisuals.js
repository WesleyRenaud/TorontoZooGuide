import {
   renderAnimalIcon,
   renderMarkerByType,
} from './markerTypeRenderers.js';
import { MarkerVisualUtils } from './markerVisualUtils.js';

export class MarkerVisuals {
   static applyMarkerVisual(markerEl, itemsAtPoint) {
      if (!markerEl) return;

      MarkerVisualUtils.resetMarkerVisual(markerEl);

      const items = Array.isArray(itemsAtPoint) ? itemsAtPoint : [];

      if (items.length === 0) {
         return;
      }

      if (renderMarkerByType(markerEl, items)) {
         return;
      }

      MarkerVisualUtils.applyCountMarker(markerEl, items.length);
   }

   static setMarkerToAnimalIcon(markerEl, animal) {
      if (!markerEl || !animal) return;

      MarkerVisualUtils.resetMarkerVisual(markerEl);
      renderAnimalIcon(markerEl, animal);
   }
}
