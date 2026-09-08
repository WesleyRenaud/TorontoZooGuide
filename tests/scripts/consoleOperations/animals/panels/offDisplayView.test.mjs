import assert from 'node:assert/strict';
import test from 'node:test';

import { OffDisplayView } from '../../../../../scripts/consoleOperations/animals/panels/offDisplayView.js';
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

test('Test_CreateOffDisplayPanel_TestDefault_ExpectPanel', () => {
   const panelEl = OffDisplayView.createOffDisplayPanel();

   assert.equal(panelEl.tagName.toUpperCase(), 'SECTION');
   assert.equal(panelEl.id, 'offDisplayPanel');
   assert.equal(panelEl.className, 'console-operations-panel');
   assert.ok(panelEl.textContent.includes(Strings.panelTitles.offDisplay));
   assert.ok(_findById(panelEl, 'offDisplayExhibit'));
   assert.ok(_findById(panelEl, 'offDisplaySpecies'));
   assert.ok(_findById(panelEl, 'offDisplaySpeciesResults'));
   assert.ok(_findById(panelEl, 'offDisplayViewingScope'));
   assert.ok(_findById(panelEl, 'offDisplayStartDate'));
   assert.ok(_findById(panelEl, 'offDisplayEndDate'));
   assert.ok(_findById(panelEl, 'offDisplayMessage'));
   assert.ok(_findById(panelEl, 'submitOffDisplay'));
   assert.ok(_findById(panelEl, 'offDisplayStatus'));
});
