import assert from 'node:assert/strict';
import test from 'node:test';

import { FocusAnimator } from '../../../scripts/focus/focusAnimator.js';
import { MapCenterHelper } from '../../../scripts/focus/mapCenterHelper.js';
import { Position } from '../../../scripts/shared/enums/position.js';
import { installDomTestHooks } from '../helpers/domTestSetup.mjs';

installDomTestHooks();


test('Test_FocusMarker_TestMissingArgs_ExpectNoOp', () => {
   const options = {};

   const focus = () => FocusAnimator.focusMarker(options);

   assert.doesNotThrow(focus);
});


test('Test_FocusMarker_TestMarker_ExpectZoomCenterAndTooltip', () => {
   const zooms = [];
   const centers = [];
   const opens = [];
   const jumps = [];
   const originalCenter = MapCenterHelper.centerMarkerWithContain;
   MapCenterHelper.centerMarkerWithContain = (...args) => { centers.push(args); };

   try {
      FocusAnimator.focusMarker({
         panzoom: {
            zoom: (...args) => { zooms.push(args); },
         },
         marker: { id: 'm1', __items: [{ type: 'animal' }] },
         viewportEl: { id: 'viewport' },
         tooltip: {
            open: (...args) => { opens.push(args); },
            jumpTo: (matchFn) => { jumps.push(matchFn); },
         },
         matchFn: () => true,
      });

      assert.deepEqual(zooms, [[FocusAnimator.FOCUS_ZOOM_LEVEL, { animate: false }]]);
      assert.equal(centers.length, 2);
      assert.equal(opens.length, Position.SECOND);
      assert.equal(jumps.length, Position.SECOND);
   } finally {
      MapCenterHelper.centerMarkerWithContain = originalCenter;
   }
});
