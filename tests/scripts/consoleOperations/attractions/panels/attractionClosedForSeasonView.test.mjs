import assert from 'node:assert/strict';
import test from 'node:test';

import { AttractionClosedForSeasonView } from '../../../../../scripts/consoleOperations/attractions/panels/attractionClosedForSeasonView.js';
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


test('Test_CreateAttractionClosedForSeasonPanel_TestDefault_ExpectPanel', () => {
   const panelEl = AttractionClosedForSeasonView.createAttractionClosedForSeasonPanel();

   assert.equal(panelEl.id, 'attractionClosedForSeasonPanel');
   assert.ok(panelEl.textContent.includes(Strings.panelTitles.attractionClosedForSeason));
   assert.ok(panelEl.textContent.includes(Strings.labels.reason));
   assert.ok(_findById(panelEl, 'attractionClosedForSeasonAttraction'));
   assert.ok(_findById(panelEl, 'attractionClosedForSeasonStartDate'));
   assert.ok(_findById(panelEl, 'attractionClosedForSeasonEndDate'));
   assert.ok(_findById(panelEl, 'attractionClosedForSeasonMessage'));
   assert.ok(_findById(panelEl, 'submitAttractionClosedForSeason'));
   assert.ok(_findById(panelEl, 'attractionClosedForSeasonStatus'));
});
