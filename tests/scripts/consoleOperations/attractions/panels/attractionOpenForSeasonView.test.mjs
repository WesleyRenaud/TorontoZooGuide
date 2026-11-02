import assert from 'node:assert/strict';
import test from 'node:test';

import { AttractionOpenForSeasonView } from '../../../../../scripts/consoleOperations/attractions/panels/attractionOpenForSeasonView.js';
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


test('Test_CreateAttractionOpenForSeasonPanel_TestDefault_ExpectAttractionOnly', () => {
   const panelEl = AttractionOpenForSeasonView.createAttractionOpenForSeasonPanel();

   assert.equal(panelEl.id, 'attractionOpenForSeasonPanel');
   assert.ok(panelEl.textContent.includes(Strings.panelTitles.attractionOpenForSeason));
   assert.ok(_findById(panelEl, 'attractionOpenForSeasonAttraction'));
   assert.equal(_findById(panelEl, 'attractionOpenForSeasonStartDate'), null);
   assert.equal(_findById(panelEl, 'attractionOpenForSeasonEndDate'), null);
   assert.ok(_findById(panelEl, 'submitAttractionOpenForSeason'));
   assert.ok(_findById(panelEl, 'attractionOpenForSeasonStatus'));
});
