import assert from 'node:assert/strict';
import test from 'node:test';

import { RestaurantOpeningScheduleView } from '../../../../../scripts/consoleOperations/restaurants/panels/restaurantOpeningScheduleView.js';
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

test('Test_CreateRestaurantOpeningSchedulePanel_TestDefault_ExpectPanel', () => {
   const panelEl = RestaurantOpeningScheduleView.createRestaurantOpeningSchedulePanel();

   assert.equal(panelEl.tagName.toUpperCase(), 'SECTION');
   assert.equal(panelEl.id, 'restaurantOpeningSchedulePanel');
   assert.equal(panelEl.className, 'console-operations-panel');
   assert.ok(panelEl.textContent.includes(Strings.panelTitles.restaurantOpeningSchedule));
   assert.ok(_findById(panelEl, 'restaurantOpeningScheduleRestaurant'));
   assert.ok(_findById(panelEl, 'restaurantOpeningSchedulePreset'));
   assert.ok(_findById(panelEl, 'restaurantOpeningScheduleStartDate'));
   assert.ok(_findById(panelEl, 'restaurantOpeningScheduleEndDate'));
   assert.ok(_findById(panelEl, 'restaurantOpeningScheduleMonday'));
   assert.ok(_findById(panelEl, 'restaurantOpeningScheduleTuesday'));
   assert.ok(_findById(panelEl, 'restaurantOpeningScheduleWednesday'));
   assert.ok(_findById(panelEl, 'restaurantOpeningScheduleThursday'));
   assert.ok(_findById(panelEl, 'restaurantOpeningScheduleFriday'));
   assert.ok(_findById(panelEl, 'restaurantOpeningScheduleSaturday'));
   assert.ok(_findById(panelEl, 'restaurantOpeningScheduleSunday'));
   assert.ok(_findById(panelEl, 'restaurantOpeningScheduleHolidaysOnly'));
   assert.ok(_findById(panelEl, 'restaurantOpeningScheduleMessage'));
   assert.ok(_findById(panelEl, 'submitRestaurantOpeningSchedule'));
   assert.ok(_findById(panelEl, 'restaurantOpeningScheduleStatus'));
});
