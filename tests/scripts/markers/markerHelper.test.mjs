import assert from 'node:assert/strict';
import test from 'node:test';

import { MarkerHelper } from '../../../scripts/markers/markerHelper.js';
import { MarkerTypeRenderer } from '../../../scripts/markers/markerTypeRenderer.js';
import { MarkerVisualHelper } from '../../../scripts/markers/markerVisualHelper.js';

test('Test_ApplyMarkerVisual_TestEmptyAndCount_ExpectVisualHelpers', () => {
   const resets = [];
   const counts = [];
   const originalReset = MarkerVisualHelper.resetMarkerVisual;
   const originalCount = MarkerVisualHelper.applyCountMarker;
   const originalRender = MarkerTypeRenderer.renderMarkerByType;

   MarkerVisualHelper.resetMarkerVisual = (el) => { resets.push(el); };
   MarkerVisualHelper.applyCountMarker = (el, count) => { counts.push({ el, count }); };
   MarkerTypeRenderer.renderMarkerByType = () => false;

   try {
      const markerEl = { id: 'm1' };
      MarkerHelper.applyMarkerVisual(null, [{ type: 'animal' }]);
      MarkerHelper.applyMarkerVisual(markerEl, []);
      MarkerHelper.applyMarkerVisual(markerEl, [{ type: 'unknown' }, { type: 'unknown' }]);
      assert.equal(resets.length, 2);
      assert.deepEqual(counts, [{ el: markerEl, count: 2 }]);
   } finally {
      MarkerVisualHelper.resetMarkerVisual = originalReset;
      MarkerVisualHelper.applyCountMarker = originalCount;
      MarkerTypeRenderer.renderMarkerByType = originalRender;
   }
});
