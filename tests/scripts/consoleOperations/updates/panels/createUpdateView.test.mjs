import assert from 'node:assert/strict';
import test from 'node:test';

import { CreateUpdateView } from '../../../../../scripts/consoleOperations/updates/panels/createUpdateView.js';
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

test('Test_CreateCreateUpdatePanel_TestDefault_ExpectPanel', () => {
   const panelEl = CreateUpdateView.createCreateUpdatePanel();

   assert.equal(panelEl.tagName.toUpperCase(), 'SECTION');
   assert.equal(panelEl.id, 'createUpdatePanel');
   assert.equal(panelEl.className, 'console-operations-panel');
   assert.ok(panelEl.textContent.includes(Strings.panelTitles.createUpdate));
   assert.ok(_findById(panelEl, 'createUpdateTitle'));
   assert.ok(_findById(panelEl, 'createUpdateDescription'));
   assert.ok(_findById(panelEl, 'createUpdateType'));
   assert.ok(_findById(panelEl, 'createUpdateStartDate'));
   assert.ok(_findById(panelEl, 'createUpdateEndDate'));
   assert.ok(_findById(panelEl, 'submitCreateUpdate'));
   assert.ok(_findById(panelEl, 'createUpdateStatus'));
});
