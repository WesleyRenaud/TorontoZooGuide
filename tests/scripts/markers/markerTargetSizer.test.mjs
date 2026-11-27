import assert from 'node:assert/strict';
import test from 'node:test';

import { MarkerTargetSizer } from '../../../scripts/markers/markerTargetSizer.js';
import { installDomTestHooks } from '../helpers/domTestSetup.mjs';

installDomTestHooks();


test('Test_ReadCenter_TestOffsets_ExpectLeftAndTop', () => {
   const markerEl = { offsetLeft: 30, offsetTop: 40 };

   const center = MarkerTargetSizer.readCenter(markerEl);

   assert.deepEqual(center, { x: 30, y: 40 });
});


test('Test_ReadCenter_TestMissingOffsets_ExpectZero', () => {
   const markerEl = {};

   const center = MarkerTargetSizer.readCenter(markerEl);

   assert.deepEqual(center, { x: 0, y: 0 });
});


test('Test_FindNearestDistance_TestThreePins_ExpectClosestOther', () => {
   const centers = [{ x: 0, y: 0 }, { x: 3, y: 4 }, { x: 100, y: 0 }];

   const nearest = MarkerTargetSizer.findNearestDistance(centers, 0);

   assert.equal(nearest, 5);
});


test('Test_FindNearestDistance_TestSinglePin_ExpectInfinity', () => {
   const centers = [{ x: 10, y: 10 }];

   const nearest = MarkerTargetSizer.findNearestDistance(centers, 0);

   assert.equal(nearest, Infinity);
});


test('Test_ComputeTargetSizes_TestIsolatedPin_ExpectMinimumTarget', () => {
   const centers = [{ x: 0, y: 0 }, { x: 200, y: 0 }];

   const sizes = MarkerTargetSizer.computeTargetSizes(centers);

   assert.deepEqual(sizes, [MarkerTargetSizer.WCAG_MIN_TARGET_PX, MarkerTargetSizer.WCAG_MIN_TARGET_PX]);
});


test('Test_ComputeTargetSizes_TestSinglePin_ExpectMinimumTarget', () => {
   const centers = [{ x: 5, y: 5 }];

   const sizes = MarkerTargetSizer.computeTargetSizes(centers);

   assert.deepEqual(sizes, [MarkerTargetSizer.WCAG_MIN_TARGET_PX]);
});


test('Test_ComputeTargetSizes_TestCrowdedPins_ExpectCappedAtNeighbourDistance', () => {
   const centers = [{ x: 0, y: 0 }, { x: 10, y: 0 }, { x: 100, y: 0 }];

   const sizes = MarkerTargetSizer.computeTargetSizes(centers);

   assert.deepEqual(sizes, [10, 10, MarkerTargetSizer.WCAG_MIN_TARGET_PX]);
});


test('Test_ComputeTargetSizes_TestAnyPair_ExpectHitAreasNeverOverlap', () => {
   const centers = [{ x: 0, y: 0 }, { x: 14, y: 0 }, { x: 20, y: 5 }, { x: 60, y: 60 }];

   const sizes = MarkerTargetSizer.computeTargetSizes(centers);

   centers.forEach((first, firstIndex) => {
      centers.forEach((second, secondIndex) => {
         if (firstIndex >= secondIndex) {
            return;
         }

         const distance = Math.hypot(first.x - second.x, first.y - second.y);
         const reach = (sizes[firstIndex] + sizes[secondIndex]) / 2;

         assert.ok(reach <= distance);
      });
   });
});


test('Test_ComputeTargetSizes_TestCustomMinimum_ExpectThatCap', () => {
   const centers = [{ x: 0, y: 0 }, { x: 200, y: 0 }];
   const minTargetPx = 44;

   const sizes = MarkerTargetSizer.computeTargetSizes(centers, minTargetPx);

   assert.deepEqual(sizes, [minTargetPx, minTargetPx]);
});


test('Test_ApplyToMarkers_TestTwoMarkers_ExpectSizeProperties', () => {
   const first = document.createElement('div');
   const second = document.createElement('div');
   first.offsetLeft = 0;
   first.offsetTop = 0;
   second.offsetLeft = 9;
   second.offsetTop = 0;

   MarkerTargetSizer.applyToMarkers([first, second]);

   assert.equal(first.style.getPropertyValue(MarkerTargetSizer.TARGET_SIZE_PROPERTY), '9px');
   assert.equal(second.style.getPropertyValue(MarkerTargetSizer.TARGET_SIZE_PROPERTY), '9px');
});
