import assert from 'node:assert/strict';
import test from 'node:test';

import { CoordinateEditingStore } from '../../../scripts/markers/coordinateEditingStore.js';
import { CoordinateEditor } from '../../../scripts/markers/coordinateEditor.js';
import { ItemType } from '../../../scripts/shared/enums/itemType.js';
import { Position } from '../../../scripts/shared/enums/position.js';


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


function _storeOriginals() {
   return {
      createDragState: CoordinateEditingStore.createDragState,
      applyMarkerEditingStyles: CoordinateEditingStore.applyMarkerEditingStyles,
      beginDragging: CoordinateEditingStore.beginDragging,
      isActivePointer: CoordinateEditingStore.isActivePointer,
      updateMarkerPosition: CoordinateEditingStore.updateMarkerPosition,
      stopMarkerEvent: CoordinateEditingStore.stopMarkerEvent,
      finishDragging: CoordinateEditingStore.finishDragging,
   };
}


test('Test_EnableMarkerCoordinateEditing_TestStyles_ExpectApplied', () => {
   const originals = _storeOriginals();
   const styles = [];
   const state = { activePointerId: 1, didDrag: false };

   CoordinateEditingStore.createDragState = () => state;
   CoordinateEditingStore.applyMarkerEditingStyles = (el) => {
      styles.push(el);
   };

   try {
      const markerEl = _createMarkerEl();

      CoordinateEditor.enableMarkerCoordinateEditing(markerEl, [{ type: ItemType.ANIMAL }], { id: 'map' });

      assert.deepEqual(styles, [markerEl]);
   } finally {
      Object.assign(CoordinateEditingStore, originals);
   }
});


test('Test_EnableMarkerCoordinateEditing_TestNonPrimaryPointer_ExpectNoBegin', () => {
   const originals = _storeOriginals();
   const begins = [];
   const state = { activePointerId: 1, didDrag: false };

   CoordinateEditingStore.createDragState = () => state;
   CoordinateEditingStore.applyMarkerEditingStyles = () => {};
   CoordinateEditingStore.beginDragging = (...args) => {
      begins.push(args);
   };

   try {
      const markerEl = _createMarkerEl();
      CoordinateEditor.enableMarkerCoordinateEditing(markerEl, [{ type: ItemType.ANIMAL }], { id: 'map' });

      markerEl.listeners.pointerdown({ button: 1, pointerId: 1 });

      assert.equal(begins.length, Position.FIRST);
   } finally {
      Object.assign(CoordinateEditingStore, originals);
   }
});


test('Test_EnableMarkerCoordinateEditing_TestPrimaryPointer_ExpectBegin', () => {
   const originals = _storeOriginals();
   const begins = [];
   const state = { activePointerId: 1, didDrag: false };

   CoordinateEditingStore.createDragState = () => state;
   CoordinateEditingStore.applyMarkerEditingStyles = () => {};
   CoordinateEditingStore.beginDragging = (...args) => {
      begins.push(args);
   };

   try {
      const markerEl = _createMarkerEl();
      CoordinateEditor.enableMarkerCoordinateEditing(markerEl, [{ type: ItemType.ANIMAL }], { id: 'map' });

      markerEl.listeners.pointerdown({ button: 0, pointerId: 1 });

      assert.equal(begins.length, Position.SECOND);
   } finally {
      Object.assign(CoordinateEditingStore, originals);
   }
});


test('Test_EnableMarkerCoordinateEditing_TestMove_ExpectDragged', () => {
   const originals = _storeOriginals();
   const stops = [];
   const state = { activePointerId: 1, didDrag: false };

   CoordinateEditingStore.createDragState = () => state;
   CoordinateEditingStore.applyMarkerEditingStyles = () => {};
   CoordinateEditingStore.beginDragging = () => {};
   CoordinateEditingStore.isActivePointer = () => true;
   CoordinateEditingStore.updateMarkerPosition = () => ({ x: 10, y: 20 });
   CoordinateEditingStore.stopMarkerEvent = (event) => {
      stops.push(event);
   };

   try {
      const markerEl = _createMarkerEl();
      CoordinateEditor.enableMarkerCoordinateEditing(markerEl, [{ type: ItemType.ANIMAL }], { id: 'map' });
      markerEl.listeners.pointermove({ pointerId: 1 });

      assert.equal(state.didDrag, true);
      assert.equal(stops.length, Position.SECOND);
   } finally {
      Object.assign(CoordinateEditingStore, originals);
   }
});


