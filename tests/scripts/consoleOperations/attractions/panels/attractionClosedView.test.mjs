import assert from 'node:assert/strict';
import test from 'node:test';

import { AttractionClosedView } from '../../../../../scripts/consoleOperations/attractions/panels/attractionClosedView.js';
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

test('Test_CreateAttractionClosedPanel_TestDefault_ExpectPanel', () => {
   const panelEl = AttractionClosedView.createAttractionClosedPanel();

   assert.equal(panelEl.tagName.toUpperCase(), 'SECTION');
   assert.equal(panelEl.id, 'attractionClosedPanel');
   assert.equal(panelEl.className, 'console-operations-panel');
   assert.ok(panelEl.textContent.includes(Strings.panelTitles.attractionClosed));
   assert.ok(_findById(panelEl, 'attractionClosedAttraction'));
   assert.ok(_findById(panelEl, 'attractionClosedStartDate'));
   assert.ok(_findById(panelEl, 'attractionClosedEndDate'));
   assert.ok(_findById(panelEl, 'attractionClosedMessage'));
   assert.ok(_findById(panelEl, 'submitAttractionClosed'));
   assert.ok(_findById(panelEl, 'attractionClosedStatus'));
});
