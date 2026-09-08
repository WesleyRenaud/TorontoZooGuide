import assert from 'node:assert/strict';
import test from 'node:test';

import { RestroomOpenView } from '../../../../../scripts/consoleOperations/restrooms/panels/restroomOpenView.js';
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

test('Test_CreateRestroomOpenPanel_TestDefault_ExpectPanel', () => {
   const panelEl = RestroomOpenView.createRestroomOpenPanel();

   assert.equal(panelEl.tagName.toUpperCase(), 'SECTION');
   assert.equal(panelEl.id, 'restroomOpenPanel');
   assert.equal(panelEl.className, 'console-operations-panel');
   assert.ok(panelEl.textContent.includes(Strings.panelTitles.restroomOpen));
   assert.ok(_findById(panelEl, 'restroomOpenRestroom'));
   assert.ok(_findById(panelEl, 'restroomOpenStartDate'));
   assert.ok(_findById(panelEl, 'restroomOpenEndDate'));
   assert.ok(_findById(panelEl, 'submitRestroomOpen'));
   assert.ok(_findById(panelEl, 'restroomOpenStatus'));
});
