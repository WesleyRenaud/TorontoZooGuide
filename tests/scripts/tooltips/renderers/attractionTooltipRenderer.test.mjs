import assert from 'node:assert/strict';
import test from 'node:test';

import { AttractionTooltipRenderer } from '../../../../scripts/tooltips/renderers/attractionTooltipRenderer.js';
import { installDomTestHooks } from '../../helpers/domTestSetup.mjs';

installDomTestHooks();

test('Test_CreateCard_TestAttraction_ExpectNamedCard', () => {
   const card = AttractionTooltipRenderer.createCard({
      name: 'Conservation Carousel',
      description: 'Ride',
      info_link: 'https://example.test/carousel',
   }, 0);
   assert.equal(AttractionTooltipRenderer.key, 'attraction');
   assert.match(card.textContent, /Conservation Carousel/);
   assert.match(card.textContent, /Ride/);
});
