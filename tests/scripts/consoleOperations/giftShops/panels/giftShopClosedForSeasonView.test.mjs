import assert from 'node:assert/strict';
import test from 'node:test';

import { GiftShopClosedForSeasonView } from '../../../../../scripts/consoleOperations/giftShops/panels/giftShopClosedForSeasonView.js';
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


test('Test_CreateGiftShopClosedForSeasonPanel_TestDefault_ExpectPanel', () => {
   const panelEl = GiftShopClosedForSeasonView.createGiftShopClosedForSeasonPanel();

   assert.equal(panelEl.id, 'giftShopClosedForSeasonPanel');
   assert.ok(panelEl.textContent.includes(Strings.panelTitles.giftShopClosedForSeason));
   assert.ok(panelEl.textContent.includes(Strings.labels.reason));
   assert.ok(_findById(panelEl, 'giftShopClosedForSeasonGiftShop'));
   assert.ok(_findById(panelEl, 'giftShopClosedForSeasonStartDate'));
   assert.ok(_findById(panelEl, 'giftShopClosedForSeasonEndDate'));
   assert.ok(_findById(panelEl, 'giftShopClosedForSeasonMessage'));
   assert.ok(_findById(panelEl, 'submitGiftShopClosedForSeason'));
   assert.ok(_findById(panelEl, 'giftShopClosedForSeasonStatus'));
});
