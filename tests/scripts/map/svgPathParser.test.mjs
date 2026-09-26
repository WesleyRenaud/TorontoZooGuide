import assert from 'node:assert/strict';
import test from 'node:test';

import { SvgPathParser } from '../../../scripts/map/svgPathParser.js';


test('Test_PointsNear_TestWithinDefaultTolerance_ExpectTrue', () => {
   const left = { x: 0, y: 0 };
   const right = { x: 1, y: 0 };

   const near = SvgPathParser.pointsNear(left, right);

   assert.equal(near, true);
});


test('Test_PointsNear_TestOutsideTolerance_ExpectFalse', () => {
   const left = { x: 0, y: 0 };
   const right = { x: 3, y: 0 };
   const tolerance = 1.5;

   const near = SvgPathParser.pointsNear(left, right, tolerance);

   assert.equal(near, false);
});


test('Test_ParseSvgPathD_TestMoveLineHVCZ_ExpectSegments', () => {
   const startX = 10;
   const startY = 20;
   const lineX = 30;
   const lineY = 40;
   const horizontalX = 50;
   const verticalY = 60;
   const control1X = 1;
   const control1Y = 2;
   const control2X = 3;
   const control2Y = 4;
   const curveX = 5;
   const curveY = 6;
   const path = `M ${startX} ${startY} L ${lineX} ${lineY} H ${horizontalX} V ${verticalY} C ${control1X} ${control1Y} ${control2X} ${control2Y} ${curveX} ${curveY} Z`;

   const segments = SvgPathParser.parseSvgPathD(path);

   assert.deepEqual(segments, [
      { tag: 'M', x: startX, y: startY, d: `M ${startX} ${startY}` },
      { tag: 'L', x: lineX, y: lineY, d: `L ${lineX} ${lineY}` },
      { tag: 'H', x: horizontalX, y: lineY, d: `L ${horizontalX} ${lineY}` },
      { tag: 'V', x: horizontalX, y: verticalY, d: `L ${horizontalX} ${verticalY}` },
      {
         tag: 'C',
         x: curveX,
         y: curveY,
         controlPoint1X: control1X,
         controlPoint1Y: control1Y,
         controlPoint2X: control2X,
         controlPoint2Y: control2Y,
         d: `C ${control1X} ${control1Y} ${control2X} ${control2Y} ${curveX} ${curveY}`,
      },
   ]);
});


test('Test_ParseSvgPathD_TestImplicitLineAfterMove_ExpectLineSegment', () => {
   const startX = 0;
   const startY = 0;
   const lineX = 10;
   const lineY = 10;
   const path = `M ${startX} ${startY} ${lineX} ${lineY}`;

   const segments = SvgPathParser.parseSvgPathD(path);

   assert.deepEqual(segments, [
      { tag: 'M', x: startX, y: startY, d: `M ${startX} ${startY}` },
      { tag: 'L', x: lineX, y: lineY, d: `L ${lineX} ${lineY}` },
   ]);
});


test('Test_ParseSvgPathD_TestEmpty_ExpectEmpty', () => {
   const path = '';

   const segments = SvgPathParser.parseSvgPathD(path);

   assert.deepEqual(segments, []);
});


test('Test_ParseSvgPathD_TestLeadingNumbers_ExpectMoveOnly', () => {
   const x = 3;
   const y = 4;
   const path = `1 2 M ${x} ${y}`;

   const segments = SvgPathParser.parseSvgPathD(path);

   assert.deepEqual(segments, [
      { tag: 'M', x, y, d: `M ${x} ${y}` },
   ]);
});


test('Test_ParseSvgPathD_TestUnknownCommand_ExpectSkipsWithoutSegment', () => {
   const x = 0;
   const y = 0;
   const path = `M ${x} ${y} X`;

   const segments = SvgPathParser.parseSvgPathD(path);

   assert.deepEqual(segments, [
      { tag: 'M', x, y, d: `M ${x} ${y}` },
   ]);
});
