import assert from 'node:assert/strict';
import test from 'node:test';

import { GiftShopClosedView } from '../../../../../scripts/consoleOperations/giftShops/panels/giftShopClosedView.js';
import { Strings } from '../../../../../scripts/strings.js';
import { installDomTestHooks } from '../../../helpers/domTestSetup.mjs';

function _findById(node, id) {
   if (node?.id === id) {
      return node;
   }

   for (const child of node?.children ?? []) {
      const found = _findById(child, id);
      if (found) {
         return found;
      }
   }

   return null;
}

installDomTestHooks();

test('Test_CreateGiftShopClosedPanel_TestDefault_ExpectPanel', () => {
   const panelEl = GiftShopClosedView.createGiftShopClosedPanel();

   assert.equal(panelEl.tagName.toUpperCase(), 'SECTION');
   assert.equal(panelEl.id, 'giftShopClosedPanel');
   assert.equal(panelEl.className, 'console-operations-panel');
   assert.ok(panelEl.textContent.includes(Strings.panelTitles.giftShopClosed));
   assert.ok(_findById(panelEl, 'giftShopClosedGiftShop'));
   assert.ok(_findById(panelEl, 'giftShopClosedStartDate'));
   assert.ok(_findById(panelEl, 'giftShopClosedEndDate'));
   assert.ok(_findById(panelEl, 'giftShopClosedMessage'));
   assert.ok(_findById(panelEl, 'submitGiftShopClosed'));
   assert.ok(_findById(panelEl, 'giftShopClosedStatus'));
});
