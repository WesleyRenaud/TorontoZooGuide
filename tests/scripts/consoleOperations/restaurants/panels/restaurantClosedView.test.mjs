import assert from 'node:assert/strict';
import test from 'node:test';

import { RestaurantClosedView } from '../../../../../scripts/consoleOperations/restaurants/panels/restaurantClosedView.js';
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

test('Test_CreateRestaurantClosedPanel_TestDefault_ExpectPanel', () => {
   const panelEl = RestaurantClosedView.createRestaurantClosedPanel();

   assert.equal(panelEl.tagName.toUpperCase(), 'SECTION');
   assert.equal(panelEl.id, 'restaurantClosedPanel');
   assert.equal(panelEl.className, 'console-operations-panel');
   assert.ok(panelEl.textContent.includes(Strings.panelTitles.restaurantClosed));
   assert.ok(_findById(panelEl, 'restaurantClosedRestaurant'));
   assert.ok(_findById(panelEl, 'restaurantClosedStartDate'));
   assert.ok(_findById(panelEl, 'restaurantClosedEndDate'));
   assert.ok(_findById(panelEl, 'restaurantClosedMessage'));
   assert.ok(_findById(panelEl, 'submitRestaurantClosed'));
   assert.ok(_findById(panelEl, 'restaurantClosedStatus'));
});
