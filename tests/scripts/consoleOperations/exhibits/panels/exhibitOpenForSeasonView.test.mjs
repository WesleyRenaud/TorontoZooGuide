import assert from 'node:assert/strict';
import test from 'node:test';

import { ExhibitOpenForSeasonView } from '../../../../../scripts/consoleOperations/exhibits/panels/exhibitOpenForSeasonView.js';
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


test('Test_CreateExhibitOpenForSeasonPanel_TestDefault_ExpectPanel', () => {
   const panelEl = ExhibitOpenForSeasonView.createExhibitOpenForSeasonPanel();

   assert.equal(panelEl.tagName.toUpperCase(), 'SECTION');
   assert.equal(panelEl.id, 'exhibitOpenForSeasonPanel');
   assert.equal(panelEl.className, 'console-operations-panel');
   assert.ok(panelEl.textContent.includes(Strings.panelTitles.exhibitOpenForSeason));
   assert.ok(_findById(panelEl, 'exhibitOpenForSeasonExhibit'));
   assert.ok(_findById(panelEl, 'exhibitOpenForSeasonStartDate'));
   assert.ok(_findById(panelEl, 'exhibitOpenForSeasonEndDate'));
   assert.ok(_findById(panelEl, 'submitExhibitOpenForSeason'));
   assert.ok(_findById(panelEl, 'exhibitOpenForSeasonStatus'));
});
