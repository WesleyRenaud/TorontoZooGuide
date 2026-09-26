import assert from 'node:assert/strict';
import test from 'node:test';

import { WalkGraphPathGeometryHelper } from '../../../scripts/map/walkGraphPathGeometryHelper.js';
import { SvgPathParser } from '../../../scripts/map/svgPathParser.js';
import { Position } from '../../../scripts/shared/enums/position.js';

const start = { x: 0, y: 0 };
const mid = { x: 10, y: 0 };
const end = { x: 20, y: 0 };


test('Test_FindSliceBetweenPoints_TestMatchingSegment_ExpectIndices', () => {
   const segments = [
      { tag: 'M', x: start.x, y: start.y, d: 'M0 0' },
      { tag: 'L', x: mid.x, y: mid.y, d: 'L10 0' },
      { tag: 'L', x: end.x, y: end.y, d: 'L20 0' },
   ];

   const slice = WalkGraphPathGeometryHelper.findSliceBetweenPoints(segments, start, end);

   assert.deepEqual(slice, { fromIndex: Position.FIRST, toIndex: 2 });
});


test('Test_FindSliceBetweenPoints_TestMoveBreaksSearch_ExpectNull', () => {
   const segments = [
      { tag: 'M', x: start.x, y: start.y, d: 'M0 0' },
      { tag: 'L', x: mid.x, y: mid.y, d: 'L10 0' },
      { tag: 'M', x: 15, y: 0, d: 'M15 0' },
      { tag: 'L', x: end.x, y: end.y, d: 'L20 0' },
   ];

   const slice = WalkGraphPathGeometryHelper.findSliceBetweenPoints(segments, start, end);

   assert.equal(slice, null);
});


test('Test_FindSliceBetweenPoints_TestSearchStartIndex_ExpectLaterMatch', () => {
   const laterStartIndex = 2;
   const segments = [
      { tag: 'M', x: start.x, y: start.y, d: 'M0 0' },
      { tag: 'L', x: 5, y: 0, d: 'L5 0' },
      { tag: 'M', x: start.x, y: start.y, d: 'M0 0' },
      { tag: 'L', x: end.x, y: end.y, d: 'L20 0' },
   ];

   const slice = WalkGraphPathGeometryHelper.findSliceBetweenPoints(
      segments,
      start,
      end,
      laterStartIndex
   );

   assert.deepEqual(slice, { fromIndex: laterStartIndex, toIndex: 3 });
});


test('Test_AppendSlice_TestIncludeMove_ExpectPathParts', () => {
   const move = 'M0 0';
   const line = 'L10 0';
   const segments = [
      { tag: 'M', x: start.x, y: start.y, d: move },
      { tag: 'L', x: mid.x, y: mid.y, d: line },
   ];
   const withMove = [];
   const withoutMove = [];

   WalkGraphPathGeometryHelper.appendSlice(withMove, segments, Position.FIRST, Position.SECOND, true);
   WalkGraphPathGeometryHelper.appendSlice(withoutMove, segments, Position.FIRST, Position.SECOND, false);

   assert.deepEqual(withMove, [move, line]);
   assert.deepEqual(withoutMove, [line]);
});


test('Test_PointsNear_TestTolerance_ExpectTrue', () => {
   const near = SvgPathParser.pointsNear(start, { x: 1, y: 0 });

   assert.equal(near, true);
});
