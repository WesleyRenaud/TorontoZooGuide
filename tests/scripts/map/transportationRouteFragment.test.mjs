import assert from 'node:assert/strict';
import test from 'node:test';

import { TransportationRouteFragment } from '../../../scripts/map/transportationRouteFragment.js';
import { Position } from '../../../scripts/shared/enums/position.js';


function _createCircle(id, { cx = 0, cy = 0 } = {}) {
   const attributes = new Map([
      ['cx', String(cx)],
      ['cy', String(cy)],
   ]);

   return {
      id,
      style: {
         values: new Map(),
         setProperty(name, value) {
            this.values.set(name, value);
         },
         removeProperty(name) {
            this.values.delete(name);
         },
      },
      getAttribute(name) {
         return attributes.get(name) ?? null;
      },
   };
}


function _createGroup(id, circles) {
   return {
      id,
      style: {
         values: new Map(),
         setProperty(name, value) {
            this.values.set(name, value);
         },
      },
      querySelectorAll(selector) {
         if (selector !== 'circle[id]') {
            return [];
         }

         return circles;
      },
   };
}


function _createSvgRoot({ summerGroup, winterGroup, summerCircles, winterCircles }) {
   const children = [];

   return {
      children,
      querySelector(selector) {
         if (selector === '#zoomobile-route-summer') {
            return summerGroup;
         }

         if (selector === '#zoomobile-route-winter') {
            return winterGroup;
         }

         if (selector === '#transportation-route-arrows') {
            return children.find((child) => child.id === 'transportation-route-arrows')
               || null;
         }

         return null;
      },
      querySelectorAll(selector) {
         if (selector.includes('circle[id]')) {
            return [...summerCircles, ...winterCircles];
         }

         return [];
      },
      appendChild(child) {
         children.push(child);
         return child;
      },
   };
}


function _installSvgDocument(svgRoot) {
   globalThis.document = {
      querySelector(selector) {
         return selector === '#zooMapMount svg' ? svgRoot : null;
      },
      createElementNS(_ns, tagName) {
         const element = {
            tagName,
            id: '',
            classList: {
               values: new Set(),
               add(value) {
                  this.values.add(value);
               },
            },
            attributes: new Map(),
            childNodes: [],
            setAttribute(name, value) {
               this.attributes.set(name, value);
               if (name === 'id') {
                  this.id = value;
               }
            },
            appendChild(child) {
               this.childNodes.push(child);
               return child;
            },
            remove() {
               const index = svgRoot.children.indexOf(this);
               if (index >= 0) {
                  svgRoot.children.splice(index, 1);
               }
            },
         };
         return element;
      },
   };
}


test('Test_ShowTransportationRouteMarkers_TestSelectedCircles_ExpectVisibleOnly', () => {
   const first = _createCircle('zm-s-005', { cx: 10, cy: 10 });
   const second = _createCircle('zm-s-006', { cx: 200, cy: 10 });
   const hidden = _createCircle('zm-s-086', { cx: 400, cy: 10 });
   const summerCircles = [first, second, hidden];
   const winterCircles = [_createCircle('zm-w-006')];
   const summerGroup = _createGroup('zoomobile-route-summer', summerCircles);
   const winterGroup = _createGroup('zoomobile-route-winter', winterCircles);
   const svgRoot = _createSvgRoot({
      summerGroup,
      winterGroup,
      summerCircles,
      winterCircles,
   });
   _installSvgDocument(svgRoot);

   try {
      TransportationRouteFragment.showTransportationRouteMarkers('summer', [[first.id, second.id]]);
      const arrowsLayer = svgRoot.children.find(
         (child) => child.id === 'transportation-route-arrows'
      );

      assert.equal(summerGroup.style.values.get('display'), '');
      assert.equal(winterGroup.style.values.get('display'), 'none');
      assert.equal(first.style.values.get('display'), '');
      assert.equal(second.style.values.get('display'), '');
      assert.equal(hidden.style.values.get('display'), 'none');
      assert.ok(arrowsLayer);
      assert.ok(arrowsLayer.childNodes.length > Position.FIRST);
   } finally {
      delete globalThis.document;
   }
});


test('Test_ShowTransportationRouteLayer_TestAfterMarkers_ExpectFiltersCleared', () => {
   const first = _createCircle('zm-s-005', { cx: 10, cy: 10 });
   const hidden = _createCircle('zm-s-086', { cx: 400, cy: 10 });
   const summerCircles = [first, hidden];
   const winterCircles = [];
   const summerGroup = _createGroup('zoomobile-route-summer', summerCircles);
   const winterGroup = _createGroup('zoomobile-route-winter', winterCircles);
   const svgRoot = _createSvgRoot({
      summerGroup,
      winterGroup,
      summerCircles,
      winterCircles,
   });
   _installSvgDocument(svgRoot);

   try {
      TransportationRouteFragment.showTransportationRouteMarkers('summer', [[first.id]]);
      TransportationRouteFragment.showTransportationRouteLayer('summer');

      assert.equal(summerGroup.style.values.get('display'), '');
      assert.equal(first.style.values.has('display'), false);
      assert.equal(hidden.style.values.has('display'), false);
      assert.equal(
         svgRoot.children.some((child) => child.id === 'transportation-route-arrows'),
         false
      );
   } finally {
      delete globalThis.document;
   }
});


