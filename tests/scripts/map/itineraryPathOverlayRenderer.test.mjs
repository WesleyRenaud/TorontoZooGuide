import assert from 'node:assert/strict';
import test from 'node:test';

import { ItineraryPathCalculator } from '../../../scripts/map/itineraryPathCalculator.js';
import { ItineraryPathOverlayRenderer } from '../../../scripts/map/itineraryPathOverlayRenderer.js';
import { ItineraryPathRenderer } from '../../../scripts/map/itineraryPathRenderer.js';
import { ZooMapConstants } from '../../../scripts/shared/zooMapConstants.js';
import { Position } from '../../../scripts/shared/enums/position.js';
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
   const svgRoot = ItineraryPathOverlayRenderer.getSvgRoot();

   assert.equal(svgRoot, null);
});


test('Test_PointToMapPx_TestPixels_ExpectMapped', () => {
   const xPx = 12;
   const yPx = 34;

   const point = ItineraryPathOverlayRenderer.pointToMapPx({ xPx, yPx });

   assert.deepEqual(point, { x: xPx, y: yPx });
});


test('Test_PointToMapPx_TestPercent_ExpectMapped', () => {
   const x = 50;
   const y = 25;

   const point = ItineraryPathOverlayRenderer.pointToMapPx({ x, y });

   assert.deepEqual(point, {
      x: x / 100 * ZooMapConstants.ZOO_MAP_WIDTH_PX,
      y: y / 100 * ZooMapConstants.ZOO_MAP_HEIGHT_PX,
   });
});


test('Test_PointToMapPx_TestEmpty_ExpectNull', () => {
   const point = ItineraryPathOverlayRenderer.pointToMapPx({});

   assert.equal(point, null);
});


test('Test_BuildPathD_TestLegs_ExpectDelegated', () => {
   const originalFromLegs = ItineraryPathCalculator.buildItineraryPathDFromWalkLegs;
   const originalRoutePoints = ItineraryPathCalculator.buildRouteMapPoints;
   const originalBuildD = ItineraryPathCalculator.buildItineraryPathD;
   const legsD = 'legs-d';

   ItineraryPathCalculator.buildItineraryPathDFromWalkLegs = () => legsD;
   ItineraryPathCalculator.buildRouteMapPoints = () => [{ x: 1, y: 1 }];
   ItineraryPathCalculator.buildItineraryPathD = () => 'points-d';

   try {
      const pathD = ItineraryPathOverlayRenderer.buildPathD({ legs: [{ id: 1 }], points: [] });

      assert.equal(pathD, legsD);
   } finally {
      ItineraryPathCalculator.buildItineraryPathDFromWalkLegs = originalFromLegs;
      ItineraryPathCalculator.buildRouteMapPoints = originalRoutePoints;
      ItineraryPathCalculator.buildItineraryPathD = originalBuildD;
   }
});


test('Test_BuildPathD_TestPoints_ExpectDelegated', () => {
   const originalFromLegs = ItineraryPathCalculator.buildItineraryPathDFromWalkLegs;
   const originalRoutePoints = ItineraryPathCalculator.buildRouteMapPoints;
   const originalBuildD = ItineraryPathCalculator.buildItineraryPathD;
   const pointsD = 'points-d';

   ItineraryPathCalculator.buildItineraryPathDFromWalkLegs = () => 'legs-d';
   ItineraryPathCalculator.buildRouteMapPoints = () => [{ x: 1, y: 1 }];
   ItineraryPathCalculator.buildItineraryPathD = () => pointsD;

   try {
      const pathD = ItineraryPathOverlayRenderer.buildPathD({ legs: [], points: [{ x: 1, y: 1 }] });

      assert.equal(pathD, pointsD);
   } finally {
      ItineraryPathCalculator.buildItineraryPathDFromWalkLegs = originalFromLegs;
      ItineraryPathCalculator.buildRouteMapPoints = originalRoutePoints;
      ItineraryPathCalculator.buildItineraryPathD = originalBuildD;
   }
});


test('Test_CreateArrowMarker_TestPlacement_ExpectGroup', () => {
   const x = 5;
   const y = 6;
   const angleDeg = 45;

   const marker = ItineraryPathOverlayRenderer.createArrowMarker({
      x,
      y,
      angleDeg,
   });

   assert.equal(marker.classList.contains(ItineraryPathOverlayRenderer.ARROW_CLASS), true);
   assert.equal(marker.getAttribute('transform'), `translate(${x} ${y}) rotate(${angleDeg})`);
});


test('Test_CreatePathLayer_TestPathD_ExpectPathAndArrows', () => {
   const originalPlacements = ItineraryPathRenderer.buildPathArrowPlacements;
   const originalOffset = ItineraryPathRenderer.offsetArrowPlacement;
   const pathD = 'M 0 0 L 10 0';

   ItineraryPathRenderer.buildPathArrowPlacements = () => [{ x: 1, y: 2, angleDeg: 0 }];
   ItineraryPathRenderer.offsetArrowPlacement = (placement) => placement;

   try {
      const layer = ItineraryPathOverlayRenderer.createPathLayer(pathD);
      const path = layer.children.at(Position.FIRST);
      const arrows = layer.children.at(Position.SECOND);

      assert.equal(layer.id, ItineraryPathOverlayRenderer.ITINERARY_PATH_LAYER_ID);
      assert.equal(layer.getAttribute('aria-hidden'), 'true');
      assert.equal(path.classList.contains(ItineraryPathOverlayRenderer.PATH_CLASS), true);
      assert.equal(path.getAttribute('d'), pathD);
      assert.equal(arrows.classList.contains(ItineraryPathOverlayRenderer.ARROWS_CLASS), true);
      assert.ok(arrows.children.length >= Position.SECOND);
   } finally {
      ItineraryPathRenderer.buildPathArrowPlacements = originalPlacements;
      ItineraryPathRenderer.offsetArrowPlacement = originalOffset;
   }
});


test('Test_AppendArrowMarkers_TestEmptyPath_ExpectNoOp', () => {
   const markersLayer = document.createElement('g');

   ItineraryPathOverlayRenderer.appendArrowMarkers(markersLayer, '');

   assert.equal(markersLayer.children.length, Position.FIRST);
});


test('Test_RemoveItineraryPathLayer_TestExisting_ExpectRemoved', () => {
   let removed = false;

   ItineraryPathOverlayRenderer.removeItineraryPathLayer({
      querySelector() {
         return {
            remove() {
               removed = true;
            },
         };
      },
   });

   assert.equal(removed, true);
});


test('Test_RemoveItineraryPathLayer_TestMissing_ExpectNoOp', () => {
   const remove = () => ItineraryPathOverlayRenderer.removeItineraryPathLayer(null);

   assert.doesNotThrow(remove);
});
