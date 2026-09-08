import assert from 'node:assert/strict';
import test from 'node:test';

import { RemoveRestroomAlertView } from '../../../../../scripts/consoleOperations/restrooms/panels/removeRestroomAlertView.js';
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

test('Test_CreateRemoveRestroomAlertPanel_TestDefault_ExpectPanel', () => {
   const panelEl = RemoveRestroomAlertView.createRemoveRestroomAlertPanel();

   assert.equal(panelEl.tagName.toUpperCase(), 'SECTION');
   assert.equal(panelEl.id, 'removeRestroomAlertPanel');
   assert.equal(panelEl.className, 'console-operations-panel');
   assert.ok(panelEl.textContent.includes(Strings.panelTitles.removeRestroomAlert));
   assert.ok(_findById(panelEl, 'removeRestroomAlertRestroom'));
   assert.ok(_findById(panelEl, 'submitRemoveRestroomAlert'));
   assert.ok(_findById(panelEl, 'removeRestroomAlertStatus'));
   assert.equal(
      _findById(panelEl, 'submitRemoveRestroomAlert').textContent,
      Strings.actions.removeAlert
   );
});
