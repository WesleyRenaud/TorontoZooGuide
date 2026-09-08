import assert from 'node:assert/strict';
import test from 'node:test';

import { MarkerVisualHelper } from '../../../scripts/markers/markerVisualHelper.js';
import { installDomTestHooks } from '../helpers/domTestSetup.mjs';

installDomTestHooks();

function _createMarkerEl() {
   const markerEl = document.createElement('div');
   const originalRemove = markerEl.classList.remove.bind(markerEl.classList);
   markerEl.classList.remove = (...values) => {
      for (const value of values) {
         originalRemove(value);
      }
   };
   return markerEl;
}

test('Test_ResetMarkerVisual_TestStyles_ExpectCleared', () => {
   const markerEl = _createMarkerEl();
   markerEl.textContent = '2';
   markerEl.classList.add('marker-restaurant');

   MarkerVisualHelper.resetMarkerVisual(markerEl);
   assert.equal(markerEl.textContent, '');
   assert.equal(markerEl.style.backgroundImage, 'none');
   assert.equal(markerEl.style.backgroundColor, 'transparent');
   assert.equal(markerEl.classList.contains('marker-restaurant'), false);
});

test('Test_ApplyMarkerClass_TestClassName_ExpectAdded', () => {
   const markerEl = _createMarkerEl();
   MarkerVisualHelper.applyMarkerClass(markerEl, 'marker-attraction');
   MarkerVisualHelper.applyMarkerClass(markerEl, '');
   assert.equal(markerEl.classList.contains('marker-attraction'), true);
});

test('Test_ApplyCountMarker_TestCount_ExpectTextAndColor', () => {
   const markerEl = _createMarkerEl();
   MarkerVisualHelper.applyCountMarker(markerEl, 3);
   assert.equal(markerEl.textContent, '3');
   assert.equal(markerEl.style.backgroundColor, MarkerVisualHelper.DEFAULT_STACK_MARKER_COLOR);
});

test('Test_ApplyBackgroundImage_TestUrl_ExpectWrapped', () => {
   const markerEl = _createMarkerEl();
   MarkerVisualHelper.applyBackgroundImage(markerEl, 'icons/lion.png', '#fff');
   assert.equal(markerEl.style.backgroundImage, 'url("icons/lion.png")');
   assert.equal(markerEl.style.backgroundColor, '#fff');

   MarkerVisualHelper.applyBackgroundImage(markerEl, 'url("icons/tiger.png")');
   assert.equal(markerEl.style.backgroundImage, 'url("icons/tiger.png")');
});

test('Test_ApplyGenericIcon_TestCount_ExpectCountOrImage', () => {
   const markerEl = _createMarkerEl();
   MarkerVisualHelper.applyGenericIcon(markerEl, 'icons/a.png', 2);
   assert.equal(markerEl.textContent, '2');

   MarkerVisualHelper.applyGenericIcon(markerEl, 'icons/a.png', 1);
   assert.equal(markerEl.style.backgroundImage, 'url("icons/a.png")');
});

test('Test_GetLikelihoodVisual_TestValues_ExpectTokens', () => {
   const partial = MarkerVisualHelper.getLikelihoodVisual(50);
   assert.equal(partial.likelihood, 50);
   assert.ok(partial.colour);
   assert.equal(partial.iconToken.includes('#'), false);

   const open = MarkerVisualHelper.getLikelihoodVisual(100);
   assert.equal(open.iconToken, 'open');
});
