import { buildHoverText } from './markerHoverText.js';
import { applyMarkerVisual } from './markerVisuals.js';
import { coordKey } from '../utils/coords.js';

function clampPercent(value) {
   return Math.max(0, Math.min(100, value));
}

function formatCoordinate(value) {
   return Number(value).toFixed(3);
}

function getMarkerItemName(item) {
   return (
      item?.name
      || item?.species
      || item?.title
      || item?.location
      || item?.type
      || 'marker'
   );
}

function logDraggedMarkerCoordinates(itemsAtPoint, x, y) {
   const formattedX = formatCoordinate(x);
   const formattedY = formatCoordinate(y);

   const coordinateRows = (itemsAtPoint || []).map(item => ({
      type: String(item?.type || ''),
      name: getMarkerItemName(item),
      x_coord: formattedX,
      y_coord: formattedY,
   }));

   window.__TZG_LAST_MARKER_COORDS = coordinateRows;

   console.log('[marker-coordinate-editor]', coordinateRows);

   if (typeof console.table === 'function') {
      console.table(coordinateRows);
   }
}

function enableMarkerCoordinateEditing(markerEl, itemsAtPoint, mapInner) {
   let activePointerId = null;
   let didDrag = false;

   markerEl.style.cursor = 'grab';
   markerEl.style.touchAction = 'none';

   function updateMarkerPosition(event) {
      const rect = mapInner.getBoundingClientRect();

      if (!rect.width || !rect.height) return;

      const x = clampPercent(((event.clientX - rect.left) / rect.width) * 100);
      const y = clampPercent(((event.clientY - rect.top) / rect.height) * 100);

      markerEl.style.left = `${x}%`;
      markerEl.style.top = `${y}%`;

      return { x, y };
   }

   markerEl.addEventListener('pointerdown', event => {
      if (event.button !== 0) return;

      activePointerId = event.pointerId;
      didDrag = false;
      markerEl.style.cursor = 'grabbing';

      markerEl.setPointerCapture?.(event.pointerId);

      event.preventDefault();
      event.stopPropagation();
   });

   markerEl.addEventListener('pointermove', event => {
      if (activePointerId !== event.pointerId) return;

      const nextPosition = updateMarkerPosition(event);

      if (!nextPosition) return;

      didDrag = true;

      event.preventDefault();
      event.stopPropagation();
   });

   function finishDragging(event) {
      if (activePointerId !== event.pointerId) return;

      const finalPosition = updateMarkerPosition(event);

      markerEl.releasePointerCapture?.(event.pointerId);
      markerEl.style.cursor = 'grab';
      activePointerId = null;

      if (didDrag && finalPosition) {
         logDraggedMarkerCoordinates(itemsAtPoint, finalPosition.x, finalPosition.y);
      }

      event.preventDefault();
      event.stopPropagation();
   }

   markerEl.addEventListener('pointerup', finishDragging);
   markerEl.addEventListener('pointercancel', finishDragging);

   markerEl.addEventListener('click', event => {
      event.preventDefault();
      event.stopPropagation();
   });
}

export function createMarkerLayer({ mapInner, tooltip, hover, enableCoordinateEditing = false }) {
   const markerElsByCoord = new Map();

   function clear() {
      mapInner.querySelectorAll('.marker').forEach((m) => m.remove());
      markerElsByCoord.clear();
   }

   function render(items) {
      clear();

      const markerMap = new Map();

      (items || []).forEach((item) => {
         const x = item.x_coord ?? item.x ?? item.X ?? null;
         const y = item.y_coord ?? item.y ?? item.Y ?? null;

         if (x == null || y == null) return;

         const key = coordKey(x, y);

         if (!markerMap.has(key)) {
            markerMap.set(key, {
               x: Number(x),
               y: Number(y),
               items: [],
            });
         }

         markerMap.get(key).items.push(item);
      });

      markerMap.forEach((group) => {
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

         if (enableCoordinateEditing) {
            enableMarkerCoordinateEditing(el, itemsAtPoint, mapInner);
            return;
         }

         const type = String(itemsAtPoint[0]?.type || '');
         const clickable = type !== 'restroom';

         tooltip.attachToMarker(el, itemsAtPoint, hover, { clickable });
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
