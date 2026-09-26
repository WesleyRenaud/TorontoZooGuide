import assert from 'node:assert/strict';
import test from 'node:test';

import { ItineraryPathArrowCalculator } from '../../../scripts/map/itineraryPathArrowCalculator.js';
import { Position } from '../../../scripts/shared/enums/position.js';

const origin = { x: 0, y: 0 };
const tenAlongX = { x: 10, y: 0 };


test('Test_CubicBezierPoint_TestMidpoint_ExpectInterpolated', () => {
   const t = 0.5;

   const point = ItineraryPathArrowCalculator.cubicBezierPoint(
      t,
      origin,
      origin,
      tenAlongX,
      tenAlongX
   );

   assert.equal(point.x, tenAlongX.x * t);
   assert.equal(point.y, origin.y);
});


test('Test_AppendCubicBezierSamples_TestChord_ExpectPolylinePoints', () => {
   const polyline = [origin];
   const minPoints = 3;

   ItineraryPathArrowCalculator.appendCubicBezierSamples(
      polyline,
      origin,
      origin,
      tenAlongX,
      tenAlongX,
      5
   );

   assert.ok(polyline.length >= minPoints);
   assert.deepEqual(polyline.at(Position.LAST), tenAlongX);
});


test('Test_PolylineLength_TestSegments_ExpectSum', () => {
   const points = [
      origin,
      { x: 3, y: 4 },
      { x: 6, y: 4 },
   ];

   const length = ItineraryPathArrowCalculator.polylineLength(points);

   assert.equal(length, 8);
});


test('Test_PointAndTangentAtDistance_TestAlongPolyline_ExpectPlacement', () => {
   const distance = 5;

   const placement = ItineraryPathArrowCalculator.pointAndTangentAtDistance(
      [origin, tenAlongX],
      distance
   );

   assert.deepEqual(placement, { x: distance, y: origin.y, angleDeg: 0 });
});


test('Test_PointAndTangentAtDistance_TestZeroLength_ExpectNull', () => {
   const placement = ItineraryPathArrowCalculator.pointAndTangentAtDistance(
      [origin, origin],
      1
   );

   assert.equal(placement, null);
});


test('Test_PointAndTangentAtDistance_TestPastEnd_ExpectNull', () => {
   const placement = ItineraryPathArrowCalculator.pointAndTangentAtDistance(
      [origin, { x: 1, y: 0 }],
      5
   );

   assert.equal(placement, null);
});


test('Test_MergeConnectedPolylines_TestEmpty_ExpectEmpty', () => {
   const merged = ItineraryPathArrowCalculator.mergeConnectedPolylines([]);

   assert.deepEqual(merged, []);
});


test('Test_MergeConnectedPolylines_TestNearAndFar_ExpectMergedOrSeparate', () => {
   const first = [origin, { x: 1, y: 0 }];
   const near = [{ x: 1.1, y: 0 }, { x: 2, y: 0 }];
   const far = [{ x: 10, y: 0 }, { x: 11, y: 0 }];

   const merged = ItineraryPathArrowCalculator.mergeConnectedPolylines([first, near, far]);

   assert.equal(merged.length, 2);
   assert.deepEqual(merged.at(Position.FIRST), [origin, first.at(Position.LAST), near.at(Position.LAST)]);
   assert.deepEqual(merged.at(Position.SECOND), far);
});


test('Test_BuildPathArrowPlacementsForPolyline_TestShort_ExpectEmpty', () => {
   const placements = ItineraryPathArrowCalculator.buildPathArrowPlacementsForPolyline(
      [origin, { x: 5, y: 0 }],
      { intervalPx: 10, skipEndPx: 1, minPathLengthPx: 20 }
   );

   assert.deepEqual(placements, []);
});


test('Test_BuildPathArrowPlacementsForPolyline_TestLong_ExpectPlacements', () => {
   const minPlacements = 2;

   const placements = ItineraryPathArrowCalculator.buildPathArrowPlacementsForPolyline(
      [origin, { x: 100, y: 0 }],
      { intervalPx: 25, skipEndPx: 10, minPathLengthPx: 20 }
   );

   assert.ok(placements.length >= minPlacements);
   assert.ok(placements.every((placement) => Number.isFinite(placement.angleDeg)));
});


test('Test_BuildPathArrowPlacementsForPolyline_TestSkipEnds_ExpectSome', () => {
   const placements = ItineraryPathArrowCalculator.buildPathArrowPlacementsForPolyline(
      [origin, { x: 100, y: 0 }],
      { intervalPx: 5, skipEndPx: 12, minPathLengthPx: 20 }
   );

   assert.ok(placements.length >= Position.SECOND);
});
