import assert from 'node:assert/strict';
import test from 'node:test';

import { CardFactory } from '../../../../scripts/tooltips/renderers/cardFactory.js';
import { installDomTestHooks } from '../../helpers/domTestSetup.mjs';

installDomTestHooks();

test('Test_CreateTooltipCard_TestTitleAndDetails_ExpectCard', () => {
   const card = CardFactory.createTooltipCard({
      index: 0,
      title: { text: 'Zootique' },
      details: ['Gift shop', ''],
   });
   assert.equal(card.className, 'tooltip-card');
   assert.match(card.textContent, /Zootique/);
   assert.match(card.textContent, /Gift shop/);
});
