import assert from 'node:assert/strict';
import test from 'node:test';

import { SvgPathParser } from '../../../scripts/map/svgPathParser.js';

test('Test_PointsNear_TestWithinTolerance_ExpectTrue', () => {
   assert.equal(SvgPathParser.pointsNear({ x: 0, y: 0 }, { x: 1, y: 0 }), true);
   assert.equal(SvgPathParser.pointsNear({ x: 0, y: 0 }, { x: 3, y: 0 }, 1.5), false);
});

test('Test_ParseSvgPathD_TestMoveLineHVCZ_ExpectSegments', () => {
   const segments = SvgPathParser.parseSvgPathD('M 10 20 L 30 40 H 50 V 60 C 1 2 3 4 5 6 Z');

   assert.deepEqual(segments, [
      { tag: 'M', x: 10, y: 20, d: 'M 10 20' },
      { tag: 'L', x: 30, y: 40, d: 'L 30 40' },
      { tag: 'H', x: 50, y: 40, d: 'L 50 40' },
      { tag: 'V', x: 50, y: 60, d: 'L 50 60' },
      {
         tag: 'C',
         x: 5,
         y: 6,
         controlPoint1X: 1,
         controlPoint1Y: 2,
         controlPoint2X: 3,
         controlPoint2Y: 4,
         d: 'C 1 2 3 4 5 6',
      },
   ]);
});

test('Test_ParseSvgPathD_TestImplicitLineAfterMove_ExpectLineSegment', () => {
   const segments = SvgPathParser.parseSvgPathD('M 0 0 10 10');

   assert.deepEqual(segments, [
      { tag: 'M', x: 0, y: 0, d: 'M 0 0' },
      { tag: 'L', x: 10, y: 10, d: 'L 10 10' },
   ]);
});

test('Test_ParseSvgPathD_TestEmptyAndLeadingNumbers_ExpectEmptyOrSkip', () => {
   assert.deepEqual(SvgPathParser.parseSvgPathD(''), []);
   assert.deepEqual(SvgPathParser.parseSvgPathD('1 2 M 3 4'), [
      { tag: 'M', x: 3, y: 4, d: 'M 3 4' },
   ]);
});

test('Test_ParseSvgPathD_TestUnknownCommand_ExpectSkipsWithoutSegment', () => {
   assert.deepEqual(SvgPathParser.parseSvgPathD('M 0 0 X'), [
      { tag: 'M', x: 0, y: 0, d: 'M 0 0' },
   ]);
});
