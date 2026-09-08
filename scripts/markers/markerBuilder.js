import { MarkerHelper } from './markerHelper.js';
import { MarkerHoverFormatter } from './markerHoverFormatter.js';

export class MarkerBuilder {
   static createMarkerElement(group) {
      const markerEl = document.createElement('div');
      markerEl.className = 'marker';
      markerEl.style.left = `${group.x}%`;
      markerEl.style.top = `${group.y}%`;
      markerEl.__items = group.items;
      markerEl.dataset.hover = MarkerHoverFormatter.buildHoverText(group.items);
      markerEl.removeAttribute('title');

      MarkerHelper.applyMarkerVisual(markerEl, group.items);

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
