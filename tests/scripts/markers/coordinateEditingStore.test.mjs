import assert from 'node:assert/strict';
import test from 'node:test';

import { CoordinateEditingStore } from '../../../scripts/markers/coordinateEditingStore.js';
import { ItemType } from '../../../scripts/shared/enums/itemType.js';
import { installDomTestHooks } from '../helpers/domTestSetup.mjs';

installDomTestHooks();

test('Test_ClampPercent_TestOutOfRange_ExpectClamped', () => {
   assert.equal(CoordinateEditingStore.clampPercent(-5), 0);
   assert.equal(CoordinateEditingStore.clampPercent(50), 50);
   assert.equal(CoordinateEditingStore.clampPercent(150), 100);
});

test('Test_FormatCoordinate_TestNumber_ExpectThreeDecimals', () => {
   assert.equal(CoordinateEditingStore.formatCoordinate(12.3456), '12.346');
});

test('Test_GetMarkerItemName_TestFallbacks_ExpectPreferredField', () => {
   assert.equal(CoordinateEditingStore.getMarkerItemName({ name: 'Lion' }), 'Lion');
   assert.equal(CoordinateEditingStore.getMarkerItemName({ species: 'Tiger' }), 'Tiger');
   assert.equal(CoordinateEditingStore.getMarkerItemName({ title: 'Restroom' }), 'Restroom');
   assert.equal(CoordinateEditingStore.getMarkerItemName({ location: 'Africa' }), 'Africa');
   assert.equal(CoordinateEditingStore.getMarkerItemName({ type: ItemType.ANIMAL }), ItemType.ANIMAL);
   assert.equal(CoordinateEditingStore.getMarkerItemName({}), 'marker');
});

test('Test_StopMarkerEvent_TestEvent_ExpectPrevented', () => {
   const calls = [];
   CoordinateEditingStore.stopMarkerEvent({
      preventDefault: () => calls.push('prevent'),
      stopPropagation: () => calls.push('stop'),
   });
   assert.deepEqual(calls, ['prevent', 'stop']);
});

test('Test_ApplyMarkerEditingStyles_TestMarker_ExpectCursor', () => {
   const markerEl = document.createElement('div');
   CoordinateEditingStore.applyMarkerEditingStyles(markerEl);
   assert.equal(markerEl.style.cursor, CoordinateEditingStore.EDIT_CURSOR);
   assert.equal(markerEl.style.touchAction, 'none');
});

test('Test_CreateDragState_TestDefault_ExpectInactive', () => {
   assert.deepEqual(CoordinateEditingStore.createDragState(), {
      activePointerId: null,
      didDrag: false,
   });
});

test('Test_IsActivePointer_TestMatchingId_ExpectBoolean', () => {
   assert.equal(
      CoordinateEditingStore.isActivePointer({ activePointerId: 3 }, { pointerId: 3 }),
      true
   );
   assert.equal(
      CoordinateEditingStore.isActivePointer({ activePointerId: 3 }, { pointerId: 4 }),
      false
   );
});

test('Test_GetPointerPositionPercent_TestRect_ExpectPercentsOrNull', () => {
   const mapInner = {
      getBoundingClientRect: () => ({ left: 0, top: 0, width: 100, height: 50 }),
   };

   assert.deepEqual(
      CoordinateEditingStore.getPointerPositionPercent({ clientX: 25, clientY: 25 }, mapInner),
      { x: 25, y: 50 }
   );
   assert.equal(
      CoordinateEditingStore.getPointerPositionPercent(
         { clientX: 0, clientY: 0 },
         { getBoundingClientRect: () => ({ left: 0, top: 0, width: 0, height: 0 }) }
      ),
      null
   );
});

test('Test_UpdateMarkerPosition_TestFalsyPointer_ExpectNull', () => {
   const markerEl = document.createElement('div');
   const position = CoordinateEditingStore.updateMarkerPosition(
      markerEl,
      { getBoundingClientRect: () => ({ left: 0, top: 0, width: 0, height: 0 }) },
      { clientX: 0, clientY: 0 }
   );

   assert.equal(position, null);
});

