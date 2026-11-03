import assert from 'node:assert/strict';
import test from 'node:test';

import { MarkerTypeRenderer } from '../../../scripts/markers/markerTypeRenderer.js';
import { MarkerTypeRendererFactory } from '../../../scripts/markers/markerTypeRendererFactory.js';
import { ItemType } from '../../../scripts/shared/enums/itemType.js';


test('Test_RenderMarkerByType_TestUnknownType_ExpectFalse', () => {
   const rendered = MarkerTypeRenderer.renderMarkerByType({}, [{ type: 'unknown' }]);

   assert.equal(rendered, false);
});


test('Test_RenderMarkerByType_TestEmptyItems_ExpectFalse', () => {
   const rendered = MarkerTypeRenderer.renderMarkerByType({}, []);

   assert.equal(rendered, false);
});


test('Test_RenderMarkerByType_TestKnownType_ExpectRendererCalled', () => {
   const calls = [];
   const markerEl = { id: 'marker' };
   const original = MarkerTypeRenderer.MARKER_TYPE_RENDERERS[ItemType.PAVILION];
   const items = [{ type: ItemType.PAVILION, name: 'African Pavilion' }];

   MarkerTypeRenderer.MARKER_TYPE_RENDERERS[ItemType.PAVILION] = (el, nextItems) => {
      calls.push([el, nextItems]);
   };

   try {
      const rendered = MarkerTypeRenderer.renderMarkerByType(markerEl, items);

      assert.equal(rendered, true);
      assert.deepEqual(calls, [[markerEl, items]]);
   } finally {
      MarkerTypeRenderer.MARKER_TYPE_RENDERERS[ItemType.PAVILION] = original;
   }
});


test('Test_RenderAnimalIcon_TestAnimal_ExpectFactoryCall', () => {
   const original = MarkerTypeRendererFactory.renderAnimalMarker;
   const calls = [];
   const markerEl = { id: 'animal-marker' };
   const animal = { species: 'African Lion' };

   MarkerTypeRendererFactory.renderAnimalMarker = (...args) => {
      calls.push(args);
   };

   try {
      MarkerTypeRenderer.renderAnimalIcon(markerEl, animal);

      assert.deepEqual(calls, [[markerEl, [animal]]]);
   } finally {
      MarkerTypeRendererFactory.renderAnimalMarker = original;
   }
});


test('Test_MarkerTypeRenderers_TestMap_ExpectExpectedKeys', () => {
   const keys = [
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
   ];

   for (const key of keys) {
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
   const items = [{ type: ItemType.ATTRACTION, name: 'Conservation Carousel' }];

   const render = () => MarkerTypeRenderer.attractionMarkerRenderer(markerEl, items);

   assert.doesNotThrow(render);
});


test('Test_AttractionMarkerRenderer_TestClosedForSeason_ExpectWinterBlueIcon', () => {
   const markerEl = {
      style: {},
      classList: { add() {}, remove() {} },
      textContent: '',
   };

   MarkerTypeRenderer.attractionMarkerRenderer(markerEl, [{
      name: 'Conservation Carousel',
      likelihood: 0,
      is_closed_for_season: true,
   }]);

   assert.match(
      markerEl.style.backgroundImage,
      /conservation-carousel-off-display\.png/
   );
});


test('Test_AttractionMarkerRenderer_TestTemporarilyClosed_ExpectClosedColourIcon', () => {
   const markerEl = {
      style: {},
      classList: { add() {}, remove() {} },
      textContent: '',
   };

   MarkerTypeRenderer.attractionMarkerRenderer(markerEl, [{
      name: 'Conservation Carousel',
      likelihood: 0,
      is_closed_for_season: false,
   }]);

   assert.match(
      markerEl.style.backgroundImage,
      /conservation-carousel-7a0000\.png/
   );
});


test('Test_AttractionMarkerRenderer_TestClosedForSeasonCount_ExpectWinterBlue', () => {
   const markerEl = {
      style: {},
      classList: { add() {}, remove() {} },
      textContent: '',
   };

   MarkerTypeRenderer.attractionMarkerRenderer(markerEl, [
      { name: 'Conservation Carousel', likelihood: 0, is_closed_for_season: true },
      { name: 'Greenhouse', likelihood: 0, is_closed_for_season: true },
   ]);

   assert.equal(markerEl.style.backgroundColor, '#9fd3f0');
   assert.equal(markerEl.textContent, '2');
});


test('Test_RestaurantMarkerRenderer_TestClosedForSeason_ExpectWinterBlueIcon', () => {
   const markerEl = {
      style: {},
      classList: { add() {}, remove() {} },
      textContent: '',
   };

   MarkerTypeRenderer.MARKER_TYPE_RENDERERS[ItemType.RESTAURANT](markerEl, [{
      name: 'Africa Restaurant',
      likelihood: 0,
      is_closed_for_season: true,
   }]);

   assert.match(markerEl.style.backgroundImage, /restaurant-off-display\.png/);
});


test('Test_RestaurantMarkerRenderer_TestTemporarilyClosed_ExpectClosedColourIcon', () => {
   const markerEl = {
      style: {},
      classList: { add() {}, remove() {} },
      textContent: '',
   };

   MarkerTypeRenderer.MARKER_TYPE_RENDERERS[ItemType.RESTAURANT](markerEl, [{
      name: 'Africa Restaurant',
      likelihood: 0,
      is_closed_for_season: false,
   }]);

   assert.match(markerEl.style.backgroundImage, /restaurant-7a0000\.png/);
});
