import assert from 'node:assert/strict';
import test from 'node:test';

import { PavilionTooltipRenderer } from '../../../../scripts/tooltips/renderers/pavilionTooltipRenderer.js';
import { installDomTestHooks } from '../../helpers/domTestSetup.mjs';

installDomTestHooks();

test('Test_CreateCard_TestPavilion_ExpectNamedCard', () => {
   const card = PavilionTooltipRenderer.createCard({
      name: 'Americas Pavilion',
      region: 'Americas',
   }, 0);
   assert.equal(PavilionTooltipRenderer.key, 'pavilion');
   assert.match(card.textContent, /Americas Pavilion/);
   assert.match(card.textContent, /Americas/);
});
