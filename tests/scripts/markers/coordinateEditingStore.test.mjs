import assert from 'node:assert/strict';
import test from 'node:test';

import { CoordinateEditingStore } from '../../../scripts/markers/coordinateEditingStore.js';
import { ItemType } from '../../../scripts/shared/enums/itemType.js';
import { LikelihoodScale } from '../../../scripts/likelihood/likelihoodScale.js';
import { Position } from '../../../scripts/shared/enums/position.js';
import { installDomTestHooks } from '../helpers/domTestSetup.mjs';

installDomTestHooks();


test('Test_ClampPercent_TestBelowMin_ExpectZero', () => {
   const clamped = CoordinateEditingStore.clampPercent(-5);

   assert.equal(clamped, LikelihoodScale.MIN_LIKELIHOOD);
});


test('Test_ClampPercent_TestMid_ExpectSame', () => {
   const value = 50;

   const clamped = CoordinateEditingStore.clampPercent(value);

   assert.equal(clamped, value);
});


test('Test_ClampPercent_TestAboveMax_ExpectHundred', () => {
   const clamped = CoordinateEditingStore.clampPercent(150);

   assert.equal(clamped, LikelihoodScale.MAX_LIKELIHOOD);
});


test('Test_FormatCoordinate_TestNumber_ExpectThreeDecimals', () => {
   const value = 12.3456;

   const formatted = CoordinateEditingStore.formatCoordinate(value);

   assert.equal(formatted, value.toFixed(3));
});


test('Test_GetMarkerItemName_TestName_ExpectName', () => {
   const name = 'African Lion';

   const itemName = CoordinateEditingStore.getMarkerItemName({ name });

   assert.equal(itemName, name);
});


test('Test_GetMarkerItemName_TestSpecies_ExpectSpecies', () => {
   const species = 'Amur Tiger';

   const itemName = CoordinateEditingStore.getMarkerItemName({ species });

   assert.equal(itemName, species);
});


test('Test_GetMarkerItemName_TestTitle_ExpectTitle', () => {
   const title = 'Restroom';

   const itemName = CoordinateEditingStore.getMarkerItemName({ title });

   assert.equal(itemName, title);
});


test('Test_GetMarkerItemName_TestLocation_ExpectLocation', () => {
   const location = 'Africa';

   const itemName = CoordinateEditingStore.getMarkerItemName({ location });

   assert.equal(itemName, location);
});


test('Test_GetMarkerItemName_TestTypeOnly_ExpectType', () => {
   const itemName = CoordinateEditingStore.getMarkerItemName({ type: ItemType.ANIMAL });

   assert.equal(itemName, ItemType.ANIMAL);
});


test('Test_GetMarkerItemName_TestEmpty_ExpectMarker', () => {
   const itemName = CoordinateEditingStore.getMarkerItemName({});

   assert.equal(itemName, 'marker');
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
   const state = CoordinateEditingStore.createDragState();

   assert.deepEqual(state, {
      activePointerId: null,
      didDrag: false,
   });
});


test('Test_IsActivePointer_TestMatchingId_ExpectTrue', () => {
   const pointerId = 3;

   const isActive = CoordinateEditingStore.isActivePointer(
      { activePointerId: pointerId },
      { pointerId }
   );

   assert.equal(isActive, true);
});


test('Test_IsActivePointer_TestDifferentId_ExpectFalse', () => {
   const isActive = CoordinateEditingStore.isActivePointer(
      { activePointerId: 3 },
      { pointerId: 4 }
   );

   assert.equal(isActive, false);
});


test('Test_GetPointerPositionPercent_TestRect_ExpectPercents', () => {
   const mapInner = {
      getBoundingClientRect: () => ({ left: 0, top: 0, width: 100, height: 50 }),
   };
   const clientX = 25;
   const clientY = 25;

   const position = CoordinateEditingStore.getPointerPositionPercent(
      { clientX, clientY },
      mapInner
   );

   assert.deepEqual(position, { x: clientX, y: 50 });
});


