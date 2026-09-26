import assert from 'node:assert/strict';
import test from 'node:test';

import { FocusTargetFinderHelper } from '../../../scripts/focus/focusTargetFinderHelper.js';
import { Position } from '../../../scripts/shared/enums/position.js';


test('Test_ItemLikelihood_TestNumber_ExpectNumber', () => {
   const likelihood = 75;

   const value = FocusTargetFinderHelper.itemLikelihood({ likelihood });

   assert.equal(value, likelihood);
});


test('Test_ItemLikelihood_TestNonNumeric_ExpectLast', () => {
   const likelihood = 'bad';

   const value = FocusTargetFinderHelper.itemLikelihood({ likelihood });

   assert.equal(value, Position.LAST);
});


test('Test_DistToViewportCenter_TestRects_ExpectDistance', () => {
   const markerSize = 10;
   const viewportSize = 100;
   const markerEl = {
      getBoundingClientRect: () => ({
         left: 0,
         top: 0,
         width: markerSize,
         height: markerSize,
      }),
   };
   const viewportEl = {
      getBoundingClientRect: () => ({
         left: 0,
         top: 0,
         width: viewportSize,
         height: viewportSize,
      }),
   };

   const distance = FocusTargetFinderHelper.distToViewportCenter(markerEl, viewportEl);

   assert.equal(
      distance,
      Math.hypot((markerSize / 2) - (viewportSize / 2), (markerSize / 2) - (viewportSize / 2))
   );
});
