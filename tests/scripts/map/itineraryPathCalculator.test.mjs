import assert from 'node:assert/strict';
import { test } from 'node:test';

import { ItineraryPathRenderer } from '../../../scripts/map/itineraryPathRenderer.js';
import { ItineraryPathCalculator } from '../../../scripts/map/itineraryPathCalculator.js';
import { SvgPathParser } from '../../../scripts/map/svgPathParser.js';
import { WalkGraphPathCalculator } from '../../../scripts/map/walkGraphPathCalculator.js';

test('Test_ParseSvgPathD_TestMoveAndCubic_ExpectParsedSegments', () => {
   const segments = SvgPathParser.parseSvgPathD(
      'M2515.53 2434.92C2515.53 2434.92 2513.03 2420.85 2511.03 2411.92'
   );

   assert.equal(segments.length, 2);
   assert.equal(segments[0].tag, 'M');
   assert.equal(segments[1].tag, 'C');
   assert.equal(segments[1].x, 2511.03);
   assert.equal(segments[1].y, 2411.92);
});

test('Test_BuildPathDFromWalkGraphSegments_TestSourceCurve_ExpectReusedGeometry', () => {
   const segments = SvgPathParser.parseSvgPathD(
      'M2515.53 2434.92C2515.53 2434.92 2513.03 2420.85 2511.03 2411.92'
   );

   assert.equal(
      WalkGraphPathCalculator.buildPathDFromWalkGraphSegments(segments, [
         { x: 2515.53, y: 2434.92 },
         { x: 2511.03, y: 2411.92 },
      ]),
      'M 2515.53 2434.92 C 2515.53 2434.92 2513.03 2420.85 2511.03 2411.92'
   );
});

test('Test_BuildSmoothedPathD_TestThreePoints_ExpectCubicPath', () => {
   const pathD = ItineraryPathCalculator.buildSmoothedPathD([
      { x: 0, y: 0 },
      { x: 100, y: 0 },
      { x: 100, y: 100 },
   ]);

   assert.match(pathD, /^M 0 0 C .+ 100 100$/);
});

test('Test_BuildSmoothedPathD_TestTwoPoints_ExpectLine', () => {
   assert.equal(
      ItineraryPathCalculator.buildSmoothedPathD([
         { x: 10, y: 20 },
         { x: 30, y: 40 },
      ]),
      'M 10 20 L 30 40'
   );
});

test('Test_BuildPathArrowPlacements_TestStraightPath_ExpectSpacedArrows', () => {
   const placements = ItineraryPathRenderer.buildPathArrowPlacements('M 0 0 L 400 0');

   assert.equal(placements.length, 6);
   assert.equal(placements[0].x, 60);
   assert.equal(placements[0].angleDeg, 0);
});

test('Test_BuildPathArrowPlacements_TestShortPath_ExpectEmpty', () => {
   assert.deepEqual(ItineraryPathRenderer.buildPathArrowPlacements('M 0 0 L 20 0'), []);
});

test('Test_BuildItineraryPathDFromWalkLegs_TestTransitGaps_ExpectDiscontinuous', () => {
   const pathD = ItineraryPathCalculator.buildItineraryPathDFromWalkLegs(
      [
         {
            nodeIds: ['a', 'b'],
         },
         {
            nodeIds: ['c', 'd'],
         },
      ],
      [
         { nodeId: 'a', x: 0, y: 0 },
         { nodeId: 'b', x: 10, y: 0 },
         { nodeId: 'c', x: 100, y: 100 },
         { nodeId: 'd', x: 110, y: 100 },
      ],
      {
         pointToMapPx: (point) => ({ x: point.x, y: point.y }),
      }
   );

   assert.equal(pathD, 'M 0 0 L 10 0 M 100 100 L 110 100');
});

test('Test_BuildItineraryPathDFromWalkLegs_TestTransitStation_ExpectContinuousLeg', () => {
   const pathD = ItineraryPathCalculator.buildItineraryPathDFromWalkLegs(
      [
         {
            nodeIds: ['exhibit', 'path', 'domain-station'],
         },
         {
            nodeIds: ['africa-station', 'next-exhibit'],
         },
      ],
      [
         { nodeId: 'exhibit', x: 0, y: 0 },
         { nodeId: 'path', x: 10, y: 0 },
         { nodeId: 'domain-station', x: 20, y: 0 },
         { nodeId: 'africa-station', x: 200, y: 200 },
         { nodeId: 'next-exhibit', x: 210, y: 200 },
      ],
      {
         pointToMapPx: (point) => ({ x: point.x, y: point.y }),
      }
   );

   assert.match(pathD, /^M 0 0[\s\S]*20 0 M 200 200 L 210 200$/);
   assert.equal(pathD.includes('L 200 200'), false);
});

