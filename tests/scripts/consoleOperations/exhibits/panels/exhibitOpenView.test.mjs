import assert from 'node:assert/strict';
import test from 'node:test';

import { ExhibitOpenView } from '../../../../../scripts/consoleOperations/exhibits/panels/exhibitOpenView.js';
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

test('Test_CreateExhibitOpenPanel_TestDefault_ExpectPanel', () => {
   const panelEl = ExhibitOpenView.createExhibitOpenPanel();

   assert.equal(panelEl.tagName.toUpperCase(), 'SECTION');
   assert.equal(panelEl.id, 'exhibitOpenPanel');
   assert.equal(panelEl.className, 'console-operations-panel');
   assert.ok(panelEl.textContent.includes(Strings.panelTitles.exhibitOpen));
   assert.ok(_findById(panelEl, 'exhibitOpenExhibit'));
   assert.ok(_findById(panelEl, 'exhibitOpenStartDate'));
   assert.ok(_findById(panelEl, 'exhibitOpenEndDate'));
   assert.ok(_findById(panelEl, 'submitExhibitOpen'));
   assert.ok(_findById(panelEl, 'exhibitOpenStatus'));
});
