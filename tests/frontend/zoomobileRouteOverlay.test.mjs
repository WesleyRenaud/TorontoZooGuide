import assert from 'node:assert/strict';
import test from 'node:test';

import {
   hideZoomobileRouteLayers,
   showZoomobileRouteLayer,
   showZoomobileRouteMarkers,
} from '../../scripts/map/zoomobileRouteOverlay.js';

function createCircle(id, { cx = 0, cy = 0 } = {}) {
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

function createGroup(id, circles) {
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

function createSvgRoot({ summerGroup, winterGroup, summerCircles, winterCircles }) {
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

test('showZoomobileRouteMarkers shows only selected circles in the route group', () => {
   const summerCircles = [
      createCircle('zm-s-005', { cx: 10, cy: 10 }),
      createCircle('zm-s-006', { cx: 200, cy: 10 }),
      createCircle('zm-s-086', { cx: 400, cy: 10 }),
   ];
   const winterCircles = [
      createCircle('zm-w-006'),
   ];
   const summerGroup = createGroup('zoomobile-route-summer', summerCircles);
   const winterGroup = createGroup('zoomobile-route-winter', winterCircles);
   const svgRoot = createSvgRoot({
      summerGroup,
      winterGroup,
      summerCircles,
      winterCircles,
   });
   const createdElements = [];

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
         createdElements.push(element);
         return element;
      },
   };

   showZoomobileRouteMarkers('summer', [['zm-s-005', 'zm-s-006']]);

   assert.equal(summerGroup.style.values.get('display'), '');
   assert.equal(winterGroup.style.values.get('display'), 'none');
   assert.equal(summerCircles[0].style.values.get('display'), '');
   assert.equal(summerCircles[1].style.values.get('display'), '');
   assert.equal(summerCircles[2].style.values.get('display'), 'none');

   const arrowsLayer = svgRoot.children.find(
      (child) => child.id === 'transportation-route-arrows'
   );
   assert.ok(arrowsLayer);
   assert.ok(arrowsLayer.childNodes.length > 0);

   showZoomobileRouteLayer('summer');

   assert.equal(summerGroup.style.values.get('display'), '');
   assert.equal(summerCircles[0].style.values.has('display'), false);
   assert.equal(summerCircles[2].style.values.has('display'), false);
   assert.equal(
      svgRoot.children.some((child) => child.id === 'transportation-route-arrows'),
      false
   );

   hideZoomobileRouteLayers();

   assert.equal(summerGroup.style.values.get('display'), 'none');
   assert.equal(winterGroup.style.values.get('display'), 'none');

   delete globalThis.document;
});

test('showZoomobileRouteMarkers places arrows on every other marker', () => {
   const summerCircles = [
      createCircle('zm-s-005', { cx: 10, cy: 10 }),
      createCircle('zm-s-006', { cx: 100, cy: 10 }),
      createCircle('zm-s-007', { cx: 200, cy: 10 }),
      createCircle('zm-s-008', { cx: 300, cy: 10 }),
      createCircle('zm-s-185', { cx: 10, cy: 200 }),
      createCircle('zm-s-186', { cx: 200, cy: 200 }),
   ];
   const summerGroup = createGroup('zoomobile-route-summer', summerCircles);
   const winterGroup = createGroup('zoomobile-route-winter', []);
   const svgRoot = createSvgRoot({
      summerGroup,
      winterGroup,
      summerCircles,
      winterCircles: [],
   });

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

   showZoomobileRouteMarkers('summer', [
      ['zm-s-005', 'zm-s-006', 'zm-s-007', 'zm-s-008'],
      ['zm-s-185', 'zm-s-186'],
   ]);

   const arrowsLayer = svgRoot.children.find(
      (child) => child.id === 'transportation-route-arrows'
   );
   assert.ok(arrowsLayer);
   assert.equal(arrowsLayer.childNodes.length, 3);

   const transforms = arrowsLayer.childNodes.map(
      (child) => child.attributes.get('transform')
   );
   assert.deepEqual(transforms, [
      'translate(10 10) rotate(0)',
      'translate(200 10) rotate(0)',
      'translate(10 200) rotate(0)',
   ]);

   delete globalThis.document;
});
