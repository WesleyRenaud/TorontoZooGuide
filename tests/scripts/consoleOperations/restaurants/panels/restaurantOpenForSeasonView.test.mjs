import assert from 'node:assert/strict';
import test from 'node:test';

import { RestaurantOpenForSeasonView } from '../../../../../scripts/consoleOperations/restaurants/panels/restaurantOpenForSeasonView.js';
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


test('Test_CreateRestaurantOpenForSeasonPanel_TestDefault_ExpectRestaurantOnly', () => {
   const panelEl = RestaurantOpenForSeasonView.createRestaurantOpenForSeasonPanel();

   assert.equal(panelEl.id, 'restaurantOpenForSeasonPanel');
   assert.ok(panelEl.textContent.includes(Strings.panelTitles.restaurantOpenForSeason));
   assert.ok(_findById(panelEl, 'restaurantOpenForSeasonRestaurant'));
   assert.equal(_findById(panelEl, 'restaurantOpenForSeasonStartDate'), null);
   assert.equal(_findById(panelEl, 'restaurantOpenForSeasonEndDate'), null);
   assert.ok(_findById(panelEl, 'submitRestaurantOpenForSeason'));
   assert.ok(_findById(panelEl, 'restaurantOpenForSeasonStatus'));
});