test('Test_UpdateMarkerPosition_TestValidPointer_ExpectApplied', () => {
   const markerEl = document.createElement('div');
   const mapInner = {
      getBoundingClientRect: () => ({ left: 0, top: 0, width: 200, height: 100 }),
   };

   const position = CoordinateEditingStore.updateMarkerPosition(
      markerEl,
      mapInner,
      { clientX: 100, clientY: 50 }
   );

   assert.deepEqual(position, { x: 50, y: 50 });
   assert.equal(markerEl.style.left, '50%');
   assert.equal(markerEl.style.top, '50%');

   assert.equal(
      CoordinateEditingStore.updateMarkerPosition(
         markerEl,
         { getBoundingClientRect: () => ({ left: 0, top: 0, width: 0, height: 0 }) },
         { clientX: 10, clientY: 10 }
      ),
      null
   );
});

test('Test_BuildDraggedMarkerCoordinateRows_TestItems_ExpectFormattedRows', () => {
   assert.deepEqual(
      CoordinateEditingStore.buildDraggedMarkerCoordinateRows(
         [{ type: ItemType.ANIMAL, species: 'Lion' }, { name: 'Shop' }],
         { x: 1.2, y: 3.4 }
      ),
      [
         { type: ItemType.ANIMAL, name: 'Lion', x_coord: '1.200', y_coord: '3.400' },
         { type: '', name: 'Shop', x_coord: '1.200', y_coord: '3.400' },
      ]
   );
});

test('Test_LogDraggedMarkerCoordinates_TestDrag_ExpectWindowAndConsole', () => {
   const logs = [];
   const tables = [];
   const originalLog = console.log;
   const originalTable = console.table;

   console.log = (...args) => logs.push(args);
   console.table = (rows) => tables.push(rows);

   try {
      CoordinateEditingStore.logDraggedMarkerCoordinates(
         [{ type: ItemType.ANIMAL, species: 'Lion' }],
         { x: 10, y: 20 }
      );

      assert.deepEqual(window[CoordinateEditingStore.COORDINATE_LOG_KEY], [
         { type: ItemType.ANIMAL, name: 'Lion', x_coord: '10.000', y_coord: '20.000' },
      ]);
      assert.equal(logs[0][0], CoordinateEditingStore.COORDINATE_LOG_LABEL);
      assert.equal(tables.length, 1);
   } finally {
      console.log = originalLog;
      console.table = originalTable;
   }
});

test('Test_BeginAndFinishDragging_TestLifecycle_ExpectCaptureAndLog', () => {
   const captures = [];
   const releases = [];
   const stops = [];
   const logs = [];
   const originalLog = console.log;
   const originalTable = console.table;

   console.log = () => logs.push(true);
   console.table = () => {};

   const markerEl = document.createElement('div');
   markerEl.setPointerCapture = (id) => captures.push(id);
   markerEl.releasePointerCapture = (id) => releases.push(id);

   const mapInner = {
      getBoundingClientRect: () => ({ left: 0, top: 0, width: 100, height: 100 }),
   };
   const state = CoordinateEditingStore.createDragState();
   const beginEvent = {
      pointerId: 7,
      preventDefault: () => stops.push('begin-prevent'),
      stopPropagation: () => stops.push('begin-stop'),
   };

   CoordinateEditingStore.beginDragging(markerEl, state, beginEvent);
   assert.equal(state.activePointerId, 7);
   assert.equal(markerEl.style.cursor, CoordinateEditingStore.DRAG_CURSOR);
   assert.deepEqual(captures, [7]);

   state.didDrag = true;
   CoordinateEditingStore.finishDragging({
      markerEl,
      mapInner,
      itemsAtPoint: [{ type: ItemType.ANIMAL, species: 'Lion' }],
      state,
      event: {
         pointerId: 7,
         clientX: 40,
         clientY: 60,
         preventDefault: () => stops.push('finish-prevent'),
         stopPropagation: () => stops.push('finish-stop'),
      },
   });

   assert.equal(state.activePointerId, null);
   assert.deepEqual(releases, [7]);
   assert.equal(markerEl.style.cursor, CoordinateEditingStore.EDIT_CURSOR);
   assert.equal(logs.length, 1);

   CoordinateEditingStore.finishDragging({
      markerEl,
      mapInner,
      itemsAtPoint: [],
      state: { activePointerId: 1, didDrag: true },
      event: { pointerId: 2 },
   });

   console.log = originalLog;
   console.table = originalTable;
});