test('Test_GetPointerPositionPercent_TestZeroSize_ExpectNull', () => {
   const position = CoordinateEditingStore.getPointerPositionPercent(
      { clientX: 0, clientY: 0 },
      { getBoundingClientRect: () => ({ left: 0, top: 0, width: 0, height: 0 }) }
   );

   assert.equal(position, null);
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
   const expected = { x: 50, y: 50 };

   const position = CoordinateEditingStore.updateMarkerPosition(
      markerEl,
      mapInner,
      { clientX: 100, clientY: 50 }
   );

   assert.deepEqual(position, expected);
   assert.equal(markerEl.style.left, `${expected.x}%`);
   assert.equal(markerEl.style.top, `${expected.y}%`);
});


test('Test_UpdateMarkerPosition_TestZeroSize_ExpectNull', () => {
   const markerEl = document.createElement('div');

   const position = CoordinateEditingStore.updateMarkerPosition(
      markerEl,
      { getBoundingClientRect: () => ({ left: 0, top: 0, width: 0, height: 0 }) },
      { clientX: 10, clientY: 10 }
   );

   assert.equal(position, null);
});


test('Test_BuildDraggedMarkerCoordinateRows_TestItems_ExpectFormattedRows', () => {
   const species = 'African Lion';
   const shop = 'Zootique';
   const x = 1.2;
   const y = 3.4;

   const rows = CoordinateEditingStore.buildDraggedMarkerCoordinateRows(
      [{ type: ItemType.ANIMAL, species }, { name: shop }],
      { x, y }
   );

   assert.deepEqual(rows, [
      {
         type: ItemType.ANIMAL,
         name: species,
         x_coord: CoordinateEditingStore.formatCoordinate(x),
         y_coord: CoordinateEditingStore.formatCoordinate(y),
      },
      {
         type: '',
         name: shop,
         x_coord: CoordinateEditingStore.formatCoordinate(x),
         y_coord: CoordinateEditingStore.formatCoordinate(y),
      },
   ]);
});


test('Test_LogDraggedMarkerCoordinates_TestDrag_ExpectWindowAndConsole', () => {
   const logs = [];
   const tables = [];
   const originalLog = console.log;
   const originalTable = console.table;
   const species = 'African Lion';
   const x = 10;
   const y = 20;
   console.log = (...args) => logs.push(args);
   console.table = (rows) => tables.push(rows);

   try {
      CoordinateEditingStore.logDraggedMarkerCoordinates(
         [{ type: ItemType.ANIMAL, species }],
         { x, y }
      );

      assert.deepEqual(window[CoordinateEditingStore.COORDINATE_LOG_KEY], [
         {
            type: ItemType.ANIMAL,
            name: species,
            x_coord: CoordinateEditingStore.formatCoordinate(x),
            y_coord: CoordinateEditingStore.formatCoordinate(y),
         },
      ]);
      assert.equal(logs.at(Position.FIRST).at(Position.FIRST), CoordinateEditingStore.COORDINATE_LOG_LABEL);
      assert.equal(tables.length, Position.SECOND);
   } finally {
      console.log = originalLog;
      console.table = originalTable;
   }
});


test('Test_BeginAndFinishDragging_TestLifecycle_ExpectCaptureAndLog', () => {
   const captures = [];
   const releases = [];
   const logs = [];
   const originalLog = console.log;
   const originalTable = console.table;
   const pointerId = 7;
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
      pointerId,
      preventDefault: () => {},
      stopPropagation: () => {},
   };

   try {
      CoordinateEditingStore.beginDragging(markerEl, state, beginEvent);
      state.didDrag = true;
      CoordinateEditingStore.finishDragging({
         markerEl,
         mapInner,
         itemsAtPoint: [{ type: ItemType.ANIMAL, species: 'African Lion' }],
         state,
         event: {
            pointerId,
            clientX: 40,
            clientY: 60,
            preventDefault: () => {},
            stopPropagation: () => {},
         },
      });
      CoordinateEditingStore.finishDragging({
         markerEl,
         mapInner,
         itemsAtPoint: [],
         state: { activePointerId: 1, didDrag: true },
         event: { pointerId: 2 },
      });

      assert.equal(state.activePointerId, null);
      assert.deepEqual(captures, [pointerId]);
      assert.deepEqual(releases, [pointerId]);
      assert.equal(markerEl.style.cursor, CoordinateEditingStore.EDIT_CURSOR);
      assert.equal(logs.length, Position.SECOND);
   } finally {
      console.log = originalLog;
      console.table = originalTable;
   }
});
