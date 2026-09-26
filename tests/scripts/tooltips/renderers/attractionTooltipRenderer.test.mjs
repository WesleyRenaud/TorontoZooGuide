import assert from 'node:assert/strict';
import test from 'node:test';

import { Position } from '../../../../scripts/shared/enums/position.js';
import { AttractionTooltipRenderer } from '../../../../scripts/tooltips/renderers/attractionTooltipRenderer.js';
import { installDomTestHooks } from '../../helpers/domTestSetup.mjs';

installDomTestHooks();


test('Test_CreateCard_TestAttraction_ExpectNamedCard', () => {
   const name = 'Conservation Carousel';
   const description = 'Ride';

   const card = AttractionTooltipRenderer.createCard({
      name,
      description,
      info_link: 'https://example.test/carousel',
   }, Position.FIRST);

   assert.equal(AttractionTooltipRenderer.key, 'attraction');
   assert.match(card.textContent, new RegExp(name));
   assert.match(card.textContent, new RegExp(description));
});
