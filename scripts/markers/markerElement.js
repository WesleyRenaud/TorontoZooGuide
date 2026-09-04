import { MarkerHoverText } from './markerHoverText.js';
import { MarkerVisuals } from './markerVisuals.js';

export class MarkerElement {
   static createMarkerElement(group) {
      const markerEl = document.createElement('div');
      markerEl.className = 'marker';
      markerEl.style.left = `${group.x}%`;
      markerEl.style.top = `${group.y}%`;
      markerEl.__items = group.items;
      markerEl.dataset.hover = MarkerHoverText.buildHoverText(group.items);
      markerEl.removeAttribute('title');

      MarkerVisuals.applyMarkerVisual(markerEl, group.items);

      return markerEl;
   }

   static bindMarkerInteractions({
      markerEl,
      group,
      mapInner,
      tooltip,
      hover,
      enableCoordinateEditing,
      enableMarkerCoordinateEditing,
   }) {
      if (enableCoordinateEditing) {
         enableMarkerCoordinateEditing(markerEl, group.items, mapInner);
         return;
      }

      tooltip.attachToMarker(markerEl, group.items, hover);
   }
}
