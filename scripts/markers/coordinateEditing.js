const EDIT_CURSOR = 'grab';
const DRAG_CURSOR = 'grabbing';
const COORDINATE_LOG_KEY = '__TZG_LAST_MARKER_COORDS';
const COORDINATE_LOG_LABEL = '[marker-coordinate-editor]';

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

function stopMarkerEvent(event) {
   event.preventDefault();
   event.stopPropagation();
}

function applyMarkerEditingStyles(markerEl) {
   markerEl.style.cursor = EDIT_CURSOR;
   markerEl.style.touchAction = 'none';
}

function createDragState() {
   return {
      activePointerId: null,
      didDrag: false,
   };
}

function isActivePointer(state, event) {
   return state.activePointerId === event.pointerId;
}

function getPointerPositionPercent(event, mapInner) {
   const rect = mapInner.getBoundingClientRect();

   if (!rect.width || !rect.height) {
      return null;
   }

   return {
      x: clampPercent(((event.clientX - rect.left) / rect.width) * 100),
      y: clampPercent(((event.clientY - rect.top) / rect.height) * 100),
   };
}

function applyMarkerPosition(markerEl, position) {
   markerEl.style.left = `${position.x}%`;
   markerEl.style.top = `${position.y}%`;
}

function updateMarkerPosition(markerEl, mapInner, event) {
   const position = getPointerPositionPercent(event, mapInner);

   if (!position) {
      return null;
   }

   applyMarkerPosition(markerEl, position);
   return position;
}

function buildDraggedMarkerCoordinateRows(itemsAtPoint, position) {
   const formattedX = formatCoordinate(position.x);
   const formattedY = formatCoordinate(position.y);

   return (itemsAtPoint || []).map((item) => ({
      type: String(item?.type || ''),
      name: getMarkerItemName(item),
      x_coord: formattedX,
      y_coord: formattedY,
   }));
}

function logDraggedMarkerCoordinates(itemsAtPoint, position) {
   const coordinateRows = buildDraggedMarkerCoordinateRows(
      itemsAtPoint,
      position
   );

   window[COORDINATE_LOG_KEY] = coordinateRows;

   console.log(COORDINATE_LOG_LABEL, coordinateRows);

   if (typeof console.table === 'function') {
      console.table(coordinateRows);
   }
}

function beginDragging(markerEl, state, event) {
   state.activePointerId = event.pointerId;
   state.didDrag = false;
   markerEl.style.cursor = DRAG_CURSOR;
   markerEl.setPointerCapture?.(event.pointerId);
   stopMarkerEvent(event);
}

function finishDragging({
   markerEl,
   mapInner,
   itemsAtPoint,
   state,
   event,
} = {}) {
   if (!isActivePointer(state, event)) {
      return;
   }

   const finalPosition = updateMarkerPosition(markerEl, mapInner, event);

   markerEl.releasePointerCapture?.(event.pointerId);
   markerEl.style.cursor = EDIT_CURSOR;
   state.activePointerId = null;

   if (state.didDrag && finalPosition) {
      logDraggedMarkerCoordinates(itemsAtPoint, finalPosition);
   }

   stopMarkerEvent(event);
}

export class CoordinateEditing {
   static enableMarkerCoordinateEditing(markerEl, itemsAtPoint, mapInner) {
      const state = createDragState();

      applyMarkerEditingStyles(markerEl);

      markerEl.addEventListener('pointerdown', (event) => {
         if (event.button !== 0) {
            return;
         }

         beginDragging(markerEl, state, event);
      });

      markerEl.addEventListener('pointermove', (event) => {
         if (!isActivePointer(state, event)) {
            return;
         }

         const nextPosition = updateMarkerPosition(markerEl, mapInner, event);

         if (!nextPosition) {
            return;
         }

         state.didDrag = true;
         stopMarkerEvent(event);
      });

      markerEl.addEventListener('pointerup', (event) => {
         finishDragging({
            markerEl,
            mapInner,
            itemsAtPoint,
            state,
            event,
         });
      });

      markerEl.addEventListener('pointercancel', (event) => {
         finishDragging({
            markerEl,
            mapInner,
            itemsAtPoint,
            state,
            event,
         });
      });

      markerEl.addEventListener('click', (event) => {
         stopMarkerEvent(event);
      });
   }
}
