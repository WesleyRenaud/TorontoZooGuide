import assert from 'node:assert/strict';
import test from 'node:test';

import { ItineraryPathRenderer } from '../../../scripts/map/itineraryPathRenderer.js';
import { Position } from '../../../scripts/shared/enums/position.js';


test('Test_BuildPathPolylines_TestCommands_ExpectPolylines', () => {
   const firstStart = { x: 0, y: 0 };
   const firstEnd = { x: 10, y: 0 };
   const secondStart = { x: 20, y: 0 };
   const secondEnd = { x: 30, y: 0 };
   const path = `M ${firstStart.x} ${firstStart.y} L ${firstEnd.x} ${firstEnd.y} M ${secondStart.x} ${secondStart.y} L ${secondEnd.x} ${secondEnd.y}`;

   const polylines = ItineraryPathRenderer.buildPathPolylines(path);

   assert.equal(polylines.length, 2);
   assert.deepEqual(polylines.at(Position.FIRST), [firstStart, firstEnd]);
   assert.deepEqual(polylines.at(Position.SECOND), [secondStart, secondEnd]);
});


test('Test_BuildPathPolylines_TestEmpty_ExpectEmpty', () => {
   const path = '';

   const polylines = ItineraryPathRenderer.buildPathPolylines(path);

   assert.deepEqual(polylines, []);
});


test('Test_BuildPathPolylines_TestLineWithoutMove_ExpectEmpty', () => {
   const path = 'L 10 0';

   const polylines = ItineraryPathRenderer.buildPathPolylines(path);

   assert.deepEqual(polylines, []);
});


test('Test_BuildPathPolylines_TestCurve_ExpectSamples', () => {
   const end = { x: 10, y: 0 };
   const sampleStep = 5;
   const path = `M 0 0 C 0 0 ${end.x} ${end.y} ${end.x} ${end.y}`;

   const curved = ItineraryPathRenderer.buildPathPolylines(path, sampleStep);

   assert.ok(curved.length === Position.SECOND);
   assert.ok(curved.at(Position.FIRST).length >= Position.FOURTH);
   assert.deepEqual(curved.at(Position.FIRST).at(Position.LAST), end);
});


test('Test_BuildPathPolylines_TestLineBeforeMove_ExpectSkipped', () => {
   const start = { x: 0, y: 0 };
   const end = { x: 20, y: 0 };
   const path = `L 10 10 M ${start.x} ${start.y} L ${end.x} ${end.y}`;

   const polylines = ItineraryPathRenderer.buildPathPolylines(path);

   assert.deepEqual(polylines, [[start, end]]);
});


test('Test_OffsetArrowPlacement_TestLeft_ExpectOffset', () => {
   const offset = 10;
   const placement = { x: 0, y: 0, angleDeg: 0 };

   const left = ItineraryPathRenderer.offsetArrowPlacement(placement, offset, 'left');

   assert.equal(left.x, placement.x);
   assert.equal(left.y, offset);
});


test('Test_OffsetArrowPlacement_TestRight_ExpectOffset', () => {
   const offset = 10;
   const placement = { x: 0, y: 0, angleDeg: 0 };

   const right = ItineraryPathRenderer.offsetArrowPlacement(placement, offset, 'right');

   assert.equal(right.x, placement.x);
   assert.equal(right.y, -offset);
});


test('Test_BuildPathArrowPlacements_TestLongPath_ExpectPlacements', () => {
   const intervalPx = 40;
   const skipEndPx = 10;
   const curveSampleStepPx = 8;
   const minPathLengthPx = 20;

   const placements = ItineraryPathRenderer.buildPathArrowPlacements(
      'M 0 0 L 200 0',
      {
         intervalPx,
         skipEndPx,
         curveSampleStepPx,
         minPathLengthPx,
      }
   );

   assert.ok(placements.length >= 2);
   assert.ok(placements.every((placement) => Number.isFinite(placement.angleDeg)));
});
