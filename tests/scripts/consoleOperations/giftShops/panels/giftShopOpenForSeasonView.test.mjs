import assert from 'node:assert/strict';
import test from 'node:test';

import { GiftShopOpenForSeasonView } from '../../../../../scripts/consoleOperations/giftShops/panels/giftShopOpenForSeasonView.js';
import { Strings } from '../../../../../scripts/strings.js';
import { installDomTestHooks } from '../../../helpers/domTestSetup.mjs';

function _findById(node, id) {
   if (node.id === id) {
      return node;
   }

   for (const child of node.children) {
      const found = _findById(child, id);
      if (found) {
         return found;
      }
   }

   return null;
}

installDomTestHooks();


test('Test_CreateGiftShopOpenForSeasonPanel_TestDefault_ExpectGiftShopOnly', () => {
   const panelEl = GiftShopOpenForSeasonView.createGiftShopOpenForSeasonPanel();

   assert.equal(panelEl.id, 'giftShopOpenForSeasonPanel');
   assert.ok(panelEl.textContent.includes(Strings.panelTitles.giftShopOpenForSeason));
   assert.ok(_findById(panelEl, 'giftShopOpenForSeasonGiftShop'));
   assert.equal(_findById(panelEl, 'giftShopOpenForSeasonStartDate'), null);
   assert.equal(_findById(panelEl, 'giftShopOpenForSeasonEndDate'), null);
   assert.ok(_findById(panelEl, 'submitGiftShopOpenForSeason'));
   assert.ok(_findById(panelEl, 'giftShopOpenForSeasonStatus'));
});
