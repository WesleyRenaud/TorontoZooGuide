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

   const coordinateRows = (itemsAtPoint || []).map((item) => ({
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

export function enableMarkerCoordinateEditing(markerEl, itemsAtPoint, mapInner) {
   let activePointerId = null;
   let didDrag = false;

   markerEl.style.cursor = 'grab';
   markerEl.style.touchAction = 'none';

   function updateMarkerPosition(event) {
      const rect = mapInner.getBoundingClientRect();

      if (!rect.width || !rect.height) {
         return null;
      }

      const x = clampPercent(((event.clientX - rect.left) / rect.width) * 100);
      const y = clampPercent(((event.clientY - rect.top) / rect.height) * 100);

      markerEl.style.left = `${x}%`;
      markerEl.style.top = `${y}%`;

      return { x, y };
   }

   markerEl.addEventListener('pointerdown', (event) => {
      if (event.button !== 0) {
         return;
      }

      activePointerId = event.pointerId;
      didDrag = false;
      markerEl.style.cursor = 'grabbing';

      markerEl.setPointerCapture?.(event.pointerId);

      event.preventDefault();
      event.stopPropagation();
   });

   markerEl.addEventListener('pointermove', (event) => {
      if (activePointerId !== event.pointerId) {
         return;
      }

      const nextPosition = updateMarkerPosition(event);

      if (!nextPosition) {
         return;
      }

      didDrag = true;

      event.preventDefault();
      event.stopPropagation();
   });

   function finishDragging(event) {
      if (activePointerId !== event.pointerId) {
         return;
      }

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

   markerEl.addEventListener('click', (event) => {
      event.preventDefault();
      event.stopPropagation();
   });
}
