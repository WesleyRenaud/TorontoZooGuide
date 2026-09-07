const EDIT_CURSOR = 'grab';
const DRAG_CURSOR = 'grabbing';
const COORDINATE_LOG_KEY = '__TZG_LAST_MARKER_COORDS';
const COORDINATE_LOG_LABEL = '[marker-coordinate-editor]';

export class CoordinateEditingSession {
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
      markerEl.style.cursor = EDIT_CURSOR;
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
         x: CoordinateEditingSession.clampPercent(((event.clientX - rect.left) / rect.width) * 100),
         y: CoordinateEditingSession.clampPercent(((event.clientY - rect.top) / rect.height) * 100),
      };
   }

   static applyMarkerPosition(markerEl, position) {
      markerEl.style.left = `${position.x}%`;
      markerEl.style.top = `${position.y}%`;
   }

   static updateMarkerPosition(markerEl, mapInner, event) {
      const position = CoordinateEditingSession.getPointerPositionPercent(event, mapInner);

      if (!position) {
         return null;
      }

      CoordinateEditingSession.applyMarkerPosition(markerEl, position);
      return position;
   }

   static buildDraggedMarkerCoordinateRows(itemsAtPoint, position) {
      const formattedX = CoordinateEditingSession.formatCoordinate(position.x);
      const formattedY = CoordinateEditingSession.formatCoordinate(position.y);

      return (itemsAtPoint || []).map((item) => ({
         type: String(item?.type || ''),
         name: CoordinateEditingSession.getMarkerItemName(item),
         x_coord: formattedX,
         y_coord: formattedY,
      }));
   }

   static logDraggedMarkerCoordinates(itemsAtPoint, position) {
      const coordinateRows = CoordinateEditingSession.buildDraggedMarkerCoordinateRows(
         itemsAtPoint,
         position
      );

      window[COORDINATE_LOG_KEY] = coordinateRows;

      console.log(COORDINATE_LOG_LABEL, coordinateRows);

      if (typeof console.table === 'function') {
         console.table(coordinateRows);
      }
   }

   static beginDragging(markerEl, state, event) {
      state.activePointerId = event.pointerId;
      state.didDrag = false;
      markerEl.style.cursor = DRAG_CURSOR;
      markerEl.setPointerCapture?.(event.pointerId);
      CoordinateEditingSession.stopMarkerEvent(event);
   }

   static finishDragging({
      markerEl,
      mapInner,
      itemsAtPoint,
      state,
      event,
   } = {}) {
      if (!CoordinateEditingSession.isActivePointer(state, event)) {
         return;
      }

      const finalPosition = CoordinateEditingSession.updateMarkerPosition(markerEl, mapInner, event);

      markerEl.releasePointerCapture?.(event.pointerId);
      markerEl.style.cursor = EDIT_CURSOR;
      state.activePointerId = null;

      if (state.didDrag && finalPosition) {
         CoordinateEditingSession.logDraggedMarkerCoordinates(itemsAtPoint, finalPosition);
      }

      CoordinateEditingSession.stopMarkerEvent(event);
   }
}
