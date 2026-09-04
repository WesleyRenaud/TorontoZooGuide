import assert from 'node:assert/strict';
import { test } from 'node:test';

import { ItineraryPathArrows } from '../../../scripts/map/itineraryPathArrows.js';
import { ItineraryPathGeometry } from '../../../scripts/map/itineraryPathGeometry.js';
import { SvgPathParsing } from '../../../scripts/map/svgPathParsing.js';
import { WalkGraphPathGeometry } from '../../../scripts/map/walkGraphPathGeometry.js';

test('Test_ParseSvgPathD_TestMoveAndCubic_ExpectParsedSegments', () => {
   const segments = SvgPathParsing.parseSvgPathD(
      'M2515.53 2434.92C2515.53 2434.92 2513.03 2420.85 2511.03 2411.92'
   );

   assert.equal(segments.length, 2);
   assert.equal(segments[0].tag, 'M');
   assert.equal(segments[1].tag, 'C');
   assert.equal(segments[1].x, 2511.03);
   assert.equal(segments[1].y, 2411.92);
});

test('Test_BuildPathDFromWalkGraphSegments_TestSourceCurve_ExpectReusedGeometry', () => {
   const segments = SvgPathParsing.parseSvgPathD(
      'M2515.53 2434.92C2515.53 2434.92 2513.03 2420.85 2511.03 2411.92'
   );

   assert.equal(
      WalkGraphPathGeometry.buildPathDFromWalkGraphSegments(segments, [
         { x: 2515.53, y: 2434.92 },
         { x: 2511.03, y: 2411.92 },
      ]),
      'M 2515.53 2434.92 C 2515.53 2434.92 2513.03 2420.85 2511.03 2411.92'
   );
});

test('Test_BuildSmoothedPathD_TestThreePoints_ExpectCubicPath', () => {
   const pathD = ItineraryPathGeometry.buildSmoothedPathD([
      { x: 0, y: 0 },
      { x: 100, y: 0 },
      { x: 100, y: 100 },
   ]);

   assert.match(pathD, /^M 0 0 C .+ 100 100$/);
});

test('Test_BuildSmoothedPathD_TestTwoPoints_ExpectLine', () => {
   assert.equal(
      ItineraryPathGeometry.buildSmoothedPathD([
         { x: 10, y: 20 },
         { x: 30, y: 40 },
      ]),
      'M 10 20 L 30 40'
   );
});

test('Test_BuildPathArrowPlacements_TestStraightPath_ExpectSpacedArrows', () => {
   const placements = ItineraryPathArrows.buildPathArrowPlacements('M 0 0 L 400 0');

   assert.equal(placements.length, 6);
   assert.equal(placements[0].x, 60);
   assert.equal(placements[0].angleDeg, 0);
});

test('Test_BuildPathArrowPlacements_TestShortPath_ExpectEmpty', () => {
   assert.deepEqual(ItineraryPathArrows.buildPathArrowPlacements('M 0 0 L 20 0'), []);
});

test('Test_BuildItineraryPathDFromWalkLegs_TestTransitGaps_ExpectDiscontinuous', () => {
   const pathD = ItineraryPathGeometry.buildItineraryPathDFromWalkLegs(
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
   const pathD = ItineraryPathGeometry.buildItineraryPathDFromWalkLegs(
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
