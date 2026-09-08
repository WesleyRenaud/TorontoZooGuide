import assert from 'node:assert/strict';
import test from 'node:test';

import { ItineraryPathRenderer } from '../../../scripts/map/itineraryPathRenderer.js';

test('Test_BuildPathPolylines_TestCommands_ExpectPolylines', () => {
   const polylines = ItineraryPathRenderer.buildPathPolylines('M 0 0 L 10 0 M 20 0 L 30 0');

   assert.equal(polylines.length, 2);
   assert.deepEqual(polylines[0], [{ x: 0, y: 0 }, { x: 10, y: 0 }]);
   assert.deepEqual(polylines[1], [{ x: 20, y: 0 }, { x: 30, y: 0 }]);
});

test('Test_BuildPathPolylines_TestCurveAndEmpty_ExpectSamplesOrEmpty', () => {
   assert.deepEqual(ItineraryPathRenderer.buildPathPolylines(''), []);
   assert.deepEqual(ItineraryPathRenderer.buildPathPolylines('L 10 0'), []);

   const curved = ItineraryPathRenderer.buildPathPolylines('M 0 0 C 0 0 10 0 10 0', 5);
   assert.ok(curved.length === 1);
   assert.ok(curved[0].length >= 3);
   assert.deepEqual(curved[0].at(-1), { x: 10, y: 0 });
});

test('Test_BuildPathPolylines_TestLineBeforeMove_ExpectSkipped', () => {
   assert.deepEqual(
      ItineraryPathRenderer.buildPathPolylines('L 10 10 M 0 0 L 20 0'),
      [[{ x: 0, y: 0 }, { x: 20, y: 0 }]]
   );
});

test('Test_OffsetArrowPlacement_TestSides_ExpectOffset', () => {
   const left = ItineraryPathRenderer.offsetArrowPlacement(
      { x: 0, y: 0, angleDeg: 0 },
      10,
      'left'
   );
   const right = ItineraryPathRenderer.offsetArrowPlacement(
      { x: 0, y: 0, angleDeg: 0 },
      10,
      'right'
   );

   assert.equal(left.x, 0);
   assert.equal(left.y, 10);
   assert.equal(right.x, 0);
   assert.equal(right.y, -10);
});

test('Test_BuildPathArrowPlacements_TestLongPath_ExpectPlacements', () => {
   const placements = ItineraryPathRenderer.buildPathArrowPlacements(
      'M 0 0 L 200 0',
      {
         intervalPx: 40,
         skipEndPx: 10,
         curveSampleStepPx: 8,
         minPathLengthPx: 20,
      }
   );

   assert.ok(placements.length >= 2);
   assert.ok(placements.every((placement) => Number.isFinite(placement.angleDeg)));
});
