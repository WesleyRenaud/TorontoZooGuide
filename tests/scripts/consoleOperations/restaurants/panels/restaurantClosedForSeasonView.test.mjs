import assert from 'node:assert/strict';
import test from 'node:test';

import { RestaurantClosedForSeasonView } from '../../../../../scripts/consoleOperations/restaurants/panels/restaurantClosedForSeasonView.js';
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


test('Test_CreateRestaurantClosedForSeasonPanel_TestDefault_ExpectPanel', () => {
   const panelEl = RestaurantClosedForSeasonView.createRestaurantClosedForSeasonPanel();

   assert.equal(panelEl.id, 'restaurantClosedForSeasonPanel');
   assert.ok(panelEl.textContent.includes(Strings.panelTitles.restaurantClosedForSeason));
   assert.ok(panelEl.textContent.includes(Strings.labels.reason));
   assert.ok(_findById(panelEl, 'restaurantClosedForSeasonRestaurant'));
   assert.ok(_findById(panelEl, 'restaurantClosedForSeasonStartDate'));
   assert.ok(_findById(panelEl, 'restaurantClosedForSeasonEndDate'));
   assert.ok(_findById(panelEl, 'restaurantClosedForSeasonMessage'));
   assert.ok(_findById(panelEl, 'submitRestaurantClosedForSeason'));
   assert.ok(_findById(panelEl, 'restaurantClosedForSeasonStatus'));
});
