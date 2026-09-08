import assert from 'node:assert/strict';
import test from 'node:test';

import { DrinkingFountainsClosedView } from '../../../../../scripts/consoleOperations/drinkingFountains/panels/drinkingFountainsClosedView.js';
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

test('Test_CreateDrinkingFountainsClosedPanel_TestDefault_ExpectPanel', () => {
   const panelEl = DrinkingFountainsClosedView.createDrinkingFountainsClosedPanel();

   assert.equal(panelEl.tagName.toUpperCase(), 'SECTION');
   assert.equal(panelEl.id, 'drinkingFountainsClosedPanel');
   assert.equal(panelEl.className, 'console-operations-panel');
   assert.ok(panelEl.textContent.includes(Strings.panelTitles.drinkingFountainsClosed));
   assert.ok(_findById(panelEl, 'drinkingFountainsClosedStartDate'));
   assert.ok(_findById(panelEl, 'drinkingFountainsClosedEndDate'));
   assert.ok(_findById(panelEl, 'drinkingFountainsClosedMessage'));
   assert.ok(_findById(panelEl, 'submitDrinkingFountainsClosed'));
   assert.ok(_findById(panelEl, 'drinkingFountainsClosedStatus'));
});