test('Test_BuildSmoothedPathD_TestTooFewPoints_ExpectEmpty', () => {
   assert.equal(ItineraryPathCalculator.buildSmoothedPathD([]), '');
   assert.equal(ItineraryPathCalculator.buildSmoothedPathD([{ x: 1, y: 1 }]), '');
});

test('Test_BuildExactPathD_TestPoints_ExpectPolyline', () => {
   assert.equal(ItineraryPathCalculator.buildExactPathD([{ x: 1, y: 1 }]), '');
   assert.equal(
      ItineraryPathCalculator.buildExactPathD([
         { x: 0, y: 0 },
         { x: 5, y: 5 },
         { x: 10, y: 0 },
      ]),
      'M 0 0 L 5 5 L 10 0'
   );
});

test('Test_BuildRouteMapPoints_TestFilterAndEntrance_ExpectMapped', () => {
   assert.deepEqual(
      ItineraryPathCalculator.buildRouteMapPoints([{ x: 1, y: 1 }], {
         withEntranceLandmark: (points) => points,
      }),
      []
   );
   assert.deepEqual(
      ItineraryPathCalculator.buildRouteMapPoints(
         [{ x: 1, y: 1 }, { x: 2, y: 2 }],
         {
            withEntranceLandmark: (points) => [{ x: 0, y: 0 }, ...points],
            pointToMapPx: (point) => (point.x === 1 ? null : { x: point.x * 10, y: point.y * 10 }),
         }
      ),
      [
         { x: 0, y: 0 },
         { x: 20, y: 20 },
      ]
   );
});

test('Test_BuildItineraryPathD_TestWalkGraphAndFallback_ExpectPath', () => {
   const routePoints = [
      { x: 0, y: 0 },
      { x: 10, y: 0 },
   ];

   assert.equal(ItineraryPathCalculator.buildItineraryPathD([{ x: 0, y: 0 }]), '');

   const originalGet = WalkGraphPathCalculator.getWalkGraphPathSegments;
   const originalBuild = WalkGraphPathCalculator.buildPathDFromWalkGraphSegments;

   WalkGraphPathCalculator.getWalkGraphPathSegments = () => [{ tag: 'M' }];
   WalkGraphPathCalculator.buildPathDFromWalkGraphSegments = () => 'M 0 0 L 10 0';

   try {
      assert.equal(ItineraryPathCalculator.buildItineraryPathD(routePoints), 'M 0 0 L 10 0');
   } finally {
      WalkGraphPathCalculator.getWalkGraphPathSegments = originalGet;
      WalkGraphPathCalculator.buildPathDFromWalkGraphSegments = originalBuild;
   }

   assert.equal(
      ItineraryPathCalculator.buildItineraryPathD(routePoints, []),
      'M 0 0 L 10 0'
   );
});

test('Test_BuildItineraryPathDFromWalkLegs_TestEmptyMappedAndSharedJoin_ExpectBranches', () => {
   assert.equal(
      ItineraryPathCalculator.buildItineraryPathDFromWalkLegs([], [{ x: 0, y: 0 }]),
      ''
   );

   const sharedPath = ItineraryPathCalculator.buildItineraryPathDFromWalkLegs(
      [
         { nodeIds: ['a', 'b'] },
         { nodeIds: ['b', 'c'] },
      ],
      [
         { nodeId: 'a', x: 0, y: 0 },
         { nodeId: 'b', x: 10, y: 0 },
         { nodeId: 'c', x: 20, y: 0 },
      ]
   );
   assert.match(sharedPath, /M 0 0/);

   assert.equal(
      ItineraryPathCalculator.buildItineraryPathDFromWalkLegs(
         [{ nodeIds: ['a', 'b', 'c'] }],
         [
            { nodeId: 'a', x: 0, y: 0 },
            { nodeId: 'b', x: 10, y: 0 },
         ]
      ),
      ''
   );

   assert.equal(
      ItineraryPathCalculator.buildItineraryPathDFromWalkLegs(
         [{ nodeIds: ['a', 'b'] }],
         [
            { nodeId: 'a', x: 0, y: 0 },
            { nodeId: 'b', x: 10, y: 0 },
         ],
         {
            pointToMapPx: (point) => (point.nodeId === 'b' ? null : point),
         }
      ),
      ''
   );

   assert.equal(
      ItineraryPathCalculator.buildItineraryPathDFromWalkLegs(
         [{ nodeIds: ['a'] }],
         [{ nodeId: 'a', x: 0, y: 0 }]
      ),
      ''
   );
});
