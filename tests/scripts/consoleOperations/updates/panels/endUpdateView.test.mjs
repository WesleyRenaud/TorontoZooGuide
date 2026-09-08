import assert from 'node:assert/strict';
import test from 'node:test';

import { EndUpdateView } from '../../../../../scripts/consoleOperations/updates/panels/endUpdateView.js';
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

test('Test_CreateEndUpdatePanel_TestDefault_ExpectPanel', () => {
   const panelEl = EndUpdateView.createEndUpdatePanel();

   assert.equal(panelEl.tagName.toUpperCase(), 'SECTION');
   assert.equal(panelEl.id, 'endUpdatePanel');
   assert.equal(panelEl.className, 'console-operations-panel');
   assert.ok(panelEl.textContent.includes(Strings.panelTitles.endUpdate));
   assert.ok(_findById(panelEl, 'endUpdateKey'));
   assert.ok(_findById(panelEl, 'endUpdateEndDate'));
   assert.ok(_findById(panelEl, 'submitEndUpdate'));
   assert.ok(_findById(panelEl, 'endUpdateStatus'));
});
