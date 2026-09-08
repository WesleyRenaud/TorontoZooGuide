import { MarkerTypeRenderer } from './markerTypeRenderer.js';
import { MarkerVisualHelper } from './markerVisualHelper.js';

export class MarkerHelper {
   static applyMarkerVisual(markerEl, itemsAtPoint) {
      if (!markerEl) return;

      MarkerVisualHelper.resetMarkerVisual(markerEl);

      const items = Array.isArray(itemsAtPoint) ? itemsAtPoint : [];

      if (items.length === 0) {
         return;
      }

      if (MarkerTypeRenderer.renderMarkerByType(markerEl, items)) {
         return;
      }

      MarkerVisualHelper.applyCountMarker(markerEl, items.length);
   }

   static setMarkerToAnimalIcon(markerEl, animal) {
      if (!markerEl || !animal) return;

      MarkerVisualHelper.resetMarkerVisual(markerEl);
      MarkerTypeRenderer.renderAnimalIcon(markerEl, animal);
   }
}
