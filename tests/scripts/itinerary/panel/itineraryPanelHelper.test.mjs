import assert from 'node:assert/strict';
import test from 'node:test';

import { ItineraryPanelHelper } from '../../../../scripts/itinerary/panel/itineraryPanelHelper.js';
import { installDomTestHooks } from '../../helpers/domTestSetup.mjs';

installDomTestHooks();


test('Test_El_TestTagClassText_ExpectElement', () => {
   const tag = 'span';
   const className = 'row-title';
   const text = 'African Lion';

   const node = ItineraryPanelHelper.el(tag, className, text);

   assert.equal(node.tagName.toUpperCase(), tag.toUpperCase());
   assert.equal(node.className, className);
   assert.equal(node.textContent, text);
});


test('Test_SafeImg_TestSrc_ExpectLazyImage', () => {
   const tag = 'img';
   const src = '/images/icon.png';

   const image = ItineraryPanelHelper.safeImg(src);

   assert.equal(image.tagName.toUpperCase(), tag.toUpperCase());
   assert.equal(image.src, src);
   assert.equal(image.alt, '');
   assert.equal(image.loading, 'lazy');
});
