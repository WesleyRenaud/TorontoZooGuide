import assert from 'node:assert/strict';
import test from 'node:test';

import { MarkerTypeRenderer } from '../../../scripts/markers/markerTypeRenderer.js';
import { MarkerTypeRendererFactory } from '../../../scripts/markers/markerTypeRendererFactory.js';

test('Test_RenderMarkerByType_TestUnknownType_ExpectFalse', () => {
   assert.equal(MarkerTypeRenderer.renderMarkerByType({}, [{ type: 'unknown' }]), false);
   assert.equal(MarkerTypeRenderer.renderMarkerByType({}, []), false);
});

test('Test_RenderMarkerByType_TestKnownType_ExpectRendererCalled', () => {
   const calls = [];
   const markerEl = { id: 'marker' };
   const original = MarkerTypeRenderer.MARKER_TYPE_RENDERERS.pavilion;

   MarkerTypeRenderer.MARKER_TYPE_RENDERERS.pavilion = (el, items) => {
      calls.push([el, items]);
   };

   try {
      const items = [{ type: 'pavilion', name: 'African Pavilion' }];
      assert.equal(MarkerTypeRenderer.renderMarkerByType(markerEl, items), true);
      assert.deepEqual(calls, [[markerEl, items]]);
   } finally {
      MarkerTypeRenderer.MARKER_TYPE_RENDERERS.pavilion = original;
   }
});

test('Test_RenderAnimalIcon_TestAnimal_ExpectFactoryCall', () => {
   const original = MarkerTypeRendererFactory.renderAnimalMarker;
   const calls = [];

   MarkerTypeRendererFactory.renderAnimalMarker = (...args) => {
      calls.push(args);
   };

   try {
      const markerEl = { id: 'animal-marker' };
      const animal = { species: 'Lion' };
      MarkerTypeRenderer.renderAnimalIcon(markerEl, animal);
      assert.deepEqual(calls, [[markerEl, [animal]]]);
   } finally {
      MarkerTypeRendererFactory.renderAnimalMarker = original;
   }
});

test('Test_MarkerTypeRenderers_TestMap_ExpectExpectedKeys', () => {
   for (const key of [
      'animal',
      'pavilion',
      'restaurant',
      'restroom',
      'giftShop',
      'attraction',
      'transportation',
      'transportationStation',
      'guardiansTalk',
      'wildEncounter',
      'drinkingFountain',
      'defibrillator',
      'emergencyIntercom',
      'guestService',
      'picnicSite',
      'eventSite',
   ]) {
      assert.equal(typeof MarkerTypeRenderer.MARKER_TYPE_RENDERERS[key], 'function');
   }

   assert.equal(
      MarkerTypeRenderer.MARKER_TYPE_RENDERERS.attraction,
      MarkerTypeRenderer.attractionMarkerRenderer
   );
   assert.equal(
      MarkerTypeRenderer.MARKER_TYPE_RENDERERS.transportation,
      MarkerTypeRenderer.attractionMarkerRenderer
   );
});

test('Test_AttractionMarkerRenderer_TestIconAndSize_ExpectCallbacks', () => {
   const markerEl = {
      style: { setProperty() {} },
      classList: { add() {}, remove() {} },
      setAttribute() {},
   };
   assert.doesNotThrow(() => {
      MarkerTypeRenderer.attractionMarkerRenderer(markerEl, [
         { type: 'attraction', name: 'Conservation Carousel' },
      ]);
   });
});
