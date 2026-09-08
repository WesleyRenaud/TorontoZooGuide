import assert from 'node:assert/strict';
import test from 'node:test';

import { ViewingAlertView } from '../../../../../scripts/consoleOperations/animals/panels/viewingAlertView.js';
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

test('Test_CreateViewingAlertPanel_TestDefault_ExpectPanel', () => {
   const panelEl = ViewingAlertView.createViewingAlertPanel();

   assert.equal(panelEl.tagName.toUpperCase(), 'SECTION');
   assert.equal(panelEl.id, 'viewingAlertPanel');
   assert.equal(panelEl.className, 'console-operations-panel');
   assert.ok(panelEl.textContent.includes(Strings.panelTitles.viewingAlert));
   assert.ok(_findById(panelEl, 'viewingAlertExhibit'));
   assert.ok(_findById(panelEl, 'viewingAlertSpecies'));
   assert.ok(_findById(panelEl, 'viewingAlertSpeciesResults'));
   assert.ok(_findById(panelEl, 'viewingAlertStartDate'));
   assert.ok(_findById(panelEl, 'viewingAlertEndDate'));
   assert.ok(_findById(panelEl, 'viewingAlertMessage'));
   assert.ok(_findById(panelEl, 'submitViewingAlert'));
   assert.ok(_findById(panelEl, 'viewingAlertStatus'));
});
