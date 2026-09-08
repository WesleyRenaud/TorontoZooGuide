import assert from 'node:assert/strict';
import test from 'node:test';

import { ItineraryPanelHelper } from '../../../../scripts/itinerary/panel/itineraryPanelHelper.js';
import { installDomTestHooks } from '../../helpers/domTestSetup.mjs';

installDomTestHooks();

test('Test_El_TestTagClassText_ExpectElement', () => {
   const node = ItineraryPanelHelper.el('span', 'row-title', 'African Lion');
   assert.equal(node.tagName.toUpperCase(), 'SPAN');
   assert.equal(node.className, 'row-title');
   assert.equal(node.textContent, 'African Lion');
});

test('Test_SafeImg_TestSrc_ExpectLazyImage', () => {
   const img = ItineraryPanelHelper.safeImg('/images/icon.png');
   assert.equal(img.tagName.toUpperCase(), 'IMG');
   assert.equal(img.src, '/images/icon.png');
   assert.equal(img.alt, '');
   assert.equal(img.loading, 'lazy');
});
