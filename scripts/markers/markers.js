import { buildHoverText } from './markerHoverText.js';
import { applyMarkerVisual } from './markerVisuals.js';
import { coordKey } from '../utils/coords.js';

export function createMarkerLayer({ mapInner, tooltip, hover }) {
   const markerElsByCoord = new Map();

   function clear() {
      mapInner.querySelectorAll('.marker').forEach(m => m.remove());
      markerElsByCoord.clear();
   }

   function render(items) {
      clear();

      const markerMap = new Map();

      (items || []).forEach(item => {
         const x = item.x_coord ?? item.x ?? item.X ?? null;
         const y = item.y_coord ?? item.y ?? item.Y ?? null;
         if (x == null || y == null) return;

         const key = coordKey(x, y);
         if (!markerMap.has(key)) markerMap.set(key, { x: Number(x), y: Number(y), items: [] });
         markerMap.get(key).items.push(item);
      });

      markerMap.forEach(group => {
         const itemsAtPoint = group.items;
         if (!itemsAtPoint.length) return;

         const el = document.createElement('div');
         el.className = 'marker';
         el.style.left = `${group.x}%`;
         el.style.top = `${group.y}%`;

         el.__items = itemsAtPoint;

         el.dataset.hover = buildHoverText(itemsAtPoint);
         el.removeAttribute('title');

         const key = coordKey(group.x, group.y);
         if (!key) return;
         markerElsByCoord.set(key, el);

         applyMarkerVisual(el, itemsAtPoint);

         mapInner.appendChild(el);

         // ✅ IMPORTANT: determine type from THIS marker's items
         const type = String(itemsAtPoint[0]?.type || '');
         const clickable = type !== 'restroom' && type !== 'wildEncounterMeetingSpot';

         // ✅ IMPORTANT: attach with THIS marker's items
         tooltip.attachToMarker(el, itemsAtPoint, hover, { clickable });
      });
   }

   function getMarkerByCoord(key) {
      const found = markerElsByCoord.get(key) || null;
      return found;
   }

   function getAllMarkers() {
      return Array.from(markerElsByCoord.values());
   }

   return { render, getMarkerByCoord, getAllMarkers };
}