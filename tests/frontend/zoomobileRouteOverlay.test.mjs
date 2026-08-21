import assert from 'node:assert/strict';
import test from 'node:test';

import {
   hideZoomobileRouteLayers,
   showZoomobileRouteLayer,
   showZoomobileRouteMarkers,
} from '../../scripts/map/zoomobileRouteOverlay.js';

function createCircle(id) {
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

test('showZoomobileRouteMarkers shows only selected circles in the route group', () => {
   const summerCircles = [
      createCircle('zm-s-005'),
      createCircle('zm-s-006'),
      createCircle('zm-s-086'),
   ];
   const winterCircles = [
      createCircle('zm-w-006'),
   ];
   const summerGroup = createGroup('zoomobile-route-summer', summerCircles);
   const winterGroup = createGroup('zoomobile-route-winter', winterCircles);
   const svgRoot = {
      querySelector(selector) {
         if (selector === '#zoomobile-route-summer') {
            return summerGroup;
         }

         if (selector === '#zoomobile-route-winter') {
            return winterGroup;
         }

         return null;
      },
      querySelectorAll(selector) {
         if (selector.includes('circle[id]')) {
            return [...summerCircles, ...winterCircles];
         }

         return [];
      },
   };

   globalThis.document = {
      querySelector(selector) {
         return selector === '#zooMapMount svg' ? svgRoot : null;
      },
   };

   showZoomobileRouteMarkers('summer', ['zm-s-005', 'zm-s-006']);

   assert.equal(summerGroup.style.values.get('display'), '');
   assert.equal(winterGroup.style.values.get('display'), 'none');
   assert.equal(summerCircles[0].style.values.get('display'), '');
   assert.equal(summerCircles[1].style.values.get('display'), '');
   assert.equal(summerCircles[2].style.values.get('display'), 'none');

   showZoomobileRouteLayer('summer');

   assert.equal(summerGroup.style.values.get('display'), '');
   assert.equal(summerCircles[0].style.values.has('display'), false);
   assert.equal(summerCircles[2].style.values.has('display'), false);

   hideZoomobileRouteLayers();

   assert.equal(summerGroup.style.values.get('display'), 'none');
   assert.equal(winterGroup.style.values.get('display'), 'none');

   delete globalThis.document;
});
