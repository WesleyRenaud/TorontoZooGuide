import assert from 'node:assert/strict';
import { test } from 'node:test';

import {
   buildPathDFromWalkGraphSegments,
   buildSmoothedPathD,
   parseSvgPathD,
} from '../../scripts/map/itineraryPathGeometry.js';

test('parseSvgPathD parses move and cubic commands', () => {
   const segments = parseSvgPathD(
      'M2515.53 2434.92C2515.53 2434.92 2513.03 2420.85 2511.03 2411.92'
   );

   assert.equal(segments.length, 2);
   assert.equal(segments[0].tag, 'M');
   assert.equal(segments[1].tag, 'C');
   assert.equal(segments[1].x, 2511.03);
   assert.equal(segments[1].y, 2411.92);
});

test('buildPathDFromWalkGraphSegments reuses source svg curve geometry', () => {
   const segments = parseSvgPathD(
      'M2515.53 2434.92C2515.53 2434.92 2513.03 2420.85 2511.03 2411.92'
   );

   assert.equal(
      buildPathDFromWalkGraphSegments(segments, [
         { x: 2515.53, y: 2434.92 },
         { x: 2511.03, y: 2411.92 },
      ]),
      'M 2515.53 2434.92 C 2515.53 2434.92 2513.03 2420.85 2511.03 2411.92'
   );
});

test('buildSmoothedPathD returns a cubic path for three or more points', () => {
   const pathD = buildSmoothedPathD([
      { x: 0, y: 0 },
      { x: 100, y: 0 },
      { x: 100, y: 100 },
   ]);

   assert.match(pathD, /^M 0 0 C .+ 100 100$/);
});

test('buildSmoothedPathD returns a line for two points', () => {
   assert.equal(
      buildSmoothedPathD([
         { x: 10, y: 20 },
         { x: 30, y: 40 },
      ]),
      'M 10 20 L 30 40'
   );
});
