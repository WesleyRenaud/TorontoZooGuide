import { enableMarkerCoordinateEditing } from './coordinateEditing.js';
import { createMarkerElement, bindMarkerInteractions } from './markerElement.js';
import { groupMarkersByCoordinate } from './markerGroups.js';

export function createMarkerLayer({ mapInner, tooltip, hover, enableCoordinateEditing = false }) {
   const markerElsByCoord = new Map();

   function clear() {
      mapInner.querySelectorAll('.marker').forEach((m) => m.remove());
      markerElsByCoord.clear();
   }

   function render(items) {
      clear();

      const markerMap = groupMarkersByCoordinate(items);

      markerMap.forEach((group) => {
         if (!group.items.length) {
            return;
         }

         const markerEl = createMarkerElement(group);
         markerElsByCoord.set(group.key, markerEl);
         mapInner.appendChild(markerEl);

         bindMarkerInteractions({
            markerEl,
            group,
            mapInner,
            tooltip,
            hover,
            enableCoordinateEditing,
            enableMarkerCoordinateEditing,
         });
      });
   }

   function getMarkerByCoord(key) {
      return markerElsByCoord.get(key) || null;
   }

   function getAllMarkers() {
      return Array.from(markerElsByCoord.values());
   }

   return { render, getMarkerByCoord, getAllMarkers };
}
