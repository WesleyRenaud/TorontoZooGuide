import { CoordinateEditor } from './coordinateEditor.js';
import { MarkerBuilder } from './markerBuilder.js';
import { MarkerGrouper } from './markerGrouper.js';
import { MarkerLayerHelper } from './markerLayerHelper.js';

export class MarkerController {
   static createMarkerLayer({
      markerSurface,
      tooltip,
      hover,
      enableCoordinateEditing = false,
   }) {
      const markerElsByCoord = new Map();

      function clear() {
         MarkerLayerHelper.removeRenderedMarkers(markerSurface);
         markerElsByCoord.clear();
      }

      function createMarkerGroupElement(group) {
         const markerEl = MarkerBuilder.createMarkerElement(group);

         markerElsByCoord.set(group.key, markerEl);

         MarkerBuilder.bindMarkerInteractions({
            markerEl,
            group,
            mapInner: markerSurface,
            tooltip,
            hover,
            enableCoordinateEditing,
            enableMarkerCoordinateEditing: CoordinateEditor.enableMarkerCoordinateEditing,
         });

         return markerEl;
      }

      function buildMarkerFragment(items) {
         const fragment = document.createDocumentFragment();
         const markerMap = MarkerGrouper.groupMarkersByCoordinate(items);

         markerMap.forEach((group) => {
            if (MarkerLayerHelper.shouldRenderMarkerGroup(group)) {
               fragment.appendChild(createMarkerGroupElement(group));
            }
         });

         return fragment;
      }

      function render(items) {
         clear();
         markerSurface.appendChild(buildMarkerFragment(items));
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
