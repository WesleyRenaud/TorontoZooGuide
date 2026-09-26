import assert from 'node:assert/strict';
import test from 'node:test';

import { MarkerLayerHelper } from '../../../scripts/markers/markerLayerHelper.js';
import { Position } from '../../../scripts/shared/enums/position.js';
import { installDomTestHooks } from '../helpers/domTestSetup.mjs';

installDomTestHooks();


test('Test_ShouldRenderMarkerGroup_TestItems_ExpectTrue', () => {
   const group = { items: [{ id: 1 }] };

   const shouldRender = MarkerLayerHelper.shouldRenderMarkerGroup(group);

   assert.equal(shouldRender, true);
});


test('Test_ShouldRenderMarkerGroup_TestEmpty_ExpectFalse', () => {
   const group = { items: [] };

   const shouldRender = MarkerLayerHelper.shouldRenderMarkerGroup(group);

   assert.equal(shouldRender, false);
});


test('Test_RemoveRenderedMarkers_TestMarkers_ExpectRemoved', () => {
   const mapInner = document.createElement('div');
   const markerEl = document.createElement('div');
   const otherClass = 'other';
   markerEl.className = 'marker';
   const otherEl = document.createElement('div');
   otherEl.className = otherClass;
   mapInner.appendChild(markerEl);
   mapInner.appendChild(otherEl);

   MarkerLayerHelper.removeRenderedMarkers(mapInner);

   assert.equal(mapInner.children.at(Position.FIRST).className, otherClass);
   assert.equal(mapInner.children.length, Position.SECOND);
});
