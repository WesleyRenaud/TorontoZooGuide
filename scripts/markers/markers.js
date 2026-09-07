import { CoordinateEditing } from './coordinateEditing.js';
import { MarkerElement } from './markerElement.js';
import { MarkerGroups } from './markerGroups.js';
import { MarkersHelpers } from './markersHelpers.js';

export class Markers {
   static createMarkerLayer({ mapInner, tooltip, hover, enableCoordinateEditing = false }) {
      const markerElsByCoord = new Map();

      function clear() {
         MarkersHelpers.removeRenderedMarkers(mapInner);
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
            if (MarkersHelpers.shouldRenderMarkerGroup(group)) {
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
