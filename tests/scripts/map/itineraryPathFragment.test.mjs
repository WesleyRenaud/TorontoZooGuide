import assert from 'node:assert/strict';
import { test } from 'node:test';

import { ItineraryPathCalculator } from '../../../scripts/map/itineraryPathCalculator.js';
import { ItineraryPathFragment } from '../../../scripts/map/itineraryPathFragment.js';
import { ZooMapConstants } from '../../../scripts/shared/zooMapConstants.js';
import { Position } from '../../../scripts/shared/enums/position.js';
import { createDomNode } from '../helpers/domNodeMock.mjs';
import { querySelectorInNode } from '../helpers/domSelectorMock.mjs';
import { installDomTestHooks } from '../helpers/domTestSetup.mjs';


function _installItineraryMapDom() {
   const svgRoot = createDomNode('svg');
   const mapMount = createDomNode('div');
   mapMount.id = 'zooMapMount';
   mapMount.appendChild(svgRoot);

   svgRoot.querySelector = (selector) => {
      if (selector === '#itinerary-path') {
         return svgRoot.children.find(
            (child) => child.getAttribute('id') === 'itinerary-path'
         ) ?? null;
      }

      if (selector === '#walk-graph-path') {
         return null;
      }

      return querySelectorInNode(svgRoot, selector);
   };

   const previousQuerySelector = document.querySelector.bind(document);

   document.querySelector = (selector) => {
      if (selector === '#zooMapMount svg') {
         return svgRoot;
      }

      return previousQuerySelector(selector);
   };

   document.createElementNS = (_namespace, tagName) => createDomNode(tagName);

   return { svgRoot, mapMount };
}

installDomTestHooks({
   before: () => {
      _installItineraryMapDom();
   },
});


test('Test_RenderItineraryPathOverlay_TestExactPath_ExpectLayerInSvg', () => {
   const startX = 2515.5;
   const startY = 2434.9;
   const endX = 2600;
   const endY = 2500;
   const points = [
      { nodeId: ZooMapConstants.ENTRANCE_WALK_NODE_ID, xPx: startX, yPx: startY },
      { nodeId: 'v-0012', xPx: startX, yPx: startY },
      { nodeId: 'v-0011', xPx: endX, yPx: endY },
   ];

   ItineraryPathFragment.renderItineraryPathOverlay({
      legs: [],
      points,
   });
   const svgRoot = document.querySelector('#zooMapMount svg');
   const path = svgRoot?.querySelector('.itinerary-path-line');
   const layer = path?.parentElement ?? path?.parent;

   assert.equal(layer?.getAttribute('id'), 'itinerary-path');
   assert.equal(path?.getAttribute('fill'), 'none');
   assert.equal(
      path?.getAttribute('d'),
      ItineraryPathCalculator.buildItineraryPathD(points.map((point) => ({
         x: point.xPx,
         y: point.yPx,
      })))
   );
});


test('Test_RenderItineraryPathOverlay_TestRoute_ExpectArrows', () => {
   const expectedArrows = 6;

   ItineraryPathFragment.renderItineraryPathOverlay({
      legs: [],
      points: [
         { nodeId: 'v-0001', xPx: 100, yPx: 200 },
         { nodeId: 'v-0002', xPx: 500, yPx: 200 },
      ],
   });
   const svgRoot = document.querySelector('#zooMapMount svg');
   const arrows = svgRoot?.querySelectorAll('.itinerary-path-arrow') ?? [];

   assert.equal(arrows.length, expectedArrows);
});


test('Test_RenderItineraryPathOverlay_TestFewerThanTwoPoints_ExpectCleared', () => {
   ItineraryPathFragment.renderItineraryPathOverlay({
      legs: [],
      points: [{ xPx: 100, yPx: 200 }],
   });
   const path = document.querySelector('#zooMapMount svg')?.querySelector('.itinerary-path-line');

   assert.equal(path, null);
});


test('Test_ClearItineraryPathOverlay_TestExistingPath_ExpectCleared', () => {
   ItineraryPathFragment.renderItineraryPathOverlay({
      legs: [],
      points: [
         { xPx: 100, yPx: 200 },
         { xPx: 300, yPx: 400 },
      ],
   });

   ItineraryPathFragment.clearItineraryPathOverlay();
   const path = document.querySelector('#zooMapMount svg')?.querySelector('.itinerary-path-line');

   assert.equal(path, null);
});


test('Test_RenderItineraryPathOverlay_TestMissingSvgRoot_ExpectNoOp', async () => {
   const { ItineraryPathOverlayRenderer } = await import(
      '../../../scripts/map/itineraryPathOverlayRenderer.js'
   );
   const originalGet = ItineraryPathOverlayRenderer.getSvgRoot;
   ItineraryPathOverlayRenderer.getSvgRoot = () => null;

   try {
      const render = () => {
         ItineraryPathFragment.renderItineraryPathOverlay({
            legs: [],
            points: [
               { xPx: 100, yPx: 200 },
               { xPx: 300, yPx: 400 },
            ],
         });
      };

      assert.doesNotThrow(render);
   } finally {
      ItineraryPathOverlayRenderer.getSvgRoot = originalGet;
   }
});
