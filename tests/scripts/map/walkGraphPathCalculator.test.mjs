import assert from 'node:assert/strict';
import test from 'node:test';

import { SvgPathParser } from '../../../scripts/map/svgPathParser.js';
import { WalkGraphPathCalculator } from '../../../scripts/map/walkGraphPathCalculator.js';
import { WalkGraphPathGeometryHelper } from '../../../scripts/map/walkGraphPathGeometryHelper.js';
import { Position } from '../../../scripts/shared/enums/position.js';
import { installDomTestHooks } from '../helpers/domTestSetup.mjs';

installDomTestHooks({
   after: () => {
      WalkGraphPathCalculator.resetWalkGraphPathCache();
   },
});


test('Test_GetWalkGraphPathSegments_TestMissingPath_ExpectNull', () => {
   WalkGraphPathCalculator.resetWalkGraphPathCache();

   const segments = WalkGraphPathCalculator.getWalkGraphPathSegments();

   assert.equal(segments, null);
});


test('Test_GetWalkGraphPathSegments_TestCachesParsedSegments_ExpectReuse', () => {
   const originalParse = SvgPathParser.parseSvgPathD;
   const originalQuery = document.querySelector;
   let parseCalls = 0;
   const pathD = 'M0 0 L10 0';
   const segments = [{ tag: 'M', x: 0, y: 0 }];
   const pathEl = {
      getAttribute(name) {
         return name === 'd' ? pathD : null;
      },
   };

   SvgPathParser.parseSvgPathD = (parsedPathD) => {
      parseCalls += 1;
      assert.equal(parsedPathD, pathD);
      return segments;
   };
   document.querySelector = (selector) => (
      selector === '#walk-graph-path' ? pathEl : null
   );

   try {
      WalkGraphPathCalculator.resetWalkGraphPathCache();
      const first = WalkGraphPathCalculator.getWalkGraphPathSegments();
      const second = WalkGraphPathCalculator.getWalkGraphPathSegments();

      assert.equal(first, segments);
      assert.equal(second, segments);
      assert.equal(parseCalls, Position.SECOND);
   } finally {
      SvgPathParser.parseSvgPathD = originalParse;
      document.querySelector = originalQuery;
      WalkGraphPathCalculator.resetWalkGraphPathCache();
   }
});


test('Test_BuildPathDFromWalkGraphSegments_TestEmptySegments_ExpectEmptyString', () => {
   const pathD = WalkGraphPathCalculator.buildPathDFromWalkGraphSegments(
      [],
      [{ x: 0, y: 0 }, { x: 1, y: 1 }]
   );

   assert.equal(pathD, '');
});


test('Test_BuildPathDFromWalkGraphSegments_TestSinglePoint_ExpectEmptyString', () => {
   const pathD = WalkGraphPathCalculator.buildPathDFromWalkGraphSegments(
      [{ tag: 'M' }],
      [{ x: 0, y: 0 }]
   );

   assert.equal(pathD, '');
});


test('Test_BuildPathDFromWalkGraphSegments_TestFallbackThenSlice_ExpectJoinedPath', () => {
   const originalFind = WalkGraphPathGeometryHelper.findSliceBetweenPoints;
   const originalAppend = WalkGraphPathGeometryHelper.appendSlice;
   const segments = [{ tag: 'M' }, { tag: 'L' }];
   const start = { x: 0, y: 0 };
   const mid = { x: 5, y: 5 };
   const curve = 'C 1 1 2 2 3 3';
   let findCalls = 0;

   WalkGraphPathGeometryHelper.findSliceBetweenPoints = () => {
      findCalls += 1;
      if (findCalls === Position.SECOND) {
         return null;
      }
      return { fromIndex: Position.FIRST, toIndex: Position.SECOND };
   };
   WalkGraphPathGeometryHelper.appendSlice = (pathParts) => {
      pathParts.push(curve);
   };

   try {
      const pathD = WalkGraphPathCalculator.buildPathDFromWalkGraphSegments(segments, [
         start,
         mid,
         { x: 10, y: 10 },
      ]);

      assert.equal(pathD, `M ${start.x} ${start.y} L ${mid.x} ${mid.y} ${curve}`);
   } finally {
      WalkGraphPathGeometryHelper.findSliceBetweenPoints = originalFind;
      WalkGraphPathGeometryHelper.appendSlice = originalAppend;
   }
});


test('Test_BuildPathDFromWalkGraphSegments_TestAllFallback_ExpectPolyline', () => {
   const originalFind = WalkGraphPathGeometryHelper.findSliceBetweenPoints;
   const originalAppend = WalkGraphPathGeometryHelper.appendSlice;
   const points = [
      { x: 1, y: 1 },
      { x: 2, y: 2 },
      { x: 3, y: 3 },
   ];

   WalkGraphPathGeometryHelper.findSliceBetweenPoints = () => null;
   WalkGraphPathGeometryHelper.appendSlice = () => {};

   try {
      const pathD = WalkGraphPathCalculator.buildPathDFromWalkGraphSegments(
         [{ tag: 'M' }, { tag: 'L' }],
         points
      );

      assert.equal(
         pathD,
         `M ${points.at(Position.FIRST).x} ${points.at(Position.FIRST).y} L ${points.at(Position.SECOND).x} ${points.at(Position.SECOND).y} L ${points.at(Position.THIRD).x} ${points.at(Position.THIRD).y}`
      );
   } finally {
      WalkGraphPathGeometryHelper.findSliceBetweenPoints = originalFind;
      WalkGraphPathGeometryHelper.appendSlice = originalAppend;
   }
});


test('Test_BuildPathDFromWalkGraphSegments_TestNoParts_ExpectEmpty', () => {
   const originalFind = WalkGraphPathGeometryHelper.findSliceBetweenPoints;
   const originalAppend = WalkGraphPathGeometryHelper.appendSlice;

   WalkGraphPathGeometryHelper.findSliceBetweenPoints = () => ({
      fromIndex: Position.FIRST,
      toIndex: Position.FIRST,
   });
   WalkGraphPathGeometryHelper.appendSlice = () => {};

   try {
      const pathD = WalkGraphPathCalculator.buildPathDFromWalkGraphSegments(
         [{ tag: 'M' }],
         [{ x: 0, y: 0 }, { x: 1, y: 1 }]
      );

      assert.equal(pathD, '');
   } finally {
      WalkGraphPathGeometryHelper.findSliceBetweenPoints = originalFind;
      WalkGraphPathGeometryHelper.appendSlice = originalAppend;
   }
});
