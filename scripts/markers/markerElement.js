import { MarkerHoverText } from './markerHoverText.js';
import { applyMarkerVisual } from './markerVisuals.js';

export function createMarkerElement(group) {
   const markerEl = document.createElement('div');
   markerEl.className = 'marker';
   markerEl.style.left = `${group.x}%`;
   markerEl.style.top = `${group.y}%`;
   markerEl.__items = group.items;
   markerEl.dataset.hover = MarkerHoverText.buildHoverText(group.items);
   markerEl.removeAttribute('title');

   applyMarkerVisual(markerEl, group.items);

   return markerEl;
}

export function bindMarkerInteractions({
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
