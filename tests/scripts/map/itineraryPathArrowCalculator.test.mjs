import assert from 'node:assert/strict';
import test from 'node:test';

import { ItineraryPathArrowCalculator } from '../../../scripts/map/itineraryPathArrowCalculator.js';

test('Test_CubicBezierPoint_TestMidpoint_ExpectInterpolated', () => {
   const point = ItineraryPathArrowCalculator.cubicBezierPoint(
      0.5,
      { x: 0, y: 0 },
      { x: 0, y: 0 },
      { x: 10, y: 0 },
      { x: 10, y: 0 }
   );

   assert.equal(point.x, 5);
   assert.equal(point.y, 0);
});

test('Test_AppendCubicBezierSamples_TestChord_ExpectPolylinePoints', () => {
   const polyline = [{ x: 0, y: 0 }];

   ItineraryPathArrowCalculator.appendCubicBezierSamples(
      polyline,
      { x: 0, y: 0 },
      { x: 0, y: 0 },
      { x: 10, y: 0 },
      { x: 10, y: 0 },
      5
   );

   assert.ok(polyline.length >= 3);
   assert.deepEqual(polyline.at(-1), { x: 10, y: 0 });
});

test('Test_PolylineLength_TestSegments_ExpectSum', () => {
   assert.equal(
      ItineraryPathArrowCalculator.polylineLength([
         { x: 0, y: 0 },
         { x: 3, y: 4 },
         { x: 6, y: 4 },
      ]),
      8
   );
});

test('Test_PointAndTangentAtDistance_TestAlongPolyline_ExpectPlacement', () => {
   const placement = ItineraryPathArrowCalculator.pointAndTangentAtDistance(
      [{ x: 0, y: 0 }, { x: 10, y: 0 }],
      5
   );

   assert.deepEqual(placement, { x: 5, y: 0, angleDeg: 0 });
   assert.equal(
      ItineraryPathArrowCalculator.pointAndTangentAtDistance([{ x: 0, y: 0 }, { x: 0, y: 0 }], 1),
      null
   );
   assert.equal(
      ItineraryPathArrowCalculator.pointAndTangentAtDistance([{ x: 0, y: 0 }, { x: 1, y: 0 }], 5),
      null
   );
});

test('Test_MergeConnectedPolylines_TestNearAndFar_ExpectMergedOrSeparate', () => {
   assert.deepEqual(ItineraryPathArrowCalculator.mergeConnectedPolylines([]), []);

   const merged = ItineraryPathArrowCalculator.mergeConnectedPolylines([
      [{ x: 0, y: 0 }, { x: 1, y: 0 }],
      [{ x: 1.1, y: 0 }, { x: 2, y: 0 }],
      [{ x: 10, y: 0 }, { x: 11, y: 0 }],
   ]);

   assert.equal(merged.length, 2);
   assert.deepEqual(merged[0], [{ x: 0, y: 0 }, { x: 1, y: 0 }, { x: 2, y: 0 }]);
   assert.deepEqual(merged[1], [{ x: 10, y: 0 }, { x: 11, y: 0 }]);
});

test('Test_BuildPathArrowPlacementsForPolyline_TestShortAndLong_ExpectPlacements', () => {
   assert.deepEqual(
      ItineraryPathArrowCalculator.buildPathArrowPlacementsForPolyline(
         [{ x: 0, y: 0 }, { x: 5, y: 0 }],
         { intervalPx: 10, skipEndPx: 1, minPathLengthPx: 20 }
      ),
      []
   );

   const placements = ItineraryPathArrowCalculator.buildPathArrowPlacementsForPolyline(
      [{ x: 0, y: 0 }, { x: 100, y: 0 }],
      { intervalPx: 25, skipEndPx: 10, minPathLengthPx: 20 }
   );

   assert.ok(placements.length >= 2);
   assert.ok(placements.every((placement) => Number.isFinite(placement.angleDeg)));
});
