import assert from 'node:assert/strict';
import test from 'node:test';

import { OffDisplayForSeasonView } from '../../../../../scripts/consoleOperations/animals/panels/offDisplayForSeasonView.js';
import { Strings } from '../../../../../scripts/strings.js';
import { installDomTestHooks } from '../../../helpers/domTestSetup.mjs';

function _findById(node, id) {
   if (node.id === id) {
      return node;
   }

   for (const child of node.children) {
      const found = _findById(child, id);
      if (found) {
         return found;
      }
   }

   return null;
}

installDomTestHooks();


test('Test_CreateOffDisplayForSeasonPanel_TestDefault_ExpectPanel', () => {
   const panelEl = OffDisplayForSeasonView.createOffDisplayForSeasonPanel();

   assert.equal(panelEl.tagName.toUpperCase(), 'SECTION');
   assert.equal(panelEl.id, 'offDisplayForSeasonPanel');
   assert.equal(panelEl.className, 'console-operations-panel');
   assert.ok(panelEl.textContent.includes(Strings.panelTitles.offDisplayForSeason));
   assert.ok(_findById(panelEl, 'offDisplayForSeasonExhibit'));
   assert.ok(_findById(panelEl, 'offDisplayForSeasonSpecies'));
   assert.ok(_findById(panelEl, 'offDisplayForSeasonSpeciesResults'));
   assert.ok(_findById(panelEl, 'offDisplayForSeasonViewingScope'));
   assert.ok(_findById(panelEl, 'offDisplayForSeasonStartDate'));
   assert.ok(_findById(panelEl, 'offDisplayForSeasonEndDate'));
   assert.ok(_findById(panelEl, 'offDisplayForSeasonMessage'));
   assert.ok(_findById(panelEl, 'submitOffDisplayForSeason'));
   assert.ok(_findById(panelEl, 'offDisplayForSeasonStatus'));
});
