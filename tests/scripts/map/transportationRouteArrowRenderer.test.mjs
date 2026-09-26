import assert from 'node:assert/strict';
import test from 'node:test';

import { TransportationRouteArrowRenderer } from '../../../scripts/map/transportationRouteArrowRenderer.js';
import { Position } from '../../../scripts/shared/enums/position.js';
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
   const svgRoot = TransportationRouteArrowRenderer.getSvgRoot();

   assert.equal(svgRoot, null);
});


test('Test_SetLayerVisibility_TestHidden_ExpectNone', () => {
   const layer = document.createElement('g');
   const selector = '#layer';
   layer.style = {
      values: new Map(),
      setProperty(name, value) {
         this.values.set(name, value);
      },
   };
   const svgRoot = {
      querySelector(nextSelector) {
         return nextSelector === selector ? layer : null;
      },
   };

   TransportationRouteArrowRenderer.setLayerVisibility(svgRoot, selector, false);

   assert.equal(layer.style.values.get('display'), 'none');
});


test('Test_SetLayerVisibility_TestVisible_ExpectCleared', () => {
   const layer = document.createElement('g');
   const selector = '#layer';
   layer.style = {
      values: new Map(),
      setProperty(name, value) {
         this.values.set(name, value);
      },
   };
   const svgRoot = {
      querySelector(nextSelector) {
         return nextSelector === selector ? layer : null;
      },
   };

   TransportationRouteArrowRenderer.setLayerVisibility(svgRoot, selector, true);

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
   const layer = {
      remove() {
         removed = true;
      },
   };
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
   const x = 10;
   const y = 20;
   const angleDeg = 90;

   const marker = TransportationRouteArrowRenderer.createArrowMarker({
      x,
      y,
      angleDeg,
   });

   assert.equal(marker.classList.contains(TransportationRouteArrowRenderer.ARROW_CLASS), true);
   assert.equal(marker.getAttribute('transform'), `translate(${x} ${y}) rotate(${angleDeg})`);
   assert.equal(
      marker.children.at(Position.FIRST).getAttribute('points'),
      TransportationRouteArrowRenderer.ARROW_HEAD_POINTS
   );
});


test('Test_CirclePoint_TestValid_ExpectPoint', () => {
   const x = 3;
   const y = 4;

   const point = TransportationRouteArrowRenderer.circlePoint({
      getAttribute(name) {
         return name === 'cx' ? String(x) : String(y);
      },
   });

   assert.deepEqual(point, { x, y });
});


test('Test_CirclePoint_TestInvalid_ExpectNull', () => {
   const point = TransportationRouteArrowRenderer.circlePoint({
      getAttribute() {
         return 'x';
      },
   });

   assert.equal(point, null);
});


test('Test_BuildMarkerArrowPlacements_TestPairs_ExpectAngles', () => {
   const start = { x: 0, y: 0 };
   const end = { x: 10, y: 0 };

   const placements = TransportationRouteArrowRenderer.buildMarkerArrowPlacements([
      start,
      end,
      end,
      end,
   ]);

   assert.deepEqual(placements, [{ ...start, angleDeg: 0 }]);
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

   assert.equal(appended.length, Position.SECOND);
   assert.equal(appended.at(Position.FIRST).id, TransportationRouteArrowRenderer.ROUTE_ARROWS_LAYER_ID);
   assert.ok(appended.at(Position.FIRST).children.length >= Position.SECOND);
});


test('Test_AppendRouteArrows_TestMissingRoot_ExpectNoOp', () => {
   const append = () => TransportationRouteArrowRenderer.appendRouteArrows(null, null, []);

   assert.doesNotThrow(append);
});
