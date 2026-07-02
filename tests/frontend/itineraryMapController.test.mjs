import assert from 'node:assert/strict';
import { test } from 'node:test';

import { clearItineraryMapDisplay } from '../../scripts/itinerary/itineraryMapController.js';
import { renderItineraryPathOverlay } from '../../scripts/map/itineraryPathOverlay.js';
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

   return svgRoot;
}

test.describe('itinerary map controller', () => {
   installDomTestHooks({
      before: () => {
         installItineraryMapDom();
      },
   });

   test('clearItineraryMapDisplay clears markers and the itinerary path overlay', () => {
      const svgRoot = document.querySelector('#zooMapMount svg');
      const renderedMarkers = [];

      renderItineraryPathOverlay({
         points: [
            { xPx: 100, yPx: 200 },
            { xPx: 300, yPx: 400 },
         ],
      });

      clearItineraryMapDisplay({
         markers: {
            render(items) {
               renderedMarkers.splice(0, renderedMarkers.length, ...items);
            },
         },
      });

      assert.deepEqual(renderedMarkers, []);
      assert.equal(svgRoot.querySelector('.itinerary-path-line'), null);
   });
});
