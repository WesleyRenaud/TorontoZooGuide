import assert from 'node:assert/strict';
import test from 'node:test';

import { Position } from '../../../../scripts/shared/enums/position.js';
import { PavilionTooltipRenderer } from '../../../../scripts/tooltips/renderers/pavilionTooltipRenderer.js';
import { installDomTestHooks } from '../../helpers/domTestSetup.mjs';

installDomTestHooks();


test('Test_CreateCard_TestPavilion_ExpectNamedCard', () => {
   const name = 'Americas Pavilion';
   const region = 'Americas';

   const card = PavilionTooltipRenderer.createCard({
      name,
      region,
   }, Position.FIRST);

   assert.equal(PavilionTooltipRenderer.key, 'pavilion');
   assert.match(card.textContent, new RegExp(name));
   assert.match(card.textContent, new RegExp(region));
});
