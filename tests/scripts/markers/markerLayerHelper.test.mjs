import assert from 'node:assert/strict';
import test from 'node:test';

import { MarkerLayerHelper } from '../../../scripts/markers/markerLayerHelper.js';
import { installDomTestHooks } from '../helpers/domTestSetup.mjs';

installDomTestHooks();

test('Test_ShouldRenderMarkerGroup_TestItems_ExpectBoolean', () => {
   assert.equal(MarkerLayerHelper.shouldRenderMarkerGroup({ items: [{ id: 1 }] }), true);
   assert.equal(MarkerLayerHelper.shouldRenderMarkerGroup({ items: [] }), false);
});

test('Test_RemoveRenderedMarkers_TestMarkers_ExpectRemoved', () => {
   const mapInner = document.createElement('div');
   const markerEl = document.createElement('div');
   markerEl.className = 'marker';
   const otherEl = document.createElement('div');
   otherEl.className = 'other';
   mapInner.appendChild(markerEl);
   mapInner.appendChild(otherEl);

   MarkerLayerHelper.removeRenderedMarkers(mapInner);
   assert.equal(mapInner.children.length, 1);
   assert.equal(mapInner.children[0].className, 'other');
});
