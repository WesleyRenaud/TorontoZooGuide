import assert from 'node:assert/strict';
import test from 'node:test';

import { GiftShopTooltipRenderer } from '../../../scripts/tooltips/renderers/giftShopTooltipRenderer.js';
import { TooltipRenderer } from '../../../scripts/tooltips/tooltipRenderer.js';

test('Test_GetRendererForItem_TestKnownAndUnknown_ExpectRendererOrNull', () => {
   assert.equal(
      TooltipRenderer.getRendererForItem({ type: 'giftShop' }),
      GiftShopTooltipRenderer
   );
   assert.equal(TooltipRenderer.getRendererForItem({ type: 'unknown' }), null);
   assert.equal(TooltipRenderer.getRendererForItem(null), null);
});
