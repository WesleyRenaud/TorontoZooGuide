import assert from 'node:assert/strict';
import test from 'node:test';

import { WalkGraphPathGeometryHelper } from '../../../scripts/map/walkGraphPathGeometryHelper.js';
import { SvgPathParser } from '../../../scripts/map/svgPathParser.js';

test('Test_FindSliceBetweenPoints_TestMatchingSegment_ExpectIndices', () => {
   const segments = [
      { tag: 'M', x: 0, y: 0, d: 'M0 0' },
      { tag: 'L', x: 10, y: 0, d: 'L10 0' },
      { tag: 'L', x: 20, y: 0, d: 'L20 0' },
   ];

   assert.deepEqual(
      WalkGraphPathGeometryHelper.findSliceBetweenPoints(
         segments,
         { x: 0, y: 0 },
         { x: 20, y: 0 }
      ),
      { fromIndex: 0, toIndex: 2 }
   );
});

test('Test_FindSliceBetweenPoints_TestMoveBreaksSearch_ExpectNull', () => {
   const segments = [
      { tag: 'M', x: 0, y: 0, d: 'M0 0' },
      { tag: 'L', x: 10, y: 0, d: 'L10 0' },
      { tag: 'M', x: 15, y: 0, d: 'M15 0' },
      { tag: 'L', x: 20, y: 0, d: 'L20 0' },
   ];

   assert.equal(
      WalkGraphPathGeometryHelper.findSliceBetweenPoints(
         segments,
         { x: 0, y: 0 },
         { x: 20, y: 0 }
      ),
      null
   );
});

test('Test_FindSliceBetweenPoints_TestSearchStartIndex_ExpectLaterMatch', () => {
   const segments = [
      { tag: 'M', x: 0, y: 0, d: 'M0 0' },
      { tag: 'L', x: 5, y: 0, d: 'L5 0' },
      { tag: 'M', x: 0, y: 0, d: 'M0 0' },
      { tag: 'L', x: 20, y: 0, d: 'L20 0' },
   ];

   assert.deepEqual(
      WalkGraphPathGeometryHelper.findSliceBetweenPoints(
         segments,
         { x: 0, y: 0 },
         { x: 20, y: 0 },
         2
      ),
      { fromIndex: 2, toIndex: 3 }
   );
});

test('Test_AppendSlice_TestIncludeMove_ExpectPathParts', () => {
   const segments = [
      { tag: 'M', x: 0, y: 0, d: 'M0 0' },
      { tag: 'L', x: 10, y: 0, d: 'L10 0' },
   ];
   const withMove = [];
   const withoutMove = [];

   WalkGraphPathGeometryHelper.appendSlice(withMove, segments, 0, 1, true);
   WalkGraphPathGeometryHelper.appendSlice(withoutMove, segments, 0, 1, false);

   assert.deepEqual(withMove, ['M0 0', 'L10 0']);
   assert.deepEqual(withoutMove, ['L10 0']);
});

test('Test_PointsNear_TestTolerance_ExpectTrue', () => {
   assert.equal(SvgPathParser.pointsNear({ x: 0, y: 0 }, { x: 1, y: 0 }), true);
});
