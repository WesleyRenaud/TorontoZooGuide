import assert from 'node:assert/strict';
import test from 'node:test';

import { LikelihoodColors } from '../../../scripts/likelihood/likelihoodColors.js';
import { MapBootstrap } from '../../../scripts/pages/mapBootstrap.js';
import { installDomTestHooks } from '../helpers/domTestSetup.mjs';


installDomTestHooks();


test('Test_PaintPinKey_TestBar_ExpectScaleGradient', () => {
   const bar = document.createElement('span');
   bar.className = 'map-pin-key-bar';
   document.body.appendChild(bar);

   MapBootstrap.paintPinKey();

   assert.equal(bar.style.backgroundImage, LikelihoodColors.toGradient());
});


test('Test_PaintPinKey_TestMissingBar_ExpectLeavesPageAlone', () => {
   MapBootstrap.paintPinKey();

   assert.equal(document.querySelector('.map-pin-key-bar'), null);
});
