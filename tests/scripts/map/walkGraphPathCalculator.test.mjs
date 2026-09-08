import assert from 'node:assert/strict';
import test from 'node:test';

import { SvgPathParser } from '../../../scripts/map/svgPathParser.js';
import { WalkGraphPathCalculator } from '../../../scripts/map/walkGraphPathCalculator.js';
import { WalkGraphPathGeometryHelper } from '../../../scripts/map/walkGraphPathGeometryHelper.js';
import { installDomTestHooks } from '../helpers/domTestSetup.mjs';

installDomTestHooks({
   after: () => {
      WalkGraphPathCalculator.resetWalkGraphPathCache();
   },
});

test('Test_GetWalkGraphPathSegments_TestMissingPath_ExpectNull', () => {
   WalkGraphPathCalculator.resetWalkGraphPathCache();
   assert.equal(WalkGraphPathCalculator.getWalkGraphPathSegments(), null);
});

test('Test_GetWalkGraphPathSegments_TestCachesParsedSegments_ExpectReuse', () => {
   const originalParse = SvgPathParser.parseSvgPathD;
   const originalQuery = document.querySelector;
   let parseCalls = 0;
   const segments = [{ tag: 'M', x: 0, y: 0 }];
   const pathEl = {
      getAttribute(name) {
         return name === 'd' ? 'M0 0 L10 0' : null;
      },
   };

   SvgPathParser.parseSvgPathD = (pathD) => {
      parseCalls += 1;
      assert.equal(pathD, 'M0 0 L10 0');
      return segments;
   };
   document.querySelector = (selector) => (
      selector === '#walk-graph-path' ? pathEl : null
   );

   try {
      WalkGraphPathCalculator.resetWalkGraphPathCache();
      assert.equal(WalkGraphPathCalculator.getWalkGraphPathSegments(), segments);
      assert.equal(WalkGraphPathCalculator.getWalkGraphPathSegments(), segments);
      assert.equal(parseCalls, 1);
   } finally {
      SvgPathParser.parseSvgPathD = originalParse;
      document.querySelector = originalQuery;
      WalkGraphPathCalculator.resetWalkGraphPathCache();
   }
});

test('Test_BuildPathDFromWalkGraphSegments_TestEmptyOrShort_ExpectEmptyString', () => {
   assert.equal(WalkGraphPathCalculator.buildPathDFromWalkGraphSegments([], [{ x: 0, y: 0 }, { x: 1, y: 1 }]), '');
   assert.equal(WalkGraphPathCalculator.buildPathDFromWalkGraphSegments([{ tag: 'M' }], [{ x: 0, y: 0 }]), '');
});

test('Test_BuildPathDFromWalkGraphSegments_TestFallbackAndSlice_ExpectJoinedPath', () => {
   const originalFind = WalkGraphPathGeometryHelper.findSliceBetweenPoints;
   const originalAppend = WalkGraphPathGeometryHelper.appendSlice;
   const segments = [{ tag: 'M' }, { tag: 'L' }];
   let findCalls = 0;

   WalkGraphPathGeometryHelper.findSliceBetweenPoints = () => {
      findCalls += 1;
      if (findCalls === 1) {
         return null;
      }
      return { fromIndex: 0, toIndex: 1 };
   };
   WalkGraphPathGeometryHelper.appendSlice = (pathParts) => {
      pathParts.push('C 1 1 2 2 3 3');
   };

   try {
      assert.equal(
         WalkGraphPathCalculator.buildPathDFromWalkGraphSegments(segments, [
            { x: 0, y: 0 },
            { x: 5, y: 5 },
            { x: 10, y: 10 },
         ]),
         'M 0 0 L 5 5 C 1 1 2 2 3 3'
      );

      WalkGraphPathGeometryHelper.findSliceBetweenPoints = () => null;
      assert.equal(
         WalkGraphPathCalculator.buildPathDFromWalkGraphSegments(segments, [
            { x: 1, y: 1 },
            { x: 2, y: 2 },
            { x: 3, y: 3 },
         ]),
         'M 1 1 L 2 2 L 3 3'
      );
   } finally {
      WalkGraphPathGeometryHelper.findSliceBetweenPoints = originalFind;
      WalkGraphPathGeometryHelper.appendSlice = originalAppend;
   }
});

test('Test_BuildPathDFromWalkGraphSegments_TestNoParts_ExpectEmpty', () => {
   const originalFind = WalkGraphPathGeometryHelper.findSliceBetweenPoints;
   const originalAppend = WalkGraphPathGeometryHelper.appendSlice;

   WalkGraphPathGeometryHelper.findSliceBetweenPoints = () => ({ fromIndex: 0, toIndex: 0 });
   WalkGraphPathGeometryHelper.appendSlice = () => {};

   try {
      assert.equal(
         WalkGraphPathCalculator.buildPathDFromWalkGraphSegments([{ tag: 'M' }], [
            { x: 0, y: 0 },
            { x: 1, y: 1 },
         ]),
         ''
      );
   } finally {
      WalkGraphPathGeometryHelper.findSliceBetweenPoints = originalFind;
      WalkGraphPathGeometryHelper.appendSlice = originalAppend;
   }
});
