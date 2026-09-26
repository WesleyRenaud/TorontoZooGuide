import assert from 'node:assert/strict';
import test from 'node:test';

import { CenterPanHelper } from '../../../scripts/focus/centerPanHelper.js';


test('Test_SetContain_TestPanzoom_ExpectOptionsUpdated', () => {
   const calls = [];
   const panzoom = {
      options: { contain: 'inside' },
      setOptions(options) { calls.push(options); },
   };

   CenterPanHelper.setContain(panzoom, CenterPanHelper.FOCUS_CONTAIN);

   assert.equal(panzoom.options.contain, CenterPanHelper.FOCUS_CONTAIN);
   assert.deepEqual(calls, [{ contain: CenterPanHelper.FOCUS_CONTAIN }]);
});


test('Test_GetPanXY_TestXY_ExpectCoordinates', () => {
   const x = 1;
   const y = 2;
   const panzoom = { getPan: () => ({ x, y }) };

   const pan = CenterPanHelper.getPanXY(panzoom);

   assert.deepEqual(pan, { x, y });
});


test('Test_GetPanXY_TestPanXY_ExpectCoordinates', () => {
   const x = 3;
   const y = 4;
   const panzoom = { getPan: () => ({ panX: x, panY: y }) };

   const pan = CenterPanHelper.getPanXY(panzoom);

   assert.deepEqual(pan, { x, y });
});


test('Test_ClampNow_TestPanzoom_ExpectPanCalled', () => {
   const x = 5;
   const y = 6;
   const calls = [];
   const panzoom = {
      getPan: () => ({ x, y }),
      pan(...args) { calls.push(args); },
   };

   CenterPanHelper.clampNow(panzoom);

   assert.deepEqual(calls, [[x, y, { animate: false }]]);
});
