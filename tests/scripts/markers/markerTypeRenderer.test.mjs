import assert from 'node:assert/strict';
import test from 'node:test';

import { MarkerTypeRenderer } from '../../../scripts/markers/markerTypeRenderer.js';
import { MarkerTypeRendererFactory } from '../../../scripts/markers/markerTypeRendererFactory.js';
import { ItemType } from '../../../scripts/shared/enums/itemType.js';

test('Test_RenderMarkerByType_TestUnknownType_ExpectFalse', () => {
   assert.equal(MarkerTypeRenderer.renderMarkerByType({}, [{ type: 'unknown' }]), false);
   assert.equal(MarkerTypeRenderer.renderMarkerByType({}, []), false);
});

test('Test_RenderMarkerByType_TestKnownType_ExpectRendererCalled', () => {
   const calls = [];
   const markerEl = { id: 'marker' };
   const original = MarkerTypeRenderer.MARKER_TYPE_RENDERERS[ItemType.PAVILION];

   MarkerTypeRenderer.MARKER_TYPE_RENDERERS[ItemType.PAVILION] = (el, items) => {
      calls.push([el, items]);
   };

   try {
      const items = [{ type: ItemType.PAVILION, name: 'African Pavilion' }];
      assert.equal(MarkerTypeRenderer.renderMarkerByType(markerEl, items), true);
      assert.deepEqual(calls, [[markerEl, items]]);
   } finally {
      MarkerTypeRenderer.MARKER_TYPE_RENDERERS[ItemType.PAVILION] = original;
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
      ItemType.ANIMAL,
      ItemType.PAVILION,
      ItemType.RESTAURANT,
      ItemType.RESTROOM,
      ItemType.GIFT_SHOP,
      ItemType.ATTRACTION,
      ItemType.TRANSPORTATION,
      ItemType.TRANSPORTATION_STATION,
      ItemType.GUARDIANS_TALK,
      ItemType.WILD_ENCOUNTER,
      ItemType.DRINKING_FOUNTAIN,
      ItemType.DEFIBRILLATOR,
      ItemType.EMERGENCY_INTERCOM,
      ItemType.GUEST_SERVICE,
      ItemType.PICNIC_SITE,
      ItemType.EVENT_SITE,
   ]) {
      assert.equal(typeof MarkerTypeRenderer.MARKER_TYPE_RENDERERS[key], 'function');
   }

   assert.equal(
      MarkerTypeRenderer.MARKER_TYPE_RENDERERS[ItemType.ATTRACTION],
      MarkerTypeRenderer.attractionMarkerRenderer
   );
   assert.equal(
      MarkerTypeRenderer.MARKER_TYPE_RENDERERS[ItemType.TRANSPORTATION],
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
         { type: ItemType.ATTRACTION, name: 'Conservation Carousel' },
      ]);
   });
});
