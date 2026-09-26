import assert from 'node:assert/strict';
import test from 'node:test';

import { GiftShopTooltipRenderer } from '../../../scripts/tooltips/renderers/giftShopTooltipRenderer.js';
import { TooltipRenderer } from '../../../scripts/tooltips/tooltipRenderer.js';


test('Test_GetRendererForItem_TestGiftShop_ExpectRenderer', () => {
   const item = { type: GiftShopTooltipRenderer.key };

   const renderer = TooltipRenderer.getRendererForItem(item);

   assert.equal(renderer, GiftShopTooltipRenderer);
});


test('Test_GetRendererForItem_TestUnknown_ExpectNull', () => {
   const item = { type: 'unknown' };

   const renderer = TooltipRenderer.getRendererForItem(item);

   assert.equal(renderer, null);
});


test('Test_GetRendererForItem_TestNull_ExpectNull', () => {
   const item = null;

   const renderer = TooltipRenderer.getRendererForItem(item);

   assert.equal(renderer, null);
});
