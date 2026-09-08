import assert from 'node:assert/strict';
import test from 'node:test';

import { ExhibitClosedView } from '../../../../../scripts/consoleOperations/exhibits/panels/exhibitClosedView.js';
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

test('Test_CreateExhibitClosedPanel_TestDefault_ExpectPanel', () => {
   const panelEl = ExhibitClosedView.createExhibitClosedPanel();

   assert.equal(panelEl.tagName.toUpperCase(), 'SECTION');
   assert.equal(panelEl.id, 'exhibitClosedPanel');
   assert.equal(panelEl.className, 'console-operations-panel');
   assert.ok(panelEl.textContent.includes(Strings.panelTitles.exhibitClosed));
   assert.ok(_findById(panelEl, 'exhibitClosedExhibit'));
   assert.ok(_findById(panelEl, 'exhibitClosedStartDate'));
   assert.ok(_findById(panelEl, 'exhibitClosedEndDate'));
   assert.ok(_findById(panelEl, 'exhibitClosedMessage'));
   assert.ok(_findById(panelEl, 'submitExhibitClosed'));
   assert.ok(_findById(panelEl, 'exhibitClosedStatus'));
});
