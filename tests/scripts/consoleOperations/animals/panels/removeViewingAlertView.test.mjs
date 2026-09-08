import assert from 'node:assert/strict';
import test from 'node:test';

import { RemoveViewingAlertView } from '../../../../../scripts/consoleOperations/animals/panels/removeViewingAlertView.js';
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

test('Test_CreateRemoveViewingAlertPanel_TestDefault_ExpectPanel', () => {
   const panelEl = RemoveViewingAlertView.createRemoveViewingAlertPanel();

   assert.equal(panelEl.tagName.toUpperCase(), 'SECTION');
   assert.equal(panelEl.id, 'removeViewingAlertPanel');
   assert.equal(panelEl.className, 'console-operations-panel');
   assert.ok(panelEl.textContent.includes(Strings.panelTitles.removeViewingAlert));
   assert.ok(_findById(panelEl, 'removeViewingAlertExhibit'));
   assert.ok(_findById(panelEl, 'removeViewingAlertSpecies'));
   assert.ok(_findById(panelEl, 'removeViewingAlertSpeciesResults'));
   assert.ok(_findById(panelEl, 'submitRemoveViewingAlert'));
   assert.ok(_findById(panelEl, 'removeViewingAlertStatus'));
   assert.equal(
      _findById(panelEl, 'submitRemoveViewingAlert').textContent,
      Strings.actions.removeAlert
   );
});
