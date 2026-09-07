import { CoordinateEditingSession } from './coordinateEditingSession.js';

export class CoordinateEditing {
   static enableMarkerCoordinateEditing(markerEl, itemsAtPoint, mapInner) {
      const state = CoordinateEditingSession.createDragState();

      CoordinateEditingSession.applyMarkerEditingStyles(markerEl);

      markerEl.addEventListener('pointerdown', (event) => {
         if (event.button !== 0) {
            return;
         }

         CoordinateEditingSession.beginDragging(markerEl, state, event);
      });

      markerEl.addEventListener('pointermove', (event) => {
         if (!CoordinateEditingSession.isActivePointer(state, event)) {
            return;
         }

         const nextPosition = CoordinateEditingSession.updateMarkerPosition(markerEl, mapInner, event);

         if (!nextPosition) {
            return;
         }

         state.didDrag = true;
         CoordinateEditingSession.stopMarkerEvent(event);
      });

      markerEl.addEventListener('pointerup', (event) => {
         CoordinateEditingSession.finishDragging({
            markerEl,
            mapInner,
            itemsAtPoint,
            state,
            event,
         });
      });

      markerEl.addEventListener('pointercancel', (event) => {
         CoordinateEditingSession.finishDragging({
            markerEl,
            mapInner,
            itemsAtPoint,
            state,
            event,
         });
      });

      markerEl.addEventListener('click', (event) => {
         CoordinateEditingSession.stopMarkerEvent(event);
      });
   }
}
