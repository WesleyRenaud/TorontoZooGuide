import assert from 'node:assert/strict';
import test from 'node:test';

import { EditUpdateView } from '../../../../../scripts/consoleOperations/updates/panels/editUpdateView.js';
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

test('Test_CreateEditUpdatePanel_TestDefault_ExpectPanel', () => {
   const panelEl = EditUpdateView.createEditUpdatePanel();

   assert.equal(panelEl.tagName.toUpperCase(), 'SECTION');
   assert.equal(panelEl.id, 'editUpdatePanel');
   assert.equal(panelEl.className, 'console-operations-panel');
   assert.ok(panelEl.textContent.includes(Strings.panelTitles.editUpdate));
   assert.ok(_findById(panelEl, 'editUpdateKey'));
   assert.ok(_findById(panelEl, 'editUpdateDescription'));
   assert.ok(_findById(panelEl, 'editUpdateType'));
   assert.ok(_findById(panelEl, 'editUpdateEndDate'));
   assert.ok(_findById(panelEl, 'submitEditUpdate'));
   assert.ok(_findById(panelEl, 'editUpdateStatus'));
});
