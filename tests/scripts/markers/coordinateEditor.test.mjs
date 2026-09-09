import assert from 'node:assert/strict';
import test from 'node:test';

import { CoordinateEditingStore } from '../../../scripts/markers/coordinateEditingStore.js';
import { CoordinateEditor } from '../../../scripts/markers/coordinateEditor.js';
import { ItemType } from '../../../scripts/shared/enums/itemType.js';

function _createMarkerEl() {
   const listeners = {};
   return {
      listeners,
      style: {},
      addEventListener(type, handler) {
         listeners[type] = handler;
      },
   };
}

test('Test_EnableMarkerCoordinateEditing_TestPointerLifecycle_ExpectStoreCalls', () => {
   const originals = {
      createDragState: CoordinateEditingStore.createDragState,
      applyMarkerEditingStyles: CoordinateEditingStore.applyMarkerEditingStyles,
      beginDragging: CoordinateEditingStore.beginDragging,
      isActivePointer: CoordinateEditingStore.isActivePointer,
      updateMarkerPosition: CoordinateEditingStore.updateMarkerPosition,
      stopMarkerEvent: CoordinateEditingStore.stopMarkerEvent,
      finishDragging: CoordinateEditingStore.finishDragging,
   };
   const calls = {
      styles: [],
      begin: [],
      finish: [],
      stop: [],
      move: [],
   };
   const state = { activePointerId: 1, didDrag: false };

   CoordinateEditingStore.createDragState = () => state;
   CoordinateEditingStore.applyMarkerEditingStyles = (el) => { calls.styles.push(el); };
   CoordinateEditingStore.beginDragging = (...args) => { calls.begin.push(args); };
   CoordinateEditingStore.isActivePointer = () => true;
   CoordinateEditingStore.updateMarkerPosition = (...args) => {
      calls.move.push(args);
      return { x: 10, y: 20 };
   };
   CoordinateEditingStore.stopMarkerEvent = (event) => { calls.stop.push(event); };
   CoordinateEditingStore.finishDragging = (args) => { calls.finish.push(args); };

   try {
      const markerEl = _createMarkerEl();
      const itemsAtPoint = [{ type: ItemType.ANIMAL }];
      const mapInner = { id: 'map' };

      CoordinateEditor.enableMarkerCoordinateEditing(markerEl, itemsAtPoint, mapInner);

      assert.equal(calls.styles.length, 1);

      markerEl.listeners.pointerdown({ button: 1, pointerId: 1 });
      assert.equal(calls.begin.length, 0);

      markerEl.listeners.pointerdown({ button: 0, pointerId: 1 });
      assert.equal(calls.begin.length, 1);

      markerEl.listeners.pointermove({ pointerId: 1 });
      assert.equal(state.didDrag, true);
      assert.equal(calls.stop.length, 1);

      markerEl.listeners.pointerup({ pointerId: 1 });
      markerEl.listeners.pointercancel({ pointerId: 1 });
      assert.equal(calls.finish.length, 2);
      assert.equal(calls.finish[0].itemsAtPoint, itemsAtPoint);

      markerEl.listeners.click({ type: 'click' });
      assert.equal(calls.stop.length, 2);
   } finally {
      Object.assign(CoordinateEditingStore, originals);
   }
});

test('Test_EnableMarkerCoordinateEditing_TestInactiveOrMissingPosition_ExpectEarlyReturn', () => {
   const originals = {
      createDragState: CoordinateEditingStore.createDragState,
      applyMarkerEditingStyles: CoordinateEditingStore.applyMarkerEditingStyles,
      isActivePointer: CoordinateEditingStore.isActivePointer,
      updateMarkerPosition: CoordinateEditingStore.updateMarkerPosition,
      stopMarkerEvent: CoordinateEditingStore.stopMarkerEvent,
      beginDragging: CoordinateEditingStore.beginDragging,
      finishDragging: CoordinateEditingStore.finishDragging,
   };
   let stopCalls = 0;

   CoordinateEditingStore.createDragState = () => ({ activePointerId: null, didDrag: false });
   CoordinateEditingStore.applyMarkerEditingStyles = () => {};
   CoordinateEditingStore.beginDragging = () => {};
   CoordinateEditingStore.finishDragging = () => {};
   CoordinateEditingStore.stopMarkerEvent = () => { stopCalls += 1; };
   CoordinateEditingStore.isActivePointer = () => false;
   CoordinateEditingStore.updateMarkerPosition = () => ({ x: 1, y: 2 });

   try {
      const markerEl = _createMarkerEl();
      CoordinateEditor.enableMarkerCoordinateEditing(markerEl, [], {});
      markerEl.listeners.pointermove({ pointerId: 9 });
      assert.equal(stopCalls, 0);

      CoordinateEditingStore.isActivePointer = () => true;
      CoordinateEditingStore.updateMarkerPosition = () => null;
      markerEl.listeners.pointermove({ pointerId: 9 });
      assert.equal(stopCalls, 0);
   } finally {
      Object.assign(CoordinateEditingStore, originals);
   }
});
