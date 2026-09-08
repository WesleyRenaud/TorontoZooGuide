import assert from 'node:assert/strict';
import test from 'node:test';

import { GiftShopTooltipRenderer } from '../../../../scripts/tooltips/renderers/giftShopTooltipRenderer.js';
import { installDomTestHooks } from '../../helpers/domTestSetup.mjs';

installDomTestHooks();

test('Test_CreateCard_TestGiftShop_ExpectNamedCard', () => {
   const card = GiftShopTooltipRenderer.createCard({
      name: 'Zootique',
      description: 'Souvenirs',
   }, 0);
   assert.equal(GiftShopTooltipRenderer.key, 'giftShop');
   assert.match(card.textContent, /Zootique/);
   assert.match(card.textContent, /Souvenirs/);
});
