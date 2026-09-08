import assert from 'node:assert/strict';
import test from 'node:test';

import { GiftShopOpeningScheduleView } from '../../../../../scripts/consoleOperations/giftShops/panels/giftShopOpeningScheduleView.js';
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

test('Test_CreateGiftShopOpeningSchedulePanel_TestDefault_ExpectPanel', () => {
   const panelEl = GiftShopOpeningScheduleView.createGiftShopOpeningSchedulePanel();

   assert.equal(panelEl.tagName.toUpperCase(), 'SECTION');
   assert.equal(panelEl.id, 'giftShopOpeningSchedulePanel');
   assert.equal(panelEl.className, 'console-operations-panel');
   assert.ok(panelEl.textContent.includes(Strings.panelTitles.giftShopOpeningSchedule));
   assert.ok(_findById(panelEl, 'giftShopOpeningScheduleGiftShop'));
   assert.ok(_findById(panelEl, 'giftShopOpeningSchedulePreset'));
   assert.ok(_findById(panelEl, 'giftShopOpeningScheduleStartDate'));
   assert.ok(_findById(panelEl, 'giftShopOpeningScheduleEndDate'));
   assert.ok(_findById(panelEl, 'giftShopOpeningScheduleMonday'));
   assert.ok(_findById(panelEl, 'giftShopOpeningScheduleTuesday'));
   assert.ok(_findById(panelEl, 'giftShopOpeningScheduleWednesday'));
   assert.ok(_findById(panelEl, 'giftShopOpeningScheduleThursday'));
   assert.ok(_findById(panelEl, 'giftShopOpeningScheduleFriday'));
   assert.ok(_findById(panelEl, 'giftShopOpeningScheduleSaturday'));
   assert.ok(_findById(panelEl, 'giftShopOpeningScheduleSunday'));
   assert.ok(_findById(panelEl, 'giftShopOpeningScheduleHolidaysOnly'));
   assert.ok(_findById(panelEl, 'giftShopOpeningScheduleMessage'));
   assert.ok(_findById(panelEl, 'submitGiftShopOpeningSchedule'));
   assert.ok(_findById(panelEl, 'giftShopOpeningScheduleStatus'));
});
