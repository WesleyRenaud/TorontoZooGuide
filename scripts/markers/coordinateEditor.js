import { CoordinateEditingStore } from './coordinateEditingStore.js';

export class CoordinateEditor {
   static enableMarkerCoordinateEditing(markerEl, itemsAtPoint, mapInner) {
      const state = CoordinateEditingStore.createDragState();

      CoordinateEditingStore.applyMarkerEditingStyles(markerEl);

      markerEl.addEventListener('pointerdown', (event) => {
         if (event.button !== 0) {
            return;
         }

         CoordinateEditingStore.beginDragging(markerEl, state, event);
      });

      markerEl.addEventListener('pointermove', (event) => {
         if (!CoordinateEditingStore.isActivePointer(state, event)) {
            return;
         }

         const nextPosition = CoordinateEditingStore.updateMarkerPosition(markerEl, mapInner, event);

         if (!nextPosition) {
            return;
         }

         state.didDrag = true;
         CoordinateEditingStore.stopMarkerEvent(event);
      });

      markerEl.addEventListener('pointerup', (event) => {
         CoordinateEditingStore.finishDragging({
            markerEl,
            mapInner,
            itemsAtPoint,
            state,
            event,
         });
      });

      markerEl.addEventListener('pointercancel', (event) => {
         CoordinateEditingStore.finishDragging({
            markerEl,
            mapInner,
            itemsAtPoint,
            state,
            event,
         });
      });

      markerEl.addEventListener('click', (event) => {
         CoordinateEditingStore.stopMarkerEvent(event);
      });
   }
}