test('Test_HideTransportationRouteLayers_TestShown_ExpectHidden', () => {
   const summerCircles = [_createCircle('zm-s-005')];
   const winterCircles = [_createCircle('zm-w-006')];
   const summerGroup = _createGroup('zoomobile-route-summer', summerCircles);
   const winterGroup = _createGroup('zoomobile-route-winter', winterCircles);
   const svgRoot = _createSvgRoot({
      summerGroup,
      winterGroup,
      summerCircles,
      winterCircles,
   });
   _installSvgDocument(svgRoot);

   try {
      TransportationRouteFragment.showTransportationRouteLayer('summer');
      TransportationRouteFragment.hideTransportationRouteLayers();

      assert.equal(summerGroup.style.values.get('display'), 'none');
      assert.equal(winterGroup.style.values.get('display'), 'none');
   } finally {
      delete globalThis.document;
   }
});


test('Test_ShowTransportationRouteLayer_TestMissingRoute_ExpectHiddenOnly', () => {
   const summerGroup = _createGroup('zoomobile-route-summer', []);
   const winterGroup = _createGroup('zoomobile-route-winter', []);
   const svgRoot = _createSvgRoot({
      summerGroup,
      winterGroup,
      summerCircles: [],
      winterCircles: [],
   });
   _installSvgDocument(svgRoot);

   try {
      TransportationRouteFragment.showTransportationRouteLayer('');

      assert.equal(summerGroup.style.values.get('display'), 'none');
      assert.equal(winterGroup.style.values.get('display'), 'none');
   } finally {
      delete globalThis.document;
   }
});


test('Test_ShowTransportationRouteMarkers_TestMissingRouteOrGroup_ExpectEarlyReturn', () => {
   const summerGroup = _createGroup('zoomobile-route-summer', [
      _createCircle('zm-s-005'),
   ]);
   const winterGroup = _createGroup('zoomobile-route-winter', []);
   const svgRoot = _createSvgRoot({
      summerGroup,
      winterGroup,
      summerCircles: [_createCircle('zm-s-005')],
      winterCircles: [],
   });
   _installSvgDocument(svgRoot);

   try {
      TransportationRouteFragment.showTransportationRouteMarkers('', [['zm-s-005']]);
      TransportationRouteFragment.showTransportationRouteMarkers('summer', []);
      TransportationRouteFragment.showTransportationRouteMarkers('missing', [['zm-s-005']]);

      assert.equal(summerGroup.style.values.get('display'), 'none');
   } finally {
      delete globalThis.document;
   }
});


test('Test_ShowTransportationRouteMarkers_TestMarkerPairs_ExpectArrows', () => {
   const first = _createCircle('zm-s-005', { cx: 10, cy: 10 });
   const second = _createCircle('zm-s-006', { cx: 100, cy: 10 });
   const third = _createCircle('zm-s-007', { cx: 200, cy: 10 });
   const fourth = _createCircle('zm-s-008', { cx: 300, cy: 10 });
   const southFirst = _createCircle('zm-s-185', { cx: 10, cy: 200 });
   const southSecond = _createCircle('zm-s-186', { cx: 200, cy: 200 });
   const summerCircles = [first, second, third, fourth, southFirst, southSecond];
   const summerGroup = _createGroup('zoomobile-route-summer', summerCircles);
   const winterGroup = _createGroup('zoomobile-route-winter', []);
   const svgRoot = _createSvgRoot({
      summerGroup,
      winterGroup,
      summerCircles,
      winterCircles: [],
   });
   _installSvgDocument(svgRoot);

   try {
      TransportationRouteFragment.showTransportationRouteMarkers('summer', [
         [first.id, second.id, third.id, fourth.id],
         [southFirst.id, southSecond.id],
      ]);
      const arrowsLayer = svgRoot.children.find(
         (child) => child.id === 'transportation-route-arrows'
      );
      const transforms = arrowsLayer.childNodes.map(
         (child) => child.attributes.get('transform')
      );

      assert.ok(arrowsLayer);
      assert.equal(arrowsLayer.childNodes.length, 3);
      assert.deepEqual(transforms, [
         `translate(${first.getAttribute('cx')} ${first.getAttribute('cy')}) rotate(0)`,
         `translate(${third.getAttribute('cx')} ${third.getAttribute('cy')}) rotate(0)`,
         `translate(${southFirst.getAttribute('cx')} ${southFirst.getAttribute('cy')}) rotate(0)`,
      ]);
   } finally {
      delete globalThis.document;
   }
});
