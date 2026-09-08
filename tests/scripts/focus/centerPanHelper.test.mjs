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
   assert.equal(panzoom.options.contain, 'none');
   assert.deepEqual(calls, [{ contain: 'none' }]);
});

test('Test_GetPanXY_TestShapes_ExpectCoordinates', () => {
   assert.deepEqual(
      CenterPanHelper.getPanXY({ getPan: () => ({ x: 1, y: 2 }) }),
      { x: 1, y: 2 }
   );
   assert.deepEqual(
      CenterPanHelper.getPanXY({ getPan: () => ({ panX: 3, panY: 4 }) }),
      { x: 3, y: 4 }
   );
});

test('Test_ClampNow_TestPanzoom_ExpectPanCalled', () => {
   const calls = [];
   const panzoom = {
      getPan: () => ({ x: 5, y: 6 }),
      pan(...args) { calls.push(args); },
   };
   CenterPanHelper.clampNow(panzoom);
   assert.deepEqual(calls, [[5, 6, { animate: false }]]);
});
