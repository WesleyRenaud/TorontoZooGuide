import assert from 'node:assert/strict';
import test from 'node:test';

import { RemoveVisibilityScheduleView } from '../../../../../scripts/consoleOperations/animals/panels/removeVisibilityScheduleView.js';
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

test('Test_CreateRemoveVisibilitySchedulePanel_TestDefault_ExpectPanel', () => {
   const panelEl = RemoveVisibilityScheduleView.createRemoveVisibilitySchedulePanel();

   assert.equal(panelEl.tagName.toUpperCase(), 'SECTION');
   assert.equal(panelEl.id, 'removeVisibilitySchedulePanel');
   assert.equal(panelEl.className, 'console-operations-panel');
   assert.ok(panelEl.textContent.includes(Strings.panelTitles.removeVisibilitySchedule));
   assert.ok(_findById(panelEl, 'removeVisibilityScheduleExhibit'));
   assert.ok(_findById(panelEl, 'removeVisibilityScheduleSpecies'));
   assert.ok(_findById(panelEl, 'removeVisibilityScheduleSpeciesResults'));
   assert.ok(_findById(panelEl, 'submitRemoveVisibilitySchedule'));
   assert.ok(_findById(panelEl, 'removeVisibilityScheduleStatus'));
});
