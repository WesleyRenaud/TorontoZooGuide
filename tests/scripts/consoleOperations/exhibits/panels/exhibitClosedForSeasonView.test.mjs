import assert from 'node:assert/strict';
import test from 'node:test';

import { ExhibitClosedForSeasonView } from '../../../../../scripts/consoleOperations/exhibits/panels/exhibitClosedForSeasonView.js';
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


test('Test_CreateExhibitClosedForSeasonPanel_TestDefault_ExpectPanel', () => {
   const panelEl = ExhibitClosedForSeasonView.createExhibitClosedForSeasonPanel();

   assert.equal(panelEl.tagName.toUpperCase(), 'SECTION');
   assert.equal(panelEl.id, 'exhibitClosedForSeasonPanel');
   assert.equal(panelEl.className, 'console-operations-panel');
   assert.ok(panelEl.textContent.includes(Strings.panelTitles.exhibitClosedForSeason));
   assert.ok(_findById(panelEl, 'exhibitClosedForSeasonExhibit'));
   assert.ok(_findById(panelEl, 'exhibitClosedForSeasonStartDate'));
   assert.ok(_findById(panelEl, 'exhibitClosedForSeasonEndDate'));
   assert.ok(_findById(panelEl, 'exhibitClosedForSeasonMessage'));
   assert.ok(_findById(panelEl, 'submitExhibitClosedForSeason'));
   assert.ok(_findById(panelEl, 'exhibitClosedForSeasonStatus'));
});
