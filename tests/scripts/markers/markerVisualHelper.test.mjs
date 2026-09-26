import assert from 'node:assert/strict';
import test from 'node:test';

import { MarkerVisualHelper } from '../../../scripts/markers/markerVisualHelper.js';
import { LikelihoodColors } from '../../../scripts/likelihood/likelihoodColors.js';
import { LikelihoodScale } from '../../../scripts/likelihood/likelihoodScale.js';
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
   const restaurantClass = 'marker-restaurant';
   markerEl.textContent = '2';
   markerEl.classList.add(restaurantClass);

   MarkerVisualHelper.resetMarkerVisual(markerEl);

   assert.equal(markerEl.textContent, '');
   assert.equal(markerEl.style.backgroundImage, 'none');
   assert.equal(markerEl.style.backgroundColor, 'transparent');
   assert.equal(markerEl.classList.contains(restaurantClass), false);
});


test('Test_ApplyMarkerClass_TestClassName_ExpectAdded', () => {
   const markerEl = _createMarkerEl();
   const className = 'marker-attraction';

   MarkerVisualHelper.applyMarkerClass(markerEl, className);
   MarkerVisualHelper.applyMarkerClass(markerEl, '');

   assert.equal(markerEl.classList.contains(className), true);
});


test('Test_ApplyCountMarker_TestCount_ExpectTextAndColor', () => {
   const markerEl = _createMarkerEl();
   const count = 3;

   MarkerVisualHelper.applyCountMarker(markerEl, count);

   assert.equal(markerEl.textContent, String(count));
   assert.equal(markerEl.style.backgroundColor, MarkerVisualHelper.DEFAULT_STACK_MARKER_COLOR);
});


test('Test_ApplyBackgroundImage_TestBareUrl_ExpectWrapped', () => {
   const markerEl = _createMarkerEl();
   const iconUrl = 'icons/lion.png';
   const backgroundColor = '#fff';

   MarkerVisualHelper.applyBackgroundImage(markerEl, iconUrl, backgroundColor);

   assert.equal(markerEl.style.backgroundImage, `url("${iconUrl}")`);
   assert.equal(markerEl.style.backgroundColor, backgroundColor);
});


test('Test_ApplyBackgroundImage_TestWrappedUrl_ExpectKept', () => {
   const markerEl = _createMarkerEl();
   const iconUrl = 'url("icons/tiger.png")';

   MarkerVisualHelper.applyBackgroundImage(markerEl, iconUrl);

   assert.equal(markerEl.style.backgroundImage, iconUrl);
});


test('Test_ApplyGenericIcon_TestStacked_ExpectCount', () => {
   const markerEl = _createMarkerEl();
   const count = 2;

   MarkerVisualHelper.applyGenericIcon(markerEl, 'icons/a.png', count);

   assert.equal(markerEl.textContent, String(count));
});


test('Test_ApplyGenericIcon_TestSingle_ExpectImage', () => {
   const markerEl = _createMarkerEl();
   const iconUrl = 'icons/a.png';

   MarkerVisualHelper.applyGenericIcon(markerEl, iconUrl, 1);

   assert.equal(markerEl.style.backgroundImage, `url("${iconUrl}")`);
});


test('Test_GetLikelihoodVisual_TestPartial_ExpectTokens', () => {
   const likelihood = 50;

   const visual = MarkerVisualHelper.getLikelihoodVisual(likelihood);

   assert.equal(visual.likelihood, likelihood);
   assert.equal(visual.colour, LikelihoodColors.likelihoodToColor(likelihood));
   assert.equal(visual.iconToken.includes('#'), false);
});


test('Test_GetLikelihoodVisual_TestMaximum_ExpectOpen', () => {
   const likelihood = LikelihoodScale.MAX_LIKELIHOOD;

   const visual = MarkerVisualHelper.getLikelihoodVisual(likelihood);

   assert.equal(visual.iconToken, 'open');
});
