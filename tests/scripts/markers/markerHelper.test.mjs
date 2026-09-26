import assert from 'node:assert/strict';
import test from 'node:test';

import { MarkerHelper } from '../../../scripts/markers/markerHelper.js';
import { MarkerTypeRenderer } from '../../../scripts/markers/markerTypeRenderer.js';
import { MarkerVisualHelper } from '../../../scripts/markers/markerVisualHelper.js';
import { ItemType } from '../../../scripts/shared/enums/itemType.js';
import { Position } from '../../../scripts/shared/enums/position.js';


test('Test_ApplyMarkerVisual_TestMissingMarker_ExpectNoOp', () => {
   const originalReset = MarkerVisualHelper.resetMarkerVisual;
   const resets = [];
   MarkerVisualHelper.resetMarkerVisual = (el) => {
      resets.push(el);
   };

   try {
      MarkerHelper.applyMarkerVisual(null, [{ type: ItemType.ANIMAL }]);

      assert.equal(resets.length, Position.FIRST);
   } finally {
      MarkerVisualHelper.resetMarkerVisual = originalReset;
   }
});


test('Test_ApplyMarkerVisual_TestEmptyItems_ExpectReset', () => {
   const originalReset = MarkerVisualHelper.resetMarkerVisual;
   const originalCount = MarkerVisualHelper.applyCountMarker;
   const originalRender = MarkerTypeRenderer.renderMarkerByType;
   const resets = [];
   const markerEl = { id: 'm1' };

   MarkerVisualHelper.resetMarkerVisual = (el) => {
      resets.push(el);
   };
   MarkerVisualHelper.applyCountMarker = () => {};
   MarkerTypeRenderer.renderMarkerByType = () => false;

   try {
      MarkerHelper.applyMarkerVisual(markerEl, []);

      assert.deepEqual(resets, [markerEl]);
   } finally {
      MarkerVisualHelper.resetMarkerVisual = originalReset;
      MarkerVisualHelper.applyCountMarker = originalCount;
      MarkerTypeRenderer.renderMarkerByType = originalRender;
   }
});


test('Test_ApplyMarkerVisual_TestUnknownTypes_ExpectCount', () => {
   const originalReset = MarkerVisualHelper.resetMarkerVisual;
   const originalCount = MarkerVisualHelper.applyCountMarker;
   const originalRender = MarkerTypeRenderer.renderMarkerByType;
   const counts = [];
   const markerEl = { id: 'm1' };
   const items = [{ type: 'unknown' }, { type: 'unknown' }];

   MarkerVisualHelper.resetMarkerVisual = () => {};
   MarkerVisualHelper.applyCountMarker = (el, count) => {
      counts.push({ el, count });
   };
   MarkerTypeRenderer.renderMarkerByType = () => false;

   try {
      MarkerHelper.applyMarkerVisual(markerEl, items);

      assert.deepEqual(counts, [{ el: markerEl, count: items.length }]);
   } finally {
      MarkerVisualHelper.resetMarkerVisual = originalReset;
      MarkerVisualHelper.applyCountMarker = originalCount;
      MarkerTypeRenderer.renderMarkerByType = originalRender;
   }
});


test('Test_ApplyMarkerVisual_TestTypeRendererHandles_ExpectNoCount', () => {
   const originalReset = MarkerVisualHelper.resetMarkerVisual;
   const originalCount = MarkerVisualHelper.applyCountMarker;
   const originalRender = MarkerTypeRenderer.renderMarkerByType;
   const counts = [];

   MarkerVisualHelper.resetMarkerVisual = () => {};
   MarkerVisualHelper.applyCountMarker = (el, count) => {
      counts.push({ el, count });
   };
   MarkerTypeRenderer.renderMarkerByType = () => true;

   try {
      MarkerHelper.applyMarkerVisual({ id: 'm1' }, [{ type: ItemType.ANIMAL }]);

      assert.deepEqual(counts, []);
   } finally {
      MarkerVisualHelper.resetMarkerVisual = originalReset;
      MarkerVisualHelper.applyCountMarker = originalCount;
      MarkerTypeRenderer.renderMarkerByType = originalRender;
   }
});


test('Test_SetMarkerToAnimalIcon_TestMissingMarker_ExpectNoOp', () => {
   const originalReset = MarkerVisualHelper.resetMarkerVisual;
   const originalRender = MarkerTypeRenderer.renderAnimalIcon;
   const resets = [];
   const animal = { species: 'African Lion' };

   MarkerVisualHelper.resetMarkerVisual = (el) => {
      resets.push(el);
   };
   MarkerTypeRenderer.renderAnimalIcon = () => {};

   try {
      MarkerHelper.setMarkerToAnimalIcon(null, animal);

      assert.deepEqual(resets, []);
   } finally {
      MarkerVisualHelper.resetMarkerVisual = originalReset;
      MarkerTypeRenderer.renderAnimalIcon = originalRender;
   }
});


test('Test_SetMarkerToAnimalIcon_TestMissingAnimal_ExpectNoOp', () => {
   const originalReset = MarkerVisualHelper.resetMarkerVisual;
   const originalRender = MarkerTypeRenderer.renderAnimalIcon;
   const resets = [];
   const markerEl = { id: 'm1' };

   MarkerVisualHelper.resetMarkerVisual = (el) => {
      resets.push(el);
   };
   MarkerTypeRenderer.renderAnimalIcon = () => {};

   try {
      MarkerHelper.setMarkerToAnimalIcon(markerEl, null);

      assert.deepEqual(resets, []);
   } finally {
      MarkerVisualHelper.resetMarkerVisual = originalReset;
      MarkerTypeRenderer.renderAnimalIcon = originalRender;
   }
});


test('Test_SetMarkerToAnimalIcon_TestValid_ExpectRendered', () => {
   const originalReset = MarkerVisualHelper.resetMarkerVisual;
   const originalRender = MarkerTypeRenderer.renderAnimalIcon;
   const resets = [];
   const rendered = [];
   const markerEl = { id: 'm1' };
   const animal = { species: 'African Lion' };

   MarkerVisualHelper.resetMarkerVisual = (el) => {
      resets.push(el);
   };
   MarkerTypeRenderer.renderAnimalIcon = (el, nextAnimal) => {
      rendered.push({ el, animal: nextAnimal });
   };

   try {
      MarkerHelper.setMarkerToAnimalIcon(markerEl, animal);

      assert.deepEqual(resets, [markerEl]);
      assert.deepEqual(rendered, [{ el: markerEl, animal }]);
   } finally {
      MarkerVisualHelper.resetMarkerVisual = originalReset;
      MarkerTypeRenderer.renderAnimalIcon = originalRender;
   }
});
