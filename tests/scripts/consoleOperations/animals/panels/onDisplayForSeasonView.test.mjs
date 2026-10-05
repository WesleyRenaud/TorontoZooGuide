import assert from 'node:assert/strict';
import test from 'node:test';

import { OnDisplayForSeasonView } from '../../../../../scripts/consoleOperations/animals/panels/onDisplayForSeasonView.js';
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


test('Test_CreateOnDisplayForSeasonPanel_TestDefault_ExpectPanel', () => {
   const panelEl = OnDisplayForSeasonView.createOnDisplayForSeasonPanel();

   assert.equal(panelEl.tagName.toUpperCase(), 'SECTION');
   assert.equal(panelEl.id, 'onDisplayForSeasonPanel');
   assert.equal(panelEl.className, 'console-operations-panel');
   assert.ok(panelEl.textContent.includes(Strings.panelTitles.onDisplayForSeason));
   assert.ok(_findById(panelEl, 'onDisplayForSeasonExhibit'));
   assert.ok(_findById(panelEl, 'onDisplayForSeasonSpecies'));
   assert.ok(_findById(panelEl, 'onDisplayForSeasonSpeciesResults'));
   assert.ok(_findById(panelEl, 'onDisplayForSeasonViewingScope'));
   assert.ok(_findById(panelEl, 'submitOnDisplayForSeason'));
   assert.ok(_findById(panelEl, 'onDisplayForSeasonStatus'));
});
