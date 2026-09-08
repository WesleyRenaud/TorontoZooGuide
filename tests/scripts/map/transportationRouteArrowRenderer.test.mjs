import assert from 'node:assert/strict';
import test from 'node:test';

import { TransportationRouteArrowRenderer } from '../../../scripts/map/transportationRouteArrowRenderer.js';
import { installDomTestHooks } from '../helpers/domTestSetup.mjs';

function _installCreateElementNS() {
   document.createElementNS = (_ns, tagName) => {
      const node = document.createElement(tagName);
      node.namespaceURI = _ns;
      node.childNodes = node.children;
      return node;
   };
}

installDomTestHooks({ before: _installCreateElementNS });

test('Test_GetSvgRoot_TestMissingMount_ExpectNull', () => {
   assert.equal(TransportationRouteArrowRenderer.getSvgRoot(), null);
});

test('Test_SetLayerVisibility_TestToggle_ExpectDisplay', () => {
   const layer = document.createElement('g');
   layer.style = {
      values: new Map(),
      setProperty(name, value) {
         this.values.set(name, value);
      },
   };
   const svgRoot = {
      querySelector(selector) {
         return selector === '#layer' ? layer : null;
      },
   };

   TransportationRouteArrowRenderer.setLayerVisibility(svgRoot, '#layer', false);
   assert.equal(layer.style.values.get('display'), 'none');
   TransportationRouteArrowRenderer.setLayerVisibility(svgRoot, '#layer', true);
   assert.equal(layer.style.values.get('display'), '');
});

test('Test_ClearRouteMarkerFilters_TestCircles_ExpectDisplayCleared', () => {
   const removed = [];
   const circle = {
      style: {
         removeProperty(name) {
            removed.push(name);
         },
      },
   };
   const svgRoot = {
      querySelectorAll() {
         return [circle];
      },
   };

   TransportationRouteArrowRenderer.clearRouteMarkerFilters(svgRoot);
   assert.deepEqual(removed, ['display']);
});

test('Test_RemoveRouteArrowsLayer_TestExisting_ExpectRemoved', () => {
   let removed = false;
   const layer = { remove() { removed = true; } };
   const svgRoot = {
      querySelector(selector) {
         return selector === `#${TransportationRouteArrowRenderer.ROUTE_ARROWS_LAYER_ID}`
            ? layer
            : null;
      },
   };

   TransportationRouteArrowRenderer.removeRouteArrowsLayer(svgRoot);
   assert.equal(removed, true);
});

test('Test_CreateArrowMarker_TestPlacement_ExpectTransformedGroup', () => {
   const marker = TransportationRouteArrowRenderer.createArrowMarker({
      x: 10,
      y: 20,
      angleDeg: 90,
   });

   assert.equal(marker.classList.contains(TransportationRouteArrowRenderer.ARROW_CLASS), true);
   assert.equal(marker.getAttribute('transform'), 'translate(10 20) rotate(90)');
   assert.equal(marker.children[0].getAttribute('points'), TransportationRouteArrowRenderer.ARROW_HEAD_POINTS);
});

test('Test_CirclePoint_TestValidAndInvalid_ExpectPointOrNull', () => {
   assert.deepEqual(
      TransportationRouteArrowRenderer.circlePoint({
         getAttribute(name) {
            return name === 'cx' ? '3' : '4';
         },
      }),
      { x: 3, y: 4 }
   );
   assert.equal(
      TransportationRouteArrowRenderer.circlePoint({
         getAttribute() {
            return 'x';
         },
      }),
      null
   );
});

test('Test_BuildMarkerArrowPlacements_TestPairs_ExpectAngles', () => {
   assert.deepEqual(
      TransportationRouteArrowRenderer.buildMarkerArrowPlacements([
         { x: 0, y: 0 },
         { x: 10, y: 0 },
         { x: 10, y: 0 },
         { x: 10, y: 0 },
      ]),
      [{ x: 0, y: 0, angleDeg: 0 }]
   );
});

test('Test_AppendRouteArrows_TestSequences_ExpectLayerAppended', () => {
   const appended = [];
   const circles = new Map([
      ['a', {
         id: 'a',
         getAttribute(name) {
            return name === 'cx' ? '0' : '0';
         },
      }],
      ['b', {
         id: 'b',
         getAttribute(name) {
            return name === 'cx' ? '10' : '0';
         },
      }],
   ]);
   const routeGroup = {
      querySelectorAll() {
         return [...circles.values()];
      },
   };
   const svgRoot = {
      querySelector() {
         return null;
      },
      appendChild(child) {
         appended.push(child);
         return child;
      },
   };

   TransportationRouteArrowRenderer.appendRouteArrows(svgRoot, routeGroup, [['a', 'b']]);
   assert.equal(appended.length, 1);
   assert.equal(appended[0].id, TransportationRouteArrowRenderer.ROUTE_ARROWS_LAYER_ID);
   assert.ok(appended[0].children.length >= 1);

   TransportationRouteArrowRenderer.appendRouteArrows(null, null, []);
});