test('Test_EnableMarkerCoordinateEditing_TestUpAndCancel_ExpectFinish', () => {
   const originals = _storeOriginals();
   const finishes = [];
   const itemsAtPoint = [{ type: ItemType.ANIMAL }];
   const state = { activePointerId: 1, didDrag: false };

   CoordinateEditingStore.createDragState = () => state;
   CoordinateEditingStore.applyMarkerEditingStyles = () => {};
   CoordinateEditingStore.finishDragging = (args) => {
      finishes.push(args);
   };

   try {
      const markerEl = _createMarkerEl();
      CoordinateEditor.enableMarkerCoordinateEditing(markerEl, itemsAtPoint, { id: 'map' });
      markerEl.listeners.pointerup({ pointerId: 1 });
      markerEl.listeners.pointercancel({ pointerId: 1 });

      assert.equal(finishes.length, 2);
      assert.equal(finishes.at(Position.FIRST).itemsAtPoint, itemsAtPoint);
   } finally {
      Object.assign(CoordinateEditingStore, originals);
   }
});


test('Test_EnableMarkerCoordinateEditing_TestClickAfterDrag_ExpectStopped', () => {
   const originals = _storeOriginals();
   const stops = [];
   const state = { activePointerId: 1, didDrag: true };

   CoordinateEditingStore.createDragState = () => state;
   CoordinateEditingStore.applyMarkerEditingStyles = () => {};
   CoordinateEditingStore.stopMarkerEvent = (event) => {
      stops.push(event);
   };

   try {
      const markerEl = _createMarkerEl();
      CoordinateEditor.enableMarkerCoordinateEditing(markerEl, [{ type: ItemType.ANIMAL }], { id: 'map' });
      markerEl.listeners.click({ type: 'click' });

      assert.equal(stops.length, Position.SECOND);
   } finally {
      Object.assign(CoordinateEditingStore, originals);
   }
});


test('Test_EnableMarkerCoordinateEditing_TestInactivePointer_ExpectNoStop', () => {
   const originals = _storeOriginals();
   let stopCalls = 0;

   CoordinateEditingStore.createDragState = () => ({ activePointerId: null, didDrag: false });
   CoordinateEditingStore.applyMarkerEditingStyles = () => {};
   CoordinateEditingStore.beginDragging = () => {};
   CoordinateEditingStore.finishDragging = () => {};
   CoordinateEditingStore.stopMarkerEvent = () => {
      stopCalls += 1;
   };
   CoordinateEditingStore.isActivePointer = () => false;
   CoordinateEditingStore.updateMarkerPosition = () => ({ x: 1, y: 2 });

   try {
      const markerEl = _createMarkerEl();
      CoordinateEditor.enableMarkerCoordinateEditing(markerEl, [], {});
      markerEl.listeners.pointermove({ pointerId: 9 });

      assert.equal(stopCalls, Position.FIRST);
   } finally {
      Object.assign(CoordinateEditingStore, originals);
   }
});


test('Test_EnableMarkerCoordinateEditing_TestMissingPosition_ExpectNoStop', () => {
   const originals = _storeOriginals();
   let stopCalls = 0;

   CoordinateEditingStore.createDragState = () => ({ activePointerId: null, didDrag: false });
   CoordinateEditingStore.applyMarkerEditingStyles = () => {};
   CoordinateEditingStore.stopMarkerEvent = () => {
      stopCalls += 1;
   };
   CoordinateEditingStore.isActivePointer = () => true;
   CoordinateEditingStore.updateMarkerPosition = () => null;

   try {
      const markerEl = _createMarkerEl();
      CoordinateEditor.enableMarkerCoordinateEditing(markerEl, [], {});
      markerEl.listeners.pointermove({ pointerId: 9 });

      assert.equal(stopCalls, Position.FIRST);
   } finally {
      Object.assign(CoordinateEditingStore, originals);
   }
});
