export class CoordinateEditingStore {
   static EDIT_CURSOR = 'grab';

   static DRAG_CURSOR = 'grabbing';

   static COORDINATE_LOG_KEY = '__TZG_LAST_MARKER_COORDS';

   static COORDINATE_LOG_LABEL = '[marker-coordinate-editor]';

   static clampPercent(value) {
      return Math.max(0, Math.min(100, value));
   }

   static formatCoordinate(value) {
      return Number(value).toFixed(3);
   }

   static getMarkerItemName(item) {
      return (
         item?.name
         || item?.species
         || item?.title
         || item?.location
         || item?.type
         || 'marker'
      );
   }

   static stopMarkerEvent(event) {
      event.preventDefault();
      event.stopPropagation();
   }

   static applyMarkerEditingStyles(markerEl) {
      markerEl.style.cursor = CoordinateEditingStore.EDIT_CURSOR;
      markerEl.style.touchAction = 'none';
   }

   static createDragState() {
      return {
         activePointerId: null,
         didDrag: false,
      };
   }

   static isActivePointer(state, event) {
      return state.activePointerId === event.pointerId;
   }

   static getPointerPositionPercent(event, mapInner) {
      const rect = mapInner.getBoundingClientRect();

      if (!rect.width || !rect.height) {
         return null;
      }

      return {
         x: CoordinateEditingStore.clampPercent(((event.clientX - rect.left) / rect.width) * 100),
         y: CoordinateEditingStore.clampPercent(((event.clientY - rect.top) / rect.height) * 100),
      };
   }

   static applyMarkerPosition(markerEl, position) {
      markerEl.style.left = `${position.x}%`;
      markerEl.style.top = `${position.y}%`;
   }

   static updateMarkerPosition(markerEl, mapInner, event) {
      const position = CoordinateEditingStore.getPointerPositionPercent(event, mapInner);

      if (!position) {
         return null;
      }

      CoordinateEditingStore.applyMarkerPosition(markerEl, position);
      return position;
   }

   static buildDraggedMarkerCoordinateRows(itemsAtPoint, position) {
      const formattedX = CoordinateEditingStore.formatCoordinate(position.x);
      const formattedY = CoordinateEditingStore.formatCoordinate(position.y);

      return (itemsAtPoint || []).map((item) => ({
         type: String(item?.type || ''),
         name: CoordinateEditingStore.getMarkerItemName(item),
         x_coord: formattedX,
         y_coord: formattedY,
      }));
   }

   static logDraggedMarkerCoordinates(itemsAtPoint, position) {
      const coordinateRows = CoordinateEditingStore.buildDraggedMarkerCoordinateRows(
         itemsAtPoint,
         position
      );

      window[CoordinateEditingStore.COORDINATE_LOG_KEY] = coordinateRows;

      console.log(CoordinateEditingStore.COORDINATE_LOG_LABEL, coordinateRows);

      if (typeof console.table === 'function') {
         console.table(coordinateRows);
      }
   }

   static beginDragging(markerEl, state, event) {
      state.activePointerId = event.pointerId;
      state.didDrag = false;
      markerEl.style.cursor = CoordinateEditingStore.DRAG_CURSOR;
      markerEl.setPointerCapture?.(event.pointerId);
      CoordinateEditingStore.stopMarkerEvent(event);
   }

   static finishDragging({
      markerEl,
      mapInner,
      itemsAtPoint,
      state,
      event,
   } = {}) {
      if (!CoordinateEditingStore.isActivePointer(state, event)) {
         return;
      }

      const finalPosition = CoordinateEditingStore.updateMarkerPosition(markerEl, mapInner, event);

      markerEl.releasePointerCapture?.(event.pointerId);
      markerEl.style.cursor = CoordinateEditingStore.EDIT_CURSOR;
      state.activePointerId = null;

      if (state.didDrag && finalPosition) {
         CoordinateEditingStore.logDraggedMarkerCoordinates(itemsAtPoint, finalPosition);
      }

      CoordinateEditingStore.stopMarkerEvent(event);
   }
}
