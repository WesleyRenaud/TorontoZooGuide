import { CoordinateEditing } from './coordinateEditing.js';
import { MarkerElement } from './markerElement.js';
import { MarkerGroups } from './markerGroups.js';

const MARKER_SELECTOR = '.marker';

function removeRenderedMarkers(mapInner) {
   mapInner.querySelectorAll(MARKER_SELECTOR).forEach((markerEl) => {
      markerEl.remove();
   });
}

function shouldRenderMarkerGroup(group) {
   return group.items.length > 0;
}

export class Markers {
   static createMarkerLayer({ mapInner, tooltip, hover, enableCoordinateEditing = false }) {
      const markerElsByCoord = new Map();

      function clear() {
         removeRenderedMarkers(mapInner);
         markerElsByCoord.clear();
      }

      function createMarkerGroupElement(group) {
         const markerEl = MarkerElement.createMarkerElement(group);

         markerElsByCoord.set(group.key, markerEl);

         MarkerElement.bindMarkerInteractions({
            markerEl,
            group,
            mapInner,
            tooltip,
            hover,
            enableCoordinateEditing,
            enableMarkerCoordinateEditing: CoordinateEditing.enableMarkerCoordinateEditing,
         });

         return markerEl;
      }

      function buildMarkerFragment(items) {
         const fragment = document.createDocumentFragment();
         const markerMap = MarkerGroups.groupMarkersByCoordinate(items);

         markerMap.forEach((group) => {
            if (shouldRenderMarkerGroup(group)) {
               fragment.appendChild(createMarkerGroupElement(group));
            }
         });

         return fragment;
      }

      function render(items) {
         clear();
         mapInner.appendChild(buildMarkerFragment(items));
      }

      function getMarkerByCoord(key) {
         return markerElsByCoord.get(key) || null;
      }

      function getAllMarkers() {
         return Array.from(markerElsByCoord.values());
      }

      return { render, getMarkerByCoord, getAllMarkers };
   }
}
