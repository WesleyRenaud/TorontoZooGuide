import assert from 'node:assert/strict';
import { test } from 'node:test';

import {
   buildItineraryPathD,
} from '../../scripts/map/itineraryPathGeometry.js';
import {
   clearItineraryPathOverlay,
   renderItineraryPathOverlay,
} from '../../scripts/map/itineraryPathOverlay.js';
import { ENTRANCE_WALK_NODE_ID } from '../../scripts/shared/zooMapConstants.js';
import { createDomNode } from './helpers/domNodeMock.mjs';
import { querySelectorInNode } from './helpers/domSelectorMock.mjs';
import { installDomTestHooks } from './helpers/domTestSetup.mjs';

function installItineraryMapDom() {
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

test.describe('itinerary path overlay', () => {
   installDomTestHooks({
      before: () => {
         installItineraryMapDom();
      },
   });

   test('renders an exact path layer inside the zoo map svg', () => {
      renderItineraryPathOverlay({
         points: [
            { nodeId: ENTRANCE_WALK_NODE_ID, xPx: 2515.5, yPx: 2434.9 },
            { nodeId: 'v-0012', xPx: 2515.5, yPx: 2434.9 },
            { nodeId: 'v-0011', xPx: 2600, yPx: 2500 },
         ],
      });

      const svgRoot = document.querySelector('#zooMapMount svg');
      const path = svgRoot?.querySelector('.itinerary-path-line');
      const layer = path?.parentElement ?? path?.parent;

      assert.equal(layer?.getAttribute('id'), 'itinerary-path');
      assert.equal(path?.getAttribute('fill'), 'none');
      assert.equal(
         path?.getAttribute('d'),
         buildItineraryPathD([
            { x: 2515.5, y: 2434.9 },
            { x: 2515.5, y: 2434.9 },
            { x: 2600, y: 2500 },
         ])
      );
   });

   test('clears the overlay when fewer than two points are available', () => {
      renderItineraryPathOverlay({
         points: [{ xPx: 100, yPx: 200 }],
      });

      assert.equal(
         document.querySelector('#zooMapMount svg')?.querySelector('.itinerary-path-line'),
         null
      );

      renderItineraryPathOverlay({
         points: [
            { xPx: 100, yPx: 200 },
            { xPx: 300, yPx: 400 },
         ],
      });

      clearItineraryPathOverlay();

      assert.equal(
         document.querySelector('#zooMapMount svg')?.querySelector('.itinerary-path-line'),
         null
      );
   });
});
