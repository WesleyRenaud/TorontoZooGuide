import assert from 'node:assert/strict';
import test from 'node:test';

import { FocusTargetFinderHelper } from '../../../scripts/focus/focusTargetFinderHelper.js';

test('Test_ItemLikelihood_TestValues_ExpectNumberOrMinusOne', () => {
   assert.equal(FocusTargetFinderHelper.itemLikelihood({ likelihood: 75 }), 75);
   assert.equal(FocusTargetFinderHelper.itemLikelihood({ likelihood: 'bad' }), -1);
});

test('Test_DistToViewportCenter_TestRects_ExpectDistance', () => {
   const markerEl = {
      getBoundingClientRect: () => ({ left: 0, top: 0, width: 10, height: 10 }),
   };
   const viewportEl = {
      getBoundingClientRect: () => ({ left: 0, top: 0, width: 100, height: 100 }),
   };

   assert.equal(
      FocusTargetFinderHelper.distToViewportCenter(markerEl, viewportEl),
      Math.hypot(5 - 50, 5 - 50)
   );
});
