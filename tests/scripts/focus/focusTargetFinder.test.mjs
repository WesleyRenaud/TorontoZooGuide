import assert from 'node:assert/strict';
import test from 'node:test';

import { FocusTargetFinder } from '../../../scripts/focus/focusTargetFinder.js';
import { FocusTargetFinderHelper } from '../../../scripts/focus/focusTargetFinderHelper.js';
import { CoordKey } from '../../../scripts/map/coordKey.js';
import { TooltipRenderer } from '../../../scripts/tooltips/tooltipRenderer.js';

const lion = 'African Lion';
const tiger = 'Amur Tiger';


test('Test_CreateFocusMatch_TestRegistryMatch_ExpectTypeAndFn', () => {
   const originalRegistry = TooltipRenderer.TYPE_REGISTRY;
   const species = lion;
   TooltipRenderer.TYPE_REGISTRY = {
      animal: {
         isMatch: (item, row) => item.species === row.species,
      },
   };

   try {
      const match = FocusTargetFinder.createFocusMatch({ species }, 'animal');

      assert.equal(match.typeKey, 'animal');
      assert.equal(match.matchFn({ species }), true);
      assert.equal(match.matchFn({ species: tiger }), false);
   } finally {
      TooltipRenderer.TYPE_REGISTRY = originalRegistry;
   }
});


test('Test_CreateFocusMatch_TestMissingRenderer_ExpectAlwaysTrue', () => {
   const originalRegistry = TooltipRenderer.TYPE_REGISTRY;
   const typeKey = 'custom';
   TooltipRenderer.TYPE_REGISTRY = {};

   try {
      const match = FocusTargetFinder.createFocusMatch({ type: typeKey });

      assert.equal(match.typeKey, typeKey);
      assert.equal(match.matchFn({}), true);
   } finally {
      TooltipRenderer.TYPE_REGISTRY = originalRegistry;
   }
});


test('Test_FindMarkerByCoordinates_TestMissingKey_ExpectNull', () => {
   const originalKey = CoordKey.coordKey;
   CoordKey.coordKey = () => '';

   try {
      const marker = FocusTargetFinder.findMarkerByCoordinates({
         x: 1,
         y: 2,
         getMarkerByCoord: () => ({ id: 'm' }),
      });

      assert.equal(marker, null);
   } finally {
      CoordKey.coordKey = originalKey;
   }
});


test('Test_FindMarkerByCoordinates_TestKnownCoord_ExpectMarker', () => {
   const marker = { id: 'marker-1' };
   const x = 10;
   const y = 20;

   const found = FocusTargetFinder.findMarkerByCoordinates({
      x,
      y,
      getMarkerByCoord: (key) => (key === CoordKey.coordKey(x, y) ? marker : null),
   });

   assert.equal(found, marker);
});


test('Test_FindBestMarkerByScan_TestScores_ExpectBestMarker', () => {
   const originalDist = FocusTargetFinderHelper.distToViewportCenter;
   const originalLikelihood = FocusTargetFinderHelper.itemLikelihood;
   const nearDistance = 5;
   const farDistance = 10;
   const farLikelihood = 10;
   FocusTargetFinderHelper.distToViewportCenter = (marker) => marker.distance;
   FocusTargetFinderHelper.itemLikelihood = (item) => item.likelihood;
   const near = {
      distance: nearDistance,
      __items: [{ type: 'animal', likelihood: 1 }],
   };
   const farBetter = {
      distance: farDistance,
      __items: [{ type: 'animal', likelihood: farLikelihood }],
   };
   const empty = { distance: 0, __items: [] };
   const wrongType = {
      distance: 0,
      __items: [{ type: 'restaurant', likelihood: 100 }],
   };

   try {
      const best = FocusTargetFinder.findBestMarkerByScan({
         typeKey: 'animal',
         matchFn: () => true,
         markers: [empty, wrongType, near, farBetter],
         viewportEl: {},
      });

      assert.equal(best.marker, farBetter);
      assert.equal(best.score, (farLikelihood * 1000) - farDistance);
   } finally {
      FocusTargetFinderHelper.distToViewportCenter = originalDist;
      FocusTargetFinderHelper.itemLikelihood = originalLikelihood;
   }
});
