import assert from 'node:assert/strict';
import test from 'node:test';

import { ItineraryPathCalculator } from '../../../scripts/map/itineraryPathCalculator.js';
import { ItineraryPathOverlayRenderer } from '../../../scripts/map/itineraryPathOverlayRenderer.js';
import { ItineraryPathRenderer } from '../../../scripts/map/itineraryPathRenderer.js';
import { ZooMapConstants } from '../../../scripts/shared/zooMapConstants.js';
import { installDomTestHooks } from '../helpers/domTestSetup.mjs';

function _installCreateElementNS() {
   document.createElementNS = (_ns, tagName) => {
      const node = document.createElement(tagName);
      node.namespaceURI = _ns;
      return node;
   };
}

installDomTestHooks({ before: _installCreateElementNS });

test('Test_GetSvgRoot_TestMissingMount_ExpectNull', () => {
   assert.equal(ItineraryPathOverlayRenderer.getSvgRoot(), null);
});

test('Test_PointToMapPx_TestPxAndPercent_ExpectMapped', () => {
   assert.deepEqual(
      ItineraryPathOverlayRenderer.pointToMapPx({ xPx: 12, yPx: 34 }),
      { x: 12, y: 34 }
   );
   assert.deepEqual(
      ItineraryPathOverlayRenderer.pointToMapPx({ x: 50, y: 25 }),
      {
         x: 50 / 100 * ZooMapConstants.ZOO_MAP_WIDTH_PX,
         y: 25 / 100 * ZooMapConstants.ZOO_MAP_HEIGHT_PX,
      }
   );
   assert.equal(ItineraryPathOverlayRenderer.pointToMapPx({}), null);
});

test('Test_BuildPathD_TestLegsAndPoints_ExpectDelegated', () => {
   const originalFromLegs = ItineraryPathCalculator.buildItineraryPathDFromWalkLegs;
   const originalRoutePoints = ItineraryPathCalculator.buildRouteMapPoints;
   const originalBuildD = ItineraryPathCalculator.buildItineraryPathD;

   ItineraryPathCalculator.buildItineraryPathDFromWalkLegs = () => 'legs-d';
   ItineraryPathCalculator.buildRouteMapPoints = () => [{ x: 1, y: 1 }];
   ItineraryPathCalculator.buildItineraryPathD = () => 'points-d';

   try {
      assert.equal(
         ItineraryPathOverlayRenderer.buildPathD({ legs: [{ id: 1 }], points: [] }),
         'legs-d'
      );
      assert.equal(
         ItineraryPathOverlayRenderer.buildPathD({ legs: [], points: [{ x: 1, y: 1 }] }),
         'points-d'
      );
   } finally {
      ItineraryPathCalculator.buildItineraryPathDFromWalkLegs = originalFromLegs;
      ItineraryPathCalculator.buildRouteMapPoints = originalRoutePoints;
      ItineraryPathCalculator.buildItineraryPathD = originalBuildD;
   }
});

test('Test_CreateArrowMarker_TestPlacement_ExpectGroup', () => {
   const marker = ItineraryPathOverlayRenderer.createArrowMarker({
      x: 5,
      y: 6,
      angleDeg: 45,
   });

   assert.equal(marker.classList.contains(ItineraryPathOverlayRenderer.ARROW_CLASS), true);
   assert.equal(marker.getAttribute('transform'), 'translate(5 6) rotate(45)');
});

test('Test_CreatePathLayer_TestPathD_ExpectPathAndArrows', () => {
   const originalPlacements = ItineraryPathRenderer.buildPathArrowPlacements;
   const originalOffset = ItineraryPathRenderer.offsetArrowPlacement;

   ItineraryPathRenderer.buildPathArrowPlacements = () => [{ x: 1, y: 2, angleDeg: 0 }];
   ItineraryPathRenderer.offsetArrowPlacement = (placement) => placement;

   try {
      const layer = ItineraryPathOverlayRenderer.createPathLayer('M 0 0 L 10 0');

      assert.equal(layer.id, ItineraryPathOverlayRenderer.ITINERARY_PATH_LAYER_ID);
      assert.equal(layer.getAttribute('aria-hidden'), 'true');
      assert.equal(layer.children[0].classList.contains(ItineraryPathOverlayRenderer.PATH_CLASS), true);
      assert.equal(layer.children[0].getAttribute('d'), 'M 0 0 L 10 0');
      assert.equal(layer.children[1].classList.contains(ItineraryPathOverlayRenderer.ARROWS_CLASS), true);
      assert.ok(layer.children[1].children.length >= 1);
   } finally {
      ItineraryPathRenderer.buildPathArrowPlacements = originalPlacements;
      ItineraryPathRenderer.offsetArrowPlacement = originalOffset;
   }
});

test('Test_AppendArrowMarkers_TestEmptyPath_ExpectNoOp', () => {
   const markersLayer = document.createElement('g');
   ItineraryPathOverlayRenderer.appendArrowMarkers(markersLayer, '');
   assert.equal(markersLayer.children.length, 0);
});

test('Test_RemoveItineraryPathLayer_TestExisting_ExpectRemoved', () => {
   let removed = false;
   ItineraryPathOverlayRenderer.removeItineraryPathLayer({
      querySelector() {
         return { remove() { removed = true; } };
      },
   });
   assert.equal(removed, true);
   ItineraryPathOverlayRenderer.removeItineraryPathLayer(null);
});
