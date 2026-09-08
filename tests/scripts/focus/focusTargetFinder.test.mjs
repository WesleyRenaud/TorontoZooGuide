import assert from 'node:assert/strict';
import test from 'node:test';

import { FocusTargetFinder } from '../../../scripts/focus/focusTargetFinder.js';
import { FocusTargetFinderHelper } from '../../../scripts/focus/focusTargetFinderHelper.js';
import { CoordKey } from '../../../scripts/map/coordKey.js';
import { TooltipRenderer } from '../../../scripts/tooltips/tooltipRenderer.js';

test('Test_CreateFocusMatch_TestRegistryMatch_ExpectTypeAndFn', () => {
   const originalRegistry = TooltipRenderer.TYPE_REGISTRY;
   TooltipRenderer.TYPE_REGISTRY = {
      animal: {
         isMatch: (item, row) => item.species === row.species,
      },
   };

   try {
      const match = FocusTargetFinder.createFocusMatch({ species: 'Lion' }, 'animal');
      assert.equal(match.typeKey, 'animal');
      assert.equal(match.matchFn({ species: 'Lion' }), true);
      assert.equal(match.matchFn({ species: 'Tiger' }), false);
   } finally {
      TooltipRenderer.TYPE_REGISTRY = originalRegistry;
   }
});

test('Test_CreateFocusMatch_TestMissingRenderer_ExpectAlwaysTrue', () => {
   const originalRegistry = TooltipRenderer.TYPE_REGISTRY;
   TooltipRenderer.TYPE_REGISTRY = {};

   try {
      const match = FocusTargetFinder.createFocusMatch({ type: 'custom' });
      assert.equal(match.typeKey, 'custom');
      assert.equal(match.matchFn({}), true);
   } finally {
      TooltipRenderer.TYPE_REGISTRY = originalRegistry;
   }
});

test('Test_FindMarkerByCoordinates_TestMissingKey_ExpectNull', () => {
   const originalKey = CoordKey.coordKey;
   CoordKey.coordKey = () => '';
   try {
      assert.equal(
         FocusTargetFinder.findMarkerByCoordinates({
            x: 1,
            y: 2,
            getMarkerByCoord: () => ({ id: 'm' }),
         }),
         null
      );
   } finally {
      CoordKey.coordKey = originalKey;
   }
});

test('Test_FindMarkerByCoordinates_TestKnownCoord_ExpectMarker', () => {
   const marker = { id: 'marker-1' };
   assert.equal(
      FocusTargetFinder.findMarkerByCoordinates({
         x: 10,
         y: 20,
         getMarkerByCoord: (key) => (key === CoordKey.coordKey(10, 20) ? marker : null),
      }),
      marker
   );
});

test('Test_FindBestMarkerByScan_TestScores_ExpectBestMarker', () => {
   const originalDist = FocusTargetFinderHelper.distToViewportCenter;
   const originalLikelihood = FocusTargetFinderHelper.itemLikelihood;
   FocusTargetFinderHelper.distToViewportCenter = (marker) => marker.distance;
   FocusTargetFinderHelper.itemLikelihood = (item) => item.likelihood;

   try {
      const near = {
         distance: 5,
         __items: [{ type: 'animal', likelihood: 1 }],
      };
      const farBetter = {
         distance: 10,
         __items: [{ type: 'animal', likelihood: 10 }],
      };
      const empty = { distance: 0, __items: [] };
      const wrongType = {
         distance: 0,
         __items: [{ type: 'restaurant', likelihood: 100 }],
      };

      const best = FocusTargetFinder.findBestMarkerByScan({
         typeKey: 'animal',
         matchFn: () => true,
         markers: [empty, wrongType, near, farBetter],
         viewportEl: {},
      });

      assert.equal(best.marker, farBetter);
      assert.equal(best.score, (10 * 1000) - 10);
   } finally {
      FocusTargetFinderHelper.distToViewportCenter = originalDist;
      FocusTargetFinderHelper.itemLikelihood = originalLikelihood;
   }
});
