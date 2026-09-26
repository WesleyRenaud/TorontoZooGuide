import assert from 'node:assert/strict';
import test from 'node:test';

import { Position } from '../../../../scripts/shared/enums/position.js';
import { GiftShopTooltipRenderer } from '../../../../scripts/tooltips/renderers/giftShopTooltipRenderer.js';
import { installDomTestHooks } from '../../helpers/domTestSetup.mjs';

installDomTestHooks();


test('Test_CreateCard_TestGiftShop_ExpectNamedCard', () => {
   const name = 'Zootique';
   const description = 'Souvenirs';

   const card = GiftShopTooltipRenderer.createCard({
      name,
      description,
   }, Position.FIRST);

   assert.equal(GiftShopTooltipRenderer.key, 'giftShop');
   assert.match(card.textContent, new RegExp(name));
   assert.match(card.textContent, new RegExp(description));
});
