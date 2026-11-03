import assert from 'node:assert/strict';
import test from 'node:test';

import { DrinkingFountainsOpenView } from '../../../../../scripts/consoleOperations/drinkingFountains/panels/drinkingFountainsOpenView.js';
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


test('Test_CreateDrinkingFountainsOpenPanel_TestDefault_ExpectPanel', () => {
   const panelEl = DrinkingFountainsOpenView.createDrinkingFountainsOpenPanel();

   assert.equal(panelEl.tagName.toUpperCase(), 'SECTION');
   assert.equal(panelEl.id, 'drinkingFountainsOpenPanel');
   assert.equal(panelEl.className, 'console-operations-panel');
   assert.ok(panelEl.textContent.includes(Strings.panelTitles.drinkingFountainsOpen));
   assert.equal(_findById(panelEl, 'drinkingFountainsOpenStartDate'), null);
   assert.equal(_findById(panelEl, 'drinkingFountainsOpenEndDate'), null);
   assert.ok(_findById(panelEl, 'submitDrinkingFountainsOpen'));
   assert.ok(_findById(panelEl, 'drinkingFountainsOpenStatus'));
});
